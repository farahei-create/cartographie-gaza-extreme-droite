"""Tests v24 : parcours pour toutes les personnes, vue Coulisses."""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "http://localhost:8765/"
D = json.load(open(os.path.join(ROOT, "data.json")))
BY = {n["id"]: n for n in D["nodes"]}
ok = fail = 0

def check(c, m):
    global ok, fail
    if c:
        ok += 1
    else:
        fail += 1
        print("FAIL:", m)

sw = open(os.path.join(ROOT, "sw.js")).read()
js = open(os.path.join(ROOT, "app.js")).read()
html = open(os.path.join(ROOT, "index.html")).read()
check('var VERSION = "onrecord-v40"' in sw, "sw onrecord-v40")
check('href="#/coulisses"' in html and 'id="view-coulisses"' in html, "entrée coulisses")
check("Suivre l'argent" in js and "Suivre les médias" in js and "Suivre les nominations" in js and "Suivre les sondages" in js, "récits")
blob = json.dumps(D, ensure_ascii=False)
for bad in ("pantin", "complice", "marionnette", "protégé", "infiltré", "copinage", "occulte"):
    check(bad not in js and bad not in html and bad not in blob, "mot exclu " + bad)

persons = [n for n in D["nodes"] if n["type"] == "person"]
missing = [n["id"] for n in persons if not n.get("parcours")]
check(not missing, "parcours pour toutes les personnes " + str(missing[:8]))
check(all(s.get("date") and str(s.get("url", "")).startswith("https://") and s.get("source")
          for n in persons for s in n["parcours"]), "étapes datées et sourcées")
for oid in ("jdd", "fayard", "europe1", "cnews", "vivendi-canal", "pericles", "issep", "valeurs-actuelles", "prisma-media", "udr"):
    check(BY[oid].get("parcours"), "frise " + oid)
for nid in ("sarah-knafo", "pascal-praud", "arnaud-rerolle", "lise-boell", "serge-nedjar", "philippe-olivier", "kevin-pfeffer", "tugdual-denis", "erik-tegner", "philippe-conrad", "eric-ciotti"):
    check(nid in BY and BY[nid].get("sphere"), "fiche " + nid)
cou = [e for e in D["edges"] if e.get("nature") == "coulisses"]
check(len(cou) >= 20, "liens coulisses " + str(len(cou)))
check(all(e.get("date") and str(e.get("url", "")).startswith("https://") for e in cou), "coulisses datés et sourcés")
rer = next(s for s in BY["arnaud-rerolle"]["statements"] if "ne finance pas" in s["quote"])
check("ni directement ni indirectement" in rer["quote"] and rer["url"].endswith(".pdf"), "démenti financement")
check(not any(e["nature"] == "coulisses" and e["target"] == "rn" and "financ" in e["relation"] for e in D["edges"]), "pas de financement du RN inventé")

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, service_workers="block")
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "#/")
    pg.wait_for_function("window.__route==='accueil'")
    check(pg.locator("#home-entries a[href='#/coulisses']").count() == 1, "carte accueil")
    pg.locator("#tab-coulisses").tap()
    pg.wait_for_function("window.__route==='coulisses'")
    check(pg.locator("#tab-coulisses[aria-current='page']").count() == 1, "onglet courant")
    pg.locator("#cou-story-argent").click()
    pg.wait_for_function("window.__coulisses().story==='argent'")
    check(pg.locator(".cou-now").count() == 1, "récit argent")
    check("argent" in pg.inner_text(".cou-now").lower(), "titre du récit")
    pg.locator(".cou-person").first.tap()
    pg.wait_for_function("window.__coulisses().selected")
    pg.wait_for_selector("#cou-sheet:not([hidden])")
    sheet = pg.inner_text("#cou-sheet")
    check("Ouvrir la fiche" in sheet, "bouton fiche")
    check(pg.locator("#cou-sheet .nat").count() >= 1, "liens par nature")
    pg.locator("#cou-sheet a", has_text="Ouvrir la fiche").click()
    pg.wait_for_function("window.__route==='fiche'")
    check(pg.locator("#parcours .p-step").count() >= 1, "parcours depuis la fiche")
    pg.emulate_media(reduced_motion="reduce")
    pg.goto(BASE + "#/coulisses/medias")
    pg.wait_for_selector(".cou-now")
    op = pg.evaluate("getComputedStyle(document.querySelector('.cou-now')).opacity")
    check(op == "1", "reduced-motion " + op)
    ov = pg.evaluate("document.documentElement.scrollWidth-innerWidth")
    check(ov <= 1, "pas de débordement " + str(ov))
    pg.goto(BASE + "#/personne/gerald-darmanin#parcours")
    pg.wait_for_selector("#parcours .p-step")
    check(pg.locator("#parcours .p-step").count() >= 2, "parcours Darmanin")
    pg.goto(BASE + "#/organisation/jdd#parcours")
    pg.wait_for_selector("#parcours h3")
    check("Lejeune" in pg.inner_text("#parcours"), "frise JDD")
    pg.goto(BASE + "#/coulisses")
    pg.wait_for_selector(".cou-person")
    os.makedirs("/opt/cursor/artifacts", exist_ok=True)
    pg.screenshot(path="/opt/cursor/artifacts/coulisses-mobile.png", full_page=False)
    ctx.close(); b.close()

check(not errs, "console " + str(errs[:4]))
print("%d OK, %d FAIL" % (ok, fail))
raise SystemExit(1 if fail else 0)
