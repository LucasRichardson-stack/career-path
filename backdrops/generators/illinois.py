import math, random
random.seed(21)
G=970
LAYERS=[]
def add(kind,d): LAYERS.append((kind,d))
def circ(cx,cy,r): return f"M{cx-r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0"
def poly(pts,close=True): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")
def rarch(x1,x2,spring,bottom,close=True):
    """round (Romanesque) arch opening"""
    r=(x2-x1)/2
    return f"M{x1} {bottom}V{spring}A{r} {r} 0 0 1 {x2} {spring}V{bottom}"+("Z" if close else "")
def voussoirs(cx,spring,r1,r2,n):
    d=f"M{cx-r2} {spring}A{r2} {r2} 0 0 1 {cx+r2} {spring}"
    for i in range(n+1):
        a=math.pi*i/n
        d+=f"M{cx-r1*math.cos(a):.1f} {spring-r1*math.sin(a):.1f}L{cx-r2*math.cos(a):.1f} {spring-r2*math.sin(a):.1f}"
    return d
def ashlar(x0,x1,y0,y1,step=9,dens=.55):
    d=""
    for y in range(int(y0)+step//2,int(y1),step):
        x=x0+random.uniform(0,10)
        while x<x1-6:
            w=random.uniform(10,22)
            if random.random()<dens: d+=f"M{x:.1f} {y}h{min(w,x1-x):.1f}"
            x+=w+random.uniform(3,8)
    return d

# ---------------- main block (behind the tower's right edge) ----------------
BX0,BX1=184,362
EAVE=722; APEX=(272,664)
add('occ',poly([(BX0,G),(BX0,EAVE),(APEX[0],APEX[1]),(BX1,EAVE),(BX1,G)]))
add('line',f"M{BX0-4} {EAVE+3}L{APEX[0]} {APEX[1]-4}L{BX1+4} {EAVE+3}")          # coping
add('line',f"M{APEX[0]} {APEX[1]-4}v-8"); add('line',circ(APEX[0],APEX[1]-15,3))
# gable: row of slim arched windows
for i,x in enumerate(range(240,306,13)):
    h=24 if i in (1,2,3) else 16
    add('line',rarch(x,x+7,EAVE-h+4,EAVE+10))
add('line',f"M{BX0} {EAVE+14}H{BX1}")                                               # string course
# three big arched windows, centre one taller, each with a hood of voussoirs
for cx,w,top in ((222,30,770),(272,34,764),(322,30,770)):
    add('occ',rarch(cx-w/2,cx+w/2,top,820))
    add('thin',voussoirs(cx,top,w/2+1,w/2+8,9))
    add('thin',f"M{cx} {top-w/2+2}V820M{cx-w/2} {top+14}H{cx+w/2}")
    add('thin',rarch(cx-w/2+4,cx-2,top+18,814,False)+rarch(cx+2,cx+w/2-4,top+18,814,False))
add('line',f"M{BX0} 826H{BX1}M{BX0} 831H{BX1}")                                   # sill band
# grand entrance: deep round arch with a wide ring of voussoirs, double doors, steps
EX=272; ESP=896
add('occ',voussoirs(EX,ESP,28,62,17)+f"M{EX-62} {ESP}V946M{EX+62} {ESP}V946")
add('occ',rarch(EX-28,EX+28,ESP,946))
add('thin',rarch(EX-22,EX+22,ESP+4,946,False)+f"M{EX} {ESP-18}V946M{EX-22} {ESP+10}H{EX+22}")
add('thin',f"M{EX-18} 878q18 -14 36 0")                                            # fanlight
for k,y in enumerate((946,954,962)):
    add('line',f"M{EX-48-k*6} {y}H{EX+48+k*6}V{y+8}")
add('line',f"M{EX-70} 970V946M{EX+70} 970V946")
# rusticated stone
add('thin',ashlar(BX0+4,BX1-4,738,760)+ashlar(BX0+4,BX0+40,836,944)+ashlar(BX1-40,BX1-4,836,944)+ashlar(BX0+60,BX1-60,836,856))

# ---------------- right corner turret with a conical roof ----------------
TX0,TX1=360,446
add('occ',poly([(TX0,G),(TX0,724),(TX1,724),(TX1,G)]))
add('occ',f"M{TX0-8} 726L{(TX0+TX1)/2} 662L{TX1+8} 726Q{(TX0+TX1)/2} 732 {TX0-8} 726Z")
for t in (.25,.5,.75): add('thin',f"M{TX0-8+(TX1-TX0+16)*t:.1f} 727L{(TX0+TX1)/2} 662")
add('line',f"M{(TX0+TX1)/2} 662v-8")
add('line',f"M{TX0} 740H{TX1}M{TX0} 826H{TX1}")
for cx in (384,422):
    add('occ',rarch(cx-9,cx+9,770,816)); add('thin',voussoirs(cx,770,10,15,7))
add('occ',rarch(394,414,890,940)); add('thin',voussoirs(404,890,11,17,7))
add('thin',ashlar(TX0+4,TX1-4,744,764)+ashlar(TX0+4,TX1-4,840,880))

# ---------------- bell tower (left) ----------------
T0,T1=56,190; TC=(T0+T1)/2
TB=584                       # top of the tower walls (base of the roof)
add('occ',poly([(T0,G),(T0,TB),(T1,TB),(T1,G)]))
# corner turrets running full height, each ending in a small pinnacle
for x in (T0-6,T1-14):
    add('occ',poly([(x,G),(x,TB-14),(x+20,TB-14),(x+20,G)]))
    add('thin',"".join(f"M{x} {y}h20" for y in range(TB,G,26)))
    add('occ',poly([(x-2,TB-14),(x+22,TB-14),(x+18,TB-22),(x+2,TB-22)]))
    add('occ',f"M{x+1} {TB-22}L{x+10} {TB-62}L{x+19} {TB-22}Z")
    add('line',f"M{x+10} {TB-62}v-6")
# steep pyramidal tile roof with a centre pinnacle in front
RA=(TC,506)
add('occ',f"M{T0+12} {TB}L{RA[0]} {RA[1]}L{T1-12} {TB}Z")
tiles=""
for y in range(RA[1]+14,TB,10):
    t=(y-RA[1])/(TB-RA[1]); hw=(T1-T0-24)/2*t
    tiles+=f"M{TC-hw:.1f} {y}H{TC+hw:.1f}"
add('thin',tiles+f"M{TC} {RA[1]}V{TB}")
add('line',f"M{RA[0]} {RA[1]}v-10"); add('line',circ(RA[0],RA[1]-13,2.5))
add('occ',poly([(TC-8,TB),(TC-8,TB-30),(TC+8,TB-30),(TC+8,TB)]))
add('occ',f"M{TC-8} {TB-30}L{TC} {TB-58}L{TC+8} {TB-30}Z")
# corbel table + belfry arcade of small round arches
add('line',f"M{T0} {TB+6}H{T1}")
add('thin',"".join(f"M{x} {TB+6}v5" for x in range(T0+4,T1,8)))
for x in range(T0+18,T1-24,16):
    add('occ',rarch(x,x+10,TB+24,TB+44))
add('line',f"M{T0} {TB+50}H{T1}")
# tall belfry lancets: three bays of paired round-headed openings with colonnettes
for bx in (T0+14,TC-17,T1-48):
    add('occ',rarch(bx,bx+34,TB+76,TB+214))
    add('thin',rarch(bx+3,bx+15,TB+86,TB+210,False)+rarch(bx+19,bx+31,TB+86,TB+210,False)+f"M{bx+17} {TB+66}V{TB+214}")
    add('thin',"".join(f"M{bx+3} {y}h12M{bx+19} {y}h12" for y in range(TB+104,TB+210,14)))
add('line',f"M{T0} {TB+222}H{T1}")
# lower shaft: two small windows and ashlar
for y in (TB+250,TB+300):
    add('occ',rarch(TC-7,TC+7,y,y+26))
add('thin',ashlar(T0+4,T1-4,TB+228,G-6,10,.5))

# ---------------- trees and shrubs in front (filled, so they hide the stone) ----------------
def canopy(cx,cy,rx,ry,n=14,j=.18):
    d=""
    for i in range(n+1):
        a=math.pi*2*i/n; f=1-j+j*2*random.random()
        x=cx+rx*f*math.cos(a); y=cy+ry*f*math.sin(a)
        if i==0: d=f"M{x:.1f} {y:.1f}"
        else:
            am=math.pi*2*(i-.5)/n
            d+=f"Q{cx+rx*1.2*math.cos(am):.1f} {cy+ry*1.2*math.sin(am):.1f} {x:.1f} {y:.1f}"
    return d+"Z"
def texture(blobs):
    t=""
    for (bx,by,rx,ry) in blobs:
        for _ in range(int(rx*ry/230)):
            a=random.uniform(0,6.28); r=random.uniform(.15,.78)
            x=bx+rx*r*math.cos(a); y=by+ry*r*math.sin(a); t+=f"M{x:.1f} {y:.1f}q4 -5 9 0"
    return t
def tree(trunk,blobs):
    add('line',trunk)
    for b in blobs: add('occ',canopy(*b))
    add('thin',texture(blobs))
tree("M78 970L84 900M84 920l-18 -22M84 930l20 -14",
     [(70,850,62,70),(30,900,36,48),(118,880,40,44),(84,790,44,40)])
tree("M470 970V900M470 920l-14 -16",[(472,820,40,58),(486,890,26,36),(440,872,26,30)])
for cx,w in ((228,22),(318,20),(196,14)):
    add('occ',canopy(cx,G-12,w,12,10,.12))

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
out+=f'<path stroke-width="1.6" d="M0 {G}H500"/>'
for kind,d in LAYERS:
    if not d: continue
    if kind=='occ': out+=f'<path class="occ" stroke-width="1.6" d="{d}"/>'
    elif kind=='line': out+=f'<path stroke-width="1.6" d="{d}"/>'
    elif kind=='thin': out+=f'<path stroke-width="1" opacity=".6" d="{d}"/>'
out+='</svg>'
open('altgeld.svg','w').write(out); print(len(out))
