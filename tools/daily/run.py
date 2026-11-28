# -*- coding: utf-8 -*-
"""Relevé du matin.

Sans GEMINI_API_KEY : message clair, aucun fichier, code 0.
--dry-run et --mock n'écrivent pas dans le dépôt.
"""
import argparse
import datetime
import json
import os
import sys
import time

from tools.daily.engine import load_index, review_pages
from tools.daily.gemini import KeyErrorRejected, QuotaError
from tools.daily import ai as ai_mod
from tools.daily import incidents
from tools.daily.engine import PERSON_MISSING
from tools.daily.store import merge_pending, merge_published, now_paris, repo_root

ROOT_DEFAULT = repo_root()
STATE = "/tmp/onrecord-daily-state.json"


def summary_markdown(stats, decision, model, requests, dry, key_missing=False, key_rejected=False):
    lines = ["## Relevé du matin", ""]
    if key_missing:
        lines.append("Arrêt propre : aucun des secrets `GEMINI_API_KEY` (IA principale) ou `XAI_API_KEY` (IA de secours) n'est configuré. Aucun fichier n'a été modifié et rien n'a été poussé sur `main`.")
        lines.append("")
        lines.append("Pour activer : créer une clé gratuite sur [Google AI Studio](https://aistudio.google.com/apikey), sans compte de facturation, puis l'ajouter dans Settings → Secrets and variables → Actions, sous le nom `GEMINI_API_KEY`.")
        return "\n".join(lines) + "\n"
    if key_rejected:
        lines.append("Les clés d'IA ont été refusées. Rien n'a été modifié et rien n'a été poussé.")
        return "\n".join(lines) + "\n"
    published = decision.get("published") or []
    pending = decision.get("pending") or []
    lines.append("- Flux lus : %d (%d en échec)" % (stats.get("feeds_ok", 0), stats.get("feeds_fail", 0)))
    for err in stats.get("feed_errors") or []:
        lines.append("  - échec : %s — %s — %s" % (err.get("outlet") or "flux", err.get("error") or "échec", err.get("url") or ""))
    lines.append("- Articles repérés : %d ; pages ouvertes : %d ; pages inaccessibles : %d" % (stats.get("items", 0), stats.get("fetched", 0), stats.get("fetch_fail", 0)))
    lines.append("- Liens Google News non résolus : %d" % stats.get("google_unresolved", 0))
    lines.append("- Requêtes IA : %d (modèle %s)" % (requests, model or "—"))
    lines.append("- Publié : %d phrase(s), %d fiche(s)" % (len(published), len({p["person"]["id"] for p in published if p.get("person")})))
    lines.append("- Écarté : %d" % len(pending))
    if dry:
        lines.append("- Mode à blanc : rien n'est écrit, rien n'est poussé.")
    lines.append("")
    lines.append("### Publié")
    if not published:
        lines.append("Rien. Aucune phrase n'a passé tous les contrôles.")
    else:
        for item in published:
            statement = item["statement"]
            lines.append("- %s, %s — %s — %s" % (
                item.get("label") or statement["person_id"], statement["date"], statement["quote"], statement["url"]))
    lines.append("")
    lines.append("### Écarté")
    if not pending:
        lines.append("Rien.")
    else:
        for item in pending[:40]:
            who = item.get("person") or item.get("title") or "sans nom"
            lines.append("- %s — %s — %s" % (item.get("reason") or "écarté", who, item.get("url") or ""))
        if len(pending) > 40:
            lines.append("- … %d de plus dans la file d'attente." % (len(pending) - 40))
    return "\n".join(lines) + "\n"


def write_summary(text):
    print(text)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(text)


def set_output(key, value):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("%s=%s\n" % (key, value))


def current_slot():
    """matin ou soir. Donné par le déclencheur (ONRECORD_SLOT), sinon par l'heure de Paris."""
    forced = (os.environ.get("ONRECORD_SLOT") or "").strip().lower()
    if forced in ("matin", "soir"):
        return forced
    return "matin" if now_paris().hour < 14 else "soir"


def _incidents_text():
    try:
        return open(incidents.path(), encoding="utf-8").read()
    except OSError:
        return ""


INCIDENTS_AT_START = _incidents_text()


def note_incidents(decision, proposals):
    """Problèmes de ce passage, pour la page admin. Jamais bloquant."""
    missing = [p for p in decision.get("pending") or [] if (p.get("reason") or "") == PERSON_MISSING]
    for item in missing:
        incidents.add(
            "personne_sans_fiche",
            "Phrase mise en attente : %s n'a pas de fiche" % (item.get("person") or "une personne"),
            "« %s » — %s. La phrase est dans la File d'attente. Crée la fiche dans Ajouter si la personne est publique, puis publie la phrase." % ((item.get("quote") or "")[:200], item.get("url") or ""),
            key="sans-fiche|" + (item.get("person") or "") + "|" + (item.get("url") or ""))
    stopped = sum(1 for v in proposals.values() if v == "quota de relecture atteint")
    if stopped:
        incidents.add("ia_quota", "Relecture interrompue : quota des IA atteint", "%d page(s) non relue(s) pendant ce passage. Elles seront retentées au prochain passage." % stopped)
    failed = sum(1 for v in proposals.values() if v == "relecture automatique impossible")
    if failed >= 5:
        incidents.add("ia_panne", "Plusieurs pages n'ont pas pu être relues par l'IA", "%d page(s) en échec de relecture pendant ce passage." % failed)


