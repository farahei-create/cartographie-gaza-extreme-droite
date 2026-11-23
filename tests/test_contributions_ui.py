"""Contributions des lecteurs, côté page (Playwright, serveur sur :8765).
Le dépôt contributions.json reste vide en ligne : ici une contribution de démonstration
est servie par interception, pour vérifier l'affichage. Captures : shots/ (ou CTB_SHOTS)."""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "http://localhost:8765/"
SHOTS = os.environ.get("CTB_SHOTS") or os.path.join(ROOT, "shots")
ok = fail = 0
def check(c, m):
    global ok, fail
    if c: ok += 1
    else:
        fail += 1; print("FAIL:", m)

sw = open(os.path.join(ROOT, "sw.js"), encoding="utf-8").read()
check('var VERSION = "onrecord-v61"' in sw, "sw onrecord-v61")
check('"contrib.js"' in sw and 'indexOf("/api/") === 0' in sw, "sw : contrib.js en cache, /api jamais")
check("contributions\\.json" in sw, "contributions.json en réseau d'abord")
pub = json.load(open(os.path.join(ROOT, "contributions.json"), encoding="utf-8"))
check(isinstance(pub.get("items"), list), "contributions.json lisible")
js = open(os.path.join(ROOT, "contrib.js"), encoding="utf-8").read()
for bad in ("complice", "génocidaire", "pantin", "infiltré", "marionnette", "copinage", "occulte"):
    check(bad not in js, "mot exclu " + bad)

DEMO = {"items": [{
    "id": "mi9demo0123456789abcdef", "person": "jordan-bardella", "pseudo": "Lecteur_75",
    "submitted": "2026-11-22T19:42:00.000Z", "approved": "2026-11-22T20:00:00.000Z", "event_date": "2026-11-20",
    "title": "Exemple de contribution (démonstration)",
    "text": "Texte d'exemple : un fait public, daté, avec un lien vers la source.\nDeuxième ligne.",
    "links": ["https://www.example.org/source"], "media": []}]}

with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ("dark", "light"):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, color_scheme=scheme, service_workers="block")
        pg = ctx.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.route("**/contributions.json*", lambda r: r.fulfill(status=200, content_type="application/json", body=json.dumps(DEMO)))
        pg.goto(BASE + "#/personne/jordan-bardella")
        pg.wait_for_selector("#ctb-fiche .ctb-item", timeout=15000)
        item = pg.locator("#ctb-fiche .ctb-item").first
        check(pg.locator("#ctb-fiche h2").first.text_content().strip().startswith("Contributions des lecteurs"), "titre du bloc")
        check("sous sa seule responsabilité" in item.inner_text(), "bandeau de responsabilité")
        check("Onrecord ne l'a pas vérifié comme ses propres sources." in item.inner_text(), "bandeau exact")
        check("20\u00a0h\u00a042" in item.inner_text() and "heure de Paris" in item.inner_text(), "heure de Paris (UTC+1)")
        check("Lecteur_75" in item.inner_text() and "@" not in item.inner_text(), "pseudo, jamais d'e-mail")
        check(item.locator("a[rel*=ugc]").count() == 1, "lien ugc nofollow")
        w = pg.evaluate("document.documentElement.scrollWidth")
        check(w <= 390, "pas de débordement horizontal (%s)" % w)
        pg.locator(".ctb-report-btn").first.click()
        check(pg.locator(".ctb-report form").count() == 1, "formulaire de signalement")
        pg.fill(".ctb-report textarea", "Test de signalement")
        pg.click(".ctb-report button[type=submit]")
        pg.wait_for_selector(".ctb-report .ctb-err:not([hidden])", timeout=5000)
        check("bientôt" in pg.locator(".ctb-report .ctb-err").text_content(), "sans /api : signalement « bientôt »")
        os.makedirs(SHOTS, exist_ok=True)
        pg.locator(".ctb-report-btn").first.click()
        pg.locator("#ctb-fiche").scroll_into_view_if_needed()
        pg.evaluate("document.getElementById('ctb-fiche').scrollIntoView({block:'start'}); window.scrollBy(0,-130)")
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(SHOTS, "mobile-fiche-contributions-%s-390x844.png" % scheme))

        pg.goto(BASE + "#/contributions/jordan-bardella")
        pg.wait_for_selector("#ctb-app .ctb-soon", timeout=10000)
        check("Bientôt disponible" in pg.locator("#ctb-app").text_content(), "sans variables : bientôt disponible")
        check(pg.locator("#ctb-charte").count() == 1 and pg.locator("#ctb-mentions").count() == 1, "charte et mentions")
        check("Covina" in pg.locator("#view-contributions").inner_text(), "hébergeur")

        pg.route("**/api/contrib/status", lambda r: r.fulfill(status=200, content_type="application/json", body='{"enabled":true,"reports":true}'))
        pg.route("**/api/contrib/me", lambda r: r.fulfill(status=200, content_type="application/json", body='{"logged":false}'))
        pg.route("**/api/contrib/send-code", lambda r: r.fulfill(status=400, content_type="application/json", body='{"ok":false,"error":"Les adresses e-mail jetables ne sont pas acceptées."}'))
        pg.evaluate("location.hash='#/contributions'"); pg.wait_for_timeout(100)
        pg.evaluate("location.hash='#/contributions/jordan-bardella'")
        pg.wait_for_selector("#ctb-login", timeout=10000)
        pg.fill("#ctb-login input[name=email]", "a@yopmail.com")
        pg.click("#ctb-login button")
        pg.wait_for_selector("#ctb-login .ctb-err:not([hidden])")
        check("charte" in pg.locator("#ctb-login .ctb-err").inner_text(), "charte obligatoire")
        pg.check("#ctb-login input[name=charter]")
        pg.click("#ctb-login button")
        pg.wait_for_function("document.querySelector('#ctb-login .ctb-err').textContent.indexOf('jetables')>=0")
        check(True, "message adresse jetable")
        if scheme == "dark":
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(SHOTS, "mobile-contributions-inscription-390x844.png"))
        check(not errors, "pas d'erreur JS : %s" % errors)
        ctx.close()
    b.close()
print("%d ok, %d fail" % (ok, fail))
raise SystemExit(1 if fail else 0)
