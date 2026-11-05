"""Tests v12 : groupes dissous (fiches, sources, liens, visibilité dans le réseau)."""
import json
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/"; D=json.load(open("site/data.json")); by={n["id"]:n for n in D["nodes"]}
G=["generation-identitaire","zouaves-paris","civitas","les-remparts","gud","pnat","cyril-hanouna"]
ok=fail=0; errs=[]
def check(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL:",m)
BAN=["revirement","pantin","complice","contradiction","alvarium","bastion social","cacqueray"]
for i in G:
    check(i in by,"node "+i)
    if i in by: check(not any(w in json.dumps(by[i],ensure_ascii=False).lower() for w in BAN),"mots exclus "+i)
for i in G[:5]: check(any(i in (e["source"],e["target"]) for e in D["edges"]),"lien "+i)
check(not any("vote" in k for k in D["meta"]["counts"]),"pas de section votes")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2).new_page()
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    for i in G[:5]:
        pg.goto(BASE+"#/personne/"+i); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(400)
        check(by[i]["name"] in pg.inner_text(".fiche"),"nom "+i)
        check(len(pg.eval_on_selector_all(".fiche a[href^='http']","e=>e.map(x=>x.href)"))>0,"sources "+i)
        if i=="generation-identitaire": pg.screenshot(path="/workspace/v12-groupes-mobile.png",full_page=True)
    pg.goto(BASE+"#/reseau"); pg.wait_for_function("window.__graphReady===true"); pg.wait_for_timeout(800)
    v=set(pg.evaluate("__visible()")); check(set(G)<=v,"visibles réseau "+str(set(G)-v))
    b.close()
check(not errs,"console "+str(errs[:3]))
print(f"{ok} ok, {fail} fail"); raise SystemExit(1 if fail else 0)
