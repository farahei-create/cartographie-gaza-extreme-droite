# -*- coding: utf-8 -*-
"""Écrit les sources du relevé : fichier publié, file d'attente, journal, version, EXPECT.

Ne pousse rien. Le workflow ne commit qu'après les tests.
"""
import datetime
import json
import os
import re

from tools.daily.textutil import french_date, norm_literal

TIER_IDS = ("evt", "col", "asso", "jour", "media", "elu", "gouv", "prop")
VERSION_FILES = (
    "sw.js",
    "tests/test_v13.py",
    "tests/test_v22.py",
    "tests/test_v23.py",
    "tests/test_v24.py",
    "tests/test_admin.py",
)
NOTICE = "File d'attente du relevé automatique. Ce n'est pas une publication."


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _write(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def published_path(root):
    return os.environ.get("ONRECORD_AUTO_JSON") or os.path.join(root, "tools", "auto_published.json")


def pending_path(root):
    return os.environ.get("ONRECORD_PENDING_JSON") or os.path.join(root, "tools", "auto_pending.json")


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def empty_published():
    return {"people": [], "statements": [], "edges": [], "log": []}


def merge_published(root, published, day):
    path = published_path(root)
    data = load_json(path, empty_published())
    data.setdefault("people", [])
    data.setdefault("statements", [])
    data.setdefault("edges", [])
    data.setdefault("log", [])
    known_people = {p.get("id") for p in data["people"]}
    seen = {(s.get("person_id"), norm_literal(s.get("quote")).lower()) for s in data["statements"]}
    people_added = 0
    statements_added = 0
    for item in published:
        person = item.get("person")
        if person and person["id"] not in known_people:
            data["people"].append(person)
            known_people.add(person["id"])
            people_added += 1
        statement = item["statement"]
        key = (statement["person_id"], norm_literal(statement["quote"]).lower())
        if key in seen:
            continue
        data["statements"].append(statement)
        seen.add(key)
        statements_added += 1
    if statements_added or people_added:
        data["log"].append({
            "date": day.isoformat(),
            "statements": statements_added,
            "people": people_added,
        })
        save_json(path, data)
    return statements_added, people_added


def merge_pending(root, items, day):
    path = pending_path(root)
    current = load_json(path, {"_notice": NOTICE, "items": []})
    by_id = {}
    for item in current.get("items") or []:
        if item.get("id"):
            by_id[item["id"]] = item
    changed = False
    for item in items:
        if item.get("id") in by_id:
            continue
        row = {
            "id": item.get("id"),
            "seen": day.isoformat(),
            "reason": item.get("reason") or "",
            "detail": item.get("detail") or "",
            "person": item.get("person") or "",
            "date": item.get("date") or "",
            "quote": item.get("quote") or "",
            "url": item.get("url") or "",
            "title": item.get("title") or "",
            "outlet": item.get("outlet") or "",
        }
        by_id[row["id"]] = row
        changed = True
    ordered = sorted(by_id.values(), key=lambda it: it.get("seen") or "", reverse=True)[:80]
    if not changed:
        return False
    save_json(path, {"_notice": NOTICE, "items": ordered})
    return True


def current_version(root):
    sw = _read(os.path.join(root, "sw.js"))
    found = re.search(r'var VERSION = "onrecord-v(\d+)"', sw)
    if not found:
        raise SystemExit("VERSION absente de sw.js")
    return int(found.group(1))


def bump_version(root):
    current = current_version(root)
    old = "onrecord-v%d" % current
    new = "onrecord-v%d" % (current + 1)
    for rel in VERSION_FILES:
        path = os.path.join(root, rel)
        text = _read(path)
        if old not in text:
            raise SystemExit("Version %s absente de %s" % (old, rel))
        _write(path, text.replace(old, new))
    return new


def _power_map(js):
    start = js.find("var POWER_OF = {")
    end = js.find("};", start)
    block = js[start:end]
    return {m.group(1): int(m.group(2)) for m in re.finditer(r'"([a-z0-9-]+)"\s*:\s*(\d+)', block)}


def fallback_tier(node):
    """Même repli que app.js, fonction fallbackPow."""
    sub = node.get("subcategory") or ""
    blob = sub + " " + (node.get("role") or "") + " " + (node.get("category") or "")
    if node.get("category") == "Événements" or re.search(r"événement", sub, re.I):
        return 0
    if node.get("type") == "org" and re.search(r"dissous|dissoute|collectif|projet", blob, re.I):
        return 1
    if re.search(r"Associations|Projets", sub):
        return 2
    if node.get("category") in ("Journalistes & éditorialistes", "Intellectuels & essayistes") or sub == "Animateurs & producteurs":
        return 3
    if sub in ("Chaînes, radios & titres", "Édition"):
        return 4
    if sub in ("Gouvernement & exécutif", "Institutions publiques"):
        return 6
    if sub == "Propriétaires, financeurs & groupes":
        return 7
    if node.get("category") == "Responsables politiques" or re.search(r"parti", sub, re.I):
        return 5
    return 3


def tier_counts(data, js):
    mapping = _power_map(js)
    counts = {key: 0 for key in TIER_IDS}
    for node in data.get("nodes") or []:
        index = mapping[node["id"]] if node["id"] in mapping else fallback_tier(node)
        counts[TIER_IDS[index]] += 1
    return counts


def expect_line(counts):
    body = ", ".join('"%s": %d' % (key, counts[key]) for key in TIER_IDS)
    return "EXPECT = {%s}" % body


def sync_expect(root):
    data = json.loads(_read(os.path.join(root, "data.json")))
    js = _read(os.path.join(root, "app.js"))
    counts = tier_counts(data, js)
    path = os.path.join(root, "tests", "test_v22.py")
    text = _read(path)
    new = expect_line(counts)
    updated, n = re.subn(r"EXPECT = \{[^}]+\}", new, text, count=1)
    if n != 1:
        raise SystemExit("Ligne EXPECT introuvable dans tests/test_v22.py")
    if updated != text:
        _write(path, updated)
    return counts, updated != text


def journal_entry(day, published, pending_count, version):
    lines = ["## %s — relevé automatique" % day.isoformat(), ""]
    if not published:
        if pending_count == 1:
            attente = "1 élément attend"
        else:
            attente = "%d éléments attendent" % pending_count
        lines.append("Tu ne publies aucune phrase. %s une relecture sur la page admin." % attente)
    else:
        people = len({item["person"]["id"] for item in published if item.get("person")})
        fiche = ""
        if people:
            fiche = " et %d fiche%s" % (people, "s" if people != 1 else "")
        lines.append(
            "Tu pars des flux publics des dernières 48 heures. Tu publies %d phrase%s%s. Pas de photo : monogramme."
            % (len(published), "s" if len(published) != 1 else "", fiche)
        )
        lines.append("")
        for item in published:
            statement = item["statement"]
            quote = statement["quote"]
            if len(quote) > 180:
                quote = quote[:177] + "…"
            lines.append("- %s, %s : « %s » — %s" % (item.get("label") or statement["person_id"], french_date(statement["date"]), quote, statement["url"]))
        lines.append("")
        lines.append(
            "Écarté, en file d'attente (%d) : ce qui n'était pas dans la page mot pour mot, hors date, hors sujet, déjà en ligne, douteux, ou personne non établie. La page admin les montre."
            % pending_count
        )
    if version:
        lines.append("")
        lines.append("Cache `%s`." % version)
    return "\n".join(lines) + "\n"


def prepend_journal(root, entry):
    path = os.path.join(root, "docs", "JOURNAL.md")
    text = _read(path)
    at = text.find("\n## ")
    if at < 0:
        _write(path, text.rstrip() + "\n\n" + entry)
        return
    _write(path, text[: at + 1] + entry.rstrip() + "\n\n" + text[at + 1 :])


def now_paris():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Paris"))
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=1)))
