import sys,re,json,urllib.request,urllib.parse
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36","Accept-Language":"fr-FR,fr;q=0.9"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30)
for vid in sys.argv[1:]:
    u="https://www.youtube.com/watch?v="+vid
    try:
        r=get("https://www.youtube.com/oembed?format=json&url="+urllib.parse.quote(u)); o=json.loads(r.read()); st=r.status
    except Exception as e: print(vid,"oembed FAIL",e); continue
    import time; time.sleep(4)
    try: h=get(u).read().decode("utf-8","replace")
    except Exception as e: h=""; print("  (watch page unavailable:",e,")")
    up=re.search(r'"uploadDate":"([^"]+)"',h) or re.search(r'"publishDate":"([^"]+)"',h)
    desc=re.search(r'"shortDescription":"(.*?)","',h)
    print(f"{vid} | {st} | {o['author_name']} | {o['author_url']} | {o['title']} | {up.group(1) if up else '?'} | {(desc.group(1)[:160] if desc else '')}")
