"""Ancienne page « Proposer une mise à jour » : retirée le 23/11 au profit des contributions.
Vérifie les liens « Ajouter une contribution », la redirection des anciennes adresses
(#/contribuer, #/enquete/relier/…) et l'absence de « Relier deux noms »."""
import re
from playwright.sync_api import sync_playwright
B="http://localhost:8765/";ok=fail=0
def chk(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL",m)
with sync_playwright() as p:
    br=p.chromium.launch()
    pg=br.new_page(viewport={"width":390,"height":844});errs=[]
    pg.on("console",lambda m: m.type=="error" and "Failed to load resource" not in m.text and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto(B+"#/accueil");pg.wait_for_function("window.__route=='accueil'")
    chk(int(re.search(r"onrecord-v(\d+)", open("site/sw.js").read()).group(1)) >= 16, "sw >= v16")
    ft=pg.inner_text("footer");chk("GitHub" not in ft and "issue" not in ft,"footer github")
    chk("Proposer une mise à jour" not in ft and "Ajouter une contribution" in ft,"footer -> contribution")
    chk(pg.locator('footer a[href="#/contributions"]').count()==1,"footer link")
    chk(pg.locator('#home-entries a[href="#/contributions"]').count()==1,"home entry")
    chk(pg.locator('a[href="#/contribuer"]').count()==0,"aucun lien vers #/contribuer")
    chk(pg.locator("#view-contribuer").count()==0 and pg.locator("#contrib-form").count()==0,"formulaire retiré")
    pg.goto(B+"#/methodologie");pg.wait_for_timeout(300)
    chk(pg.locator('#view-methodologie a[href="#/contributions"]').count()==1,"meth link")
    chk("GitHub" not in pg.content(),"no github anywhere")
    pg.goto(B+"#/methode");pg.wait_for_timeout(300);chk(pg.locator('#view-methode a[href="#/contributions"]').count()>=1,"methode link")
    pg.goto(B+"#/contribuer");pg.wait_for_timeout(500)
    chk(pg.evaluate("location.hash")=="#/contributions" and pg.evaluate("window.__route")=="contributions","#/contribuer -> #/contributions")
    pg.goto(B+"#/enquete/relier/marine-le-pen/jordan-bardella");pg.wait_for_timeout(800)
    chk(pg.evaluate("location.hash")=="#/enquete" and pg.evaluate("window.__route")=="enquete","relier -> #/enquete")
    chk(pg.locator("#enq-relier").count()==0 and pg.locator("#enq-path").count()==0,"Relier deux noms retiré")
    chk("Relier" not in pg.inner_text("#view-enquete"),"pas de texte Relier")
    pg.fill("#enq-q","Bardella");pg.wait_for_timeout(300)
    chk(pg.locator("#enq-results a").count()>=1,"recherche Enquête intacte")
    chk(not errs,"console "+str(errs))
    br.close()
print(f"{ok} ok, {fail} fail")
