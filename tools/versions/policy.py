# -*- coding: utf-8 -*-
"""Règle d'un retour en arrière.

Le site public (pages, style, script, données, citations, y compris
tools/auto_published.json) redevient celui de la version choisie.

On ne revient pas sur :
- le relevé du matin (code, workflow, tests de garde-fous) ;
- la file d'attente auto_pending.json (ce n'est pas publié) ;
- la page admin et ce mode d'emploi, pour pouvoir encore enregistrer ou revenir ;
- le journal, qui reçoit une ligne nouvelle.

tools/auto_published.json est remis avec la version. Sinon le prochain
build.py réinjecterait les phrases parues après, et le retour ne tiendrait pas.
Une phrase encore dans les 48 heures peut être retrouvée par le relevé du
lendemain : les mêmes contrôles s'appliquent. Au-delà, elle ne revient pas seule.
"""
import re

TAG_RE = re.compile(r"^version-[0-9]{4}-[0-9]{2}-[0-9]{2}(-[a-z0-9]+)*$")

KEEP_EXACT = {
    "auto_pending.json",
    "docs/JOURNAL.md",
    "docs/REPRISE.md",
    "AGENTS.md",
    "admin.html",
    "admin.js",
    "tests/test_daily.py",
    "versions.json",
}
KEEP_PREFIXES = (
    ".github/",
    "tools/daily/",
    "tools/versions/",
)
VERSION_FILES = (
    "sw.js",
    "tests/test_v13.py",
    "tests/test_v22.py",
    "tests/test_v23.py",
    "tests/test_v24.py",
    "tests/test_admin.py",
)


def tag_ok(name):
    if not name or "/" in name or ".." in name:
        return False
    return bool(TAG_RE.match(name))


def keep_path(path):
    path = (path or "").replace("\\", "/")
    if path.startswith("./"):
        path = path[2:]
    if path in KEEP_EXACT:
        return True
    return any(path.startswith(prefix) for prefix in KEEP_PREFIXES)
