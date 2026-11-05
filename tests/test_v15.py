"""Tests v15 : portrait sur les cartes de partage (fond + médaillon), sans photo inchangé."""
import base64
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/"; ok=fail=0; errs=[]
def check(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL:",m)
import re as _re; check(int(_re.search(r"onrecord-v(\d+)",open("site/sw.js").read()).group(1))>=15,"sw v15+")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,accept_downloads=True).new_page()
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    def share(pid, sel="[data-act='share']"):
        pg.goto(BASE+"#/personne/"+pid); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(900)
        pg.evaluate("window.__lastCard=null"); pg.locator(".fiche "+sel).first.click(); pg.wait_for_timeout(500)
        return pg.evaluate("window.__lastCard && {w:__lastCard.w,h:__lastCard.h,size:__lastCard.size,portrait:__lastCard.portrait,d:__lastCard.dataUrl}")
    c=share("emmanuel-macron")
    check(c and c["w"]==1080 and c["h"]==1350,"taille carte photo"); check(c and c["portrait"] is True,"portrait dessiné")
    check(pg.evaluate("window.__lastCardHadPortrait") is True,"hook portrait")
    open("/workspace/v15-card-portrait.png","wb").write(base64.b64decode(c["d"].split(",")[1]))
    c0=share("jean-luc-melenchon")
    check(c0 and c0["w"]==1080 and c0["h"]==1350,"carte sans photo"); check(c0 and c0["portrait"] is False,"pas de portrait sans photo")
    check(c["size"]>c0["size"],"carte photo plus lourde")
    pg.goto(BASE+"#/personne/marine-le-pen"); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(900)
    if pg.locator(".fiche [data-act='share-duo']").count():
        pg.evaluate("window.__lastCard=null"); pg.locator(".fiche [data-act='share-duo']").first.click(); pg.wait_for_timeout(500)
        d=pg.evaluate("window.__lastCard && {w:__lastCard.w,portrait:__lastCard.portrait,d:__lastCard.dataUrl}")
        check(d and d["w"]==1080 and d["portrait"] is True,"duo portrait")
        if d: open("/workspace/v15-card-duo.png","wb").write(base64.b64decode(d["d"].split(",")[1]))
    else: check(False,"pas de duo Le Pen")
    b.close()
check(not errs,"console "+str(errs[:3]))
print(f"{ok} ok, {fail} fail"); raise SystemExit(1 if fail else 0)
