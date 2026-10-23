import math, random
random.seed(4)
LAYERS=[]
def add(kind,d): LAYERS.append((kind,d))
def circ(cx,cy,r): return f"M{cx-r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0"
def poly(pts,close=True): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")
def smooth(pts,close=True,t=.5):
    P=list(pts)
    P=([P[-1]]+P+[P[0],P[1]]) if close else ([P[0]]+P+[P[-1]])
    d=f"M{P[1][0]:.1f} {P[1][1]:.1f}"
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        c1=(p1[0]+(p2[0]-p0[0])*t/3,p1[1]+(p2[1]-p0[1])*t/3)
        c2=(p2[0]-(p3[0]-p1[0])*t/3,p2[1]-(p3[1]-p1[1])*t/3)
        d+=f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d+("Z" if close else "")
def mix(pts,sharp):   # polyline with only some corners rounded: sharp = list of bools
    return poly(pts) if all(sharp) else smooth(pts)

# ======================= ROBOT (behind the bike) =======================
# BX-style proportions taken off the product photo: big round J2/J3 housings with
# square motor caps, thick tapered lower arm, chunky barrel upper arm, J4 motor behind the elbow
J2=(146,872); J3=(178,654); rJ2=46; rJ3=39
def rot(pts,c,deg):
    a=math.radians(deg); ca,sa=math.cos(a),math.sin(a)
    return [(c[0]+(x-c[0])*ca-(y-c[1])*sa, c[1]+(x-c[0])*sa+(y-c[1])*ca) for x,y in pts]
def rsq(c,half,deg,rr=.28):   # rounded square motor cap
    h=half; pts=[(c[0]-h,c[1]-h),(c[0]+h,c[1]-h),(c[0]+h,c[1]+h),(c[0]-h,c[1]+h)]
    pts=rot(pts,c,deg)
    d=""
    for i in range(4):
        p0,p1,p2=pts[i-1],pts[i],pts[(i+1)%4]
        a=(p1[0]+(p0[0]-p1[0])*rr,p1[1]+(p0[1]-p1[1])*rr); b=(p1[0]+(p2[0]-p1[0])*rr,p1[1]+(p2[1]-p1[1])*rr)
        d+=("M" if i==0 else "L")+f"{a[0]:.1f} {a[1]:.1f}Q{p1[0]:.1f} {p1[1]:.1f} {b[0]:.1f} {b[1]:.1f}"
    return d+"Z"
# base: wide plinth, turntable, J1 servo standing on the back corner
add('occ',smooth([(56,970),(56,936),(64,930),(236,930),(244,936),(244,970)],t=.05))
add('thin',"M64 946H236M200 930V970")
add('occ',smooth([(82,930),(84,912),(208,912),(210,930)],t=.1))
add('thin',"M90 920H202")
add('occ',smooth([(58,902),(86,902),(86,930),(58,930)],t=.1)); add('occ',smooth([(64,894),(80,894),(80,902),(64,902)],t=.1))
add('thin',"M58 912H86")
# lower arm: thick, slightly waisted, leaning toward the bike
la=math.atan2(J3[1]-J2[1],J3[0]-J2[0]); n=(math.cos(la+math.pi/2),math.sin(la+math.pi/2))
def at(t,w):
    x=J2[0]+(J3[0]-J2[0])*t; y=J2[1]+(J3[1]-J2[1])*t; return (x+n[0]*w,y+n[1]*w)
LA=[at(0,40),at(.35,30),at(.7,30),at(1,36),at(1,-34),at(.7,-27),at(.35,-28),at(0,-38)]
add('occ',smooth(LA,t=.35))
add('thin',smooth([at(.12,20),at(.5,17),at(.88,20)],close=False)+smooth([at(.12,-18),at(.5,-15),at(.88,-18)],close=False))
LEANDEG=math.degrees(la)+90
add('occ',circ(*J2,rJ2)); add('thin',circ(*J2,rJ2-8))
add('occ',rsq(J2,rJ2*.62,LEANDEG)); add('line',circ(*J2,10)); add('thin',circ(*J2,4))
for k in range(8):
    a=math.radians(k*45+10); add('thin',circ(J2[0]+(rJ2-4)*math.cos(a),J2[1]+(rJ2-4)*math.sin(a),1.2))
# upper arm
ANG=math.radians(19); UL=206
def arm(u,v):
    c,s=math.cos(ANG),math.sin(ANG); return (J3[0]+u*c-v*s, J3[1]+u*s+v*c)
