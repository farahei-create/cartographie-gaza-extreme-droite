"""Contrôle la page admin : logique GitHub simulée, et build.py sur un fichier source."""
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

ok = fail = 0

def check(c, m):
    global ok, fail
    if c:
        ok += 1
    else:
        fail += 1
        print("FAIL:", m)

node = subprocess.run(["node", "tests/admin_mock.test.mjs"], cwd=ROOT, capture_output=True, text=True)
check(node.returncode == 0, (node.stdout + node.stderr)[-500:])

spec = importlib.util.spec_from_file_location("commit_data", os.path.join(ROOT, "tools", "commit_data_if_content.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
old = {"meta": {"generated": "2020-01-01", "methodology": "testée le 2020-01-01", "counts": {"statements": 1}}, "nodes": [{"id": "a"}], "edges": []}
new = {"meta": {"generated": "2026-11-12", "methodology": "testée le 2026-11-12", "counts": {"statements": 1}}, "nodes": [{"id": "a"}], "edges": []}
check(not mod.content_changed(old, new), "date seule")
new2 = json.loads(json.dumps(new))
new2["nodes"].append({"id": "b"})
check(mod.content_changed(old, new2), "contenu")

import admin_content
wiki = json.load(open("tests/fixtures/admin_wiki.json", encoding="utf-8"))
errs = admin_content.validate(wiki, {"marine-le-pen"})
check(any("Wikipédia" in e or "wikipedia" in e.lower() for e in errs), errs)

html = open("index.html", encoding="utf-8").read()
check("admin.html" not in html and "href=\"admin" not in html, "pas de lien depuis l'accueil")
admin = open("admin.html", encoding="utf-8").read()
check('content="noindex, nofollow"' in admin, "noindex")
check("admin.html" in open("robots.txt", encoding="utf-8").read(), "robots")
check("onrecord-v40" in open("sw.js", encoding="utf-8").read(), "sw v40")
check("admin.html" in open("sw.js", encoding="utf-8").read() and "admin.js" in open("sw.js", encoding="utf-8").read(), "précache admin")

out = "/tmp/onrecord-admin-ok.json"
env = os.environ.copy()
env["ONRECORD_ADMIN_JSON"] = os.path.join(ROOT, "tests/fixtures/admin_ok.json")
env["ONRECORD_DATA_OUT"] = out
built = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env=env, capture_output=True, text=True)
check(built.returncode == 0, built.stderr[-800:] or built.stdout[-400:])
if built.returncode == 0:
    data = json.load(open(out, encoding="utf-8"))
    by = {n["id"]: n for n in data["nodes"]}
    p = by.get("personne-admin-fixture")
    check(p is not None, "fiche fixture")
    if p:
        check(p.get("parcours") and p["parcours"][0]["url"].startswith("https://"), "parcours sourcé")
        check(p.get("image", "").endswith(".webp") and p.get("image_credit", {}).get("author"), "crédit photo")
        check(any("générateur" in s["quote"] for s in p["statements"]), "citation")
        check(p["category"] in data["meta"]["category_order"], "catégorie")
        blob = (p["role"] + p["description"] + p["statements"][0]["medium"]).lower()
        for bad in ("complice", "pantin", "marionnette", "génocidaire", "infiltré", "copinage", "occulte"):
            check(bad not in blob, "mot " + bad)
    check(any(e["source"] == "personne-admin-fixture" and e["target"] == "rn" and e["nature"] == "autre" for e in data["edges"]), "lien")
    ids = {n["id"] for n in data["nodes"]}
    check(all(e["source"] in ids and e["target"] in ids for e in data["edges"]), "extrémités")

env["ONRECORD_ADMIN_JSON"] = os.path.join(ROOT, "tests/fixtures/admin_wiki.json")
env["ONRECORD_DATA_OUT"] = "/tmp/onrecord-admin-wiki.json"
bad = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env=env, capture_output=True, text=True)
check(bad.returncode != 0 and "Wikipédia" in (bad.stderr + bad.stdout), (bad.stderr + bad.stdout)[-400:])

print(f"{ok} ok, {fail} fail")
sys.exit(1 if fail else 0)
