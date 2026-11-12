"""Tests v23 : parcours d'ascension et liens classés par nature."""
import json, os, re
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
check('var VERSION = "onrecord-v38"' in sw, "sw onrecord-v38")
html = open(os.path.join(ROOT, "index.html")).read()
js = open(os.path.join(ROOT, "app.js")).read()
check("Voir comment il est arrivé là" in js, "libellé parcours")
for bad in ("pantin", "complice", "marionnette", "protégé"):
    check(bad not in js and bad not in html and bad not in json.dumps(D, ensure_ascii=False), "mot exclu " + bad)

bard = BY["jordan-bardella"]["parcours"]
check(len(bard) >= 10, "bardella étapes " + str(len(bard)))
check(all(s.get("date") and s.get("url", "").startswith("https://") and s.get("source") for s in bard), "bardella daté et sourcé")
patrons = [s for s in bard if s.get("by")]
check(any(s["by"] == "marine-le-pen" and "porte-parole" in s.get("verb", "") for s in patrons), "le pen porte-parole")
check(any(s["by"] == "marine-le-pen" and "2019" in s.get("verb", "") for s in patrons), "le pen européennes 2019")
check(any("intérim" in s.get("verb", "") for s in patrons), "intérim")
check(all(s.get("by") in BY for s in patrons), "parrains connus")
# pas de parrain sur l'élection interne de 2022
elu = [s for s in bard if s["date"] == "2022-11-05"]
check(elu and not elu[0].get("by"), "présidence 2022 sans parrain inventé")

nats = {}
for e in D["edges"]:
    nats[e.get("nature")] = nats.get(e.get("nature"), 0) + 1
check(set(nats) <= {"ascension", "opposition", "autre", "coulisses"} and nats.get("ascension") and nats.get("opposition"), "natures " + str(nats))
boll = [e for e in D["edges"] if {e["source"], e["target"]} == {"vincent-bollore", "arcom"}]
check(boll and all(e["nature"] == "opposition" for e in boll), "bolloré-arcom opposition")
lej = [e for e in D["edges"] if {e["source"], e["target"]} == {"geoffroy-lejeune", "jdd"}]
check(lej and lej[0]["nature"] == "ascension" and "directeur" in lej[0]["relation"], "lejeune-jdd ascension")

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, service_workers="block")
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "#/personne/jordan-bardella")
    pg.wait_for_function("window.__route==='fiche'")
    pg.wait_for_selector("#parcours .p-step")
    check(pg.locator("a", has_text="Voir comment il est arrivé là").count() == 1, "entrée parcours")
    nsteps = pg.locator("#parcours .p-step").count()
    check(nsteps == len(bard), "frise " + str(nsteps))
    check(pg.locator("#parcours .p-by", has_text="Marine Le Pen").count() >= 3, "pastilles Le Pen")
    check("porte-parole" in pg.inner_text("#parcours"), "texte porte-parole")
    # tap : ouvre le parcours de Marine Le Pen
    pg.locator("#parcours .p-by", has_text="Marine Le Pen").first.tap()
    pg.wait_for_function("location.hash.indexOf('marine-le-pen')>=0")
    pg.wait_for_selector("#parcours")
    check(pg.locator("#parcours h3", has_text="Front national").count() >= 1, "parcours Le Pen")
    check("Voir comment elle est arrivée là" in pg.inner_text("#fiche-body"), "accord elle")
    # retour Bardella, mouvement réduit
    pg.emulate_media(reduced_motion="reduce")
    pg.goto(BASE + "#/personne/jordan-bardella#parcours")
    pg.wait_for_selector("#parcours .p-step")
    op = pg.evaluate("getComputedStyle(document.querySelector('#parcours .p-step')).opacity")
    check(op == "1", "reduced-motion visible " + op)
    ov = pg.evaluate("document.documentElement.scrollWidth-innerWidth")
    check(ov <= 1, "pas de débordement " + str(ov))
    pg.locator("#parcours").scroll_into_view_if_needed()
    pg.evaluate("""() => {
      const el = document.querySelector('.f-actions');
      if (!el) return;
      const top = el.getBoundingClientRect().top + scrollY - 64;
      scrollTo(0, Math.max(0, top));
    }""")
    pg.wait_for_timeout(150)
    os.makedirs("/opt/cursor/artifacts", exist_ok=True)
    pg.screenshot(path="/opt/cursor/artifacts/parcours-bardella-mobile.png")
    # échelle : ascension par défaut, Bolloré–Arcom caché, fil Lejeune inchangé
    pg.goto(BASE + "#/pouvoir/vincent-bollore")
    pg.wait_for_selector("#pow-sheet:not([hidden])")
    sheet = pg.inner_text("#pow-sheet")
    check("audition" not in sheet.lower(), "arcom pas en mode ascension")
    check(pg.locator("#pow-ascension[aria-selected='true']").count() == 1, "mode ascension")
    pg.locator("#pow-opposition").click()
    pg.wait_for_function("window.__power().nature==='opposition'")
    check("audition" in pg.inner_text("#pow-sheet").lower(), "arcom en opposition")
    check(pg.locator("#pow-sheet .nat-opposition").count() >= 1, "style opposition")
    pg.locator("#pow-ascension").click()
    pg.wait_for_function("window.__power().nature==='ascension'")
    pg.locator(".pow-node[data-id='geoffroy-lejeune']").click()
    pg.wait_for_function("window.__power().selected==='geoffroy-lejeune'")
    path = pg.evaluate("window.__power().path")
    check(path[0] == "geoffroy-lejeune" and "jdd" in path and path[-1] in ("lagardere", "vivendi-canal", "vincent-bollore"), "fil " + " ".join(path))
    ctx.close(); b.close()

check(not errs, "console " + str(errs[:4]))
print("%d OK, %d FAIL" % (ok, fail))
raise SystemExit(1 if fail else 0)
