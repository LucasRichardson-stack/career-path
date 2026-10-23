import math, random
random.seed(7)
W=500; G=970
P=[]; F=[]; OCC=[]   # OCC: (outline_d, detail_list) drawn later, filled with bg
def L(x1,y1,x2,y2,f=False): (F if f else P).append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
def path(d,f=False): (F if f else P).append(d)

# --- Ala-Too range behind everything ---
ridge=[(0,700),(40,660),(70,672),(110,610),(140,630),(175,575),(205,600),(240,548),
       (268,566),(300,520),(330,560),(352,548),(390,600),(420,585),(455,630),(500,610)]
path("M"+"L".join(f"{x} {y}" for x,y in ridge))
# snow caps: follow each slope down, close with a ragged melt line
def slope_x(i,dir,y):
    (x0,y0)=ridge[i]; (x1,y1)=ridge[i+dir]
    t=(y-y0)/(y1-y0); return x0+(x1-x0)*min(t,1)
for i in (5,7,9,11):
    px,py=ridge[i]; dep=26 if i!=9 else 34
    xl=slope_x(i,-1,py+dep); xr=slope_x(i,1,py+dep)
    d=f"M{xl:.1f} {py+dep}"
    n=6
    for k in range(1,n):
        x=xl+(xr-xl)*k/n; y=py+dep+(9 if k%2 else -4)
        d+=f"L{x:.1f} {y:.1f}"
    d+=f"L{xr:.1f} {py+dep}"
    path(d,True)
    # a couple of short couloirs below the snow
    for k in (-.3,.25):
        x=px+(xr-xl)*k; path(f"M{x:.1f} {py+dep+12}q{k*20:.1f} 18 {k*30:.1f} 34",True)
# second, nearer ridge (foothills)
path("M0 790Q60 740 130 770T260 760T380 750T500 770",True)
path("M0 860Q90 820 180 842T340 830T500 850",True)

# --- yurt (boz üy) ---
cx=310; wl,wr=196,424; wt,wb=872,966
outline=(f"M{wl} {wb}V{wt}Q{wl+22} {wt-34} {cx-28} {792}"
         f"L{cx+28} 792Q{wr-22} {wt-34} {wr} {wt}V{wb}Z")
det=[]
# roof ribs (uuk) from crown to wall top
for i in range(1,12):
    t=i/12
    x2=wl+(wr-wl)*t; x1=cx-28+56*t
    det.append(f"M{x1:.1f} 794Q{(x1+x2)/2:.1f} {wt-24:.1f} {x2:.1f} {wt-2}")
# roof band with ram's-horn (kochkor muyuz) scrolls
det.append(f"M{wl} {wt}H{wr}M{wl} {wt+12}H{wr}")
for x in range(wl+12,wr-6,24):
    det.append(f"M{x-8} {wt+9}q0 -6 5 -6q4 0 3 4M{x+8} {wt+9}q0 -6 -5 -6q-4 0 -3 4")
# crown ring (tündük) with crossed bars
det.append(f"M{cx-28} 792Q{cx} 782 {cx+28} 792")
det.append(f"M{cx-20} 789L{cx+20} 789M{cx-10} 785L{cx-6} 792M{cx+10} 785L{cx+6} 792")
det.append(f"M{cx-6} 783V776M{cx+6} 783V776M{cx-9} 776H{cx+9}")
# felt seams on roof
det.append(f"M{wl+40} {wt-30}Q{cx} {wt-50} {wr-40} {wt-30}")
# lattice wall (kerege)
for x in range(wl-60,wr+20,16):
    det.append(f"M{max(x,wl)} {wt+12+(max(x,wl)-x)}L{min(x+60,wr)} {min(wb,wt+12+min(x+60,wr)-x)}")
    det.append(f"M{min(x+60,wr)} {wt+12+(x+60-min(x+60,wr))}L{max(x,wl)} {min(wb,wt+12+(x+60-max(x,wl)))}")
door=f"M{cx-20} {wb}V{wt+20}H{cx+20}V{wb}"
OCC.append((outline,det,[door,f"M{cx-24} {wt+16}H{cx+24}V{wb}M{cx-24} {wt+16}V{wb}",
                         f"M{cx-12} {wt+34}q-6 0 -6 6q0 6 6 6M{cx+12} {wt+34}q6 0 6 6q0 6 -6 6M{cx} {wt+28}v24"]))

# --- poplars (tall village windbreak) on the left, in front of the hills ---
def poplar(x,top,w):
    h=G-12-top
    d=f"M{x} {top}"
    pts=[]
    for i in range(1,13):
        t=i/12; y=top+h*t
        ww=w*(math.sin(math.pi*min(t*1.6,1)/2)**.8 if t<.62 else 1-((t-.62)/.38)**1.6*.7)*(1+random.uniform(-.12,.12))
        pts.append((x+ww,y))
    for px,py in pts: d+=f"L{px:.1f} {py:.1f}"
    for px,py in reversed(pts): d+=f"L{2*x-px+random.uniform(-2,2):.1f} {py:.1f}"
    d+="Z"
    tex=[f"M{x} {G}V{G-14}"]
    for _ in range(int(h/9)):
        y=random.uniform(top+14,G-30); ww=w*.55
        xx=x+random.uniform(-ww,ww)
        tex.append(f"M{xx:.1f} {y:.1f}q3 -5 6 0")
    return (d,tex,[])
for x,top,w in [(48,470,20),(92,430,24),(136,500,20),(168,560,17)]:
    OCC.append(poplar(x,top,w))

# ground and grass
L(0,G,500,G); L(20,G+8,480,G+8,True)
for x in range(14,490,22):
    if 196<x<404: continue
    path(f"M{x} {G}l-3 -8M{x} {G}l1 -10M{x} {G}l4 -7",True)
# path to the door
path(f"M{cx-20} {G}Q{cx-30} {G+10} {cx-60} {G+18}M{cx+20} {G}Q{cx+30} {G+10} {cx+70} {G+18}",True)

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
out+=f'<path stroke-width="1.6" d="{"".join(P)}"/><path stroke-width="1" opacity=".6" d="{"".join(F)}"/>'
for d,det,bold in OCC:
    out+=f'<path class="occ" stroke-width="1.6" d="{d}"/>'
    if det: out+=f'<path stroke-width="1" opacity=".6" d="{"".join(det)}"/>'
    if bold: out+=f'<path stroke-width="1.6" class="occ" d="{"".join(bold)}"/>'
out+='</svg>'
open('peacecorps.svg','w').write(out); print(len(out))
