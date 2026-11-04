"""Tests v8 : section « Déclarations et votes »."""
import json, base64, sys
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8765/"
D = json.load(open("site/data.json")); V = D["votes"]
ok = fail = 0
def check(c, m):
    global ok, fail
    if c: ok += 1
    else: fail += 1; print("FAIL:", m)
errs = []
BAN = ["contradiction", "revirement", "trahison", "volte-face", "incohéren"]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, accept_downloads=True).new_page()
    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE); pg.wait_for_function("window.__route==='accueil'")
    check(pg.locator("#home-entries .entry").count() == 5, "5 cartes accueil")
    pg.click("#home-votes"); pg.wait_for_function("window.__route==='votes'")
    check(pg.locator("#footer-votes").count() == 1, "lien footer")
    check(pg.locator("#votes-list .vt").count() == len(V) == 3, "3 entrées")
    for v in V:
        a = pg.locator("#vote-" + v["id"])
        t = a.text_content()
        check("Ce qui a été déclaré" in t and "Le vote officiel" in t, "blocs " + v["id"])
        check(a.locator(".vt-pos strong").inner_text() == v["vote"]["position"], "position " + v["id"])
        check(a.locator('a[href="%s"]' % v["vote"]["url"]).count() >= 1, "lien scrutin " + v["id"])
        check(a.locator('a[href="%s"]' % v["statement"]["url"]).count() >= 1, "lien source " + v["id"])
    sec = pg.inner_text("#view-votes").lower()
    check(not any(w in sec for w in BAN), "vocabulaire neutre")
    check("Des déclarations publiques mises en regard de votes nominatifs officiels sur le même sujet." in pg.inner_text("#view-votes"), "intro")
    r = pg.locator("#votes-reply a"); check(r.get_attribute("href") == "#/methode", "lien droit de réponse")
    pg.wait_for_timeout(400); pg.screenshot(path="v8-votes-mobile.png")
    w = pg.evaluate("[...document.querySelectorAll('#view-votes .vt-b')].map(e=>e.getBoundingClientRect().left)")
    check(len(set(round(x) for x in w)) == 1, "blocs empilés sur mobile")
    check(not pg.evaluate("document.documentElement.scrollWidth>innerWidth"), "pas de débordement")
    for v in V:
        rr = pg.evaluate("id=>window.__renderVoteCard(id)", v["id"]); raw = base64.b64decode(rr["dataUrl"].split(",")[1])
        check(raw[:4] == b"\x89PNG" and len(raw) > 20000, "png " + v["id"])
    with pg.expect_download() as dl:
        pg.click("#vote-%s button[data-act=share-vote]" % V[1]["id"])
    data = open(dl.value.path(), "rb").read(); check(len(data) > 20000, "png téléchargé"); open("v8-card.png", "wb").write(data)
    r.click(); pg.wait_for_function("window.__route==='methode'")
    check("vote de groupe n'est jamais attribué à une personne" in pg.inner_text("#methode-votes"), "critères méthode")
    for v in V:
        nid = v["person_id"] or v["group"]; kind = "personne" if v["person_id"] else "organisation"
        pg.goto(BASE + "#/%s/%s" % (kind, nid)); pg.wait_for_selector("#votes-fiche"); check(pg.locator("#view-fiche #vote-" + v["id"]).count() == 1, "fiche " + nid)
    pg.goto(BASE + "#/organisation/renaissance-epr"); pg.wait_for_timeout(200); check(pg.locator("#votes-fiche").count() == 0, "pas d'attribution au groupe RE")
    b.close()
with sync_playwright() as p:
    pass
check(not errs, "console: " + "; ".join(errs))
print(f"{ok} OK, {fail} FAIL"); sys.exit(1 if fail else 0)
