from fractions import Fraction as F
import math
def rh(x): return math.floor(x + F(1,2))
out=[]
def chk(name, got, want):
    out.append((name, got==want, got, want))
# L04 base
yL,yH,cL,cH=4_000_000,6_000_000,1_000_000,500_000
def wage(e,t): return yH if e>=t else yL
def U(c,e,t): return wage(e,t)-c*e
def sep(t,yH=yH,cL=cL,cH=cH):
    G=range(7)
    hi=U(cH,t,t)==max(U(cH,e,t) for e in G) if True else None
    return t>0 and hi and U(cL,0,t)==max(U(cL,e,t) for e in G)
def wage2(e,t,yH=yH): return yH if e>=t else yL
S=[t for t in range(7) if t>0 and  (lambda t: (wage(t,t)-cH*t)==max(wage(e,t)-cH*e for e in range(7)) and (wage(0,t)-0)==max(wage(e,t)-cL*e for e in range(7)))(t)]
chk("L04 base separating set", S, [2,3,4])
chk("L04 t=1 utility at e=1 (low)", U(cL,1,1), 5_000_000)
chk("L04 t=5 high u at t vs best", (U(cH,5,5), max(U(cH,e,5) for e in range(7))), (3_500_000,4_000_000))
chk("L04 t=6 high u", U(cH,6,6), 3_000_000)
chk("L04 least-cost utility", U(cH,2,2), 5_000_000)
chk("L04 e1 c_H=400k separating", [t for t in range(7) if t>0 and (wage(t,t)-400_000*t)==max(wage(e,t)-400_000*e for e in range(7)) and wage(0,t)==max(wage(e,t)-cL*e for e in range(7))], [2,3,4,5])
yH2=5_000_000
def w2(e,t): return yH2 if e>=t else yL
chk("L04 e2 yH=5M separating", [t for t in range(1,7) if (w2(t,t)-cH*t)==max(w2(e,t)-cH*e for e in range(7)) and yL==max(w2(e,t)-cL*e for e in range(7))], [1,2])
chk("L04 m1 upper", F(2_000_000,250_000), 8)
chk("L04 m3 interval", (F(1_500_000,1_000_000),F(1_500_000,500_000)), (F(3,2),3))
# L05
th_L,th_H=3000,6000; pL,pH=F(3,4),F(1,4)
qL=th_L-pH/pL*(th_H-th_L); chk("L05 qL*", qL, 2000)
mL=th_L*qL; mH=th_H*6000-(th_H-th_L)*qL
def prof(qL,qH):
    mL=th_L*qL; mH=th_H*qH-(th_H-th_L)*qL
    return pL*(mL-F(qL)**2/2)+pH*(mH-F(qH)**2/2)
chk("L05 profit", prof(2000,6000), 6_000_000)
fb=pL*(F(3000)*3000-F(3000)**2/2)+pH*(F(6000)*6000-F(6000)**2/2)
chk("L05 first best", fb, 7_875_000)
chk("L05 gap", fb-prof(2000,6000), 1_875_000)
chk("L05 remark2.1 low part", pL*(F(4_500_000)-F(4_000_000)), 375_000)
chk("L05 remark2.1 high part", pH*6_000_000, 1_500_000)
chk("L05 FOC", pL*(th_L-2000), pH*(th_H-th_L))
chk("L05 pct loss", round(float(1_875_000/7_875_000*100),2), 23.81)
chk("L05 pct first over menu", round(float((7_875_000/6_000_000-1)*100),2), 31.25)
# grid low-type optimum at pH=1/3, qH=6000
pL2,pH2=F(2,3),F(1,3)
def prof2(qL,qH=6000):
    mL=th_L*qL; mH=th_H*qH-(th_H-th_L)*qL
    return pL2*(mL-F(qL)**2/2)+pH2*(mH-F(qH)**2/2)
best=max(range(0,6001), key=lambda q:(prof2(q),-q))
chk("L05 e1 best qL", best, 1500)
chk("L05 e1 profit at 1500", prof2(1500), 6_750_000)
chk("L05 e1 menu at 2000 rounded", rh(prof2(2000)), 6_666_667)
fb2=pL2*(F(3000)*3000-F(3000)**2/2)+pH2*(F(6000)*6000-F(6000)**2/2)
chk("L05 e1 fb", fb2, 9_000_000)
chk("L05 e1 gap at 2000", rh(fb2-prof2(2000)), 2_333_333)
chk("L05 e1 gap at 1500", fb2-prof2(1500), 2_250_000)
chk("L05 m2 mH", 36_000_000-3_000_000, 33_000_000)
chk("L05 m3 profit", pL*(3_000_000-F(1000)**2/2)+pH*(33_000_000-F(6000)**2/2), 5_625_000)
chk("L05 m1 profit", F(1,2)*(36_000_000-F(6000)**2/2), 9_000_000)
# L06
EH=F(3,4)*1_000_000; EL=F(1,4)*1_000_000; cHc=100_000
def pr(b): 
    uh=b*EH-cHc; ul=b*EL
    if uh>=ul and uh>=0: return EH-b*EH,'high',uh
    if ul>=0: return EL-b*EL,'low',uh
    return F(0),'refuse',uh
grid=[F(k,100) for k in range(101)]
bb=max(grid,key=lambda b:(pr(b)[0],-b))
chk("L06 best share", bb, F(1,5))
chk("L06 best profit", pr(bb)[0], 600_000)
chk("L06 share .30 profit", pr(F(3,10))[0], 525_000)
chk("L06 m1 uh", F(1,4)*EH-cHc, 87_500)
chk("L06 m1 profit", pr(F(1,4))[0], 562_500)
chk("L06 m2 uh 2/15", F(2,15)*EH-cHc, 0)
chk("L06 m3 profit", EH-(10_000+F(1,5)*EH), 590_000)
chk("L06 p1 uh", -1_000_000+F(1,2)*EH-cHc, -725_000)
chk("L06 p1 ul", -1_000_000+F(1,2)*EL, -875_000)
chk("L06 e1 best", max(grid,key=lambda b: (EH*(1-b) if b>=F(3,10) else EL*(1-b), -b)), F(3,10))
chk("L06 e2 profit", rh(F(800_000)*F(5,6)), 666_667)
chk("L06 e2 beta bound", F(100_000,600_000), F(1,6))
chk("L06 C part alpha .5", cHc-F(1,2)*EH, -275_000)
chk("L06 C part alpha 1", cHc-EH, -650_000)
chk("L06 C profit b=.2", EH-((cHc-F(1,5)*EH)+F(1,5)*EH), 650_000)
for name,g,got,want in out:
    print("PASS" if g else "FAIL", name, "" if g else f"got={got!r} want={want!r}")
print("ALL", all(g for _,g,_,_ in out), len(out))
