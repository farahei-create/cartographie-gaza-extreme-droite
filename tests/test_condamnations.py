"""Section « Condamnations » (v60) : données condamnations.json, garde-fous juridiques,
cinquième onglet de la barre, filtres personne / statut / année, lien depuis les fiches."""
import json, re
from playwright.sync_api import sync_playwright
B = "http://localhost:8765/"; ok = fail = 0
def chk(c, m):
    global ok, fail
    if c: ok += 1
    else: fail += 1; print("FAIL", m)

C = json.load(open("condamnations.json")); D = json.load(open("data.json"))
ids = {n["id"]: n for n in D["nodes"]}
ST = {"definitive", "appel", "cassation", "relaxe", "non_confirme"}
NONFINAL = {"appel", "cassation", "non_confirme"}
FORBIDDEN = ["complice", "génocidaire", "pantin", "infiltré", "marionnette", "protégé", "copinage", "occulte"]
dec, proc = C["decisions"], C["procedures"]
chk(len(dec) >= 10, "au moins 10 décisions")
chk(set(C["meta"]["statuses"]) == ST, "libellés de statut")
seen = set()
for e in dec + proc:
    chk(e["id"] not in seen, "id unique " + e["id"]); seen.add(e["id"])
    chk(e["person"] in ids, "personne dans data.json " + e["person"])
    chk(e["person_name"] == ids.get(e["person"], {}).get("name"), "nom repris de data.json " + e["id"])
    chk(re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", e["date"]) is not None, "date ISO " + e["id"])
    chk(len(e["sources"]) >= 1 and all(s["url"].startswith("https://") for s in e["sources"]), "sources https " + e["id"])
    chk(not any("wikipedia.org" in s["url"] for s in e["sources"]), "jamais Wikipédia " + e["id"])
    txt = json.dumps(e, ensure_ascii=False).lower()
    chk(not any(w in txt for w in FORBIDDEN), "vocabulaire neutre " + e["id"])
for e in dec:
    chk(e["status"] in ST, "statut connu " + e["id"])
    for k in ("court", "offence", "sentence", "affaire"):
        chk(bool(e.get(k)), k + " renseigné " + e["id"])
    if e["status"] == "definitive":
        chk(e["date"] <= "2026-11-23", "décision définitive datée du passé " + e["id"])
chk(any(ids[e["person"]]["type"] == "org" for e in dec), "au moins une personne morale (parti)")
chk(any(e["status"] == "relaxe" for e in dec), "les relaxes figurent")
chk(all(e["date"] >= "2022" for e in dec), "pas de décision ancienne (réhabilitation, sursis non avenu)")

with sync_playwright() as p:
    br = p.chromium.launch()
    for theme in ("dark", "light"):
        ctx = br.new_context(viewport={"width": 390, "height": 844}, color_scheme=theme)
        ctx.add_init_script("localStorage.setItem('onrecord-theme','%s')" % theme)
        pg = ctx.new_page(); errs = []
        pg.on("console", lambda m: m.type == "error" and "Failed to load resource" not in m.text and errs.append(m.text)); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(B + "#/condamnations"); pg.wait_for_function("window.__route=='condamnations'"); pg.wait_for_selector("#cond-list li.cond")
        tabs = pg.locator("#tabnav a")
        chk(tabs.count() == 5, theme + " cinq onglets")
        t = pg.locator("#tab-condamnations")
        chk(t.get_attribute("aria-current") == "page", theme + " onglet actif")
        chk(t.inner_text().strip() == "Condamnations", theme + " libellé")
        chk(t.locator("svg rect").count() == 1 and t.locator("svg path").count() == 1, theme + " icône barreaux (trait)")
        for i in range(5):
            bb = tabs.nth(i).bounding_box()
            chk(bb["height"] >= 44 and bb["width"] >= 44, theme + " cible tactile onglet %d" % i)
        chk(pg.evaluate("[...document.querySelectorAll('#tabnav a span')].every(s=>s.scrollWidth<=s.clientWidth)"), theme + " libellés entiers à 390 px")
        chk(pg.evaluate("document.documentElement.scrollWidth<=innerWidth"), theme + " pas de défilement horizontal")
        n = pg.locator("#cond-list > li.cond").count()
        chk(n == len(dec), theme + " toutes les décisions affichées")
        nf = pg.locator("#cond-list > li.cond .cond-pi").count()
        chk(nf == sum(e["status"] in NONFINAL for e in dec), theme + " mention présomption d'innocence sur chaque décision non définitive")
        chk("Présomption d'innocence : décision non définitive" in pg.inner_text("#cond-list"), theme + " texte exact de la mention")
        for b in pg.locator("#cond-status button").all():
            chk(b.bounding_box()["height"] >= 44, theme + " segment 44 px")
        pg.click('#cond-status [data-st="definitive"]')
        chk(pg.locator("#cond-list > li.cond").count() == sum(e["status"] == "definitive" for e in dec), theme + " filtre définitives")
        pg.click('#cond-status [data-st="nonfinal"]')
        chk(pg.locator("#cond-list > li.cond").count() == sum(e["status"] in NONFINAL for e in dec), theme + " filtre non définitives")
        pg.click('#cond-status [data-st=""]')
        pg.select_option("#cond-year", "2025")
        chk(pg.locator("#cond-list > li.cond").count() == sum(e["date"].startswith("2025") for e in dec), theme + " filtre année")
        pg.select_option("#cond-year", "")
        pg.select_option("#cond-person", "eric-zemmour"); pg.wait_for_timeout(300)
        chk(pg.evaluate("location.hash") == "#/condamnations/eric-zemmour", theme + " personne dans l'adresse")
        chk(pg.locator("#cond-list > li.cond").count() == sum(e["person"] == "eric-zemmour" for e in dec), theme + " filtre personne")
        pg.goto(B + "#/condamnations/vincent-bollore"); pg.wait_for_timeout(400)
        chk(pg.is_visible("#cond-proc-wrap") and pg.locator("#cond-proc li").count() >= 1, theme + " procédures en cours séparées")
        chk("aucune décision sur le fond" in pg.inner_text("#cond-proc"), theme + " procédure : présomption d'innocence")
        pg.goto(B + "#/condamnations"); pg.wait_for_timeout(300)
        meth = pg.text_content("#cond-method")
        for k in ("133-11", "Présomption d'innocence : décision non définitive", "relaxes", "mise en examen", "Wikipédia", "personnalités publiques"):
            chk(k in meth, theme + " méthode : " + k)
        pg.goto(B + "#/personne/marine-le-pen"); pg.wait_for_selector("#fiche-cond")
        chk(pg.get_attribute("#fiche-cond", "href") == "#/condamnations/marine-le-pen", theme + " lien depuis la fiche")
        pg.goto(B + "#/personne/jordan-bardella"); pg.wait_for_timeout(800)
        chk(pg.locator("#fiche-cond").count() == 0, theme + " pas de lien sans décision")
        chk(not errs, theme + " console " + str(errs))
        ctx.close()
    pg = br.new_page(viewport={"width": 1280, "height": 800})
    pg.goto(B + "#/condamnations"); pg.wait_for_function("window.__route=='condamnations'")
    r = pg.evaluate("(()=>{const a=[...document.querySelectorAll('#tabnav a')].map(x=>x.getBoundingClientRect());const act=document.querySelector('.appbar-act').getBoundingClientRect();return [a[4].right, act.left, a.every(x=>x.top===a[0].top)]})()")
    chk(r[0] < r[1] and r[2], "bureau : cinq onglets sur une ligne dans la barre")
    br.close()
sw = open("sw.js").read()
chk('"condamnations.json"' in sw, "condamnations.json dans la coque hors ligne")
print(f"{ok} ok, {fail} fail")
