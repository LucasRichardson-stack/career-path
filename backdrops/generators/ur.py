import math, random
random.seed(9)
G=970
LAYERS=[]
def add(kind,d): LAYERS.append((kind,d))
def circ(cx,cy,r): return f"M{cx-r:.1f} {cy:.1f}a{r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0"
def poly(pts,close=True): return "M"+"L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else "")
def rrect(x,y,w,h,r): return f"M{x+r} {y}H{x+w-r}Q{x+w} {y} {x+w} {y+r}V{y+h-r}Q{x+w} {y+h} {x+w-r} {y+h}H{x+r}Q{x} {y+h} {x} {y+h-r}V{y+r}Q{x} {y} {x+r} {y}Z"
def smooth(pts,close=True,t=.5):
    P=list(pts); P=([P[-1]]+P+[P[0],P[1]]) if close else ([P[0]]+P+[P[-1]])
    d=f"M{P[1][0]:.1f} {P[1][1]:.1f}"
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        c1=(p1[0]+(p2[0]-p0[0])*t/3,p1[1]+(p2[1]-p0[1])*t/3); c2=(p2[0]-(p3[0]-p1[0])*t/3,p2[1]-(p3[1]-p1[1])*t/3)
        d+=f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d+("Z" if close else "")
def tube(a,b,r):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); nx,ny=-math.sin(ang)*r,math.cos(ang)*r
    return poly([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),(b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)])
def band(a,b,r,t):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); nx,ny=-math.sin(ang)*r,math.cos(ang)*r
    x,y=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
    return f"M{x+nx:.1f} {y+ny:.1f}L{x-nx:.1f} {y-ny:.1f}"

add('line',f"M0 {G}H500")
add('thin',''.join(f'M{x0} {G+5}H{x1}' for x0,x1 in ((84,150),(176,252),(256,296),(288,496))))

# ===================== CNC lathe (right) =====================
MX0,MX1=284,498
add('occ',rrect(MX0+6,946,MX1-MX0-6,24,3))                               # plinth
add('thin',f"M{MX0+14} 958H{MX1-6}")
add('occ',smooth([(MX0,946),(MX0,712),(MX0+8,696),(MX1,696),(MX1,946)],t=.05))   # cabinet
add('occ',poly([(MX0+26,696),(MX0+34,676),(MX1-30,676),(MX1-22,696)]))   # top cover
add('thin',f"M{MX0+40} 686H{MX1-36}")
# work door opening with the door slid right
DX0,DX1,DY0,DY1=MX0+14,MX0+128,724,880
add('occ',rrect(DX0,DY0,DX1-DX0,DY1-DY0,4))
add('thin',rrect(DX0+5,DY0+5,DX1-DX0-10,DY1-DY0-10,3))
# inside: spindle housing + chuck with jaws, tool turret
add('occ',rrect(DX0+8,772,26,52,3))
CH=(DX0+50,798)
add('occ',circ(CH[0],CH[1],20)); add('thin',circ(CH[0],CH[1],14))
for k in range(3):
    a=math.radians(90+k*120); add('line',f"M{CH[0]+6*math.cos(a):.1f} {CH[1]-6*math.sin(a):.1f}L{CH[0]+14*math.cos(a):.1f} {CH[1]-14*math.sin(a):.1f}")
add('occ',poly([(DX1-28,826),(DX1-6,826),(DX1-6,868),(DX1-28,868)]))
add('thin',f"M{DX1-26} 812h18v14M{DX0+6} 870H{DX1-6}")
# door panel parked to the right, with window and handle
add('occ',rrect(DX1+4,DY0-6,92,DY1-DY0+12,4))
add('thin',rrect(DX1+14,DY0+8,72,96,3)+f"M{DX1+22} {DY0+18}l14 -6M{DX1+22} {DY0+28}l30 -12")
add('line',f"M{DX1+10} {DY0+40}V{DY0+110}")
# control panel (pendant) on the right edge
add('occ',rrect(MX1-46,712,40,64,3)); add('thin',rrect(MX1-41,718,30,22,2))
for i in range(3):
    for j in range(2): add('thin',circ(MX1-36+i*10,752+j*12,2.5))
