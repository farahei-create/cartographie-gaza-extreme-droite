"""Tests v22 : vue Échelle du pouvoir (#/pouvoir)."""
import json, os, re
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "http://localhost:8765/"
D = json.load(open(os.path.join(ROOT, "data.json")))
BY = {n["id"]: n for n in D["nodes"]}
EDGES = D["edges"]
ok = fail = 0
errs = []

def check(c, m):
    global ok, fail
    if c:
        ok += 1
    else:
        fail += 1
        print("FAIL:", m)

sw = open(os.path.join(ROOT, "sw.js")).read()
check('var VERSION = "onrecord-v24"' in sw, "sw onrecord-v24")
js = open(os.path.join(ROOT, "app.js")).read()
html = open(os.path.join(ROOT, "index.html")).read()
check("Échelle du pouvoir" in html and 'href="#/pouvoir"' in html, "lien navigation")
check("Classement par fonction publique documentée, fortune seulement si sourcée." in html, "méthode dans la vue")
for bad in ("pantin", "complice", "revirement"):
    check(bad not in js and bad not in html, "mot exclu " + bad)

EXPECT = {"evt": 3, "col": 7, "asso": 10, "jour": 21, "media": 14, "elu": 28, "gouv": 8, "prop": 7}

def relations(a, b):
    return [e["relation"] for e in EDGES if {e["source"], e["target"]} == {a, b}]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, service_workers="block")
    pg = ctx.new_page()
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "#/pouvoir")
    pg.wait_for_function("window.__route==='pouvoir' && window.__power")
    pg.wait_for_selector("#pow-ladder .pow-node")
    info = pg.evaluate("window.__power()")
    check(pg.locator("#tab-pouvoir[aria-current='page']").count() == 1, "onglet courant")
    check(sum(t["n"] for t in info["tiers"]) == len(D["nodes"]) == pg.locator(".pow-node").count(), "toutes les fiches")
    for t in info["tiers"]:
        check(t["n"] == EXPECT.get(t["id"]), t["id"] + " " + str(t["n"]))
    check("plus long fil" in pg.inner_text("#pow-stats"), "mini-stat fil")
    pg.goto(BASE + "#/")
    pg.wait_for_function("window.__route==='accueil'")
    check(pg.locator("#home-entries a[href='#/pouvoir']").count() == 1, "carte accueil")
    pg.locator("#tab-pouvoir").tap()
    pg.wait_for_function("window.__route==='pouvoir'")
    # filtre France : moins de fiches, pas de débordement
    pg.locator("#pow-france").click()
    pg.wait_for_function("window.__power().filter==='france'")
    fr = pg.evaluate("window.__power().tiers.reduce((a,t)=>a+t.n,0)")
    # le compteur du filtre est le nombre total France, les cartes visibles aussi
    shown = pg.locator(".pow-node").count()
    check(shown < len(D["nodes"]) and shown == sum(1 for n in D["nodes"] if "france" in n.get("sections", [])), "filtre France " + str(shown))
    pg.locator("#pow-gaza").click()
    pg.wait_for_function("window.__power().filter==='gaza'")
    gz = pg.locator(".pow-node").count()
    check(gz == sum(1 for n in D["nodes"] if "gaza" in n.get("sections", [])), "filtre Gaza " + str(gz))
    pg.locator("#pow-tout").click()
    pg.wait_for_function("window.__power().filter==='tout'")
    # sélection : liens existants, haut / bas, fiche
    pg.locator(".pow-node[data-id='geoffroy-lejeune']").click()
    pg.wait_for_function("window.__power().selected==='geoffroy-lejeune'")
    pg.wait_for_selector("#pow-sheet:not([hidden])")
    sheet = pg.inner_text("#pow-sheet")
    rel = relations("geoffroy-lejeune", "jdd")
    check(rel and rel[0] in sheet, "texte de relation existant")
    check("Relié à" in sheet and "plus haut" in sheet, "stat plus haut")
    check("Ouvrir la fiche" in sheet, "bouton fiche")
    path = pg.evaluate("window.__power().path")
    check(path[0] == "geoffroy-lejeune" and "jdd" in path and path[-1] in ("lagardere", "vivendi-canal", "vincent-bollore"), "fil " + " ".join(path))
    # chaque pas du fil est une arête réelle
    linked = all(relations(path[i], path[i + 1]) for i in range(len(path) - 1))
    check(linked, "fil sans relation inventée")
    check("Remonter jusqu'au sommet" in sheet or "Remonter le fil" in sheet, "bouton remonter")
    # fortune : rang sourcé, pas de montant inventé
    pg.locator(".pow-node[data-id='vincent-bollore']").click()
    pg.wait_for_function("window.__power().selected==='vincent-bollore'")
    fort = pg.locator("#pow-sheet .pow-fort")
    check(fort.count() == 1 and fort.get_attribute("href").startswith("https://www.challenges.fr/classements/fortune/"), "lien Challenges")
    ftxt = pg.inner_text("#pow-sheet")
    check("13e rang" in ftxt and "8 juillet 2026" in ftxt, "rang daté")
    check(not re.search(r"\d[\d\s.,]*\s*(milliards?|Md €|Mds)", ftxt), "pas de montant")
    pg.evaluate("document.querySelector('.pow-node[data-id=pierre-edouard-sterin]').click()")
    pg.wait_for_function("window.__power().selected==='pierre-edouard-sterin'")
    check("74e rang" in pg.inner_text("#pow-sheet"), "rang Stérin")
    # remonter depuis un journaliste, mouvement réduit
    pg.emulate_media(reduced_motion="reduce")
    pg.evaluate("document.querySelector('.pow-node[data-id=geoffroy-lejeune]').click()")
    pg.wait_for_function("window.__power().selected==='geoffroy-lejeune'")
    before = pg.evaluate("window.__power().path")
    pg.locator("#pow-climb").click()
    pg.wait_for_function("window.__power().selected==='%s'" % before[-1], timeout=4000)
    check(pg.evaluate("window.__power().selected") == before[-1], "remonter reduced-motion")
    dur = pg.evaluate("getComputedStyle(document.querySelector('.pow-node.is-on')).animationDuration")
    check(dur in ("0s", "0.01ms", "0.00001s", "1e-05s"), "anim courte " + dur)
    # ouvrir la fiche
    pg.locator("#pow-sheet a", has_text="Ouvrir la fiche").click()
    pg.wait_for_function("window.__route==='fiche'")
    check(pg.locator(".fiche").count() == 1, "fiche ouverte")
    check(pg.locator("a[href^='#/pouvoir/']").count() >= 1, "retour échelle depuis la fiche")
    # débordement mobile
    pg.goto(BASE + "#/pouvoir/nemesis")
    pg.wait_for_selector("#pow-sheet:not([hidden])")
    pg.wait_for_timeout(400)
    ov = pg.evaluate("document.documentElement.scrollWidth-innerWidth")
    check(ov <= 1, "pas de débordement " + str(ov))
    shot = "/opt/cursor/artifacts/echelle-pouvoir-mobile.png"
    os.makedirs("/opt/cursor/artifacts", exist_ok=True)
    pg.screenshot(path=shot)
    # bureau : les onglets restent dans la barre
    ctx2 = b.new_context(viewport={"width": 1280, "height": 860}, service_workers="block")
    dpg = ctx2.new_page()
    dpg.goto(BASE + "#/")
    dpg.wait_for_function("window.__route==='accueil'")
    box = dpg.evaluate("""() => {
      const tabs = document.querySelector('.tabnav').getBoundingClientRect();
      const brand = document.querySelector('.brand').getBoundingClientRect();
      const don = document.querySelector('.donate-head');
      const dr = don && !don.hidden ? don.getBoundingClientRect() : null;
      return {tabs:[tabs.left,tabs.right,tabs.bottom], brand:brand.right, don: dr && dr.width ? [dr.left, dr.right] : null, w: innerWidth};
    }""")
    check(box["tabs"][2] < 70, "onglets en haut " + str(box))
    check(box["tabs"][0] >= box["brand"] - 2 and box["tabs"][1] <= box["w"] + 1, "onglets dans la fenêtre " + str(box))
    if box["don"]:
        check(box["tabs"][1] <= box["don"][0] + 2, "onglets ne couvrent pas Soutenir " + str(box))
    ctx.close(); ctx2.close(); b.close()

check(not errs, "console " + str(errs[:4]))
print("%d OK, %d FAIL" % (ok, fail))
raise SystemExit(1 if fail else 0)
