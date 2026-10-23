import math, random
random.seed(5)
W=500; G=970
P=[]; F=[]; OCC=[]; FRONT=[]
def L(x1,y1,x2,y2,f=False): (F if f else P).append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
def path(d,f=False): (F if f else P).append(d)
def poly(pts,close=False): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")

# ---------- car body-in-white, side profile, facing left ----------
TOP=[(34,880),(44,860),(150,842),(168,838),(228,790),(332,788),(398,832),(456,840),(467,862)]
def top_y(x):
    for (x0,y0),(x1,y1) in zip(TOP,TOP[1:]):
        if x0<=x<=x1: return y0+(y1-y0)*(x-x0)/(x1-x0)
    return None
SILL=905
def arch(cx,r=36,dir=1):
    # semicircle opening (no wheels: it's a bare body)
    return f"A{r} {r} 0 0 1 {cx-r*dir:.1f} {SILL}" if False else ""
body=(poly(TOP)+f"L466 900L413 {SILL}A38 38 0 0 0 337 {SILL}L153 {SILL}A38 38 0 0 0 77 {SILL}L38 905L34 880Z")
det=[]
# window openings (no glass on a bare body)
det.append(poly([(178,842),(232,800),(278,798),(278,842)],True))
det.append(poly([(286,798),(328,797),(380,840),(286,842)],True))
# door cut lines
det.append("M172 842L176 900M282 800V900M372 842L366 900")
# character line, sill, shut lines, fuel door
det.append("M48 868Q250 858 460 866M150 896H340")
det.append("M70 852L150 846M402 836L450 843")
det.append("M395 858h10v10h-10z")
# underbody structure visible through wheel openings
det.append("M90 905h50M350 905h50")
OCC.append((body,det))

# ---------- skid and roller conveyor ----------
skid=[]
skid.append(poly([(20,926),(480,926),(480,936),(20,936)],True))
for x in (150,340):
    skid.append(f"M{x-6} {SILL}L{x-6} 926M{x+6} {SILL}L{x+6} 926M{x-12} {SILL}H{x+12}")
for x in range(34,480,36):
    skid.append(f"M{x-7} 945a7 7 0 1 0 14 0a7 7 0 1 0 -14 0")
skid.append("M10 952H490M10 938H490")
for x in (14,486):
    skid.append(f"M{x} 938V{G}")
for x in range(60,480,80): skid.append(f"M{x} 952V{G}")
P.append("".join(skid))

# ---------- overhead gantry ----------
BT,BB=548,572
path(poly([(8,BT),(492,BT),(492,BB),(8,BB)],True))
for x in range(8,492,32):
    L(x,BT,x+16,BB,True); L(x+16,BB,x+32,BT,True)
for x0 in (16,470):
    path(f"M{x0} {BB}V{G}M{x0+14} {BB}V{G}")
    for y in range(600,G,40): L(x0,y,x0+14,y+20,True)
    path(f"M{x0-6} {G}h26",False)
# cable tray
path("M40 534H460M40 540H460",True)
for x in range(60,460,50): L(x,534,x,548,True)

# ---------- cameras ----------
CAMS=[]
def fixed_cam(x,mount_y,lens_y):
    d=f"M{x} {mount_y}V{lens_y-26}"                      # drop rod
    d+=f"M{x-12} {lens_y-26}h24v20h-24z"                   # body
    d+=f"M{x-7} {lens_y-6}h14l-2 6h-10z"                   # lens hood
    d+=f"M{x-16} {mount_y}h32"                             # clamp
    P.append(d)
    F.append(f"M{x-8} {lens_y-20}h6")                     # status light
    return (x,lens_y)
# a hanging 6-axis arm carrying the third camera
def robot(bx):
    d=f"M{bx-18} {BB}h36v10h-36z"                          # base flange
    d+=f"M{bx-12} {BB+10}h24v16h-24z"                      # turret
    # upper arm down-left to elbow
    d+=f"M{bx-6} {BB+26}L{bx-36} {BB+86}M{bx+8} {BB+28}L{bx-24} {BB+92}"
    d+=f"M{bx-30} {BB+89}m-11 0a11 11 0 1 0 22 0a11 11 0 1 0 -22 0"
    # forearm down-right to wrist
    d+=f"M{bx-24} {BB+82}L{bx+28} {BB+120}M{bx-34} {BB+98}L{bx+20} {BB+132}"
    d+=f"M{bx+24} {BB+126}m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0"
    # camera on the flange, tilted
    d+=f"M{bx+18} {BB+134}l20 -6l6 18l-20 6z"
    d+=f"M{bx+30} {BB+152}l10 -3l3 8l-10 3z"
    P.append(d)
    F.append(f"M{bx-20} {BB+60}q-20 20 -6 40")             # dress pack cable
    return (bx+38,BB+158)
CAMS.append((fixed_cam(104,BB,660),(58,150)))
CAMS.append((robot(236),(232,330)))
CAMS.append((fixed_cam(420,BB,676),(398,462)))

# ---------- how the cameras 'see': rays, scanned surface, target marks ----------
RAYS=[]; SCAN=[]; MARKS=[]
for (cx,cy),(xa,xb) in CAMS:
    ya,yb=top_y(xa),top_y(xb)
    for (x,y) in ((xa,ya),(xb,yb)):
        RAYS.append(f"M{cx} {cy}L{x:.1f} {y:.1f}")
    # scanned strip: surface segment lifted a hair, drawn bold
    pts=[(x,top_y(x)-3) for x in range(xa,xb+1,4)]
    SCAN.append(poly(pts))
    # projected light stripes crossing the surface
    for i in range(1,8):
        x=xa+(xb-xa)*i/8; y=top_y(x)
        SCAN.append(f"M{x:.1f} {y-7:.1f}V{y+1:.1f}")
    # one target mark (crosshair) mid-strip
    mx=(xa+xb)/2; my=top_y(mx)-16
    MARKS.append(f"M{mx-7:.1f} {my:.1f}h4M{mx+3:.1f} {my:.1f}h4M{mx:.1f} {my-7:.1f}v4M{mx:.1f} {my+3:.1f}v4M{mx-4:.1f} {my:.1f}a4 4 0 1 0 8 0a4 4 0 1 0 -8 0")

# floor safety stripes either side of the line
for x in range(30,480,18): path(f"M{x} {G+4}l8 8",True)
L(0,G,500,G)

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
out+=f'<path stroke-width="1.6" d="{"".join(P)}"/><path stroke-width="1" opacity=".6" d="{"".join(F)}"/>'
out+=f'<path stroke-width="1" stroke-dasharray="2 5" d="{"".join(RAYS)}"/>'
for d,det in OCC:
    out+=f'<path class="occ" stroke-width="1.6" d="{d}"/>'
    out+=f'<path stroke-width="1" opacity=".7" d="{"".join(det)}"/>'
out+=f'<path stroke-width="2.4" d="{"".join(SCAN)}"/>'
out+=f'<path stroke-width="1.1" d="{"".join(MARKS)}"/>'
out+='</svg>'
open('liberty.svg','w').write(out); print(len(out))
