import math, random
random.seed(17)
G=970
LAYERS=[]
def add(kind,d): LAYERS.append((kind,d))
def circ(cx,cy,r): return f"M{cx-r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0"
def poly(pts,close=True): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")
def rrect(x,y,w,h,r): return f"M{x+r} {y}H{x+w-r}Q{x+w} {y} {x+w} {y+r}V{y+h-r}Q{x+w} {y+h} {x+w-r} {y+h}H{x+r}Q{x} {y+h} {x} {y+h-r}V{y+r}Q{x} {y} {x+r} {y}Z"
def tf(pts,cx,cy,deg,s=1):
    a=math.radians(deg); c,si=math.cos(a),math.sin(a)
    return [(cx+(x*c-y*si)*s, cy+(x*si+y*c)*s) for x,y in pts]

# ---------------- wire bin (slight oblique so the open top shows) ----------------
FX0,FX1,FT,FB=46,300,848,950       # front face
DX,DY=28,-22                       # depth offset to the back edge
BX0,BX1,BT=FX0+DX,FX1+DX,FT+DY

# back + right inner faces (mesh seen through the parts)
add('thin',"".join(f"M{x} {BT}V{FB+DY}" for x in range(BX0,BX1+1,14)))
add('thin',"".join(f"M{BX0} {y}H{BX1}" for y in range(BT,FB+DY+1,14)))

# ---------------- randomised parts filling the bin ----------------
SHAPES=[
 [(0,0),(20,0),(20,6),(6,6),(6,16),(0,16)],                         # L bracket
 [(0,0),(22,0),(22,6),(14,6),(14,15),(8,15),(8,6),(0,6)],           # T bracket
 [(0,0),(24,0),(24,8),(0,8)],                                       # flat bar
 [(0,0),(16,0),(19,5),(16,10),(0,10),(-3,5)],                       # hex stock
]
def part(cx,cy,deg,s,kind=None):
    k=random.randrange(5) if kind is None else kind
    if k<4:
        pts=SHAPES[k]; mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
        P=tf([(x-mx,y-my) for x,y in pts],cx,cy,deg,s)
        det=""
        if k==2:
            for hx in (-7,7):
                q=tf([(hx,0)],cx,cy,deg,s)[0]; det+=circ(q[0],q[1],1.8*s)
        return poly(P),det
    r=7*s
    return circ(cx,cy,r), circ(cx,cy,r*.45)                         # washer / ring
random.seed(17)
parts=[]
# deep layers, seen through the front mesh
for _ in range(85):
    x=random.uniform(FX0+8,BX1-8); y=random.uniform(BT+8,FB-8)
    if x>FX1 and y>FB+DY-4: continue
    parts.append((y,x))
# heap on top, bulging a little above the rim in the middle
for _ in range(46):
    x=random.uniform(FX0+12,BX1-12)
    t=(x-FX0)/(BX1-FX0); bulge=14*math.sin(math.pi*t)
    y=random.uniform(BT-bulge+4,FT)
    parts.append((y,x))
parts.sort()
for y,x in parts:
    d,det=part(x,y,random.uniform(0,360),random.uniform(.85,1.2))
    add('part',d)
    if det: add('partd',det)

# the part the vision system picked: drawn bold, boxed, with its pose axes
PK=(204,818)
pd,_=part(PK[0],PK[1],-18,1.25,kind=0)
add('occ',pd); add('line',pd)

# front + right mesh over the parts, rims and casters
add('thin',"".join(f"M{x} {FT}V{FB}" for x in range(FX0,FX1+1,14)))
add('thin',"".join(f"M{FX0} {y}H{FX1}" for y in range(FT,FB+1,14)))
for i in range(0,DX+1,14):
    pass
side=""
for k in range(0,9):
    t=k/8; side+=f"M{FX1+DX*t:.1f} {FT+DY*t:.1f}V{FB+DY*t:.1f}"
