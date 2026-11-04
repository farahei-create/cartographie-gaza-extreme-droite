import sys,re,json,urllib.request,urllib.parse
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36","Accept-Language":"fr-FR,fr;q=0.9"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read().decode("utf-8","replace")
for q in sys.argv[1:]:
    h=get("https://www.youtube.com/results?search_query="+urllib.parse.quote(q)+"&hl=fr&gl=FR")
    m=re.search(r"var ytInitialData = (\{.*?\});</script>",h)
    print("==",q)
    if not m: print("  no data"); continue
    d=json.loads(m.group(1)); n=0
    def walk(o):
        global n
        if isinstance(o,dict):
            if "videoRenderer" in o:
                v=o["videoRenderer"]; t="".join(r.get("text","") for r in v.get("title",{}).get("runs",[]))
                ch="".join(r.get("text","") for r in v.get("ownerText",{}).get("runs",[]))
                pt=v.get("publishedTimeText",{}).get("simpleText",""); ln=v.get("lengthText",{}).get("simpleText","")
                if n<8: print(f"  {v['videoId']} | {ch} | {t} | {pt} | {ln}")
                n+=1
            for x in o.values(): walk(x)
        elif isinstance(o,list):
            for x in o: walk(x)
    walk(d)
