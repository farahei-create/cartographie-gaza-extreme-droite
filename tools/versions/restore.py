# -*- coding: utf-8 -*-
"""Remet le site public à une version enregistrée, par un commit nouveau.

Pas de force-push : l'historique reste, et l'état d'avant le retour est
lui-même tagué. Voir tools/versions/policy.py pour ce qui est gardé.
"""
import datetime
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

from tools.versions.catalog import write_catalog
from tools.versions.policy import VERSION_FILES, keep_path, tag_ok
from tools.versions.save import create_tag, peel

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARIS = ZoneInfo("Europe/Paris")


def git(root, *args, check=True):
    result = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit((result.stderr or result.stdout or "git a échoué").strip())
    return result


def files_at(root, rev):
    result = git(root, "ls-tree", "-r", "--name-only", rev)
    return [line for line in result.stdout.splitlines() if line]


def version_number(root):
    path = os.path.join(root, "sw.js")
    if not os.path.exists(path):
        return 0
    text = open(path, encoding="utf-8").read()
    found = re.search(r"onrecord-v(\d+)", text)
    return int(found.group(1)) if found else 0


def force_version(root, number):
    new = "onrecord-v%d" % number
    for rel in VERSION_FILES:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        updated = re.sub(r"onrecord-v\d+", new, text)
        if updated != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(updated)
    return new


def prepend_journal(root, entry):
    path = os.path.join(root, "docs", "JOURNAL.md")
    if not os.path.exists(path):
        return
    text = open(path, encoding="utf-8").read()
    at = text.find("\n## ")
    if at < 0:
        text = text.rstrip() + "\n\n" + entry
    else:
        text = text[: at + 1] + entry.rstrip() + "\n\n" + text[at + 1 :]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def batched(root, args, paths):
    for start in range(0, len(paths), 80):
        git(root, *args, *paths[start : start + 80])


def plan(root, version):
    tag_files = files_at(root, "refs/tags/" + version)
    head_files = files_at(root, "HEAD")
    tag_set = set(tag_files)
    restore = [path for path in tag_files if not keep_path(path)]
    remove = [path for path in head_files if path not in tag_set and not keep_path(path)]
    return restore, remove


def journal_entry(day, version, safety, cache):
    return "\n".join([
        "## %s — retour à %s" % (day.isoformat(), version),
        "",
        "Tu remets le site public à `%s` : pages, citations, et mémoire du relevé automatique (`tools/auto_published.json`)." % version,
        "La file d'attente du matin est gardée. L'état d'avant ce retour est `%s`, pour annuler l'annulation." % safety,
        "Une phrase sortie du site peut revenir seulement si le relevé du lendemain la retrouve encore, dans les 48 heures, et qu'elle passe les contrôles.",
        "",
        "Cache `%s`." % cache,
        "",
    ])


def apply_restore(root, version, push):
    if not tag_ok(version):
        raise SystemExit("Nom de version refusé. Il commence par version- et une date.")
    git(root, "rev-parse", "--verify", "refs/tags/" + version)
    dirty = git(root, "status", "--porcelain", check=False)
    if dirty.stdout.strip():
        raise SystemExit("Le dépôt a des fichiers non enregistrés. Rien n'a été changé.")
    target = peel(root, "refs/tags/" + version)
    head = peel(root, "HEAD")
    if target == head:
        print("Le site est déjà à cette version. Rien à faire.")
        return 0
    before_n = version_number(root)
    safety = create_tag(
        root, "HEAD",
        "État enregistré automatiquement avant le retour à %s." % version,
        slug="avant-retour",
    )
    print("État courant enregistré :", safety)
    restore, remove = plan(root, version)
    if remove:
        batched(root, ["rm", "-f", "--"], remove)
    if restore:
        batched(root, ["checkout", "refs/tags/" + version, "--"], restore)
    after_n = version_number(root)
    cache = force_version(root, max(before_n, after_n) + 1)
    write_catalog(root)
    day = datetime.datetime.now(PARIS).date()
    prepend_journal(root, journal_entry(day, version, safety, cache))
    git(root, "add", "-A")
    cached = git(root, "diff", "--cached", "--quiet", check=False)
    if cached.returncode == 0:
        print("Aucun changement de fichiers.")
        return 1
    message = "Mise à jour du %s : retour à %s" % (day.strftime("%d/%m"), version)
    git(root, "commit", "-m", message)
    print(message)
    print("Cache", cache)
    if push:
        branch = git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if branch != "main":
            raise SystemExit("Refus de pousser : la branche n'est pas main.")
        git(root, "push", "origin", "HEAD:main")
        git(root, "push", "origin", "refs/tags/" + safety)
        print("Poussé sur main.")
    return 0


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    root = os.environ.get("ONRECORD_ROOT") or ROOT
    version = os.environ.get("VERSION") or ""
    confirm = os.environ.get("CONFIRM") or ""
    push = "--push" in argv
    apply = "--apply" in argv
    if "--version" in argv:
        version = argv[argv.index("--version") + 1]
    if "--confirm" in argv:
        confirm = argv[argv.index("--confirm") + 1]
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
    if not version:
        raise SystemExit("Indique le nom de la version.")
    if not apply:
        if not tag_ok(version):
            raise SystemExit("Nom de version refusé.")
        restore, remove = plan(root, version)
        print("Remettrait %d fichiers, retirerait %d fichiers." % (len(restore), len(remove)))
        print("Gardés : file d'attente, admin, relevé du matin, mode d'emploi.")
        print("tools/auto_published.json est remis avec la version.")
        return 0
    if confirm != "REVENIR":
        raise SystemExit("Confirmation refusée. Écris REVENIR pour lancer le retour.")
    return apply_restore(root, version, push)


if __name__ == "__main__":
    raise SystemExit(main())
