"""Accueil v40 : pas de chevauchement, trait du wordmark, page admin."""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "http://127.0.0.1:8765/"
ART = "/opt/cursor/artifacts"
os.makedirs(ART, exist_ok=True)
ok = fail = 0

def check(c, m):
    global ok, fail
    if c:
        ok += 1
        print("PASS", m)
    else:
        fail += 1
        print("FAIL", m)

MEASURE = """() => {
  function box(sel) {
    const el = document.querySelector(sel);
    if (!el || el.hidden) return null;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return null;
    const r = el.getBoundingClientRect();
    if (r.height < 2 || r.width < 2) return null;
    return {top: r.top, bottom: r.bottom, left: r.left, right: r.right, height: r.height};
  }
  const search = box(".hero .home-search .search-box");
  const stats = box("#home-stats");
  const resume = box("#home-resume");
  const next = box("#view-accueil .h-sec");
  const pillars = box(".hero-pillars");
  const tab = box(".tabnav");
  function space(a, b) { return (a && b) ? +(b.top - a.bottom).toFixed(1) : null; }
  const h = document.getElementById("home-title");
  const word = document.querySelector(".onrecord-word");
  const after = getComputedStyle(word, "::after");
  const wr = word.getBoundingClientRect();
  return {
    sw: document.documentElement.scrollWidth - innerWidth,
    gapSearchStats: space(search, stats),
    gapPillarsSearch: space(pillars, search),
    gapStatsResume: resume ? space(stats, resume) : null,
    gapAfterResume: resume ? space(resume, next) : space(stats, next),
    searchBottom: search && search.bottom,
    tabTop: tab && tab.top,
    tabIsBottom: tab ? tab.top > innerHeight * 0.5 : false,
    shadow: getComputedStyle(h).textShadow,
    lineW: parseFloat(after.width),
    lineH: parseFloat(after.height),
    wordW: wr.width,
    title: (h.textContent || "").replace(/\\s+/g, " ").trim()
  };
}"""

