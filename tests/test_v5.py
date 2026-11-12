"""Tests v5 : accueil, sections/catégories, fiches, chronologie, réseau (+ plein écran), routage,
débordements / superpositions à 390x844 et 375x667, clair + sombre, PWA (manifeste, icônes, service worker),
données (catégories, sections, archives), absence d'erreurs console."""
import asyncio, json, os, re, struct
from playwright.async_api import async_playwright

HERE=os.path.dirname(os.path.abspath(__file__))
SITE=os.path.join(HERE,"site") if os.path.isdir(os.path.join(HERE,"site")) else os.path.dirname(HERE)
DATA=json.load(open(os.path.join(SITE,"data.json")))
URL="http://localhost:8765/"
NN=len(DATA["nodes"]); NST=sum(len(n.get("statements",[])) for n in DATA["nodes"])
NDATED_E=sum(1 for e in DATA["edges"] if e.get("date"))
res=[]
def ok(name, cond, info=""):
    res.append((name, bool(cond), info)); print(("PASS " if cond else "FAIL ")+name+("" if cond else "  "+str(info)[:300]))

YT_STUB="<!doctype html><title>stub</title><body style='background:#000'></body>"
def hook(pg, errs, tag):
    pg.on("console", lambda m: errs.append(f"[{tag}] console {m.text}") if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append(f"[{tag}] pageerror {e}"))

# overlays / éléments fixes devant rester dans la fenêtre
INSIDE_JS="""() => {
  const W=innerWidth,H=innerHeight,bad=[];
  const sel=['.appbar','.tabnav','#panel:not([hidden])','.toast.show','.search-results:not([hidden])','.fiche-bar','.sheet-scrim'];
  document.querySelectorAll(sel.join(',')).forEach(el=>{
    const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden'||el.offsetParent===null&&cs.position!=='fixed') return;
    const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
    const fixed=cs.position==='fixed';
    if(r.left<-1||r.right>W+1||(fixed&&(r.top<-1||r.bottom>H+1))) bad.push((el.id||el.className)+' '+[r.left,r.top,r.right,r.bottom].map(Math.round));
  });
  // tout élément visible dépassant horizontalement
  document.querySelectorAll('body *').forEach(el=>{
    if(el.closest('.graph-wrap,.vis-network,.sr-only,.skip')) return;
    const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden') return;
    const r=el.getBoundingClientRect(); if(!r.width) return;
    if(r.right>W+1||r.left<-1) bad.push('X '+el.tagName+'.'+String(el.className).slice(0,40)+' '+Math.round(r.left)+'..'+Math.round(r.right));
  });
  return {sw:document.documentElement.scrollWidth, bw:document.body.scrollWidth, W, bad:bad.slice(0,8), n:bad.length};
}"""

def png_size(p):
    with open(p,"rb") as f: h=f.read(24)
    return struct.unpack(">II", h[16:24])

def static_checks():
    T="[static]"
    m=json.load(open(os.path.join(SITE,"manifest.webmanifest")))
    ok(f"{T} manifest name/short_name", m.get("name") and m.get("name")=="Onrecord" and m.get("short_name")=="Onrecord")
    ok(f"{T} manifest standalone/start_url/scope relative", m["display"]=="standalone" and not m["start_url"].startswith(("/","http")) and not m["scope"].startswith(("/","http")))
    ok(f"{T} manifest violet theme/background", m["theme_color"].lower()=="#3b0a57" and m["background_color"].lower()=="#3b0a57")
    sizes={(i["sizes"],i.get("purpose","any")) for i in m["icons"]}
    ok(f"{T} manifest icons 192/512 any + maskable", {("192x192","any"),("512x512","any"),("192x192","maskable"),("512x512","maskable")}<=sizes, sizes)
    for i in m["icons"]:
        p=os.path.join(SITE,i["src"]); w,h=png_size(p)
        ok(f"{T} icon {i['src']} is {i['sizes']}", f"{w}x{h}"==i["sizes"])
    ok(f"{T} apple-touch-icon 180", png_size(os.path.join(SITE,"icons/apple-touch-icon.png"))==(180,180))
    html=open(os.path.join(SITE,"index.html")).read()
    for k in ['name="apple-mobile-web-app-capable" content="yes"','name="apple-mobile-web-app-status-bar-style" content="black-translucent"',
              'name="apple-mobile-web-app-title" content="Onrecord"','name="theme-color"','rel="manifest" href="manifest.webmanifest"',
              'rel="apple-touch-icon"','viewport-fit=cover']:
        ok(f"{T} head has {k}", k in html)
    ok(f"{T} no external CDN/fonts", not re.search(r'(src|href)="https?://(?!www\.youtube-nocookie)[^"]*\.(js|css|woff2?)', html) and "fonts.googleapis" not in html)
    ok(f"{T} no absolute local paths", not re.search(r'(src|href)="/(?!/)', html))
    ok(f"{T} sw.js network-first data.json", "data\\.json" in open(os.path.join(SITE,"sw.js")).read())
    ok(f"{T} download link", 'href="data.json" download' in html)
    meth=html[html.index('id="view-methodologie"'):]
    ok(f"{T} methodology archiving + citation paragraphs", "Archivage des sources" in meth and "Citer ce site" in meth)
    # données
    ok(f"{T} every node has category + subcategory", all(n.get("category") and n.get("subcategory") for n in DATA["nodes"]))
    ok(f"{T} category_order covers categories", {n["category"] for n in DATA["nodes"]}<=set(DATA["meta"]["category_order"]))
    sts=[s for n in DATA["nodes"] for s in n.get("statements",[])]
    ok(f"{T} every statement has section", all(s.get("section") in ("gaza","france") for s in sts))
    ok(f"{T} every statement has url/date/quote/medium", all(s.get("url") and s.get("date") and s.get("quote") and s.get("medium") for s in sts))
    arch=[o for o in sts+DATA["edges"] if o.get("archive_url")]
    ok(f"{T} archive_url format", all(o["archive_url"].startswith("https://web.archive.org/web/") and re.match(r"\d{4}-\d{2}-\d{2}$",o.get("archived","")) for o in arch), len(arch))
    ok(f"{T} some sources archived", len(arch)>0, len(arch))
    txt=json.dumps(DATA,ensure_ascii=False).lower()+html.lower()
    ok(f"{T} neutral wording (no 'complice')", "complice" not in txt)

