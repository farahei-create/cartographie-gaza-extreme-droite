# -*- coding: utf-8 -*-
"""Commit et push sur main, seulement des fichiers nommés. Pas de git add -A."""
import json
import os
import subprocess
import sys

from tools.daily import incidents
from tools.daily.store import bump_version, journal_entry, prepend_journal, sync_expect, write_resume

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = "/tmp/onrecord-daily-state.json"
ALLOWED = (
    "tools/auto_published.json",
    "auto_pending.json",
    "incidents.json",
    "resume.json",
    "tools/archives.json",
    "data.json",
    "sw.js",
    "docs/JOURNAL.md",
    "tests/test_v13.py",
    "tests/test_v22.py",
    "tests/test_v23.py",
    "tests/test_v24.py",
    "tests/test_admin.py",
)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True)


def content_same(path):
    """data.json : ignorer un écart qui n'est que la date."""
    sys.path.insert(0, ROOT)
    import tools.commit_data_if_content as commit_data
    shown = git("show", "HEAD:data.json")
    if shown.returncode != 0:
        return False
    old = json.loads(shown.stdout)
    new = json.loads(open(path, encoding="utf-8").read())
    return not commit_data.content_changed(old, new)


def finalize():
    if not os.path.exists(STATE):
        print("Pas d'état de relevé.")
        return 0
    state = json.loads(open(STATE, encoding="utf-8").read())
    if not state.get("content") and not state.get("pending_changed"):
        print("Rien à finaliser (journal des problèmes seulement)." if state.get("incidents_changed") else "Rien à finaliser.")
        return 0
    version = ""
    if state.get("content"):
        version = bump_version(ROOT)
        sync_expect(ROOT)
        try:
            write_resume(ROOT, state)
        except Exception as exc:  # le résumé ne bloque jamais la publication
            incidents.add("resume", "Résumé du jour non écrit", str(exc))
    import datetime
    day = datetime.date.fromisoformat(state["day"])
    entry = journal_entry(day, state.get("published") or [], state.get("pending_count") or 0, version)
    prepend_journal(ROOT, entry)
    if version:
        with open("/tmp/onrecord-daily-version.txt", "w", encoding="utf-8") as handle:
            handle.write(version)
    print("Finalisé.", version or "sans nouvelle version de cache")
    return 0


def publish():
    if not os.path.exists(STATE):
        print("Pas d'état : rien à pousser.")
        return 0
    state = json.loads(open(STATE, encoding="utf-8").read())
    if not state.get("content") and not state.get("pending_changed") and not state.get("incidents_changed"):
        print("Rien à pousser.")
        return 0
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    paths = []
    for rel in ALLOWED:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        if rel == "data.json" and content_same(path):
            git("checkout", "--", "data.json")
            continue
        diff = git("diff", "--", rel)
        staged = git("diff", "--cached", "--", rel)
        untracked = git("ls-files", "--others", "--exclude-standard", "--", rel)
        if diff.stdout.strip() or staged.stdout.strip() or untracked.stdout.strip():
            paths.append(rel)
    share = git("status", "--porcelain", "-uall", "--", "c")
    share_hit = False
    for line in (share.stdout or "").splitlines():
        path = line[3:].strip().strip('"')
        if path.startswith("c/") and path.endswith(".html"):
            share_hit = True
            break
    if share_hit:
        git("add", "-A", "--", "c")
        paths.append("c/")
    if not paths:
        print("Arbre inchangé.")
        return 0
    add = git("add", "--", *paths)
    if add.returncode != 0:
        print(add.stderr)
        return 1
    import datetime
    day = datetime.date.fromisoformat(state["day"])
    stamp = day.strftime("%d/%m")
    if state.get("slot") in ("matin", "soir"):
        stamp += " (%s)" % state["slot"]
    if state.get("content"):
        message = "Mise à jour du %s : relevé automatique, %d phrase%s" % (
            stamp, state.get("added") or 0, "s" if (state.get("added") or 0) != 1 else "")
    elif state.get("pending_changed"):
        message = "Mise à jour du %s : file d'attente, rien publié" % stamp
    else:
        message = "Mise à jour du %s : journal des problèmes" % stamp
    commit = git("commit", "-m", message)
    if commit.returncode != 0:
        print(commit.stderr or commit.stdout)
        return 1
    print(commit.stdout.strip())
    # Tout ce qui n'est pas publié (captures de tests, fichiers temporaires) est mis de côté :
    # un arbre « sale » faisait échouer le pull --rebase (panne du 25 au 27/11).
    leftovers = git("status", "--porcelain")
    if (leftovers.stdout or "").strip():
        print("Mis de côté avant le pull :\n" + leftovers.stdout.strip()[:1500])
        git("stash", "push", "--include-untracked", "-m", "onrecord-daily-leftovers")
    for attempt in range(3):
        pull = git("pull", "--rebase", "origin", "main")
        if pull.returncode == 0:
            push = git("push", "origin", "HEAD:main")
            if push.returncode == 0:
                print("Poussé sur main.")
                return 0
            print(push.stderr or push.stdout)
        else:
            print(pull.stderr or pull.stdout)
            git("rebase", "--abort")
        import time
        time.sleep(10 * (attempt + 1))
    return 1


def main(argv):
    os.chdir(ROOT)
    cmd = argv[1] if len(argv) > 1 else "publish"
    if cmd == "finalize":
        return finalize()
    if cmd == "publish":
        return publish()
    print("Commande inconnue.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
