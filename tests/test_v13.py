"""Tests v13 : dons (Leetchi), citation du jour, continuer à explorer, reprise, stats cliquables."""
import re
from playwright.sync_api import sync_playwright
BASE="http://localhost:8765/"; ok=fail=0; errs=[]
def check(c,m):
    global ok,fail
    if c: ok+=1
    else: fail+=1; print("FAIL:",m)
cfg=open("site/config.js").read()
m=re.search(r'DONATION_URL:\s*"([^"]*)"',cfg); url=m.group(1) if m else ""
check(url.startswith("https://www.leetchi.com/") and "utm_" not in url,"DONATION_URL "+url)
check(re.search(r'CORRECTION_EMAIL:\s*""',cfg),"CORRECTION_EMAIL vide")
import re as _re
_sw=open("site/sw.js").read()
check(int(_re.search(r"onrecord-v(\d+)",_sw).group(1))>=18,"sw >= v18")
check('var VERSION = "onrecord-v20"' in _sw,"sw onrecord-v20")
BAN=["pantin","revirement","complice","contradiction"]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2); ctx.grant_permissions(["clipboard-read","clipboard-write"])
    pg=ctx.new_page()
    pg.on("console",lambda m: m.type=="error" and errs.append(m.text)); pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto(BASE); pg.wait_for_selector("#home-qotd:not([hidden])"); pg.wait_for_timeout(400)
    check(pg.is_visible(".donate-head"),"bouton don en-tête")
    check(pg.inner_text(".donate-head").strip()=="Soutenir","libellé en-tête Soutenir")
    check(pg.get_attribute(".donate-head","href")==url,"href en-tête")
    check(pg.get_attribute(".donate-head","target")=="_blank","target blank en-tête")
    check(pg.locator(".donate-foot").count()>0 and pg.get_attribute(".donate-foot","href")==url,"bouton don pied")
    check(pg.inner_text(".donate-foot").strip()=="Soutenir","libellé pied Soutenir")
    check("Soutenir ce travail" not in pg.content(),"plus de « Soutenir ce travail »")
    t=pg.inner_text("#home-qotd"); check("citation du jour" in t.lower(),"citation du jour")
    check(pg.locator("#home-qotd a[href^='#/personne/']").count()>0,"lien fiche citation")
    check(pg.locator("#home-qotd [data-act='share'], #home-qotd button").count()>0,"bouton partage citation")
    q1=pg.evaluate("__qotd('2026-11-05')"); q2=pg.evaluate("__qotd('2026-11-05')"); q3=pg.evaluate("__qotd('2026-11-06')")
    check(q1==q2 and q1 is not None,"déterministe"); check(q1!=q3,"change selon le jour")
    check(pg.locator("#home-stats a.stat-a").count()>=6,"stats cliquables")
    check(pg.is_hidden("#home-resume"),"pas de reprise sans visite")
    pg.goto(BASE+"#/personne/cyril-hanouna"); pg.wait_for_selector(".fiche"); pg.wait_for_timeout(400)
    ex=pg.inner_text("#explore") if pg.locator("#explore").count() else ""
    check("Continuer à explorer" in ex,"continuer à explorer"); check(pg.locator("#explore a.explore-it").count()==3,"3 suggestions")
    check(pg.locator("#donate-invite").count()==0,"pas d'invitation avant partage")
    pg.locator(".fiche [data-act='copy']").first.click(); pg.wait_for_timeout(400)
    check(pg.locator("#donate-invite:not([hidden])").count()==1 and "Onrecord vit des dons" in pg.inner_text("#donate-invite"),"invitation après copie")
    pg.screenshot(path="/workspace/v13-person-mobile.png",full_page=False)
    pg.goto(BASE+"#/accueil"); pg.wait_for_timeout(3000)
    check(pg.is_visible("#home-resume") and "Reprendre" in pg.inner_text("#home-resume"),"chip reprendre")
    pg.screenshot(path="/workspace/v13-home-mobile.png",full_page=True)
    pg.goto(BASE+"#/methode"); pg.wait_for_timeout(400); mt=pg.inner_text("#view-methode")
    check("dons" in mt and "Leetchi" in mt,"méthode dons/leetchi"); check("Proposer une mise à jour" in mt,"contact -> contribuer")
    check(pg.is_visible(".donate-methode"),"cta méthode")
    for r in ["", "#/methode", "#/personne/cyril-hanouna"]:
        pg.goto(BASE+r); pg.wait_for_timeout(300); body=pg.inner_text("body").lower()
        check(not any(w in body for w in BAN),"mots exclus "+r)
    ctx.route("https://www.leetchi.com/**", lambda route: route.fulfill(status=200, content_type="text/html", body="<p>ok</p>"))
    pg.goto(BASE); pg.wait_for_selector(".donate-head:not([hidden])")
    def scale():
        return pg.evaluate("""() => {
          var t = getComputedStyle(document.querySelector('.donate-head')).transform;
          var m = t && t.match(/matrix\\(([^)]+)\\)/);
          return m ? parseFloat(m[1].split(',')[0]) : 1;
        }""")
    with pg.expect_popup() as pop_info:
        pg.locator(".donate-head").click()
    pop=pop_info.value
    check("is-loved" in (pg.get_attribute(".donate-head","class") or ""),"anim au tap")
    check(pg.locator(".donate-head .donate-spark").count()>=4,"éclats au tap")
    samples=[scale()]
    for _ in range(7):
        pg.wait_for_timeout(40); samples.append(scale())
    check(max(samples)>1.08 and min(samples)<0.98,"rebond "+str([round(s,3) for s in samples]))
    check("leetchi.com" in pop.url,"tap ouvre Leetchi "+pop.url)
    check(pg.get_attribute(".donate-head","target")=="_blank","target reste _blank")
    pop.close()
    pg.wait_for_timeout(250)
    check("is-loved" not in (pg.get_attribute(".donate-head","class") or ""),"anim courte")
    pg.emulate_media(reduced_motion="reduce")
    with pg.expect_popup() as pop2:
        pg.locator(".donate-head").click()
    p2=pop2.value
    check("is-loved" in (pg.get_attribute(".donate-head","class") or ""),"feedback reduced-motion")
    check(pg.locator(".donate-spark").count()==0,"pas d'éclats si reduced-motion")
    anim=pg.evaluate("getComputedStyle(document.querySelector('.donate-head')).animationName")
    check(anim=="none","pas de rebond si reduced-motion")
    p2.close()
    b.close()
check(not errs,"console "+str(errs[:3]))
print(f"{ok} ok, {fail} fail"); raise SystemExit(1 if fail else 0)