# chip tray / lower panels
add('thin',f"M{MX0+8} 900H{MX1-8}M{MX0+20} 912h60v26h-60zM{MX0+96} 912h60v26h-60z")
# stack light
add('occ',rrect(MX1-26,632,12,40,3)); add('thin',f"M{MX1-26} 645h12M{MX1-26} 658h12")
add('line',f"M{MX1-20} 672V676")

# ===================== UR robot on a pedestal =====================
PX=214
add('occ',poly([(PX-32,966),(PX+32,966),(PX+32,970),(PX-32,970)]))
add('occ',rrect(PX-22,874,44,92,3))
add('thin',f"M{PX-22} 886H{PX+22}M{PX-12} 900h24v20h-24z")
add('thin',"".join(circ(PX+sx*16,y,1.2) for sx in (-1,1) for y in (880,960)))
add('occ',rrect(PX-28,866,56,8,2))
def cap(c,r):
    """UR joint seen end-on: housing, dark seal ring, blue cap with 4 screws, centre logo boss"""
    # 'joint' strokes recolored light blue in the SVG emitter
    add('joint_occ',circ(*c,r)); add('joint_line',circ(*c,r*.86)); add('joint_thin',circ(*c,r*.80))
    for k in range(4):
        a=math.radians(45+k*90); add('joint_thin',circ(c[0]+r*.6*math.cos(a),c[1]+r*.6*math.sin(a),.9))
    add('joint_thin',f"M{c[0]-r*.22:.1f} {c[1]+r*.2:.1f}Q{c[0]-r*.3:.1f} {c[1]-r*.3:.1f} {c[0]+r*.1:.1f} {c[1]-r*.28:.1f}")
def tube(a,b,r):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); nx,ny=-math.sin(ang)*r,math.cos(ang)*r
    return poly([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),(b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)])
def ring(a,b,r,t,w=3):
    ang=math.atan2(b[1]-a[1],b[0]-a[0]); nx,ny=-math.sin(ang)*r,math.cos(ang)*r
    ux,uy=math.cos(ang),math.sin(ang); x,y=a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t
    return poly([(x+nx,y+ny),(x+nx+ux*w,y+ny+uy*w),(x-nx+ux*w,y-ny+uy*w),(x-nx,y-ny)])
# base: flared aluminium foot, J1 housing with dark band
add('occ',smooth([(PX-21,866),(PX-14,852),(PX+14,852),(PX+21,866)],t=.2))
add('occ',rrect(PX-15,828,30,25,3)); add('line',f"M{PX-15} 846H{PX+15}"); add('thin',f"M{PX-15} 843H{PX+15}")
SH=(PX,822); EL=(PX-16,732); WR1=(PX+70,770)
# links: upper arm (thicker), forearm, each with a dark ring where it meets a joint
add('occ',tube(SH,EL,10.5)); add('line',ring(SH,EL,10.5,.17)+ring(SH,EL,10.5,.80))
add('occ',tube(EL,WR1,8.5));  add('line',ring(EL,WR1,8.5,.16)+ring(EL,WR1,8.5,.82))
cap(SH,16); cap(EL,13.5)
# wrist: J4 end-on, J5 housing pointing down, J6 flange facing the machine
add('occ',rrect(WR1[0]-9,WR1[1]-2,18,28,4)); add('line',f"M{WR1[0]-9} {WR1[1]+18}h18")
cap(WR1,10.5)
J6=(WR1[0]+6,WR1[1]+32)
add('occ',rrect(J6[0]-12,J6[1]-9,22,18,4)); add('line',f"M{J6[0]+4} {J6[1]-9}v18")
add('occ',smooth([(J6[0]+10,J6[1]-8),(J6[0]+14,J6[1]-8),(J6[0]+15,J6[1]),(J6[0]+14,J6[1]+8),(J6[0]+10,J6[1]+8)],t=.3))
# two-finger gripper holding a turned blank, reaching into the chuck
GX=J6[0]+15; GY=J6[1]
add('occ',rrect(GX,GY-10,13,20,3)); add('thin',f"M{GX+4} {GY-10}v20")
add('line',f"M{GX+13} {GY-9}h9v4h-5M{GX+13} {GY+9}h9v-4h-5")
add('occ',rrect(GX+19,GY-5,13,10,2)); add('thin',f"M{GX+23} {GY-5}v10M{GX+27} {GY-5}v10")
# controller box on the floor, cable to the base
add('thin',smooth([(PX+22,952),(PX+36,964),(PX+50,966),(PX+56,958)],close=False))
add('occ',rrect(PX+44,928,34,34,2)); add('thin',rrect(PX+49,934,24,12,1)+f"M{PX+50} 962v8M{PX+72} 962v8"+circ(PX+68,954,2))

