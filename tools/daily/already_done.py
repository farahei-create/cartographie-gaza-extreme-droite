# -*- coding: utf-8 -*-
"""Le relevé du jour (Europe/Paris) a-t-il déjà été publié sur main ?

Empêche un doublon entre la routine de 8 h et le workflow GitHub, y compris
quand un cron part en retard. Ne publie rien dans ce cas : succès propre.
"""
import datetime
import os
import re
import subprocess

from tools.daily.store import now_paris

PHRASE_IN_SUBJECT = re.compile(r"\d+\s+phrases?\b", re.I)


def avant_maj_tag(day):
    return "version-%s-avant-maj" % day.isoformat()


def is_daily_update_subject(subject, day):
    """Un commit de relevé du jour, pas une simple évolution du site.

    Exemples retenus :
    - Mise à jour du 24/11 : relevé automatique, 6 phrases
    - Mise à jour du 24/11 : file d'attente, rien publié
    - Mise à jour du 24/11 : 31 phrases du 22 au 24/11 (…) (cache v62)

    Exemples écartés : « liste des versions », un onglet, un bouton, un filet
    de secours technique.
    """
    subject = (subject or "").strip()
    prefix = "Mise à jour du %s :" % day.strftime("%d/%m")
    if not subject.startswith(prefix):
        return False
    rest = subject[len(prefix):]
    if "relevé automatique" in rest:
        return True
    if "file d'attente" in rest:
        return True
    if PHRASE_IN_SUBJECT.search(rest):
        return True
    return False


def _git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def fetch_origin(root):
    """Met à jour origin/main et les tags, sans toucher à l'arbre de travail."""
    result = _git(root, "fetch", "origin", "main", "--tags", "--force")
    return result.returncode == 0, (result.stderr or result.stdout or "").strip()


def _resolve_ref(root, ref=None):
    if ref:
        return ref
    probed = _git(root, "rev-parse", "--verify", "origin/main")
    if probed.returncode == 0:
        return "origin/main"
    return "HEAD"


def _commit_date_paris(stamp):
    if not stamp:
        return None
    try:
        when = datetime.datetime.fromisoformat(stamp)
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=datetime.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        return when.astimezone(ZoneInfo("Europe/Paris")).date()
    except Exception:
        return when.astimezone(datetime.timezone(datetime.timedelta(hours=1))).date()


def update_already_done(root, day=None, ref=None, fetch=False):
    """Renvoie un dict {done, reason}. done=True si le jour est déjà couvert."""
    day = day or now_paris().date()
    fetch_error = ""
    if fetch:
        ok, output = fetch_origin(root)
        if not ok:
            fetch_error = output or "git fetch a échoué"
    ref = _resolve_ref(root, ref)
    tag = avant_maj_tag(day)
    listed = _git(root, "tag", "-l", tag)
    if listed.returncode == 0 and listed.stdout.strip() == tag:
        result = {
            "done": True,
            "reason": "tag %s" % tag,
            "tag": tag,
            "subject": "",
        }
        if fetch_error:
            result["fetch_error"] = fetch_error
        return result

    log = _git(root, "log", "--format=%aI\t%s", ref)
    if log.returncode != 0:
        return {
            "done": False,
            "reason": "",
            "tag": tag,
            "subject": "",
            "error": (log.stderr or log.stdout or "git log a échoué").strip(),
        }
    for line in (log.stdout or "").splitlines():
        if "\t" not in line:
            continue
        stamp, subject = line.split("\t", 1)
        when = _commit_date_paris(stamp)
        if when != day:
            continue
        if is_daily_update_subject(subject, day):
            return {
                "done": True,
                "reason": "commit « %s »" % subject,
                "tag": tag,
                "subject": subject,
            }
    result = {"done": False, "reason": "", "tag": tag, "subject": ""}
    if fetch_error:
        result["fetch_error"] = fetch_error
    return result


def summary_already_done(hit, day=None):
    day = day or now_paris().date()
    lines = ["## Relevé du matin", ""]
    if hit.get("done"):
        lines.append(
            "Mise à jour du %s déjà présente sur `main` (%s). "
            "Rien n'est lu, rien n'est écrit, rien n'est poussé. "
            "C'est le filet de secours : la routine de 8 h (Europe/Paris) "
            "ou un précédent passage du workflow a déjà couvert la journée."
            % (day.strftime("%d/%m"), hit.get("reason") or "déjà fait")
        )
    else:
        lines.append("Aucune mise à jour du %s n'a été trouvée sur `main`." % day.strftime("%d/%m"))
    if hit.get("fetch_error"):
        lines.append("")
        lines.append("Note : git fetch a signalé : %s" % hit["fetch_error"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    import sys
    from tools.daily.store import repo_root
    from tools.daily.run import set_output, write_summary

    root = repo_root()
    fetch = os.environ.get("GITHUB_ACTIONS") == "true" or (argv and "--fetch" in argv)
    hit = update_already_done(root, fetch=fetch)
    text = summary_already_done(hit)
    write_summary(text)
    set_output("already_done", "true" if hit.get("done") else "false")
    if hit.get("done"):
        set_output("ready", "false")
        set_output("content", "false")
        set_output("publish_count", "0")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