def A(pts): return [arm(u,v) for u,v in pts]
add('occ',smooth(A([(-74,-15),(-24,-17),(-24,15),(-74,13)]),t=.12))              # J4 motor
add('thin',poly(A([(-64,-15),(-64,14)]),False)+poly(A([(-74,-6),(-80,-6),(-80,4),(-74,4)]),False))
add('occ',smooth(A([(-16,-36),(56,-34),(110,-27),(UL-26,-20),(UL-26,19),(110,25),(56,31),(-16,34)]),t=.25))
add('thin',poly(A([(56,-34),(54,31)]),False)+poly(A([(110,-27),(108,25)]),False)+poly(A([(64,-6),(UL-32,-6)]),False))
add('occ',smooth(A([(98,6),(130,6),(130,24),(98,24)]),t=.1))                    # J5 motor
add('occ',circ(*J3,rJ3)); add('thin',circ(*J3,rJ3-7))
add('occ',rsq(J3,rJ3*.62,LEANDEG)); add('line',circ(*J3,9)); add('thin',circ(*J3,3.5))
for k in range(8):
    a=math.radians(k*45+10); add('thin',circ(J3[0]+(rJ3-3.5)*math.cos(a),J3[1]+(rJ3-3.5)*math.sin(a),1.1))
add('occ',smooth(A([(UL-30,-19),(UL+2,-17),(UL+2,17),(UL-30,19)]),t=.15))      # wrist
add('occ',smooth(A([(UL+2,-15),(UL+9,-14),(UL+9,14),(UL+2,15)]),t=.2))         # flange
add('thin',smooth([arm(UL-36,-20),arm(130,-46),arm(10,-50),arm(-50,-20)],close=False))
# spray gun pointing down at the tank
GA=math.radians(96)
F=arm(UL+9,0)
def g(u,v):
    c,s=math.cos(GA),math.sin(GA); return (F[0]+u*c-v*s, F[1]+u*s+v*c)
add('occ',smooth([g(-2,-9),g(22,-9),g(27,-5),g(27,5),g(22,9),g(-2,9)],t=.1))
add('occ',smooth([g(27,-3.5),g(38,-3),g(38,3),g(27,3.5)],t=.1))
add('thin',poly([g(8,-9),g(8,9)],False))
NZ=g(40,0)
MIST=""
for k in range(110):
    t=random.random()**.6; a=GA+random.uniform(-1,1)*t*0.38
    d=6+t*(800-NZ[1]-4)/max(math.sin(a),.5)
    x,y=NZ[0]+d*math.cos(a),NZ[1]+d*math.sin(a)
    if y<804: MIST+=f"M{x:.1f} {y:.1f}h.1"
CONE=""
for sg in (-1,1):
    a=GA+sg*.38; L_=(802-NZ[1])/math.sin(a)
    CONE+=f"M{NZ[0]+5*math.cos(a):.1f} {NZ[1]+5*math.sin(a):.1f}L{NZ[0]+L_*math.cos(a):.1f} {NZ[1]+L_*math.sin(a):.1f}"
ROBOT_N=len(LAYERS)
print('nozzle',NZ)

# ======================= FLOOR / PLATFORM =======================
add('line',"M0 970H500")
add('occ',poly([(150,958),(498,958),(498,966),(150,966)]))
for x in range(162,498,24): add('thin',f"M{x} 974l8 8")

# ======================= NINJA-STYLE BIKE (in front) =======================
R=46; RW=(226,912); FW=(436,912)
def wheel(cx,cy,front):
    add('occ',circ(cx,cy,R))
    t=circ(cx,cy,R-7)+circ(cx,cy,R-10)+circ(cx,cy,6)
    for k in range(5):
        a=math.radians(90+k*72)
        for s in (-.11,.11):
            t+=(f"M{cx+7*math.cos(a+s):.1f} {cy-7*math.sin(a+s):.1f}"
                f"L{cx+(R-10)*math.cos(a+s*2.4):.1f} {cy-(R-10)*math.sin(a+s*2.4):.1f}")
    add('line',t)
    if front:
        add('thin',circ(cx,cy,27)+circ(cx,cy,22))
        add('occ',smooth([(cx-34,cy-24),(cx-24,cy-34),(cx-14,cy-26),(cx-24,cy-14)],t=.2))
    else:
        add('thin',circ(cx,cy,17))
wheel(*RW,False); wheel(*FW,True)
PV=(318,872)
add('occ',smooth([(RW[0]-3,RW[1]-7),(PV[0]-2,PV[1]-9),(PV[0]+8,PV[1]+1),(PV[0]-2,PV[1]+9),(RW[0]+3,RW[1]+8)],t=.2))
add('thin',f"M{RW[0]} {RW[1]-17}L{PV[0]-4} {PV[1]-6}M{RW[0]} {RW[1]+17}L{PV[0]} {PV[1]+8}")
add('occ',poly([(398,814),(410,812),(442,910),(430,913)]))                       # fork
add('thin',"M416 852L437 904")
add('occ',smooth([(404,876),(436,860),(474,872),(478,880),(436,868),(410,884)],t=.35))   # fender
# engine & exhaust (seen below/behind the fairing)
add('occ',smooth([(300,846),(354,844),(360,890),(344,918),(306,918),(294,884)],t=.3))
add('thin',"M304 860H352M302 872H356M304 884H356M310 900q18 8 36 0")
add('line',smooth([(352,918),(326,928),(296,924),(272,914)],close=False,t=.4))
add('occ',smooth([(282,908),(240,890),(232,892),(228,902),(236,912),(276,924)],t=.2))  # muffler
add('occ',poly([(232,892),(224,890),(222,908),(234,910)]))
add('thin',"M246 892l-6 18M272 904l-5 15")
add('line',"M306 878l-10 16l-10 2M262 872l-10 14l-8 1")                         # pegs
# bodywork: tail, pillion + rider seats, tank, side fairing, nose, belly pan
BODY=[(174,812),(196,815),(232,820),(250,826),(262,836),(294,842),(320,836),
      (334,818),(352,806),(374,802),(394,806),(404,812),
      (416,806),(430,804),(452,812),(474,826),(492,840),
      (486,850),(470,856),(458,860),(442,872),(420,882),
      (408,904),(380,922),(344,926),(330,914),(346,880),(328,862),
      (300,856),(270,856),(236,854),(206,844),(186,828)]
