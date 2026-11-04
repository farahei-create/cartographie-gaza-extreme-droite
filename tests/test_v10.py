"""Tests v10 : fiches cyril-hanouna, nemesis, issep (rendu + sources), capture mobile."""
import json
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/"; D=json.load(open("site/data.json")); by={n["id"]:n for n in D["nodes"]}
ok=fail=0; errs=[]
def check(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL:",m)
BAN=["revirement","pantin","complice","contradiction"]
for i in ["cyril-hanouna","nemesis","issep","m6"]:
    check(i in by,"node "+i); t=json.dumps(by[i],ensure_ascii=False).lower()
    check(not any(w in t for w in BAN),"mots interdits "+i)
for w in ["antipodes","Télé Star","IFP"]: check(w not in json.dumps(by["cyril-hanouna"],ensure_ascii=False),"à vérifier exclu "+w)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2).new_page()
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    for i in ["cyril-hanouna","nemesis","issep"]:
        n=by[i]; pg.goto(BASE+"#/personne/"+i); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(500)
        txt=pg.inner_text(".fiche"); check(n["name"] in txt,"nom "+i)
        hrefs=pg.eval_on_selector_all(".fiche a[href^='http']","els=>els.map(e=>e.href)")
        urls={s["url"] for s in n["statements"]}|{e["url"] for e in D["edges"] if i in (e["source"],e["target"])}
        check(len(hrefs)>0,"sources visibles "+i)
        if n["statements"]:
            check(pg.locator(".fiche .tl-item a.src").count()==len(n["statements"]),"liens source "+i)
        if i=="cyril-hanouna":
            check(pg.locator("#am").count()==1,"bloc Avant / maintenant")
            check(any("web.archive.org" in h for h in hrefs),"lien archive")
            pg.screenshot(path="/workspace/v10-hanouna-mobile.png",full_page=True)
    b.close()
check(not errs,"console "+str(errs[:3]))
print(f"{ok} ok, {fail} fail"); raise SystemExit(1 if fail else 0)
