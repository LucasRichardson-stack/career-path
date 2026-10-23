import math, random
random.seed(8)
G=970
LAYERS=[]
def add(kind,d): LAYERS.append((kind,d))
def circ(cx,cy,r): return f"M{cx-r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0"
def poly(pts,close=True): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")
def rect(x,y,w,h): return f"M{x} {y}h{w}v{h}h{-w}Z"
def text(x,y,s,size,ls,weight=700):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" fill="currentColor" stroke="none">{s}</text>')

PX0,PX1=148,352; CX=(PX0+PX1)/2      # stone entrance pavilion
TOP=560

# ---------------- brick wings ----------------
def wing(x0,x1,top):
    add('occ',rect(x0,top,x1-x0,G-top))
    br=""
    for i,y in enumerate(range(top+6,G-4,7)):
        if 696<y<704 or 816<y<824: continue
        br+=f"M{x0} {y}H{x1}"
        off=0 if i%2 else 7
        for x in range(int(x0)+off,int(x1),14):
            if random.random()<.35: br+=f"M{x} {y}v7"
    add('brick',br)
    add('line',f"M{x0} 696H{x1}M{x0} 704H{x1}M{x0} 816H{x1}M{x0} 824H{x1}")   # stone bands
    # steel multi-pane windows, three storeys
    ww=46
    xs=[x0+14+i*(ww+16) for i in range(int((x1-x0-14)//(ww+16)))]
    for x in xs:
        for (y0,y1) in ((top+18,688),(712,808),(834,936)):
            add('occ',rect(x,y0,ww,y1-y0))
            g=""
            for k in range(1,4): g+=f"M{x+ww*k/4:.1f} {y0}V{y1}"
            for yy in range(y0+12,y1,12): g+=f"M{x} {yy}H{x+ww}"
            add('thin',g)
            add('line',rect(x-3,y1,ww+6,4))                                  # stone sill
wing(0,PX0,592); wing(PX1,500,592)

# ---------------- stone pavilion ----------------
add('occ',rect(PX0,TOP,PX1-PX0,G-TOP))
add('line',f"M{PX0-4} {TOP}H{PX1+4}M{PX0-4} {TOP+4}H{PX1+4}")                  # cornice
add('occ',rect(PX0+6,TOP+10,PX1-PX0-12,22))                                    # inscription frieze
add('text',text(CX,TOP+25,"INSTITUTE · OF · TECHNOLOGY",7.2,1.4,400))
# stone coursing on the piers
j=""
for y in range(TOP+40,930,16):
    j+=f"M{PX0} {y}h24M{PX1} {y}h-24"
add('thin',j+f"M{PX0+24} {TOP+36}V930M{PX1-24} {TOP+36}V930")
# deep round arch with stepped surrounds and a keystone
AX0,AX1,ASP=PX0+30,PX1-30,690; R=(AX1-AX0)/2
for k,dr in enumerate((0,7,13)):
    r=R-dr
    add('line' if k==0 else 'thin',f"M{CX-r} 860V{ASP}A{r} {r} 0 0 1 {CX+r} {ASP}V860")
add('occ',poly([(CX-7,ASP-R-2),(CX+7,ASP-R-2),(CX+5,ASP-R+14),(CX-5,ASP-R+14)]))
# the great window: steel grid, clipped to the arch
WX0,WX1=AX0+16,AX1-16; WR=(WX1-WX0)/2; WB=790
add('occ',f"M{WX0} {WB}V{ASP}A{WR} {WR} 0 0 1 {WX1} {ASP}V{WB}Z")
grid=""
for x in range(int(WX0)+12,int(WX1),12):
    dx=abs(x-CX); ytop=ASP-math.sqrt(max(WR*WR-dx*dx,0))
    grid+=f"M{x} {ytop:.1f}V{WB}"
for y in range(int(ASP-WR)+12,WB,12):
    if y>=ASP: grid+=f"M{WX0} {y}H{WX1}"
    else:
        h=math.sqrt(max(WR*WR-(ASP-y)**2,0)); grid+=f"M{CX-h:.1f} {y}H{CX+h:.1f}"
add('thin',grid)
add('line',f"M{CX-38} {ASP-WR+6}V{WB}M{CX+38} {ASP-WR+6}V{WB}".replace(f"{ASP-WR+6}",f"{ASP-math.sqrt(WR*WR-38*38):.1f}"))  # heavy mullions
add('line',f"M{WX0} 742H{WX1}")                                                                              # transom bar
# lettered panel
add('occ',rect(WX0-4,798,WX1-WX0+8,50)); add('thin',rect(WX0,802,WX1-WX0,42))
add('text',text(CX,818,"GENERAL MOTORS",8.6,1.6))
add('text',text(CX,836,"INSTITUTE",8.6,1.6))
# entrance: two pairs of glass doors with a central pier
add('occ',rect(WX0-4,852,WX1-WX0+8,80))
d=""
for x0 in (WX0,CX+4):
    w=(WX1-WX0)/2-4
    for k in range(2):
        xx=x0+k*w/2; d+=rect(xx+2,858,w/2-4,72)+rect(xx+6,864,w/2-12,40)
        d+=f"M{xx+w/2-6 if k==0 else xx+4} 892v10"                                                          # pull handles
add('thin',d+f"M{CX} 852V932")
# steps with cheek walls
for k,y in enumerate((932,944,956)):
    add('line',f"M{PX0+6-k*10} {y}H{PX1-6+k*10}V{y+12}")
add('occ',rect(PX0-14,936,22,34)); add('occ',rect(PX1-8,936,22,34))
# wall lanterns on the brick either side
for x in (PX0-16,PX1+16):
    add('line',f"M{x} 800v-6M{x-5} 794h10")
    add('occ',poly([(x-6,800),(x+6,800),(x+8,824),(x-8,824)])); add('thin',f"M{x} 800V824M{x-7} 812h14")
    add('occ',poly([(x-9,824),(x+9,824),(x+4,830),(x-4,830)]))

# ---------------- bare winter trees in front of the wings ----------------
def branch(x,y,ang,length,w,depth,out):
    if depth==0 or length<6: return
    x2=x+length*math.cos(ang); y2=y+length*math.sin(ang)
    out.append((w,f"M{x:.1f} {y:.1f}L{x2:.1f} {y2:.1f}"))
    n=2
    for i in range(n):
        da=random.uniform(.25,.55)*(1 if i%2 else -1)+random.uniform(-.1,.1)
        branch(x2,y2,ang+da,length*random.uniform(.62,.78),max(w*.62,.6),depth-1,out)
def tree(x,top,lean=0):
    trunk=f"M{x-5} {G}C{x-4} {(G+top)/2} {x-2+lean} {top+30} {x-1+lean} {top}L{x+2+lean} {top}C{x+3+lean} {top+30} {x+5} {(G+top)/2} {x+6} {G}Z"
    add('occ',trunk)
    add('thin',"".join(f"M{x-3+random.uniform(0,6):.1f} {y}h{random.uniform(2,4):.1f}" for y in range(int(top)+40,G-10,22)))   # birch marks
    out=[]
    for ang,L,sy in ((-1.9,54,top+40),(-1.2,50,top+70),(-2.3,46,top+110),(-.8,44,top+150),(-1.57,58,top)):
        sx=x+lean*(1-(sy-top)/(G-top))
        branch(sx,sy,ang+random.uniform(-.1,.1),L*.8,1.6,5,out)
    for w,d in out: add('twig' if w<1.1 else 'line',d)
tree(62,640,6); tree(120,690,-4); tree(436,660,-6); tree(484,700,4)

out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
out+=f'<path stroke-width="1.6" d="M0 {G}H500"/>'
for kind,d in LAYERS:
    if not d: continue
    if kind=='occ': out+=f'<path class="occ" stroke-width="1.5" d="{d}"/>'
    elif kind=='line': out+=f'<path stroke-width="1.5" d="{d}"/>'
    elif kind=='thin': out+=f'<path stroke-width=".9" opacity=".6" d="{d}"/>'
    elif kind=='brick': out+=f'<path stroke-width=".6" opacity=".35" d="{d}"/>'
    elif kind=='twig': out+=f'<path stroke-width=".8" opacity=".7" d="{d}"/>'
    elif kind=='text': out+=d
out+='</svg>'
open('kettering.svg','w').write(out); print(len(out))
