import re,sys
from playwright.sync_api import sync_playwright
B="http://localhost:8765/";ok=fail=0
def chk(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL",m)
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=br.new_page(viewport={"width":390,"height":844});errs=[]
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto(B+"#/accueil");pg.wait_for_function("window.__route=='accueil'")
    chk("onrecord-v16" in open("site/sw.js").read(),"sw v16")
    ft=pg.inner_text("footer");chk("GitHub" not in ft and "issue" not in ft,"footer github");chk("Proposer une mise à jour" in ft,"footer link")
    pg.goto(B+"#/methodologie");pg.wait_for_timeout(300)
    t=pg.inner_text("#view-methodologie");chk("GitHub" not in t,"meth github");chk(pg.locator('#view-methodologie a[href="#/contribuer"]').count()==1,"meth link")
    chk("GitHub" not in pg.content(),"no github anywhere")
    pg.goto(B+"#/methode");pg.wait_for_timeout(300);chk(pg.locator('#view-methode a[href="#/contribuer"]').count()>=1,"methode link")
    pg.goto(B+"#/accueil");pg.wait_for_timeout(300);chk(pg.locator('#home-entries a[href="#/contribuer"]').count()==1,"home entry")
    pg.screenshot(path="/workspace/v16-footer-mobile.png",clip={"x":0,"y":max(0,pg.evaluate("document.body.scrollHeight")-600),"width":390,"height":600},full_page=True)
    pg.goto(B+"#/contribuer");pg.wait_for_timeout(300)
    chk(not pg.locator("#view-contribuer").is_hidden(),"view shown");chk(pg.title().startswith("Proposer une mise à jour"),"title")
    chk(pg.locator("#cf-type option").count()==6,"type options")
    pg.click("#cf-submit");chk(pg.is_visible("#cf-err"),"validation err");chk(pg.locator("#cf-out").is_hidden(),"no out on err")
    pg.select_option("#cf-type",index=2);pg.fill("#cf-who","Exemple");pg.fill("#cf-date","2025-07-24");pg.fill("#cf-text","Texte « test »")
    pg.fill("#cf-src","pas une url");pg.click("#cf-submit");chk(pg.is_visible("#cf-err"),"bad url rejected")
    pg.fill("#cf-src","https://example.org/a");pg.click("#cf-submit")
    chk(pg.is_visible("#cf-out"),"copy box shown");m=pg.input_value("#cf-msg")
    chk("Nouvelle déclaration" in m and "https://example.org/a" in m and "2025" in m,"msg content")
    pg.context.grant_permissions(["clipboard-read","clipboard-write"]);pg.click("#cf-copy");pg.wait_for_timeout(300)
    chk(pg.evaluate("navigator.clipboard.readText()")==m,"clipboard")
    pg.screenshot(path="/workspace/v16-contribuer-mobile.png",full_page=True)
    pg.evaluate("window.SITE_CONFIG.CORRECTION_EMAIL='test@example.org'")
    pg.route("**/*",lambda r: r.continue_())
    pg.evaluate("document.getElementById('cf-out').hidden=true")
    pg.click("#cf-submit");pg.wait_for_timeout(300)
    h=pg.evaluate("window.__lastMailto||''")
    chk(h.startswith("mailto:test@example.org?subject=Onrecord%20%3A%20proposition"),"mailto "+h[:60])
    chk("example.org%2Fa" in h,"mailto body");chk(pg.locator("#cf-out").is_hidden(),"no copybox w/ mail")
    chk(not errs,"console "+str(errs))
    br.close()
print(f"{ok} ok, {fail} fail")
