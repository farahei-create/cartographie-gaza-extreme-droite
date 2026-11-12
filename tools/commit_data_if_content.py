#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commit data.json seulement si le contenu a changé, pas si seule la date bouge."""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data.json")


def canon(d):
    meta = dict(d.get("meta") or {})
    meta.pop("generated", None)
    meth = meta.get("methodology") or ""
    meta["methodology"] = re.sub(r"\d{4}-\d{2}-\d{2}", "DATE", meth)
    return json.dumps(
        {"meta": meta, "nodes": d.get("nodes"), "edges": d.get("edges")},
        ensure_ascii=False,
        sort_keys=True,
    )


def content_changed(old, new):
    return canon(old) != canon(new)


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True)


def main():
    with open(PATH, encoding="utf-8") as f:
        new = json.load(f)
    shown = _git("show", "HEAD:data.json")
    if shown.returncode == 0:
        old = json.loads(shown.stdout)
        if not content_changed(old, new):
            print("data.json : seule la date change, pas de commit")
            return 0
    add = _git("add", "data.json")
    if add.returncode != 0:
        print(add.stderr)
        return 1
    diff = _git("diff", "--cached", "--quiet", "--", "data.json")
    if diff.returncode == 0:
        print("data.json inchangé")
        return 0
    msg = os.environ.get("ONRECORD_DATA_COMMIT_MSG") or "admin: data.json régénéré"
    commit = _git("commit", "-m", msg)
    if commit.returncode != 0:
        print(commit.stderr or commit.stdout)
        return 1
    print(commit.stdout.strip())
    if os.environ.get("CI"):
        push = _git("push", "origin", "HEAD:main")
        if push.returncode != 0:
            print(push.stderr)
            return 1
        print("data.json poussé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
