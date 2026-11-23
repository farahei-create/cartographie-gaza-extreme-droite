import re
# -*- coding: utf-8 -*-
"""Enquête : données publiques, anciens liens, barre à cinq onglets."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)


ok = fail = 0
FORBIDDEN = ("complice", "génocidaire", "genocidaire", "pantin", "infiltré", "infiltre", "marionnette", "protégé", "protege", "copinage", "occulte")
PRIVATE_KEYS = {"adresse", "voie", "codepostal", "ville", "email", "telephone", "telephonedec", "datenaissance", "nomconjoint", "enfant", "enfants", "patrimoine", "pieceidentite"}


def check(cond, message):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print("FAIL:", message)


def keys(obj, found):
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.add(str(key).lower())
            keys(value, found)
    elif isinstance(obj, list):
        for item in obj:
            keys(item, found)


data = json.load(open("data.json", encoding="utf-8"))
enq = json.load(open("enquete.json", encoding="utf-8"))
edges = data["edges"]
ids = {n["id"] for n in data["nodes"]}
found = set()
keys(enq, found)
check(not (found & PRIVATE_KEYS), "pas de champ privé " + str(found & PRIVATE_KEYS))
blob = json.dumps(enq["hatvp"], ensure_ascii=False).lower()
check(not any(word in blob for word in FORBIDDEN), "mots interdits absents des intérêts")
check(len(enq["hatvp"]) >= 20, "au moins vingt fiches HATVP " + str(len(enq["hatvp"])))
for pid, row in enq["hatvp"].items():
    check(pid in ids, "fiche inconnue " + pid)
    check(str(row.get("url") or "").startswith("https://www.hatvp.fr/"), "lien HATVP " + pid)
    for group in ("mandates", "activities", "participations", "collaborators", "spouse_activity"):
        for item in row.get(group) or []:
            check(item.get("value") and item.get("url", "").startswith("https://"), "fait sans source " + pid)
            check("non publi" not in item["value"].lower(), "donnée non publiée recopiée " + pid)
check(all(m.get("url", "").startswith("https://") and m.get("media_id") in ids for m in enq["medias"]), "médias sourcés")

js = open("app.js", encoding="utf-8").read()
html = open("index.html", encoding="utf-8").read()
check("Citations" in html and "Enquête" in html and 'id="tab-liens"' in html and 'id="tab-condamnations"' in html, "barre à cinq onglets")
check("#/methodologie" in html or 'id="footer-methode"' in html, "méthode encore liée")
check("function shortestPath" not in js and "enquete/relier" not in html and "renderRail" in js, "Relier deux noms retiré, défilement gardé")
check(int(re.search(r'var VERSION = "onrecord-v(\d+)"', open("sw.js", encoding="utf-8").read()).group(1)) >= 52, "cache v52+")

print("%d ok, %d fail" % (ok, fail))
sys.exit(1 if fail else 0)
