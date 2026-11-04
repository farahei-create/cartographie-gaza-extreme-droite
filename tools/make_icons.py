"""Icônes PWA : dégradé violet profond -> violet, glyphe « réseau » blanc (nœuds + liens)."""
from PIL import Image, ImageDraw
import os
OUT="/workspace/gaza-site/site/icons"
C1=(59,10,87); C2=(123,44,191); PINK=(240,98,146)
def grad(S):
    im=Image.new("RGB",(S,S))
    px=im.load()
    for y in range(S):
        for x in range(S):
            t=(x+y)/(2*S-2)
            px[x,y]=tuple(int(C1[i]+(C2[i]-C1[i])*t) for i in range(3))
    return im
NODES=[(.50,.30),(.27,.55),(.73,.55),(.40,.76),(.66,.80),(.50,.56)]
LINKS=[(0,5),(1,5),(2,5),(3,5),(4,5),(0,1),(0,2),(1,3),(2,4),(3,4)]
def draw(S, scale):
    im=grad(S*4); d=ImageDraw.Draw(im); W=S*4
    def P(p): return (W/2+(p[0]-.5)*W*scale, W/2+(p[1]-.53)*W*scale)
    lw=int(W*0.022*scale/0.8)
    for a,b in LINKS: d.line([P(NODES[a]),P(NODES[b])], fill=(255,255,255,), width=lw)
    for i,p in enumerate(NODES):
        r=W*(0.085 if i==5 else 0.06)*scale/0.8; x,y=P(p)
        d.ellipse([x-r,y-r,x+r,y+r], fill=PINK if i==5 else (255,255,255))
        if i==5:
            r2=r*0.45; d.ellipse([x-r2,y-r2,x+r2,y+r2], fill=(255,255,255))
    return im.resize((S,S), Image.LANCZOS)
draw(180,1.0).save(f"{OUT}/apple-touch-icon.png", optimize=True)
draw(192,1.0).save(f"{OUT}/icon-192.png", optimize=True)
draw(512,1.0).save(f"{OUT}/icon-512.png", optimize=True)
draw(512,0.74).save(f"{OUT}/icon-maskable-512.png", optimize=True)
draw(192,0.74).save(f"{OUT}/icon-maskable-192.png", optimize=True)
im=draw(64,1.15); im.save(f"{OUT}/favicon-64.png", optimize=True)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f"{OUT}/{f}"))