async def mobile(b, w, h, scheme, errs):
    T=f"[{w}x{h} {scheme}]"
    ctx=await b.new_context(viewport={"width":w,"height":h}, device_scale_factor=2, is_mobile=True, has_touch=True, color_scheme=scheme, service_workers="block")
    yt=[]
    await ctx.route(re.compile(r"https://(www\.)?(youtube-nocookie|youtube)\.com/.*"), lambda r: (yt.append(r.request.url), asyncio.ensure_future(r.fulfill(status=200, content_type="text/html", body=YT_STUB)))[1])
    pg=await ctx.new_page(); hook(pg, errs, T)
    shot = (w==390 and scheme=="light")
    async def check(label):
        await pg.wait_for_timeout(450)
        r=await pg.evaluate(INSIDE_JS)
        ok(f"{T} {label}: no horizontal overflow / overlays inside", r["sw"]<=w and r["n"]==0, r)
    await pg.goto(URL, wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    ok(f"{T} landing is Accueil", await pg.evaluate("window.__route")=="accueil")
    ok(f"{T} tab bar visible at bottom", await pg.evaluate("(()=>{const r=document.querySelector('.tabnav').getBoundingClientRect();return Math.abs(r.bottom-innerHeight)<1&&r.height>=56})()"))
    tabs=await pg.evaluate("[...document.querySelectorAll('#tabnav a')].map(a=>[a.textContent.trim(),a.getBoundingClientRect().height,a.getBoundingClientRect().width])")
    ok(f"{T} 7 tabs with big targets", [t[0] for t in tabs]==["Accueil","Sections","Chronologie","Réseau","Échelle","Coulisses","Méthode"] and all(t[1]>=44 and t[2]>=44 for t in tabs), tabs)
    ok(f"{T} home stats", await pg.locator("#home-stats .stat").count()==7)
    ok(f"{T} home stats values", (await pg.locator("#home-stats .stat").nth(2).locator("dd").inner_text()).strip()==str(NST))
    ok(f"{T} home entry cards", await pg.locator("#home-entries .entry").count()==8)
    ok(f"{T} home latest 6", await pg.locator("#home-latest li").count()==6)
    dates=await pg.evaluate("[...document.querySelectorAll('#home-latest time')].map(t=>t.getAttribute('datetime'))")
    ok(f"{T} latest sorted desc", dates==sorted(dates, reverse=True), dates)
    bg=await pg.evaluate("getComputedStyle(document.querySelector('.hero')).backgroundImage")
    ok(f"{T} violet hero", "7, 3, 15" in bg or "20, 7, 38" in bg, bg[:180])
    hb=await pg.evaluate("""(()=>{const h=document.getElementById('home-title'),r=h.getBoundingClientRect(),t=document.querySelector('.tagline'),tr=t.getBoundingClientRect(),cs=getComputedStyle(h);
      return {text:h.textContent.replace(/\\s+/g,' ').trim(),l:r.left,r:innerWidth-r.right,top:r.top,w:r.width,sw:h.scrollWidth,cw:h.clientWidth,fs:parseFloat(cs.fontSize),fw:cs.fontWeight,vis:cs.visibility,
        tag:t.textContent.replace(/\\s+/g,' ').trim(), tl:tr.left, trr:innerWidth-tr.right, title:document.title}})()""")
    ok(f"{T} brand wordmark visible", hb["text"]=="Onrecord" and hb["vis"]=="visible" and 0<=hb["top"]<200, hb)
    ok(f"{T} brand wordmark large & bold", hb["fs"]>=72 and int(hb["fw"])>=700, hb)
    ok(f"{T} brand wordmark centered", abs(hb["l"]-hb["r"])<=2 and abs(hb["tl"]-hb["trr"])<=2, hb)
    ok(f"{T} brand wordmark not overflowing", hb["l"]>=-1 and hb["r"]>=-1 and hb["sw"]<=hb["cw"]+1, hb)
    ok(f"{T} punchline + document title", hb["tag"]=="ILS L’ONT DIT ON L’A ARCHIVÉ" and hb["title"]=="Onrecord — Leurs mots, datés et sourcés", hb)
    purpose=(await pg.locator(".hero-purpose").inner_text()).strip()
    ok(f"{T} purpose line", purpose=="Déclarations publiques sur Gaza, la banalisation de l’extrême droite en France, et les liens entre leurs auteurs.", purpose)
    labels=await pg.evaluate("[...document.querySelectorAll('.hero-pillar strong')].map(e=>e.textContent.trim())")
    ok(f"{T} pillar labels", labels==["Gaza","Extrême droite","Les liens"], labels)
    hints=await pg.evaluate("[...document.querySelectorAll('.hero-pillar small')].map(e=>e.textContent.trim())")
    ok(f"{T} pillar hints", hints==["Qui a dit quoi","Sa normalisation","Personnes, médias, argent"], hints)
    gone=await pg.locator(".hero").inner_text()
    ok(f"{T} old hero copy gone", "place publique" not in gone and "Archive citoyenne" not in gone and "Ce qu'ils ont dit" not in gone, gone[:240])
    if w==390 and h==844:
        fold=await pg.evaluate("""(()=>{const s=document.querySelector('.home-search .search-box').getBoundingClientRect();const tab=document.querySelector('.tabnav').getBoundingClientRect();const el=document.querySelector('.hero-purpose');const lh=parseFloat(getComputedStyle(el).lineHeight);return {searchBottom:s.bottom, tabTop:tab.top, purposeLines:el.getBoundingClientRect().height/lh}})()""")
        ok(f"{T} search above the fold", fold["searchBottom"]<=fold["tabTop"]+1, fold)
        ok(f"{T} purpose at most three lines", fold["purposeLines"]<=3.35, fold)
    hrefs=await pg.evaluate("[...document.querySelectorAll('.hero-pillar')].map(a=>a.getAttribute('href'))")
    ok(f"{T} three hero pillars", hrefs==["#/sections/gaza","#/sections/france","#/coulisses"], hrefs)
    ok(f"{T} hero canvas", await pg.locator("#hero-net").count()==1)
    net=await pg.evaluate("""(()=>{const c=document.getElementById('hero-net');const s=getComputedStyle(c);const x=c.getContext('2d');
      const x0=Math.floor(c.width*0.12), y0=Math.floor(c.height*0.04), rw=Math.floor(c.width*0.76), rh=Math.max(2, Math.floor(c.height*0.34));
      let n=0; if(c.width&&c.height){const d=x.getImageData(x0,y0,rw,rh).data; for(let i=3;i<d.length;i+=32) if(d[i]>28) n++;}
      const h=document.getElementById('home-title'); const hs=getComputedStyle(h);
      return {n, op:+s.opacity, disp:s.display, dpr:c.clientWidth?+(c.width/c.clientWidth).toFixed(2):0, ff:hs.fontFamily, tf:hs.textTransform, fw:hs.fontWeight}})()""")
    ok(f"{T} hero net visible behind the title", net["n"]>12 and net["op"]>0.8 and net["disp"]!="none" and net["dpr"]<=2.05, net)
    ok(f"{T} Anton uppercase wordmark", "Anton" in net["ff"] and net["tf"]=="uppercase" and int(net["fw"])>=900, net)
    ok(f"{T} brand text Onrecord", (await pg.locator(".appbar .brand span").inner_text()).strip()=="Onrecord")
    await check("home")
    if shot:
        await pg.screenshot(path=os.path.join(HERE,"v5-home-mobile.png")); await pg.screenshot(path=os.path.join(HERE,"onrecord-home-mobile-v2.png"))
    # recherche
    await pg.fill("#home-search","bardella")
    ok(f"{T} home search results", await pg.locator("#home-results a").count()>=1)
    await check("home search open")
    await pg.locator("#home-results a").first.tap()
    await pg.wait_for_timeout(500)
    ok(f"{T} search → fiche", (await pg.evaluate("location.hash")).startswith("#/personne/jordan-bardella"))
    # sections
    await pg.locator("#tab-sections").tap(); await pg.wait_for_timeout(500)
    ok(f"{T} tab Sections route", await pg.evaluate("window.__route")=="sections")
    ok(f"{T} Sections tab current", await pg.get_attribute("#tab-sections","aria-current")=="page")
    ncat=await pg.locator("#sec-groups details.cat").count()
    ok(f"{T} categories accordion", ncat==len(DATA["meta"]["category_order"]) or ncat==len({n['category'] for n in DATA['nodes']}), ncat)
    ok(f"{T} all fiches listed", await pg.locator("#sec-groups li[data-id]").count()==NN)
    ok(f"{T} avatars present", await pg.locator("#sec-groups .ncard .av").count()==NN)
    await check("sections")
    if shot: await pg.screenshot(path=os.path.join(HERE,"v5-sections-mobile.png"))
    await pg.locator('#sec-seg [data-sec="france"]').tap(); await pg.wait_for_timeout(400)
    vis=await pg.evaluate("[...document.querySelectorAll('#sec-groups li[data-id]')].filter(l=>!l.hidden).map(l=>l.dataset.id)")
    exp=[n["id"] for n in DATA["nodes"] if "france" in n.get("sections",[])]
    ok(f"{T} section France filter", sorted(vis)==sorted(exp), (len(vis),len(exp)))
    await pg.locator('#sec-seg [data-sec="commun"]').tap(); await pg.wait_for_timeout(400)
    vis=await pg.evaluate("[...document.querySelectorAll('#sec-groups li[data-id]')].filter(l=>!l.hidden).length")
    ok(f"{T} section Communs filter", vis==sum(1 for n in DATA["nodes"] if {"gaza","france"}<=set(n.get("sections",[]))))
    await pg.locator('#sec-seg [data-sec="tout"]').tap(); await pg.wait_for_timeout(300)
    # accordéon
    first=pg.locator("#sec-groups details.cat").first
    await first.locator("summary").tap(); await pg.wait_for_timeout(300)
    ok(f"{T} accordion collapses", not await first.evaluate("d=>d.open"))
    await first.locator("summary").tap(); await pg.wait_for_timeout(300)
    await pg.fill("#sec-search","zemmour"); await pg.wait_for_timeout(200)
    ok(f"{T} sections search", await pg.evaluate("[...document.querySelectorAll('#sec-groups li[data-id]')].filter(l=>!l.hidden).map(l=>l.dataset.id)")==["eric-zemmour"])
    await pg.fill("#sec-search","")
    # fiche
    pid=max((n for n in DATA["nodes"] if n["type"]=="person"), key=lambda n:(bool(n.get("image")), len(n.get("statements",[]))))["id"]
    await pg.locator(f'#sec-groups li[data-id="{pid}"] a').tap(); await pg.wait_for_timeout(600)
    n=[x for x in DATA["nodes"] if x["id"]==pid][0]
    ok(f"{T} fiche route", await pg.evaluate("location.hash")==f"#/personne/{pid}" and await pg.evaluate("window.__route")=="fiche")
    ok(f"{T} fiche name", (await pg.locator(".f-name").inner_text()).strip()==n["name"])
    ok(f"{T} fiche photo + credit", await pg.locator(".f-media img").count()==1 and await pg.locator(".f-media .credit").count()==1)
    ok(f"{T} fiche categories", n["category"] in await pg.locator(".f-cat").inner_text())
    ok(f"{T} fiche timeline items", await pg.locator(".fiche .tl > .tl-item").count()==len(n["statements"]))
    d=await pg.evaluate("[...document.querySelectorAll('.fiche .tl-date')].map(t=>t.getAttribute('datetime'))")
    ok(f"{T} fiche timeline ascending", d==sorted(d))
    ok(f"{T} fiche 'Lire la source' links", await pg.locator(".fiche .tl-item a.src").count()==len(n["statements"]))
    na=sum(1 for s in n["statements"] if s.get("archive_url"))
    ok(f"{T} fiche archive links", await pg.locator(".fiche .tl-item a.arch").count()==na, na)
    ok(f"{T} fiche theme tags", await pg.locator(".fiche .tl-item .theme").count()==sum(1 for s in n["statements"] if s.get("theme")))
    ok(f"{T} fiche relations", await pg.locator(".fiche .rel-card").count()==sum(1 for e in DATA["edges"] if pid in (e["source"],e["target"])))
    await check("fiche")
    if shot: await pg.screenshot(path=os.path.join(HERE,"v5-person-mobile.png"))
    # partage (fallback copie)
    await pg.evaluate("navigator.share=undefined; window.__copied=null; navigator.clipboard && (navigator.clipboard.writeText=(t)=>{window.__copied=t;return Promise.resolve()})")
    await pg.locator("#fiche-share").tap(); await pg.wait_for_timeout(400)
    ok(f"{T} share copy fallback + toast", (await pg.evaluate("window.__copied") or "").endswith(f"#/personne/{pid}") and await pg.locator(".toast.show").count()==1)
    await check("toast")
    # Web Share
    await pg.evaluate("window.__shared=null; navigator.share=(d)=>{window.__shared=d;return Promise.resolve()}")
    await pg.locator("#fiche-share").tap(); await pg.wait_for_timeout(200)
    ok(f"{T} Web Share API used", ((await pg.evaluate("window.__shared")) or {}).get("url","").endswith(f"#/personne/{pid}"))
    # vidéo au clic
    vn=next((x for x in DATA["nodes"] if any((s.get("video") or {}).get("provider")=="youtube" for s in x.get("statements",[]))), None)
    if vn:
        await pg.goto(URL+"#/personne/"+vn["id"]); await pg.wait_for_timeout(600)
        ok(f"{T} no YouTube request before click", len(yt)==0, yt)
        await pg.locator(".fiche .video-btn").first.tap(); await pg.wait_for_timeout(800)
        ok(f"{T} YouTube nocookie on click", any("youtube-nocookie.com" in u for u in yt) and await pg.locator(".fiche iframe").count()==1, yt)
        await check("fiche video")
    # relation → navigation
    await pg.goto(URL+f"#/personne/{pid}"); await pg.wait_for_timeout(500)
    href=await pg.locator(".fiche .rel-main").first.get_attribute("href")
    await pg.locator(".fiche .rel-main").first.tap(); await pg.wait_for_timeout(500)
    ok(f"{T} relation tap navigates", await pg.evaluate("location.hash")==href)
    await pg.locator("#fiche-back").tap(); await pg.wait_for_timeout(500)
    ok(f"{T} back button", await pg.evaluate("location.hash")==f"#/personne/{pid}")
    # organisation deep link
    org=next(x for x in DATA["nodes"] if x["type"]!="person")
    await pg.goto(URL+"#/organisation/"+org["id"]); await pg.wait_for_timeout(500)
    ok(f"{T} organisation deep link", (await pg.locator(".f-name").inner_text()).strip()==org["name"])
    await pg.goto(URL+"#/personne/n-existe-pas"); await pg.wait_for_timeout(400)
    ok(f"{T} unknown fiche handled", "introuvable" in await pg.locator("#fiche-body").inner_text())
    # ancre d'une déclaration
    await pg.goto(URL+f"#/personne/{pid}#d0"); await pg.wait_for_timeout(1200)
    ok(f"{T} statement anchor in view", await pg.evaluate("(()=>{const r=document.getElementById('d0').getBoundingClientRect();return r.top<innerHeight&&r.bottom>0})()"))
    # chronologie
    await pg.locator("#tab-chronologie").tap(); await pg.wait_for_timeout(600)
    ok(f"{T} chronologie all items", await pg.locator("#timeline .tl-item").count()==NST+NDATED_E, (await pg.locator("#timeline .tl-item").count(), NST+NDATED_E))
    d=await pg.evaluate("[...document.querySelectorAll('#timeline .tl-date')].map(t=>t.getAttribute('datetime'))")
    ok(f"{T} chronologie ascending", d==sorted(d))
    await check("chronologie")
    if shot: await pg.screenshot(path=os.path.join(HERE,"v5-timeline-mobile.png"))
    await pg.select_option("#tl-section","france"); await pg.wait_for_timeout(200)
    secs=set(await pg.evaluate("[...document.querySelectorAll('#timeline .tl-item')].map(i=>i.dataset.sec)"))
    ok(f"{T} filter section", secs=={"france"}, secs)
    await pg.select_option("#tl-section",""); 
    cat=DATA["meta"]["category_order"][0]
    await pg.select_option("#tl-category",cat); await pg.wait_for_timeout(200)
    exp=sum(1 for n in DATA["nodes"] if n["category"]==cat for s in n.get("statements",[]))+sum(1 for e in DATA["edges"] if e.get("date") and cat in ([x["category"] for x in DATA["nodes"] if x["id"] in (e["source"],e["target"])]))
    ok(f"{T} filter category", await pg.locator("#timeline .tl-item").count()==exp, exp)
    await pg.select_option("#tl-category","")
    th=next(s["theme"] for n in DATA["nodes"] for s in n.get("statements",[]) if s.get("theme"))
    await pg.select_option("#tl-theme",th); await pg.wait_for_timeout(200)
    ok(f"{T} filter theme", await pg.locator("#timeline .tl-item").count()==sum(1 for n in DATA["nodes"] for s in n.get("statements",[]) if s.get("theme")==th) and await pg.locator("#timeline .k-e").count()==0)
    await pg.select_option("#tl-theme","__links__"); await pg.wait_for_timeout(200)
    ok(f"{T} filter links only", await pg.locator("#timeline .tl-item").count()==NDATED_E==await pg.locator("#timeline .k-e").count())
    await pg.select_option("#tl-theme","")
    yr=d[len(d)//2][:4]
    await pg.select_option("#tl-year",yr); await pg.wait_for_timeout(200)
    yrs=set(await pg.evaluate("[...document.querySelectorAll('#timeline .tl-date')].map(t=>t.getAttribute('datetime').slice(0,4))"))
    ok(f"{T} filter year", yrs=={yr}, yrs)
    await pg.select_option("#tl-year","")
    await pg.locator("#tl-order").tap(); await pg.wait_for_timeout(200)
    d2=await pg.evaluate("[...document.querySelectorAll('#timeline .tl-date')].map(t=>t.getAttribute('datetime'))")
    ok(f"{T} order toggle desc", d2==sorted(d2, reverse=True))
    await pg.locator("#tl-order").tap()
    # réseau
    await pg.locator("#tab-reseau").tap()
    await pg.wait_for_function("window.__graphReady===true", timeout=30000); await pg.wait_for_timeout(800)
    ok(f"{T} graph built lazily on Réseau", await pg.evaluate("window.__route")=="reseau" and len(await pg.evaluate("__visible()"))==NN)
    gh=await pg.evaluate("(()=>{const r=document.getElementById('graph').getBoundingClientRect();return [r.height,r.bottom,document.querySelector('.tabnav').getBoundingClientRect().top]})()")
    ok(f"{T} graph sized above tab bar", gh[0]>200 and gh[1]<=gh[2]+1, gh)
    await check("reseau")
    # tap noeud → panneau
    pos=await pg.evaluate(f"__nodeDOM('{pid}')")
    if pos:
        await pg.touchscreen.tap(pos["x"], pos["y"]); await pg.wait_for_timeout(900)
    pname=next(n["name"] for n in DATA["nodes"] if n["id"]==pid)
    if await pg.evaluate("document.getElementById('panel').hidden") or pname not in (await pg.inner_text("#panel-body")):
        # le tap peut tomber sur une arête si la simulation n'est pas encore stabilisée : repli sur la route directe
        await pg.goto(URL+f"#/reseau/{pid}"); await pg.wait_for_function("window.__graphReady===true"); await pg.wait_for_timeout(1200)
    ok(f"{T} panel opens", not await pg.evaluate("document.getElementById('panel').hidden"))
    ok(f"{T} panel link to fiche", await pg.locator("#panel .to-fiche").count()>=1)
    await check("reseau panel")
    pr=await pg.evaluate("(()=>{const r=document.getElementById('panel').getBoundingClientRect();return [r.top,r.bottom,innerHeight]})()")
    ok(f"{T} panel within viewport", pr[0]>=0 and pr[1]<=pr[2]+1, pr)
    await pg.locator("#panel .to-fiche").first.tap(); await pg.wait_for_timeout(600)
    ok(f"{T} panel → fiche", await pg.evaluate("window.__route")=="fiche" and await pg.evaluate("document.getElementById('panel').hidden"))
    # plein écran
    await pg.goto(URL+"#/reseau"); await pg.wait_for_function("window.__graphReady===true"); await pg.wait_for_timeout(500)
    await pg.locator("#btn-fs").tap(); await pg.wait_for_timeout(900)
    ok(f"{T} fullscreen on", await pg.evaluate("__fs()") in ("native","pseudo"))
    fr=await pg.evaluate("(()=>{const r=document.querySelector('.graph-shell').getBoundingClientRect();return [r.left,r.top,r.width,r.height,innerWidth,innerHeight]})()")
    ok(f"{T} fullscreen fills viewport", abs(fr[2]-fr[4])<2 and abs(fr[3]-fr[5])<2, fr)
    ok(f"{T} tab bar hidden in fullscreen", await pg.evaluate("getComputedStyle(document.querySelector('.tabnav')).visibility")=="hidden" or await pg.evaluate("__fs()")=="native")
    await check("fullscreen")
    await pg.locator("#btn-fs").tap(); await pg.wait_for_timeout(700)
    ok(f"{T} fullscreen off", not await pg.evaluate("__fs()"))
    # méthodologie
    await pg.locator("#tab-methodologie").tap(); await pg.wait_for_timeout(500)
    ok(f"{T} méthodologie view", await pg.evaluate("window.__route")=="methodologie" and await pg.locator("#view-methodologie h3:has-text('Archivage des sources')").count()==1)
    await check("methodologie")
    # anciennes adresses
    for old,new in [("#graphe","#/reseau"),("#liste","#/sections"),("#methodologie","#/methodologie"),(f"#graphe/{pid}",f"#/reseau/{pid}")]:
        await pg.goto(URL+old); await pg.wait_for_timeout(500)
        ok(f"{T} legacy {old} → {new}", await pg.evaluate("location.hash")==new)
    await pg.goto(URL+"#/n-importe-quoi"); await pg.wait_for_timeout(300)
    ok(f"{T} unknown route → accueil", await pg.evaluate("window.__route")=="accueil")
    # contraste approximatif de l'accent
    c=await pg.evaluate("[getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(), getComputedStyle(document.body).backgroundColor]")
    ok(f"{T} accent is violet", c[0].lower() in ("#7b2cbf","#c9a2f5"), c)
    await ctx.close()

async def desktop(b, scheme, errs):
    T=f"[desktop {scheme}]"
    ctx=await b.new_context(viewport={"width":1280,"height":860}, color_scheme=scheme)
    pg=await ctx.new_page(); hook(pg, errs, T)
    await pg.goto(URL, wait_until="networkidle"); await pg.wait_for_timeout(500)
    r=await pg.evaluate(INSIDE_JS); ok(f"{T} no overflow", r["sw"]<=1280 and r["n"]==0, r)
    nb=await pg.evaluate("(()=>{const r=document.querySelector('.tabnav').getBoundingClientRect();return [r.top,r.bottom]})()")
    ok(f"{T} tabs at top on desktop", nb[1]<70, nb)
    wr=await pg.evaluate("(()=>{const r=document.querySelector('.home-body').getBoundingClientRect();return [r.left, innerWidth-r.right]})()")
    ok(f"{T} centered layout", abs(wr[0]-wr[1])<20, wr)
    pl=await pg.evaluate("""(()=>{const el=document.querySelector('.hero-purpose');const lh=parseFloat(getComputedStyle(el).lineHeight);return el.getBoundingClientRect().height/lh})()""")
    ok(f"{T} purpose one line", pl<=1.2, pl)
    if scheme=="light": await pg.screenshot(path=os.path.join(HERE,"v5-home-desktop.png"))
    else: await pg.screenshot(path="/tmp/v5-home-desktop-dark.png")
    for v in ["sections","chronologie","methodologie","personne/emmanuel-macron"]:
        await pg.goto(URL+"#/"+v); await pg.wait_for_timeout(500)
        r=await pg.evaluate(INSIDE_JS); ok(f"{T} {v} no overflow", r["n"]==0, r)
    await pg.goto(URL+"#/reseau"); await pg.wait_for_function("window.__graphReady===true && window.__imagesDone===true", timeout=30000)
    st=await pg.evaluate("window.__imgState"); ok(f"{T} graph images loaded", st["failed"]==0, st)
    await pg.locator("#btn-fs").click(); await pg.wait_for_timeout(800)
    ok(f"{T} fullscreen on", await pg.evaluate("__fs()") in ("native","pseudo"))
    await pg.keyboard.press("Escape"); await pg.wait_for_timeout(600)
    if await pg.evaluate("__fs()"): await pg.locator("#btn-fs").click(); await pg.wait_for_timeout(500)
    ok(f"{T} fullscreen off", not await pg.evaluate("__fs()"))
    # dark: couleurs
    bgc=await pg.evaluate("getComputedStyle(document.body).backgroundColor")
    ok(f"{T} body background matches scheme", (bgc=="rgb(15, 10, 21)") if scheme=="dark" else (bgc=="rgb(247, 244, 250)"), bgc)
    await ctx.close()

async def pwa(b, errs):
    T="[pwa]"
    ctx=await b.new_context(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True)
    pg=await ctx.new_page(); hook(pg, errs, T)
    await pg.goto(URL, wait_until="networkidle")
    await pg.wait_for_function("window.__swRegistered===true || window.__swError", timeout=15000)
    ok(f"{T} service worker registers", await pg.evaluate("window.__swRegistered===true"), await pg.evaluate("window.__swError"))
    await pg.wait_for_function("navigator.serviceWorker.controller!==null || true")
    await pg.evaluate("navigator.serviceWorker.ready")
    await pg.wait_for_timeout(2500)
    keys=await pg.evaluate("caches.keys().then(async ks=>{const out={};for(const k of ks){const c=await caches.open(k);out[k]=(await c.keys()).map(r=>r.url.replace(location.origin+'/',''))}return out})")
    allk=[u for v in keys.values() for u in v]
    ok(f"{T} shell cached", all(x in allk for x in ["index.html","style.css","app.js","data.json","vendor/vis-network.min.js"]), list(keys))
    nimg=sum(1 for n in DATA["nodes"] for k in ("image","logo") if n.get(k))
    ok(f"{T} images cached", sum(1 for u in allk if u.startswith("img/") or "/img" in u or u.endswith((".jpg",".png",".webp",".svg")) and not u.startswith("icons"))>=nimg*0.9, (nimg, len(allk)))
    man=await pg.evaluate("fetch(document.querySelector('link[rel=manifest]').href).then(r=>r.json())")
    ok(f"{T} manifest served", man["short_name"]=="Onrecord")
    for i in man["icons"]+[{"src":"icons/apple-touch-icon.png"},{"src":"icons/favicon-64.png"}]:
        st=await pg.evaluate("(u)=>new Promise(r=>{const im=new Image();im.onload=()=>r(im.naturalWidth);im.onerror=()=>r(0);im.src=u})", i["src"])
        ok(f"{T} icon loads {i['src']}", st>0)
    # hors ligne : rechargement depuis le cache
    await pg.reload(wait_until="networkidle"); await pg.wait_for_timeout(500)
    await ctx.set_offline(True)
    await pg.reload(); await pg.wait_for_timeout(1500)
    ok(f"{T} works offline (cached shell + data)", await pg.locator("#home-stats .stat").count()==7)
    await pg.goto(URL+"#/personne/jordan-bardella"); await pg.wait_for_timeout(800)
    ok(f"{T} offline fiche + photo", await pg.evaluate("(()=>{const i=document.querySelector('.f-media img');return !!i&&i.complete&&i.naturalWidth>0})()"))
    await ctx.set_offline(False)
    errs[:]=[e for e in errs if not ("[pwa]" in e and "ERR_INTERNET_DISCONNECTED" in e)]
    await ctx.close()

async def reduced_motion(b, errs):
    ctx=await b.new_context(viewport={"width":375,"height":667}, reduced_motion="reduce", service_workers="block")
    pg=await ctx.new_page(); hook(pg, errs, "[rm]")
    await pg.goto(URL+"#/sections", wait_until="networkidle")
    d=await pg.evaluate("getComputedStyle(document.querySelector('#view-sections')).animationDuration")
    ok("[reduced motion] animations disabled", d in ("1e-05s","0.00001s") or float(d.rstrip("s"))<0.001, d)
    await ctx.close()

async def hero_center(b, errs):
    """Centre du titre et du slogan, sans débordement. Le dessin au pixel (PIL) reste le contrôle visuel."""
    import io
    from PIL import Image
    for w in (375,390,430):
        for scheme in ("light","dark"):
            T=f"[hero {w} {scheme}]"
            ctx=await b.new_context(viewport={"width":w,"height":844}, device_scale_factor=2, is_mobile=True, has_touch=True, color_scheme=scheme, service_workers="block")
            pg=await ctx.new_page(); hook(pg, errs, T)
            await pg.goto(URL, wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(800)
            await pg.evaluate("""()=>{const n=document.getElementById('hero-net'); if(n) n.style.visibility='hidden';
              document.querySelectorAll('.hero-marquee,.hero-glow').forEach(e=>{e.style.visibility='hidden'});
              const s=document.createElement('style');
              s.textContent='.tagline::before,.tagline::after,.hero h1.onrecord::before{display:none !important}';
              document.head.appendChild(s);}""")
            async def ink(sel):
                r=await pg.evaluate("(s)=>{const e=document.querySelector(s),g=document.createRange();g.selectNodeContents(e);const b=g.getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]}", sel)
                png=await pg.screenshot(clip={"x":0,"y":r[1],"width":w,"height":max(1, r[3]-r[1])})
                im=Image.open(io.BytesIO(png)).convert("RGB"); W,H=im.size; px=im.load()
                def lit(rgb):
                    return sum(rgb)>500
                cols=[x for x in range(W) if sum(1 for y in range(H) if lit(px[x,y]))>=max(3, H*0.1)]
                if not cols: cols=[x for x in range(W) if any(sum(px[x,y])>420 for y in range(H))]
                return cols[0]/2, (cols[-1]+1)/2, r
            tl,tr,trect=await ink("#home-title"); gl,gr,grect=await ink(".tagline")
            tc,gc=(tl+tr)/2,(gl+gr)/2
            ok(f"{T} title ink centered on page (<=2px)", abs(tc-w/2)<=2, (tc,w/2))
            ok(f"{T} title and tagline centers within 2px (ink)", abs(tc-gc)<=2, (tc,gc))
            bx=await pg.evaluate("[...['#home-title','.tagline']].map(s=>{const r=document.querySelector(s).getBoundingClientRect();return (r.left+r.right)/2})")
            ok(f"{T} title and tagline element boxes centered (<=2px)", abs(bx[0]-w/2)<=2 and abs(bx[1]-w/2)<=2, bx)
            ok(f"{T} title inside viewport", tl>=4 and tr<=w-4, (tl,tr,trect))
            fs=await pg.evaluate("parseFloat(getComputedStyle(document.getElementById('home-title')).fontSize)")
            ok(f"{T} title large", fs>=24, fs)
            ov=await pg.evaluate("document.documentElement.scrollWidth-innerWidth")
            ok(f"{T} no horizontal overflow", ov<=0, ov)
            await ctx.close()

async def main():
    static_checks()
    errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for scheme in ("light","dark"):
            for (w,h) in ((390,844),(375,667)):
                await mobile(b,w,h,scheme,errs)
            await desktop(b,scheme,errs)
        await hero_center(b,errs)
        await pwa(b,errs)
        await reduced_motion(b,errs)
        await b.close()
    ok("no console errors", not errs, errs[:10])
    n=sum(1 for r in res if r[1]); print(f"\n{n}/{len(res)} passed")
    json.dump([{"name":a,"pass":b_,"info":str(c)[:300]} for a,b_,c in res], open("/tmp/test_v5_results.json","w"), ensure_ascii=False, indent=1)
asyncio.run(main())
