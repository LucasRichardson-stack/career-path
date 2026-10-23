import math, random
random.seed(11)
W=500; G=970
P=[]; F=[]
def L(x1,y1,x2,y2,f=False): (F if f else P).append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
def path(d,f=False): (F if f else P).append(d)
def M(x): return W-x
def parch(x1,x2,spring,apex,bottom,close=False):
    m=(x1+x2)/2; k=apex+(spring-apex)*0.25
    d=f"M{x1} {bottom}V{spring}Q{x1} {k} {m} {apex}Q{x2} {k} {x2} {spring}V{bottom}"
    return d+("Z" if close else "")

# ground
L(10,G,490,G); L(40,G+10,460,G+10,True)

# shaft faces
L(205,246,205,G); L(295,246,295,G)
# corner buttresses, full height, two set-offs
lb=[(205,G),(182,G),(182,760),(188,748),(188,520),(193,510),(193,246)]
for pts in (lb,[(M(x),y) for x,y in lb]):
    path("M"+"L".join(f"{x} {y}" for x,y in pts))
# quoins on buttress faces
for y in range(250,G-10,18):
    w = 8 if (y//18)%2 else 5
    xl = 182 if y>760 else 188 if y>520 else 193
    L(xl,y,xl+w,y,True); L(M(xl),y,M(xl)-w,y,True)

# horizontal stone bands
for y in (232,410,475,690,785,950):
    L(205,y,295,y)
L(178,950,322,950); L(178,942,322,942,True)

# --- top: parapet, small pinnacles, corner turrets ---
# blind arcade band under parapet
for i in range(5):
    x1=208+i*17
    path(parch(x1+2,x1+15,252,240,262),True)
L(205,264,295,264,True)
# parapet wall, spanning between the corner turrets
path("M207 232V214H293V232")
for cx in (222,236,250,264,278):
    path(f"M{cx-4} 214V196L{cx} 182L{cx+4} 196V214")
    L(cx-2,190,cx-6,186,True); L(cx+2,190,cx+6,186,True)
# corner turrets rise straight out of the buttresses (corbelled out slightly)
def turret(xl,xr,top):
    # body plus corbel taper down onto the buttress/shaft corner
    bl = 193 if xl<250 else 295
    br = 205 if xl<250 else 307
    path(f"M{xl} {top}V232L{bl} 246M{xr} {top}V232L{br} 246")
    L(xl,232,xr,232,True); L(xl,top,xr,top)
turret(187,207,140)
L(187,160,207,160,True); L(187,200,207,200,True)
for x1 in (191,199): path(parch(x1,x1+6,182,175,198),True)
path("M187 140L197 54L207 140")
for t in (.25,.45,.65,.82):
    y=140-86*t; xl=187+10*t; xr=207-10*t
    L(xl,y,xl-4,y-3,True); L(xr,y,xr+4,y-3,True)
L(197,54,197,44); path("M197 40a3.5 3.5 0 1 0 .1 0",True)
turret(293,313,158)
L(293,176,313,176,True)
for x1 in (296,305): path(parch(x1,x1+6,200,192,224),True)
path("M293 158L303 128L313 158")
L(303,128,303,120); path("M303 116a3 3 0 1 0 .1 0",True)
for x in (293,313): L(x,158,x+(4 if x==293 else -4),150,True)

# --- belfry: twin tall lancets with louvers inside a recessed arch ---
path(parch(214,286,300,266,406),True)
for x1 in (222,254):
    path(parch(x1,x1+24,300,276,400))
    for y in range(306,398,8): L(x1+3,y,x1+21,y,True)
    L(x1+12,290,x1+12,400,True)
L(214,406,286,406)

# --- clock with little hood ---
cx,cy=250,444
path(f"M232 424L250 414L268 424",True)
path(f"M{cx} {cy-21}a21 21 0 1 0 .1 0")
path(f"M{cx} {cy-16}a16 16 0 1 0 .1 0",True)
for k in range(12):
    a=math.pi*2*k/12
    L(cx+16*math.sin(a),cy-16*math.cos(a),cx+20*math.sin(a),cy-20*math.cos(a),k%3!=0)
L(cx,cy,cx-9*math.sin(math.radians(60)),cy-9*math.cos(math.radians(60)))
L(cx,cy,cx+14*math.sin(math.radians(60)),cy-14*math.cos(math.radians(60)))
L(214,420,214,470,True); L(286,420,286,470,True)

# --- brick coursing on the long shaft ---
for y in range(484,688,12):
    for _ in range(2):
        x0=random.uniform(209,280); L(x0,y,min(x0+random.uniform(8,18),291),y,True)
for y in range(796,938,12):
    if 852<y: 
        for x0 in (209+random.uniform(0,6),276+random.uniform(0,6)): L(x0,y,x0+10,y,True)
    else:
        x0=random.uniform(209,280); L(x0,y,min(x0+14,291),y,True)

# --- The Sower relief panel (Lee Lawrie) ---
path("M214 694H286V779H214Z")
path("M220 700H280V773H220Z",True)
L(210,779,290,779,True)
def dot(x,y,r=1.1): return f"M{x-r:.1f} {y}a{r} {r} 0 1 0 {2*r:.1f} 0a{r} {r} 0 1 0 {-2*r:.1f} 0"
# broad-brim hat and head
path("M236 713q12 -4 24 0",True)
path("M242 712q0 -7 6 -7q6 0 6 7",True)
path("M244 713q0 7 5 7q4 0 5 -6",True)
# shoulders and robe, flared at the hem, belted
path("M243 724q5 -3 11 0L257 736L262 754L237 754L241 736Z",True)
L(241,737,257,737,True)
path("M246 740L244 753M251 740L251 753M255 740L258 753",True)
# seed bag slung on a strap over the far shoulder
L(254,724,240,739,True)
path("M241 737q-8 1 -7 11q5 5 11 0q1 -7 -4 -11Z",True)
# near arm reaching into the bag
path("M244 725q-4 6 -3 13M247 727q-2 6 -2 11",True)
# casting arm swung forward, open hand
path("M254 724q9 0 13 -7M255 729q8 0 13 -9",True)
path("M268 717l3 -3M268 718l4 -1M268 720l3 1",True)
# scattered seed
for x,y in ((272,714),(275,720),(271,708),(276,727),(273,733)): path(dot(x,y),True)
# striding legs and feet
path("M251 754L259 767l6 0M255 754L262 765",True)
path("M246 754L238 766l-6 1M242 754L235 763",True)
# ploughed furrows
path("M222 770q9 -3 18 0t18 0t20 0",True)
# --- entrance: pointed arch doorway with stone surround, double door ---
path(parch(220,280,894,856,950))
path(parch(228,272,898,868,950))
L(250,872,250,950,True)
for x in (236,264): L(x,906,x,946,True)
L(230,920,270,920,True)
for x in (220,280): L(x,950,x,G)

# --- low annex on the right ---
path("M310 830H368V970")
path("M310 822H372V830",True)
for x in (316,330,344,358): L(x,822,x,816,True)
path(parch(330,346,872,858,910),True)
L(338,860,338,910,True)

# --- foreground trees (filled, so they sit in front of the tower) ---
TREES=[]
def canopy(cx,cy,rx,ry,n=13,j=.16):
    d=""
    for i in range(n+1):
        a=math.pi*2*i/n
        f=1-j+j*2*random.random()
        x=cx+rx*f*math.cos(a); y=cy+ry*f*math.sin(a)
        if i==0: d=f"M{x:.1f} {y:.1f}"
        else:
            am=math.pi*2*(i-.5)/n
            d+=f"Q{cx+rx*1.18*math.cos(am):.1f} {cy+ry*1.18*math.sin(am):.1f} {x:.1f} {y:.1f}"
    return d+"Z"
def tree(cx,base,trunk,blobs):
    T=[f"M{cx} {base}L{cx} {base-trunk}", f"M{cx} {base-trunk*.6}l-14 -18", f"M{cx} {base-trunk*.75}l12 -14"]
    shapes=[canopy(*b) for b in blobs]
    tex=[]
    for (bx,by,rx,ry) in blobs:
        for _ in range(int(rx*ry/260)):
            a=random.uniform(0,6.28); r=random.uniform(.15,.75)
            x=bx+rx*r*math.cos(a); y=by+ry*r*math.sin(a)
            tex.append(f"M{x:.1f} {y:.1f}q4 -5 9 0")
    TREES.append((T,shapes,tex))
tree(92,G,150,[(96,770,82,70),(60,840,52,44),(140,850,50,40)])
tree(410,G,160,[(404,760,76,72),(438,842,44,40),(368,858,46,38)])
SHRUBS=[canopy(cx,G-14,30,16,9,.12) for cx in (196,304)]

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#FFFFFF" stroke-linecap="round" stroke-linejoin="round">'
out+=f'<path stroke-width="1.6" d="{"".join(P)}"/><path stroke-width="1" opacity=".6" d="{"".join(F)}"/>'
for T,shapes,tex in TREES:
    out+=f'<path stroke-width="1.6" d="{"".join(T)}"/>'
    for sh in shapes: out+=f'<path class="occ" stroke-width="1.6" d="{sh}"/>'
    out+=f'<path stroke-width="1" opacity=".6" d="{"".join(tex)}"/>'
for sh in SHRUBS: out+=f'<path class="occ" stroke-width="1.2" d="{sh}"/>'
out+='</svg>'
open('msu.svg','w').write(out); print(len(out))
