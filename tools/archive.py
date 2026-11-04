"""Archives Wayback Machine pour chaque URL de source (déclarations, liens, vidéos).
1) API de disponibilité ; 2) sinon demande d'archivage /save/ (séquentiel, poli, 1 nouvel essai).
Résultat : tools/archives.json {url: {archive_url, archived, status}}"""
import json, os, time, urllib.parse, urllib.request, re, sys
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(HERE,"tools/archives.json")
D=json.load(open(os.path.join(HERE,"site/data.json")))
urls=[]
for n in D["nodes"]:
    for s in n["statements"]:
        urls.append(s["url"])
        if s.get("video"): urls.append(s["video"]["url"])
for e in D["edges"]: urls.append(e["url"])
urls=list(dict.fromkeys(urls))
if len(sys.argv)>1: urls=[u for u in sys.argv[1:]]   # URL précises (ex. nouveaux ajouts)
res=json.load(open(OUT)) if os.path.exists(OUT) else {}
UA="Cartographie-archivage/1.0 (projet citoyen; contact via GitHub)"
def get(u, timeout=60):
    r=urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":UA}), timeout=timeout)
    return r.status, r.geturl(), r.read().decode("utf-8","replace"), dict(r.headers)
def avail(u):
    st,_,body,_=get("https://archive.org/wayback/available?url="+urllib.parse.quote(u, safe=""))
    s=json.loads(body).get("archived_snapshots",{}).get("closest")
    if s and s.get("available") and str(s.get("status","200")).startswith(("2","3")): return s["url"].replace("http://","https://"), s["timestamp"]
    return None
def save(u):
    st,final,body,h=get("https://web.archive.org/save/"+u, timeout=120)
    m=re.search(r"/web/(\d{14})/", final) or re.search(r"/web/(\d{14})/", h.get("Content-Location","")+" "+body[:5000])
    if m: return "https://web.archive.org/web/"+m.group(1)+"/"+u, m.group(1)
    return None
print(len(urls),"urls", flush=True)
for i,u in enumerate(urls):
    if u in res and res[u].get("archive_url"): continue
    if u.startswith("https://x.com/") is False: pass
    out=None; how=None; err=""
    for attempt in (1,2):
        try:
            a=avail(u)
            if a: out,how=a,"existing"; break
        except Exception as e: err="avail:"+str(e)[:80]
        time.sleep(3)
        try:
            a=save(u)
            if a: out,how=a,"saved"; break
            err="save: no timestamp"
        except Exception as e: err="save:"+str(e)[:80]
        time.sleep(8)
    if out: res[u]={"archive_url":out[0],"archived":out[1][:4]+"-"+out[1][4:6]+"-"+out[1][6:8],"status":how}
    else: res[u]={"archive_url":None,"status":"failed","error":err}
    print(i, res[u]["status"], u[:90], err, flush=True)
    json.dump(res,open(OUT,"w"),indent=1,ensure_ascii=False)
    time.sleep(4)
print("DONE", {k:sum(1 for v in res.values() if v["status"]==k) for k in ("existing","saved","failed")})
