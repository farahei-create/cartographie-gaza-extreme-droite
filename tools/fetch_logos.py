import json, re, urllib.request, urllib.parse, io, html
from PIL import Image
UA={"User-Agent":"gaza-site-local-builder/1.0 (static documentary site)"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
def api(host,p):
    p.update(format="json",formatversion="2"); return json.loads(get(f"https://{host}/w/api.php?"+urllib.parse.urlencode(p)))
ORGS={"rn":"Rassemblement national","reconquete":"Reconquête (parti politique)","identite-libertes":"Identité-Libertés",
"lr":"Les Républicains","renaissance-epr":"Renaissance (parti)","vivendi-canal":"Groupe Canal+","lagardere":"Lagardère (entreprise)",
"cnews":"CNews","europe1":"Europe 1","jdd":"Le Journal du dimanche","valeurs-actuelles":"Valeurs actuelles",
"franc-tireur":"Franc-Tireur (hebdomadaire)","causeur":"Causeur","sud-radio":"Sud Radio","le-point":"Le Point",
"crif":"Conseil représentatif des institutions juives de France","yad-vashem-fr":"Comité français pour Yad Vashem",
"lexpress":"L'Express","arcom":"Autorité de régulation de la communication audiovisuelle et numérique",
"conseil-etat":"Conseil d'État (France)","conseil-constitutionnel":"Conseil constitutionnel (France)","c8":"C8","fayard":"Éditions Fayard"}
DIRECT={"cnews":"CNews logo.svg","franc-tireur":"Logo-ft.svg","sud-radio":"Logo Sud Radio 2014.svg","lexpress":"Logo L'Express.svg","c8":"Logo C8 2016.svg","le-point":"LogoPoint.jpg"}
FREE=re.compile(r"^(CC[ -]BY|CC0|Public domain|PD|Attribution)",re.I)
def strip(s): return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>","",s or ""))).strip()
out={}
for oid,title in ORGS.items():
    if oid in DIRECT: f=DIRECT[oid]; q=lab="direct"
    else:
      r=api("fr.wikipedia.org",dict(action="query",prop="pageprops",titles=title,redirects=1))
      p=r["query"]["pages"][0]; q=p.get("pageprops",{}).get("wikibase_item")
      if not q: print("!!",oid,"no wikidata",p.get("title"),p.get("missing")); continue
      w=json.loads(get(f"https://www.wikidata.org/wiki/Special:EntityData/{q}.json"))["entities"][q]
      lab=w.get("labels",{}).get("fr",{}).get("value")
      cl=w["claims"].get("P154",[])
      # prefer preferred rank, else last (most recent) normal
      pref=[c for c in cl if c.get("rank")=="preferred"] or [c for c in cl if c.get("rank")=="normal"]
      if not pref: print("!!",oid,q,lab,"no P154"); continue
      f=pref[0]["mainsnak"]["datavalue"]["value"]
    c=api("commons.wikimedia.org",dict(action="query",titles="File:"+f,prop="imageinfo",iiprop="url|extmetadata|mime",iiurlwidth=320))
    ii=c["query"]["pages"][0]["imageinfo"][0]; em=ii["extmetadata"]
    lic=strip(em.get("LicenseShortName",{}).get("value",""))
    if not FREE.match(lic): print("!!",oid,f,"license",lic); continue
    im=Image.open(io.BytesIO(get(ii["thumburl"]))).convert("RGBA")
    bb=im.getbbox()
    if bb: im=im.crop(bb)
    im.thumbnail((256,256),Image.LANCZOS)
    path=f"img/orgs/{oid}.webp"; im.save("site/"+path,"WEBP",quality=90,method=6)
    out[oid]=dict(logo=path,logo_credit=dict(license=lic,source_url=ii["descriptionurl"],file=f,
        author=strip(em.get("Artist",{}).get("value",""))[:100]))
    print("ok",oid,q,lab,"|",f,"|",lic,"|",im.size)
json.dump(out,open("tools/org_logos.json","w"),ensure_ascii=False,indent=1)