# ===================== operator, right next to the robot, no fence =====================
# 3/4 view, 8-head proportions, looking down at a tablet held in both hands
add('occ',smooth([(94,840),(112,840),(112,872),(110,902),(110,954),(96,954),(94,902),(92,870)],t=.3))       # far leg
add('occ',smooth([(110,838),(133,838),(134,870),(131,902),(131,954),(116,954),(113,902),(111,870)],t=.3))   # near leg
add('thin',"M120 896q6 3 11 0M98 898q5 3 10 0M122 848l2 22")                                                  # knees, crease
add('occ',smooth([(94,952),(112,952),(116,962),(118,970),(90,970),(91,960)],t=.25))                          # far boot
add('occ',smooth([(116,952),(132,952),(142,962),(144,970),(113,970),(114,960)],t=.25))                       # near boot
add('thin',"M92 966h24M115 966h28")
torso=smooth([(91,758),(104,750),(121,750),(130,756),(135,772),(133,794),(130,814),(132,838),(92,840),(93,812),(89,786)],t=.42)
add('occ',torso)
# hi-vis vest: armhole, front opening, two reflective bands, hem
add('occ',smooth([(95,758),(103,752),(110,770),(118,770),(122,751),(130,757),(134,774),(132,800),(130,830),(93,832),(93,806),(90,784)],t=.3))
add('line',"M92 796H133M92 803H133M92 818H131M92 825H131")
add('thin',"M118 770V830M104 752l7 10l7 -10")
add('occ',rrect(92,830,40,8,2)); add('thin',"M110 830v8")                                                    # belt
# far forearm and hand crossing to the tablet
add('occ',smooth([(128,800),(140,786),(145,791),(132,806)],t=.3))
# tablet tilted up toward the face
add('occ',poly([(138,776),(161,766),(171,790),(148,801)]))
add('thin',poly([(142,778),(159,771),(166,788),(149,796)]))
add('occ',smooth([(139,782),(146,779),(148,787),(141,790)],t=.4))                                            # far thumb
# near arm: shoulder, bent elbow, forearm up to the tablet edge
add('occ',smooth([(121,756),(132,758),(135,780),(133,800),(150,790),(156,796),(136,812),(124,812),(120,790)],t=.35))
add('thin',"M146 790l5 6M125 798q5 3 10 0")
add('occ',smooth([(150,788),(158,785),(162,794),(154,800)],t=.4))                                            # near hand
# neck and head, tipped forward to read the screen
add('occ',poly([(105,738),(118,740),(121,752),(104,752)]))
head=smooth([(102,738),(98,724),(103,711),(114,706),(124,710),(128,718),(132,726),(129,729),(130,733),(127,735),(126,739),(119,743),(110,743)],t=.45)
add('occ',head)
add('thin',"M118 723l10 1M108 721q-4 4 0 9M124 737h-3")                                                     # glasses, ear, mouth
add('occ',smooth([(98,722),(102,710),(113,704),(124,707),(129,714),(119,714),(106,717)],t=.45))             # cap crown
add('occ',smooth([(124,712),(142,719),(140,723),(126,718)],t=.2))                                            # brim
JOINT='#7EC8E3'
out='<svg viewBox="0 30 500 960" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
for kind,d in LAYERS:
    if not d: continue
    if kind=='occ': out+=f'<path class="occ" stroke-width="1.6" d="{d}"/>'
    elif kind=='line': out+=f'<path stroke-width="1.6" d="{d}"/>'
    elif kind=='thin': out+=f'<path stroke-width="1" opacity=".6" d="{d}"/>'
    elif kind=='joint_occ': out+=f'<path class="occ" stroke="{JOINT}" stroke-width="1.6" d="{d}"/>'
    elif kind=='joint_line': out+=f'<path stroke="{JOINT}" stroke-width="1.6" d="{d}"/>'
    elif kind=='joint_thin': out+=f'<path stroke="{JOINT}" stroke-width="1" opacity=".75" d="{d}"/>'
out+='</svg>'
open('ur.svg','w').write(out); print(len(out),'grip',GX+32,GY,'chuck',CH)