def mock_page(now):
    day = (now.date() - datetime.timedelta(days=1)).isoformat()
    y, m, d = day.split("-")
    months = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre")
    pretty = "%d %s %s" % (int(d), months[int(m) - 1], y)
    quote = "La phrase de contrôle du relevé automatique reste dans l'extrait et ne doit pas être publiée."
    text = (
        "Article du %s. Marine Le Pen, députée, a déclaré au sujet de l'immigration : « %s » "
        "Le Rassemblement national était le cadre de l'entretien."
    ) % (pretty, quote)
    return {
        "url": "https://www.example.com/onrecord-releve-controle",
        "outlet": "Exemple",
        "title": "Contrôle du relevé, à ne pas publier",
        "text": text,
        "html": "<p>%s</p>" % text,
        "dates": [day],
        "feed_date": day,
    }, [{
        "person_name": "Marine Le Pen",
        "quote": quote,
        "date": day,
        "section": "france",
        "theme": "France – normalisation de l'extrême droite",
        "context": "",
        "denial": "",
        "video_url": "",
        "doubt": "",
        "public_role": "",
    }]


def run_review(pages, proposals, index, now):
    return review_pages(pages, proposals, index, now)


def collect_proposals(pages, ai, names, pause):
    proposals = {}
    stopped = None
    for page in pages:
        url = page.get("url") or ""
        if stopped:
            proposals[url] = stopped
            continue
        if page.get("fetch_error") or not (page.get("text") or "").strip():
            proposals[url] = "page inaccessible"
            continue
        if len(page.get("text") or "") < 400:
            proposals[url] = []
            continue
        try:
            proposals[url] = ai.extract(page, names)
            pause()
        except QuotaError:
            stopped = "quota de relecture atteint"
            proposals[url] = stopped
        except KeyErrorRejected:
            raise
        except (ValueError, json.JSONDecodeError, OSError) as exc:
            proposals[url] = "relecture automatique impossible"
            sys.stderr.write("relecture : %s\n" % exc)
    return proposals


def main(argv=None):
    parser = argparse.ArgumentParser(description="Relevé Onrecord du matin")
    parser.add_argument("--dry-run", action="store_true", help="Ne rien écrire")
    parser.add_argument("--mock", action="store_true", help="IA simulée, sans réseau et sans clé")
    parser.add_argument("--root", default=ROOT_DEFAULT)
    args = parser.parse_args(argv)
    root = args.root
    dry = args.dry_run or args.mock or os.environ.get("ONRECORD_DRY_RUN") == "1"
    # --mock n'écrit jamais dans le dépôt réel.
    if args.mock and not args.dry_run and os.path.abspath(root) == os.path.abspath(ROOT_DEFAULT):
        dry = True

    slot = current_slot()
    if not args.mock and not ai_mod.available():
        write_summary(summary_markdown({}, {}, "", 0, True, key_missing=True))
        set_output("ready", "false")
        set_output("publish_count", "0")
        return 0

    if not args.mock:
        from tools.daily.already_done import summary_already_done, update_already_done
        hit = update_already_done(root, fetch=os.environ.get("GITHUB_ACTIONS") == "true", slot=slot)
        if hit.get("done"):
            write_summary(summary_already_done(hit, slot=slot))
            set_output("ready", "false")
            set_output("already_done", "true")
            set_output("content", "false")
            set_output("publish_count", "0")
            return 0

    index_data = json.load(open(os.path.join(root, "data.json"), encoding="utf-8"))
    index = load_index(index_data)
    now = now_paris()
    stats = {"feeds_ok": 0, "feeds_fail": 0, "items": 0, "google_unresolved": 0, "fetched": 0, "fetch_fail": 0}

    if args.mock:
        page, items = mock_page(now)
        pages = [page]
        proposals = {page["url"]: items}
        model, requests = "simulation", 0
        stats["fetched"] = 1
        stats["items"] = 1
    else:
        from tools.daily.collect import collect
        from tools.daily.gemini import PAUSE_SECONDS
        pages, stats = collect(index, now)
        ai = ai_mod.Relecture()
        names = [n.get("name") or "" for n in index["nodes"]]
        try:
            proposals = collect_proposals(pages, ai, names, lambda: time.sleep(PAUSE_SECONDS))
        except KeyErrorRejected as exc:
            write_summary(summary_markdown(stats, {}, "", ai.requests, True, key_rejected=True))
            sys.stderr.write(str(exc) + "\n")
            incidents.add("ia_cle", "Relevé arrêté : clé(s) d'IA refusée(s)", "Aucune IA n'a accepté sa clé. Vérifie GEMINI_API_KEY et XAI_API_KEY dans GitHub → Settings → Secrets and variables → Actions.")
            set_output("ready", "false")
            return 1
        model, requests = ai.model, ai.requests

    decision = run_review(pages, proposals, index, now)
    if not dry:
        note_incidents(decision, proposals)
    write_summary(summary_markdown(stats, decision, model, requests, dry))
    published = decision["published"]
    pending = decision["pending"]
    set_output("publish_count", str(len(published)))
    set_output("pending_count", str(len(pending)))

    if dry:
        set_output("ready", "false")
        return 0

    day = now.date()
    added, people = merge_published(root, published, day)
    pending_changed = merge_pending(root, pending, day)
    state = {
        "day": day.isoformat(),
        "published": published,
        "pending_count": len(pending),
        "added": added,
        "people": people,
        "urls": sorted({item["statement"]["url"] for item in published}),
        "content": added > 0,
        "pending_changed": pending_changed,
        "slot": slot,
    }
    state["incidents_changed"] = _incidents_text() != INCIDENTS_AT_START
    with open(STATE, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False)
    ready = added > 0 or pending_changed or state["incidents_changed"]
    set_output("ready", "true" if ready else "false")
    set_output("content", "true" if added else "false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
