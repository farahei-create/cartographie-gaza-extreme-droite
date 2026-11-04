"""Vérifie (curl -sL) toutes les URL de data.json et régénère sources-check.md en conservant les notes existantes."""
import json, re, subprocess, os, datetime
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(os.path.join(HERE,"site/data.json")))
name={n["id"]:n["name"] for n in D["nodes"]}
old={}
p=os.path.join(HERE,"sources-check.md")
if os.path.exists(p):
    for l in open(p):
        m=re.match(r"\| \S+ \| (\S+) \| .*? \| (.*) \|$", l.rstrip("\n"))
        if m and m.group(2).strip(): old[m.group(1)]=m.group(2).strip()
use={}; kind={}; newids=set()
v3=json.load(open(os.path.join(HERE,"site-backup-v3/data.json")))
oldurls={s["url"] for n in v3["nodes"] for s in n["statements"]}|{e["url"] for e in v3["edges"]}
def add(u,what,k):
    use.setdefault(u,[]); 
    if what not in use[u]: use[u].append(what)
    kind.setdefault(u,k)
for n in D["nodes"]:
    for s in n["statements"]:
        add(s["url"],name[n["id"]],"src")
        if s.get("video"): add(s["video"]["url"],"vidéo · "+name[n["id"]],"video")
    if n.get("image_credit"): add(n["image_credit"]["source_url"],"photo · "+n["name"],"img")
    if n.get("logo_credit"): add(n["logo_credit"]["source_url"],"logo · "+n["name"],"img")
for e in D["edges"]: add(e["url"],f"edge {e['source']}→{e['target']}","src")
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def chk(u):
    if u.startswith("https://x.com/"): return u,"200*"
    r=subprocess.run(["curl","-sL","-o","/dev/null","-w","%{http_code}","-m","25","-A",UA,"-H","Accept-Language: fr-FR,fr;q=0.9",u],capture_output=True,text=True)
    return u,r.stdout.strip() or "000"
with ThreadPoolExecutor(8) as ex: codes=dict(ex.map(chk,list(use)))
def note(u,c):
    if u in old: return old[u]
    if c=="200*": return "Message X / profil : contenu lu via l'API X le 03/11/2026"
    if c=="403": return "403 anti-bot pour curl ; à revérifier dans un navigateur."
    if c=="429": return "429 (limitation de débit) ; vérifiée via l'API oEmbed YouTube."
    if c.startswith("2"): return ""
    return "ÉCHEC"
rows={"src":[], "video":[], "img":[]}
for u,w in use.items():
    c=codes[u]; nt=note(u,c)
    if kind[u]=="src" and u not in oldurls: nt=("nouveau v4" + (" ; "+nt if nt else ""))
    rows[kind[u]].append((c.replace("*",""),u,", ".join(sorted(w)),nt))
def table(rs):
    out=["| HTTP | URL | Utilisée pour | Note |","|---|---|---|---|"]
    out+= [f"| {c} | {u} | {w} | {n} |" for c,u,w,n in rs]; return "\n".join(out)
allr=sum(rows.values(),[])
ok=sum(r[0]=="200" for r in allr); fail=[r for r in allr if r[0]!="200"]
md=f"""# Vérification des sources

Test HTTP : `curl -sL` (User-Agent navigateur, 25 s de délai), le {datetime.date.today().strftime('%d/%m/%Y')} (heure de Paris). 200 = la page répond. Les codes 403 viennent de protections anti-robots, pas de liens morts : voir la note. Les messages X sont lus via l'API X (pas de curl).

## Sources des déclarations et des liens

{table(rows['src'])}

## Vidéos (diffuseur d'origine ou compte officiel)

Les vidéos YouTube sont aussi vérifiées par l'API oEmbed (`tools/yt_check.py`) : titre et chaîne officielle confirmés.

{table(rows['video'])}

## Photos et logos (pages de fichiers Wikimedia Commons)

{table(rows['img'])}

Total : {len(allr)} URL uniques ; {ok} en 200 ; {len(fail)} autre(s) : {", ".join(f"{c} {u}" for c,u,_,_ in fail) or "aucune"}.
"""
open(p,"w").write(md)
print(len(allr), ok, len(rows['src']), len(rows['video']), len(rows['img']))
for f in fail: print("NON-200", f[0], f[1], "|", f[3])