def measure(page, label):
    m = page.evaluate(MEASURE)
    check(m["sw"] <= 1, label + " pas de débordement " + str(m["sw"]))
    check(m["gapPillarsSearch"] is not None and m["gapPillarsSearch"] >= 8, label + " piliers / recherche " + str(m["gapPillarsSearch"]))
    check(m["gapSearchStats"] is not None and m["gapSearchStats"] >= 16, label + " recherche / chiffres " + str(m["gapSearchStats"]))
    if m["gapStatsResume"] is not None:
        check(m["gapStatsResume"] >= 16, label + " chiffres / reprendre " + str(m["gapStatsResume"]))
    check(m["gapAfterResume"] is not None and m["gapAfterResume"] >= 8, label + " bloc suivant " + str(m["gapAfterResume"]))
    if m["tabIsBottom"]:
        check(m["searchBottom"] <= m["tabTop"] + 1, label + " recherche au-dessus des onglets " + str(m["searchBottom"]))
    check(m["title"] == "Onrecord", label + " titre")
    white = "255, 255, 255" in m["shadow"] or "255,255,255" in m["shadow"]
    check(not white, label + " lueur non blanche")
    check(m["lineH"] >= 2 and 20 < m["lineW"] < m["wordW"] * 0.92, label + " trait " + str(m["lineW"]) + "/" + str(m["wordW"]))
    return m

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for scheme in ("dark", "light"):
        for w, h, resume in ((390, 844, False), (390, 844, True), (430, 932, False), (430, 932, True), (1280, 800, False), (1280, 800, True)):
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, color_scheme=scheme, service_workers="block")
            if resume:
                ctx.add_init_script("localStorage.setItem('onrecord:last','marine-le-pen')")
            pg = ctx.new_page()
            pg.goto(BASE, wait_until="networkidle")
            pg.wait_for_selector("#home-stats .stat")
            pg.evaluate("document.fonts.ready")
            label = f"[{w} {scheme} resume={resume}]"
            if resume:
                check(pg.locator("#home-resume").is_visible() and "Reprendre" in pg.inner_text("#home-resume"), label + " reprendre visible")
            else:
                check(pg.locator("#home-resume").is_hidden(), label + " reprendre caché")
            measure(pg, label)
            if w == 390 and scheme == "dark" and not resume:
                pg.locator(".hero").screenshot(path=os.path.join(ART, "hero-390-sombre.png"))
            ctx.close()

    ctx = b.new_context(viewport={"width": 390, "height": 1680}, device_scale_factor=2, color_scheme="dark", service_workers="block")
    ctx.add_init_script("localStorage.setItem('onrecord:last','marine-le-pen')")
    pg = ctx.new_page()
    pg.goto(BASE, wait_until="networkidle")
    pg.wait_for_selector("#home-resume:not([hidden])")
    pg.evaluate("document.fonts.ready")
    zone = pg.evaluate("""() => {
      const a = document.querySelector('.hero .home-search').getBoundingClientRect();
      const c = document.querySelector('.home-quick').getBoundingClientRect();
      const top = Math.max(0, a.top - 8);
      return {x: 0, y: top, width: 390, height: Math.ceil(c.bottom - top + 12)};
    }""")
    pg.screenshot(path=os.path.join(ART, "accueil-recherche-reprendre-390.png"), clip=zone)
    ctx.close()

    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, color_scheme="dark", service_workers="block")
    pg = ctx.new_page()
    pg.goto(BASE + "admin.html", wait_until="networkidle")
    check(pg.locator("#gate").is_visible(), "écran connexion")
    check("noindex" in (pg.locator('meta[name="robots"]').get_attribute("content") or ""), "meta robots")
    pg.screenshot(path=os.path.join(ART, "admin-connexion-390.png"), full_page=True)

    seen = []
    def on_route(route):
        seen.append(route.request.url)
        if route.request.url.startswith("https://api.github.com/"):
            route.fulfill(status=200, content_type="application/json", body='{"full_name":"farahei-create/cartographie-gaza-extreme-droite"}')
        else:
            route.continue_()
    pg.route("https://api.github.com/**", on_route)
    pg.evaluate("localStorage.setItem('onrecord:admin-token','github_pat_exemple_pour_capture_000')")
    pg.reload(wait_until="networkidle")
    pg.wait_for_selector("#workspace:not([hidden])")
    pg.wait_for_function("document.querySelectorAll('#st-person option').length > 5")
    check(all(u.startswith("https://api.github.com/") for u in seen), "jeton seulement vers api.github.com " + str(seen[:4]))
    webp = pg.evaluate("""async () => {
      const c = document.createElement('canvas');
      c.width = 800; c.height = 600;
      const x = c.getContext('2d');
      x.fillStyle = '#5b21b6'; x.fillRect(0, 0, 800, 600);
      const blob = await new Promise(r => c.toBlob(r, 'image/png'));
      const file = new File([blob], 'portrait.png', {type: 'image/png'});
      return OnrecordAdmin.fileToWebp(file, 400);
    }""")
    check(webp["w"] <= 400 and webp["h"] <= 400 and webp["w"] == 400, "webp " + str(webp.get("w")) + "x" + str(webp.get("h")))
    check("webp" in (webp.get("type") or "") and len(webp.get("base64") or "") > 40, "webp base64")
    pg.locator('.tabs button[data-tab="statement"]').click()
    pg.locator("#st-filter").fill("le pen")
    pg.locator("#st-person").select_option("marine-le-pen")
    pg.locator("#st-quote").fill("Phrase d’exemple pour l’aperçu. Elle n’est pas publiée.")
    pg.locator("#st-date").fill("2026-11-12")
    pg.locator("#st-medium").fill("Journal de 20 heures, TF1")
    pg.locator("#st-url").fill("https://www.tf1info.fr/politique/exemple-apercu")
    pg.locator("#st-theme").select_option("France – normalisation de l'extrême droite")
    pg.locator("#st-context").fill("Contexte lu dans la même page, à titre d’exemple.")
    pg.locator("#pane-statement").screenshot(path=os.path.join(ART, "admin-declaration-390.png"))
    b.close()

print(f"{ok} ok, {fail} fail")
raise SystemExit(1 if fail else 0)
