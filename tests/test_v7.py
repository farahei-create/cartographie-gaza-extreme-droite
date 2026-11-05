"""Tests v7 : carte PNG, #/methode, Avant / maintenant, erreurs console."""
import json, base64, sys
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8765/"
D = json.load(open("site/data.json"))
ok = fail = 0
def check(c, m):
    global ok, fail
    if c: ok += 1
    else: fail += 1; print("FAIL:", m)
def dated(n): return [s for s in n.get("statements", []) if len(s.get("date") or "") == 10]
persons = [n for n in D["nodes"] if n["type"] == "person"]
multi = [n for n in persons if len(dated(n)) >= 2]
single = [n for n in persons if len(dated(n)) < 2]
others = [n for n in D["nodes"] if n["type"] != "person" and n.get("statements")]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "#/methode"); pg.wait_for_function("window.__route==='methode'")
    check(pg.is_visible("#view-methode h2"), "methode visible")
    check(pg.locator("#view-methode a[href=\"#/contribuer\"]").count() >= 1 and "GitHub" not in pg.content(), "fallback -> contribuer")
    check(pg.locator("#tabnav a[aria-current=page]").get_attribute("data-tab") == "methodologie", "tab méthode active")
    check("mailto" not in pg.inner_html("#view-methode"), "pas d'adresse inventée")
    pg.screenshot(path="v7-methode-mobile.png", full_page=True)
    pg.goto(BASE); pg.wait_for_function("window.__route==='accueil'")
    pg.click("#home-methode"); pg.wait_for_function("window.__route==='methode'"); check(True, "lien accueil")
    check(pg.locator("#footer-methode").count() == 1, "lien footer")
    # carte PNG pour chaque déclaration
    for n in D["nodes"]:
        for i, s in enumerate(n.get("statements", [])):
            r = pg.evaluate("([a,b])=>window.__renderCard(a,b)", [n["id"], i])
            raw = base64.b64decode(r["dataUrl"].split(",")[1])
            check(raw[:8] == b"\x89PNG\r\n\x1a\n" and len(raw) > 20000, f"png {n['id']} {i}")
            if r["truncated"]: print("tronquée:", n["id"], i, len(s["quote"]))
    r = pg.evaluate("()=>window.__renderCardQuote('eric-zemmour','mot '.repeat(600))")
    check(r["truncated"], "très longue citation tronquée")
    # fiche multi : Avant/maintenant + partage (téléchargement en headless)
    z = "eric-zemmour" if any(n["id"] == "eric-zemmour" for n in multi) else multi[0]["id"]
    pg.goto(BASE + "#/personne/" + z); pg.wait_for_selector("#am")
    check(pg.locator("#am .am-card").count() == 2, "2 colonnes")
    with pg.expect_download() as dl:
        pg.click("#am button[data-act=share-duo]")
    path = dl.value.path(); data = open(path, "rb").read()
    check(data[:4] == b"\x89PNG" and len(data) > 20000, "png duo téléchargé")
    open("v7-card-duo.png", "wb").write(data)
    with pg.expect_download() as dl:
        pg.click("#d0 button[data-act=share]")
    data = open(dl.value.path(), "rb").read(); check(len(data) > 20000, "png déclaration téléchargé")
    open("v7-card.png", "wb").write(data)
    pg.goto(BASE + "#/personne/" + z + "#am"); pg.reload(); pg.wait_for_selector("#am"); pg.wait_for_timeout(1500)
    pg.evaluate("document.getElementById('am').scrollIntoView()"); pg.wait_for_timeout(300)
    pg.screenshot(path="v7-avant-maintenant-mobile.png")
    sel = pg.locator("#am-a option").count(); check(sel >= 2, "sélecteur")
    pg.select_option("#am-a", index=1); check(pg.locator("#am .am-card").count() == 2, "changement de paire")
    ov = pg.evaluate("document.documentElement.scrollWidth>innerWidth"); check(not ov, "pas de débordement")
    for n in multi: pg.goto(BASE + "#/personne/" + n["id"]); pg.wait_for_selector("#panel-body, .fiche-head", state="attached"); pg.wait_for_timeout(50); check(pg.locator("#am").count() == 1, "am " + n["id"])
    for n in single + others:
        pg.goto(BASE + ("#/personne/" if n["type"] == "person" else "#/organisation/") + n["id"]); pg.wait_for_timeout(120); check(pg.locator("#am").count() == 0, "pas d'am " + n["id"])
    pg.goto(BASE + "#/chronologie"); pg.wait_for_timeout(300)
    check(pg.locator("#view-chronologie button[data-act=share]").count() == sum(len(n.get("statements", [])) for n in D["nodes"]) or pg.locator("#view-chronologie button[data-act=share]").count() > 0, "partager chronologie")
    check(pg.locator("#view-chronologie button[data-act=copy]").count() > 0, "copier chronologie")
    b.close()
check(not errs, "console: " + "; ".join(errs))
print(f"{ok} OK, {fail} FAIL; multi={len(multi)} single={len(single)}")
sys.exit(1 if fail else 0)