for y in range(FT,FB+1,14): side+=f"M{FX1} {y}L{FX1+DX} {y+DY}"
add('thin',side)
add('line',poly([(FX0,FT),(FX1,FT),(FX1,FB),(FX0,FB)])+f"M{FX0} {FT}L{BX0} {BT}H{BX1}L{FX1} {FT}M{BX1} {BT}V{FB+DY}L{FX1} {FB}")
# heavy top rail (tube), corner posts, steel skid, swivel casters
add('line',f"M{FX0} {FT-2}H{FX1}M{FX0} {FT+2}H{FX1}M{BX0} {BT-2}H{BX1}M{FX1} {FT-2}L{BX1} {BT-2}M{FX0} {FT-2}L{BX0} {BT-2}")
for x in (FX0,FX1): add('occ',rrect(x-3,FT-3,6,FB-FT+6,1))
add('occ',f"M{BX1-3} {BT-3}h6V{FB+DY}h-6Z")
add('thin',"".join(f"M{FX0+60*i} {FT}V{FB}" for i in (1,2,3)))
add('occ',rrect(FX0-6,FB+2,FX1-FX0+12,8,1)); add('thin',f"M{FX0-6} {FB+6}H{FX1+6}")
add('occ',poly([(FX1+6,FB+2),(FX1+6+DX*.6,FB+2+DY*.6),(FX1+6+DX*.6,FB+10+DY*.6),(FX1+6,FB+10)]))
for x in (FX0+14,FX1-14):
    add('occ',poly([(x-6,FB+10),(x+6,FB+10),(x+4,FB+15),(x-4,FB+15)]))
    add('occ',circ(x+2,G-5,5)); add('thin',circ(x+2,G-5,1.6))
add('thin',f"M{FX0-10} {G+5}H{FX1+DX}")                                     # floor shadow

# ---------------- overhead camera mount ----------------
CX=PK[0]-14
PX0,PX1=12,24
add('occ',rrect(4,960,28,10,1)); add('thin',"".join(circ(x,965,1.4) for x in (9,27)))       # base plate + bolts
add('occ',rrect(PX0,596,PX1-PX0,364,1)); add('thin',f"M{PX0+3} 600V958")                    # post (square tube)
add('occ',rrect(PX0-2,586,CX+10,12,1)); add('thin',f"M{PX0} 590H{CX+6}")                    # boom
add('occ',rrect(CX+6,584,6,16,1))                                                            # end cap
add('occ',poly([(PX1,598),(PX1+34,598),(PX1,632)])); add('thin',circ(PX1+8,606,1.4)+circ(PX1+20,606,1.4)+circ(PX1+8,618,1.4))   # gusset
add('occ',rrect(CX-16,598,32,6,1)); add('thin',circ(CX-11,601,1)+circ(CX+11,601,1))         # camera mount plate
add('line',f"M{CX-6} 604v4M{CX+6} 604v4")
# cable: camera -> along the boom -> down the post (clipped every so often)
cab=f"M{CX+30} 612Q{CX+40} 600 {CX+20} 584L{PX1+12} 584Q{PX1+4} 584 {PX1+3} 600L{PX1+3} 940Q{PX1+3} 960 {PX1+20} 966"
add('thin',cab+"".join(f"M{x} 581v6" for x in range(60,int(CX),36))+"".join(f"M{PX1} {y}h6" for y in range(640,940,60)))
# Apera Vue-style stereo camera: long chamfered bar, APERA wordmark on the side,
# a big black lens barrel at each end pointing down, cooling ribs on the underside between them
add('occ',f"M{CX-50} 606L{CX-46} 602H{CX+46}L{CX+50} 606V624L{CX+47} 627H{CX-47}L{CX-50} 624Z")   # bar housing
add('thin',f"M{CX-46} 602L{CX-48} 608H{CX+48}L{CX+46} 602")                                       # top chamfer
add('thin',"".join(circ(CX+dx,605,.9) for dx in (-44,44)))                                        # screws
add('text',f'<text x="{CX}" y="620" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="9" font-weight="700" letter-spacing="3.2" fill="currentColor" stroke="none">ΛPERΛ</text>')
add('thin',"".join(f"M{x} 627v5" for x in range(int(CX-20),int(CX+21),4)))                       # underside ribs
add('thin',f"M{CX-22} 632H{CX+22}")
for dx in (-36,36):
    add('occ',rrect(CX+dx-12,620,24,24,3))                                # lens barrel
    add('thin',f"M{CX+dx-12} 630h24M{CX+dx-12} 634h24M{CX+dx-12} 637h24") # focus rings
    add('occ',f"M{CX+dx-11} 644a11 3.4 0 1 0 22 0a11 3.4 0 1 0 -22 0Z")    # front glass
    add('thin',f"M{CX+dx-6} 644a6 1.8 0 1 0 12 0a6 1.8 0 1 0 -12 0Z")
add('occ',rrect(CX+50,610,6,9,1))                                         # cable gland
CAM=(CX,646)
# ---- what the camera sees: dotted view frustum to the bin opening ----
RAYS=""
for lx in (CX-36,CX+36):
    for x,y in ((FX0,FT),(FX1,FT)):
        RAYS+=f"M{lx} 647L{x} {y}"
