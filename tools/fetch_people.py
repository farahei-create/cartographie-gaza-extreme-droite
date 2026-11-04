import json, re, sys, urllib.request, urllib.parse, io, html
from PIL import Image
UA={"User-Agent":"gaza-site-local-builder/1.0 (static documentary site; contact via owner)"}
def get(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=30) as r: return r.read()
def api(host,params):
    params.update(format="json",formatversion="2")
    return json.loads(get(f"https://{host}/w/api.php?"+urllib.parse.urlencode(params)))
PEOPLE={
"caroline-yadan":"Caroline Yadan","aurore-berge":"Aurore Bergé","patrick-klugman":"Patrick Klugman","meyer-habib":"Meyer Habib",
"marine-le-pen":"Marine Le Pen","jordan-bardella":"Jordan Bardella","marion-marechal":"Marion Maréchal","eric-zemmour":"Éric Zemmour",
"eric-ciotti":"Éric Ciotti","yael-braun-pivet":"Yaël Braun-Pivet","robert-menard":"Robert Ménard","manuel-valls":"Manuel Valls",
"bernard-henri-levy":"Bernard-Henri Lévy","raphael-enthoven":"Raphaël Enthoven","caroline-fourest":"Caroline Fourest",
"gilles-william-goldnadel":"Gilles-William Goldnadel","jules-torres":"Jules Torres","gerard-carreyrou":"Gérard Carreyrou",
"joseph-thouvenel":"Joseph Thouvenel","elisabeth-levy":"Élisabeth Lévy","yonathan-arfi":"Yonathan Arfi",
"jean-dominique-merchet":"Jean-Dominique Merchet","serge-klarsfeld":"Serge Klarsfeld","vincent-bollore":"Vincent Bolloré",
"geoffroy-lejeune":"Geoffroy Lejeune","gerald-darmanin":"Gérald Darmanin","bruno-retailleau":"Bruno Retailleau",
"valerie-pecresse":"Valérie Pécresse","emmanuel-macron":"Emmanuel Macron","pierre-edouard-sterin":"Pierre-Édouard Stérin",
"renaud-camus":"Renaud Camus"}
OVERRIDE={"jordan-bardella":"Jordan Bardella - Strasbourg European Parliament September 2022 (Cropped).jpg",
"marion-marechal":"Portrait de Marion Maréchal, avril 2022.jpg"}
def clean_artist(a):
    if "Peter Potrowl" in a: return "© Peter Potrowl"
    if a.startswith("http") and "youtube" in a: return "Capture d'une vidéo YouTube sous licence libre"
    return a
FREE=re.compile(r"^(CC[ -]BY|CC0|Public domain|PD|Attribution|GFDL|FAL|Free Art)",re.I)
def strip(s): return html.unescape(re.sub(r"<[^>]+>","",s or "")).strip()
out={}
for pid,title in PEOPLE.items():
    r=api("fr.wikipedia.org",dict(action="query",prop="pageimages|pageprops",piprop="name",pilicense="free",titles=title,redirects=1))
    p=r["query"]["pages"][0]
    desc=p.get("pageprops",{}).get("wikibase-shortdesc","")
    name=OVERRIDE.get(pid) or p.get("pageimage")
    if p.get("missing") or not name:
        print(f"!! {pid}: no page/free image (missing={p.get('missing')}) desc={desc}"); continue
    c=api("commons.wikimedia.org",dict(action="query",titles="File:"+name,prop="imageinfo",iiprop="url|extmetadata|size|mime",iiurlwidth=480))
    cp=c["query"]["pages"][0]
    if cp.get("missing") or "imageinfo" not in cp:
        print(f"!! {pid}: {name} not on Commons"); continue
    ii=cp["imageinfo"][0]; em=ii.get("extmetadata",{})
    lic=strip(em.get("LicenseShortName",{}).get("value",""))
    if not FREE.match(lic) or em.get("NonFree",{}).get("value") in ("true",True):
        print(f"!! {pid}: non-free license {lic}"); continue
    artist=strip(em.get("Artist",{}).get("value","")) or "Auteur inconnu"
    artist=clean_artist(re.sub(r"\s+"," ",artist))[:120]
    data=get(ii["thumburl"])
    im=Image.open(io.BytesIO(data)).convert("RGB")
    w,h=im.size; s=min(w,h)
    top=int((h-s)*0.12) if h>w else 0
    left=(w-s)//2
    im=im.crop((left,top,left+s,top+s)).resize((256,256),Image.LANCZOS)
    path=f"img/people/{pid}.webp"
    im.save("site/"+path,"WEBP",quality=78,method=6)
    out[pid]=dict(image=path,image_credit=dict(author=artist,license=lic,license_url=em.get("LicenseUrl",{}).get("value",""),
        source_url=ii["descriptionurl"],file=name))
    print(f"ok {pid}: {name} | {lic} | {artist} | {desc}")
json.dump(out,open("tools/people_images.json","w"),ensure_ascii=False,indent=1)
