# -*- coding: utf-8 -*-
"""Crée un tag annoté version-AAAA-MM-JJ-… sur un commit. Pas de force."""
import datetime
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

from tools.versions.catalog import write_catalog
from tools.versions.policy import tag_ok

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARIS = ZoneInfo("Europe/Paris")


def git(root, *args, check=True):
    result = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit((result.stderr or result.stdout or "git a échoué").strip())
    return result


def clean_note(note):
    text = re.sub(r"\s+", " ", (note or "").replace("\x00", " ")).strip()
    if not text:
        text = "Version enregistrée."
    return text[:400]


def slugify(text):
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40].strip("-")


def already_tagged(root, rev):
    result = git(root, "tag", "--points-at", rev, "version-*", check=False)
    if result.returncode != 0:
        return False
    return any(tag_ok(line.strip()) for line in result.stdout.splitlines())


def peel(root, rev):
    result = git(root, "rev-parse", "--verify", rev + "^{commit}")
    return result.stdout.strip()


def unique_name(root, base):
    name = base
    n = 2
    while git(root, "rev-parse", "--verify", "--quiet", "refs/tags/" + name, check=False).returncode == 0:
        name = base + "-" + str(n)
        n += 1
        if not tag_ok(name):
            raise SystemExit("Nom de version impossible : " + name)
    return name


def create_tag(root, rev, note, slug="", when=None):
    when = when or datetime.datetime.now(PARIS)
    commit = peel(root, rev)
    stamp = when.strftime("%Y-%m-%d")
    clock = when.strftime("%H%M")
    extra = slugify(slug)
    if extra:
        base = "version-%s-%s" % (stamp, extra)
    else:
        base = "version-%s-%s" % (stamp, clock)
    if not tag_ok(base):
        raise SystemExit("Nom de version refusé : " + base)
    name = unique_name(root, base)
    message = clean_note(note) + "\n"
    git(root, "tag", "-a", name, commit, "-m", message)
    return name


def commit_catalog(root, push):
    if not write_catalog(root):
        print("Liste des versions inchangée.")
        return False
    git(root, "add", "--", "versions.json")
    quiet = git(root, "diff", "--cached", "--quiet", "--", "versions.json", check=False)
    if quiet.returncode == 0:
        return False
    day = datetime.datetime.now(PARIS).strftime("%d/%m")
    git(root, "commit", "-m", "Mise à jour du %s : liste des versions" % day)
    if push:
        git(root, "push", "origin", "HEAD:main")
    return True


def push_tag(root, name):
    git(root, "push", "origin", "refs/tags/" + name)


def run(root, event, note, slug, before, push):
    if event == "push":
        if not before or set(before) <= {"0"}:
            print("Pas de commit précédent à enregistrer.")
            return 0
        if already_tagged(root, before):
            print("Ce commit a déjà une version.")
            return 0
        name = create_tag(
            root, before,
            "Version enregistrée avant une modification de l'interface.",
            slug="avant-modif",
        )
        print("Version enregistrée :", name)
        if push:
            push_tag(root, name)
        return 0
    if event == "schedule":
        head = peel(root, "HEAD")
        parent = git(root, "rev-parse", "--verify", "HEAD^", check=False)
        parent_ok = parent.returncode == 0 and already_tagged(root, parent.stdout.strip())
        if already_tagged(root, head) or parent_ok:
            print("Ce commit a déjà une version. Pas de doublon du dimanche.")
            return 0
        name = create_tag(root, "HEAD", "Version automatique du dimanche.", slug="hebdo")
        print("Version enregistrée :", name)
        commit_catalog(root, push)
        if push:
            push_tag(root, name)
        return 0
    name = create_tag(root, "HEAD", note or "Version enregistrée à la main.", slug=slug)
    print("Version enregistrée :", name)
    commit_catalog(root, push)
    if push:
        push_tag(root, name)
    return 0


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    root = os.environ.get("ONRECORD_ROOT") or ROOT
    event = os.environ.get("EVENT") or os.environ.get("GITHUB_EVENT_NAME") or "workflow_dispatch"
    note = os.environ.get("NOTE") or ""
    slug = os.environ.get("NOM") or ""
    before = os.environ.get("BEFORE") or ""
    push = os.environ.get("GITHUB_ACTIONS") == "true"
    if "--no-push" in argv:
        push = False
    return run(root, event, note, slug, before, push)


if __name__ == "__main__":
    raise SystemExit(main())