add('ray',RAYS)
# ---------------- 6-axis robot on a riser, gripper closing on the chosen part ----------------
def smooth(pts,close=True,t=.5):
    P=list(pts); P=([P[-1]]+P+[P[0],P[1]]) if close else ([P[0]]+P+[P[-1]])
    d=f"M{P[1][0]:.1f} {P[1][1]:.1f}"
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        c1=(p1[0]+(p2[0]-p0[0])*t/3,p1[1]+(p2[1]-p0[1])*t/3); c2=(p2[0]-(p3[0]-p1[0])*t/3,p2[1]-(p3[1]-p1[1])*t/3)
        d+=f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d+("Z" if close else "")
def link(a,b,r1,r2):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); n=(-math.sin(ang),math.cos(ang))
    p=[(a[0]+n[0]*r1,a[1]+n[1]*r1),(b[0]+n[0]*r2,b[1]+n[1]*r2),(b[0]-n[0]*r2,b[1]-n[1]*r2),(a[0]-n[0]*r1,a[1]-n[1]*r1)]
    return (f"M{p[0][0]:.1f} {p[0][1]:.1f}L{p[1][0]:.1f} {p[1][1]:.1f}A{r2} {r2} 0 0 0 {p[2][0]:.1f} {p[2][1]:.1f}"
            f"L{p[3][0]:.1f} {p[3][1]:.1f}A{r1} {r1} 0 0 0 {p[0][0]:.1f} {p[0][1]:.1f}Z")
RX=444
add('occ',rrect(RX-32,962,64,8,1)); add('thin',"".join(circ(x,966,1.3) for x in (RX-26,RX+26)))
add('occ',rrect(RX-24,900,48,62,2)); add('thin',f"M{RX-24} 912H{RX+24}M{RX-14} 928h28v18h-28z")          # riser
add('occ',smooth([(RX-30,900),(RX-28,884),(RX+28,884),(RX+30,900)],t=.1)); add('thin',f"M{RX-28} 892H{RX+28}")   # J1 base
add('occ',smooth([(RX-22,884),(RX-20,862),(RX+22,862),(RX+24,884)],t=.2))                                       # turret
add('occ',rrect(RX+18,866,16,20,3)); add('thin',f"M{RX+18} 872h16")                                             # J1 motor
J2=(RX-2,856); J3=(RX+6,738); WR=(PK[0]+24,PK[1]-80)
add('occ',link(J2,J3,25,19))                                                                                    # lower arm
add('thin',smooth([(J2[0]-10,J2[1]-20),(J2[0]-4,(J2[1]+J3[1])/2),(J3[0]-6,J3[1]+20)],close=False))
add('occ',circ(*J2,28)); add('thin',circ(*J2,20)); add('line',circ(*J2,7))
add('thin',''.join(circ(J2[0]+24*math.cos(k*math.pi/4),J2[1]+24*math.sin(k*math.pi/4),1.1) for k in range(8)))
add('occ',rrect(J2[0]+18,J2[1]-11,18,22,3)); add('thin',f"M{J2[0]+24} {J2[1]-11}v22")   # J2 motor
# counterbalance cylinder from the turret to the lower arm
CB0=(RX-26,876); CB1=(J2[0]-14,(J2[1]+J3[1])/2+6)
add('occ',link(CB0,(CB0[0]+(CB1[0]-CB0[0])*.55,CB0[1]+(CB1[1]-CB0[1])*.55),7,7))
add('line',f"M{CB0[0]+(CB1[0]-CB0[0])*.55:.1f} {CB0[1]+(CB1[1]-CB0[1])*.55:.1f}L{CB1[0]:.1f} {CB1[1]:.1f}")
add('occ',circ(*CB1,4)); add('occ',circ(*CB0,5))
# forearm: J3 housing with rear motor, roll seam, slim wrist
add('occ',rrect(J3[0]+14,J3[1]-16,26,26,4)); add('thin',f"M{J3[0]+22} {J3[1]-16}v26")                          # J3/J4 motors behind
add('occ',link(J3,WR,17,9))
ang=math.atan2(WR[1]-J3[1],WR[0]-J3[0]); n=(-math.sin(ang),math.cos(ang))
for t,r in ((.33,14.5),(.36,14.3)):
    x,y=J3[0]+(WR[0]-J3[0])*t,J3[1]+(WR[1]-J3[1])*t
    add('line' if t==.33 else 'thin',f"M{x+n[0]*r:.1f} {y+n[1]*r:.1f}L{x-n[0]*r:.1f} {y-n[1]*r:.1f}")
