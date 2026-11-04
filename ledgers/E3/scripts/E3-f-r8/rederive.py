import math
from fractions import Fraction as F
# L02 Example 1.5
EW = 0.25*40+0.5*100+0.25*160
Eu = 0.25*math.sqrt(40)+0.5*math.sqrt(100)+0.25*math.sqrt(160)
CE = Eu**2
print("L02 Ex1.5 E sqrtW", repr(Eu), "CE", repr(CE), "premium", repr(100-CE), "ce_cents", math.floor(CE*100+0.5), "prem_cents", math.floor((100-CE)*100+0.5))
# L02 lab: gamble X in {-60,0,60} p 1/4,1/2,1/4; w=100
X=[(-60,0.25),(0,0.5),(60,0.25)]
var=sum(p*x*x for x,p in X); print("var", var)
def ce_sqrt(eps):
    Eu=sum(p*math.sqrt(100+eps*x) for x,p in X)
    return Eu**2  # inverse of sqrt
for eps in (1.0,0.5,0.25,0.1,0.01):
    c=ce_sqrt(eps); prem=100-c
    print("eps",eps,"ce",repr(c),"prem",repr(prem),"prem/eps^2",repr(prem/eps**2),"gap",repr(prem/eps**2-4.5))
print("pratt 0.5*rA*var", 0.5*0.005*var)
print("ce_cents", math.floor(ce_sqrt(1.0)*100+0.5), "prem_cents", math.floor((100-ce_sqrt(1.0))*100+0.5))
print("err share", (100-ce_sqrt(1.0)-4.5)/(100-ce_sqrt(1.0)), (100-ce_sqrt(1.0)-4.5)/4.5)
# L03 lab
prizes=(5000,10000,20000); probs=(0.25,0.5,0.25)
def ce(g):
    if g==1.0: return math.exp(sum(p*math.log(x) for p,x in zip(probs,prizes)))
    s=1-g
    return sum(p*x**s for p,x in zip(probs,prizes))**(1/s)
for g in (0.0,0.25,0.5,1.0,2.0,4.0):
    c=ce(g); print("gamma",g,"ce %.4f"%c, "rounded", math.floor(c+0.5))
print("harmonic", 1/sum(p/x for p,x in zip(probs,prizes)), 80000/9)
print("M gamma2 check", sum(p/x for p,x in zip(probs,prizes)), 9/80000)
print("L03 E2 check", 0.25/5000+0.5/10000+0.25/20000)
print("L03 M2", 0.25/1000+0.75/9000, 1/3000, "CE", 1/(0.25/1000+0.75/9000))
print("L03 M3", 1/(0.25/3000+0.75/27000))
print("Ex2.5 gamma2", 1/(0.5/1000+0.5/4000), "gamma1", math.exp(0.5*math.log(1000)+0.5*math.log(4000)))
print("R1 unrounded diff", "n/a")
print("L03 E1 10615.8009 ->", math.floor(10615.8009+0.5))
print("L03 interp 10931.7733 check", ce(0.25), ce(0.5), ce(4.0))
# L04 Example 2.5 integrated values
def I(pmf,t,S):
    return sum(p*max(t-x,0) for x,p in pmf)
X=[(2000,0.5),(4000,0.5)]; Y=[(1000,0.25),(3000,0.5),(5000,0.25)]
print("I_X", [I(X,t,None) for t in (1000,2000,3000,4000,5000)])
print("I_Y", [I(Y,t,None) for t in (1000,2000,3000,4000,5000)])
# Example 2.6
X6=[(1000,0.5),(5000,0.5)]; Y6=[(3000,1.0)]
print("I_X6", [I(X6,t,None) for t in (1000,3000,5000)], "I_Y6", [I(Y6,t,None) for t in (1000,3000,5000)])
# Example 1.5 lab check (L01)
print("L01 A eu quad", 0*0.25+10000*0.5+40000*0.25)
