# -*- coding: utf-8 -*-
"""Vérifie que le site répond. Avant le push : la version en ligne charge.
Après le push d'un contenu : la nouvelle version de sw.js finit par répondre.
"""
import json
import os
import sys
import time
import urllib.request

SITE = "https://onrecord-fr.vercel.app"
UA = "OnrecordDaily/1.0 (+https://onrecord-fr.vercel.app/)"


def fetch(path, timeout=25):
    req = urllib.request.Request(SITE + path, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.status, res.read()


def preflight():
    status, sw = fetch("/sw.js")
    text = sw.decode("utf-8", "replace")
    if status != 200 or "onrecord-v" not in text:
        print("sw.js en ligne illisible")
        return 1
    status, raw = fetch("/data.json")
    data = json.loads(raw.decode("utf-8"))
    if status != 200 or not data.get("nodes"):
        print("data.json en ligne illisible")
        return 1
    status, _ = fetch("/")
    if status != 200:
        print("page d'accueil indisponible")
        return 1
    version = text.split('var VERSION = "')[1].split('"')[0]
    print("Site en ligne :", version, "phrases", data["meta"]["counts"].get("statements"))
    return 0


def postflight(version, attempts=12, pause=15):
    if not version:
        return preflight()
    for _ in range(attempts):
        try:
            status, sw = fetch("/sw.js")
            text = sw.decode("utf-8", "replace")
            if status == 200 and version in text:
                _, raw = fetch("/data.json")
                data = json.loads(raw.decode("utf-8"))
                print("En ligne :", version, "phrases", data["meta"]["counts"].get("statements"))
                return 0
        except Exception as exc:
            print("attente :", exc)
        time.sleep(pause)
    print("La version %s n'est pas encore servie." % version)
    return 1


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "preflight"
    if cmd == "preflight":
        return preflight()
    if cmd == "postflight":
        version = argv[2] if len(argv) > 2 else ""
        if not version and os.path.exists("/tmp/onrecord-daily-version.txt"):
            version = open("/tmp/onrecord-daily-version.txt", encoding="utf-8").read().strip()
        return postflight(version)
    print("Commande inconnue.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
