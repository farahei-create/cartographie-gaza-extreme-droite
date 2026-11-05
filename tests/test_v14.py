"""Tests v14 : candidats à la présidentielle 2027 (fiches, citations sourcées, liens, réseau)."""
import json
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/"; D=json.load(open("site/data.json")); by={n["id"]:n for n in D["nodes"]}
G=["jean-luc-melenchon","raphael-glucksmann","fabien-roussel","marine-tondelier","edouard-philippe","gabriel-attal","xavier-bertrand","dominique-de-villepin"]
ok=fail=0; errs=[]
def check(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL:",m)
BAN=["revirement","pantin","complice","contradiction"]
for i in G:
    check(i in by and by[i]["type"]=="person","node "+i)
    if i not in by: continue
    n=by[i]; check(n["subcategory"]=="Candidats à la présidentielle 2027","sous-catégorie "+i)
    check(len(n["statements"])>=1 and all(s["url"].startswith("https://") and len(s["date"])==10 for s in n["statements"]),"citations datées "+i)
    check(not any(w in json.dumps(n,ensure_ascii=False).lower() for w in BAN),"mots exclus "+i)
    check(any(i in (e["source"],e["target"]) for e in D["edges"]),"lien "+i)
check(len(by["emmanuel-macron"]["statements"])>=3,"Macron renforcé")
check(not any("vote" in k for k in D["meta"]["counts"]),"pas de section votes")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2).new_page()
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    for i in G:
        pg.goto(BASE+"#/personne/"+i); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(300)
        t=pg.inner_text(".fiche"); check(by[i]["name"] in t,"nom "+i)
        check(not any(w in t.lower() for w in BAN),"mots exclus page "+i)
        if i=="jean-luc-melenchon": pg.screenshot(path="/workspace/v14-melenchon-mobile.png")
        if i=="xavier-bertrand": pg.screenshot(path="/workspace/v14-bertrand-mobile.png")
    pg.goto(BASE+"#/reseau"); pg.wait_for_function("window.__graphReady===true"); pg.wait_for_timeout(800)
    v=set(pg.evaluate("__visible()")); check(set(G)<=v,"visibles réseau "+str(set(G)-v))
    b.close()
check(not errs,"console "+str(errs[:3]))
print(f"{ok} ok, {fail} fail"); raise SystemExit(1 if fail else 0)