add('occ',circ(*J3,22)); add('thin',circ(*J3,15)); add('line',circ(*J3,5))
add('thin',''.join(circ(J3[0]+18.5*math.cos(k*math.pi/4),J3[1]+18.5*math.sin(k*math.pi/4),1) for k in range(8)))
add('occ',circ(*WR,10)); add('thin',circ(*WR,4))                                                                # J5
# J6 flange + gripper body pointing straight down; fingers either side of the part
GB=(PK[0]+2,PK[1]-46)
add('occ',link(WR,(GB[0],GB[1]-10),7,6))
add('occ',rrect(GB[0]-15,GB[1]-10,30,12,2)); add('thin',f"M{GB[0]-15} {GB[1]-5}h30")
add('occ',rrect(GB[0]-20,GB[1]+2,40,5,1))
add('occ',poly([(GB[0]-20,GB[1]+7),(GB[0]-15,GB[1]+7),(GB[0]-15,GB[1]+22),(GB[0]-17,GB[1]+26),(GB[0]-20,GB[1]+24)]))
add('occ',poly([(GB[0]+20,GB[1]+7),(GB[0]+15,GB[1]+7),(GB[0]+15,GB[1]+22),(GB[0]+17,GB[1]+26),(GB[0]+20,GB[1]+24)]))
add('thin',f"M{GB[0]-8} {GB[1]+8}l-4 0l2 -2M{GB[0]+8} {GB[1]+8}l4 0l-2 -2")   # opening arrows
# dress-pack hose along the arm
add('thin',smooth([(J2[0]+20,J2[1]-30),(J3[0]+30,J3[1]+30),(J3[0]+20,J3[1]-24),((J3[0]+WR[0])/2,J3[1]-14),(WR[0]+10,WR[1]-14)],close=False))
add('thin',f"M{RX-34} {G+5}H{RX+34}")

# ---- detection overlay on the chosen part: corner brackets, centre mark, pose axes ----
x0,y0,x1,y1=PK[0]-19,PK[1]-17,PK[0]+19,PK[1]+17
br=""
for (x,y,sx,sy) in ((x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)):
    br+=f"M{x} {y+7*sy}V{y}H{x+7*sx}"
add('mark',br)
ax=f"M{PK[0]} {PK[1]}l12 -4l-3 -1M{PK[0]+12} {PK[1]-4}l-2 3"                   # x
ax+=f"M{PK[0]} {PK[1]}l-4 -12l-1 3M{PK[0]-4} {PK[1]-12}l2 2"                 # z
ax+=f"M{PK[0]} {PK[1]}l-9 5"                                               # y
add('mark',ax+circ(PK[0],PK[1],2.2))
add('ray',f"M{CX-36} 647L{PK[0]} {PK[1]}M{CX+36} 647L{PK[0]} {PK[1]}")


out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
clip=poly([(FX0,FB),(FX0,FT),(BX0,BT-24),(BX1,BT-24),(BX1,FB+DY),(FX1,FB)])
out+=f'<defs><clipPath id="aperaBin"><path d="{clip}"/></clipPath></defs>'
out+=f'<path stroke-width="1.6" d="M0 {G}H500"/>'
ingroup=False
for kind,d in LAYERS:
    if not d: continue
    if kind in ('part','partd') and not ingroup: out+='<g clip-path="url(#aperaBin)">'; ingroup=True
    if kind not in ('part','partd') and ingroup: out+='</g>'; ingroup=False
    if kind=='part': out+=f'<path class="occ" stroke-width="1" d="{d}"/>'
    elif kind=='partd': out+=f'<path stroke-width=".8" opacity=".55" d="{d}"/>'
    elif kind=='occ': out+=f'<path class="occ" stroke-width="1.3" d="{d}"/>'
    elif kind=='line': out+=f'<path stroke-width="1.6" d="{d}"/>'
    elif kind=='thin': out+=f'<path stroke-width=".9" opacity=".55" d="{d}"/>'
    elif kind=='ray': out+=f'<path stroke-width="1" stroke-dasharray="2 5" d="{d}"/>'
    elif kind=='text': out+=d
    elif kind=='mark': out+=f'<path stroke-width="2" d="{d}"/>'
out+='</svg>'
open('apera.svg','w').write(out); print(len(out))
