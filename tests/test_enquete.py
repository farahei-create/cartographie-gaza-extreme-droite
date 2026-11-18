# -*- coding: utf-8 -*-
"""Enquête : chemin, données publiques, anciens liens, barre à quatre onglets."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from tools.enquete_path import shortest_path

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
check(shortest_path(edges, "marine-le-pen", "marine-le-pen") == [], "même fiche")
check(shortest_path(edges, "personne-absente", "marine-le-pen") is None, "fiche inconnue")
# un lien direct, s'il existe
direct = next((e for e in edges if e["source"] == "marine-le-pen" and e.get("url")), None)
if direct:
    path = shortest_path(edges, direct["source"], direct["target"])
    check(path and path[0]["url"].startswith("https://") and path[0].get("date"), "étape directe sourcée")
else:
    check(False, "pas de lien Le Pen")
# deux fiches sans lien forcé : le résultat est une liste ou None, jamais une relation inventée
ghost = shortest_path([{"source": "a", "target": "b", "url": "https://exemple.fr", "date": "2020-01-01", "nature": "autre", "relation": "x"}], "a", "c")
check(ghost is None, "aucun chemin")
one = shortest_path([
    {"source": "a", "target": "b", "url": "https://exemple.fr/1", "date": "2020-01-01", "nature": "ascension", "relation": "a nommé"},
    {"source": "b", "target": "c", "url": "https://exemple.fr/2", "date": "2021-01-01", "nature": "opposition", "relation": "a critiqué"},
], "a", "c")
check(one and len(one) == 2 and one[0]["date"] == "2020-01-01" and one[1]["url"].endswith("/2"), "chemin de deux étapes")

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
check("Citations" in html and "Enquête" in html and 'id="tab-liens"' in html, "barre à quatre onglets")
check("#/methodologie" in html or 'id="footer-methode"' in html, "méthode encore liée")
check("function shortestPath" in js and "renderRail" in js, "chemin et défilement dans la page")
check('var VERSION = "onrecord-v51"' in open("sw.js", encoding="utf-8").read(), "cache v51")

print("%d ok, %d fail" % (ok, fail))
sys.exit(1 if fail else 0)