add('occ',poly(BODY))
add('occ',poly([(420,807),(408,784),(412,778),(422,778),(462,817),(444,811)]))   # screen
add('thin',"M414 784L452 812")
add('line',"M400 810L384 802l-10 2")                                              # clip-on
add('thin',
    "M196 815Q214 826 232 828L250 826"             # pillion seat edge
    "M262 836Q290 848 320 840"                      # rider seat edge
    "M320 840Q330 848 346 850L398 842"             # tank lower edge
    "M346 850L366 826L388 820"                      # knee recess
    "M404 812L420 838L460 848L486 850"             # upper fairing lower edge
    "M474 826L452 834L470 846"                      # twin headlamp
    "M460 848L444 852"
    "M352 856L384 852L394 872L364 878Z"            # shroud vent triangle
    "M344 880L398 878L430 870"                      # mid fairing crease
    "M338 906L376 908L408 896"                      # belly crease
    "M184 822L214 836L252 844L276 852"             # tail panel crease
    "M178 814l8 4")                                 # tail light
add('line',"M214 842L198 858l-10 2")                                              # plate bracket

# spray mist drawn last so it sits on the bike
add('mist',MIST); add('cone',CONE)

# robot first (behind), then floor, then bike
ROBOT=LAYERS[:ROBOT_N]
REST=LAYERS[ROBOT_N:]
# floor/platform kinds stay neutral; bike gets neon green
# REST starts with floor then bike — split after spray mist was appended at end
# Actually mist/cone are bike-adjacent spray; keep with bike. Floor is first few after ROBOT_N.
# Count floor adds: line, occ, then thin loop — identify by regenerating with tags.
# Simpler: mark floor layer range. Floor was added as: line, occ, thin*... before wheel().
# ROBOT_N is end of robot. Floor: lines until wheel() starts — wheel is first bike geometry.
# Re-tag: rebuild REST with explicit groups by re-running structure.
# Easiest reliable approach: emit robot group red, then remaining paths neon green
# EXCEPT floor paths which we leave as #111 / current black.
# Floor paths are the first 3+ thin hatch adds after ROBOT_N before wheels.
# From source: after ROBOT_N: line ground, occ platform, thin hatch loop (many), then wheels...
# We'll tag floor by regenerating with kind prefixes.

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-linecap="round" stroke-linejoin="round">'
def emit(kind,d,stroke=None):
    global out
    st=f' stroke="{stroke}"' if stroke else ''
    if kind=='occ': out+=f'<path class="occ"{st} stroke-width="1.6" d="{d}"/>'
    elif kind=='line': out+=f'<path{st} stroke-width="1.6" d="{d}"/>'
    elif kind=='thin': out+=f'<path{st} stroke-width="1" opacity=".6" d="{d}"/>'
    elif kind=='cone': out+=f'<path{st} stroke-width="1" stroke-dasharray="1 4" opacity=".6" d="{d}"/>'
    elif kind=='mist': out+=f'<path{st} stroke-width="2.2" opacity=".55" d="{d}"/>'

# floor: from ROBOT_N until first wheel circ — wheels use circ around RW/FW y=912 r=46
# Count floor entries: 1 line + 1 occ + hatch thins. Hatch: for x in range(162,498,24) => 14 thins
FLOOR_N = 2 + len(range(162,498,24))  # line+occ+hatches = 2+14=16
FLOOR=REST[:FLOOR_N]
BIKE=REST[FLOOR_N:]

out+='<g stroke="#E60012">'  # Kawasaki red robot
for kind,d in ROBOT: emit(kind,d)
out+='</g>'
out+='<g stroke="#161616">'  # neutral floor/frame
for kind,d in FLOOR: emit(kind,d)
out+='</g>'
out+='<g stroke="#1B8A3E">'  # neon green motorcycle
for kind,d in BIKE: emit(kind,d)
out+='</g>'
out+='</svg>'
open('kawasaki4.svg','w').write(out); print(len(out), 'robot', len(ROBOT), 'floor', len(FLOOR), 'bike', len(BIKE))
