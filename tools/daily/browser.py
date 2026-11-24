# -*- coding: utf-8 -*-
"""Navigateur des tests : Chrome système en CI, sinon le Chromium de Playwright."""
import os

CANDIDATES = (
    os.environ.get("ONRECORD_CHROME"),
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
)


def chrome_executable():
    for path in CANDIDATES:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def launch_chromium(playwright, **kwargs):
    """Comme les tests historiques : /usr/bin/google-chrome s'il est là.

    Un simple playwright.chromium.launch() cherche le Chromium empaqueté,
    qui n'est pas installé sur le runner GitHub (échec du 23/11/2026).
    """
    path = chrome_executable()
    if path:
        kwargs.setdefault("executable_path", path)
    return playwright.chromium.launch(**kwargs)
