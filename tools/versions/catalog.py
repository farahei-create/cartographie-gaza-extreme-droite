# -*- coding: utf-8 -*-
"""Lit les tags version-* et écrit versions.json, lu par la page admin."""
import json
import os
import subprocess

from tools.versions.policy import tag_ok

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = "farahei-create/cartographie-gaza-extreme-droite"
NOTICE = "Versions enregistrées du site. Le retour se fait depuis la page admin, sur GitHub."


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True)


def read_tags(root):
    sep = "\x1f"
    fmt = sep.join([
        "%(refname:short)", "%(*objectname)", "%(objectname)",
        "%(creatordate:iso-strict)", "%(subject)",
    ])
    result = git(root, "for-each-ref", "--sort=-creatordate", "--format=" + fmt, "refs/tags/version-*")
    if result.returncode != 0:
        raise SystemExit(result.stderr or "Lecture des tags impossible.")
    items = []
    for line in result.stdout.splitlines():
        parts = line.split(sep)
        if len(parts) < 5:
            continue
        name, peeled, obj, date, subject = parts[0], parts[1], parts[2], parts[3], parts[4]
        if not tag_ok(name):
            continue
        commit = peeled or obj
        items.append({
            "name": name,
            "date": date,
            "note": (subject or "").strip(),
            "commit": commit,
            "github": "https://github.com/%s/tree/%s" % (REPO, name),
        })
    return items


def write_catalog(root=None):
    root = root or ROOT
    items = read_tags(root)
    path = os.path.join(root, "versions.json")
    payload = {"_notice": NOTICE, "versions": items}
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    previous = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            previous = handle.read()
    if previous == text:
        return False
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return True


def main():
    changed = write_catalog(ROOT)
    print("versions.json", "mis à jour" if changed else "inchangé", len(read_tags(ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
