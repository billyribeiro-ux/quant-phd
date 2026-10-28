"""Independent recomputation of the numbers printed in E3 slice L01-L03 (verifier E3-a round 1).

Uses decimal at 50 significant digits and fractions; no lab code is imported.
"""
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
from fractions import Fraction as F
import math

getcontext().prec = 50

def sqrt(x):
    return D(x).sqrt()

def ln(x):
    return D(x).ln()

def exp(x):
    return D(x).exp()

out = []
def show(name, val):
    out.append(f"{name}: {val}")

# L02 Example 1.5 : W pays 40,100,160 with 1/4,1/2,1/4 ; u = sqrt
EU = D(1)/4*sqrt(40) + D(1)/2*sqrt(100) + D(1)/4*sqrt(160)
CE = EU*EU
show("L02 Ex1.5 EU", EU)
show("L02 Ex1.5 CE", CE)
show("L02 Ex1.5 premium", D(100)-CE)
show("L02 Ex1.5 premium cents half-up", (D(100)-CE)*100)
show("L02 Ex1.5 CE cents", CE*100)

# L02 Part A / Part B quantities: var=1800, rA(100)=0.005, Pratt approx=4.5
var = D(1800)
rA = D("0.005")
approx = D("0.5")*rA*var
show("L02 pratt approx", approx)
prem1 = D(100) - CE_eps1 if False else None
def ce_sqrt(eps):
    e = D(0)
    for x, p in [(-60, D(1)/4), (0, D(1)/2), (60, D(1)/4)]:
        e += p*sqrt(100+eps*x)
    return e*e
for eps in [D(1), D("0.5"), D("0.25"), D("0.1"), D("0.01")]:
    prem = D(100)-ce_sqrt(eps)
    ratio = prem/(eps*eps)
    show(f"L02 PartB eps={eps} premium={prem:.9f} ratio={ratio:.9f} gap={abs(ratio-D('4.5')):.9f}", "")
# L02 misconception: 900/premium
prem1 = D(100)-ce_sqrt(D(1))
show("L02 ratio error share of exact premium (0.565835/5.065835)", (D("0.565835")/prem1))
show("L02 ratio error share, unrounded (exact prem - 4.5)/exact prem", (prem1-D("4.5"))/prem1)
show("L02 E2 error share of approx", (prem1-D("4.5"))/D("4.5"))
show("L02 misc 900/exact premium", D(900)/prem1)
show("L02 E1 gap 0.1 minus 4.5", ce_sqrt(D("0.1")))

# L02 M1: W pays 4 or 16 with 1/2: CE = 9, premium 1
show("L02 M1 EU", D(1)/2*sqrt(4)+D(1)/2*sqrt(16))

# L03 Example 2.5
M2 = D(1)/2*D(1)/1000 + D(1)/2*D(1)/4000
show("L03 Ex2.5 CE_2", 1/M2)
show("L03 Ex2.5 CE_1", exp(D(1)/2*ln(1000)+D(1)/2*ln(4000)))
# L03 lab lottery
P = [D(1)/4, D(1)/2, D(1)/4]; X=[5000,10000,20000]
def ce(g):
    if g == 1:
        return exp(sum(p*ln(x) for p,x in zip(P,X)))
    s = 1-D(g)
    M = sum(p*(D(x)**s) for p,x in zip(P,X))
    return M ** (1/s)
for g in ["0","0.25","0.5","1","2","4"]:
    c = ce(D(g)) if D(g)!=1 else ce(1)
    show(f"L03 lab CE gamma={g}", f"{c:.6f} half-up {(c).quantize(D(1), rounding=ROUND_HALF_UP)}")
show("L03 E1 CE 0.5 cents", ce(D("0.5")))
show("L03 E2 exact 80000/9", D(80000)/9)
show("L03 M2 CE_2 ", D(1)/(D(1)/4/1000 + D(3)/4/9000))
show("L03 M3 CE_2(3X)", D(1)/(D(1)/4/3000 + D(3)/4/27000))
show("L03 E2 M", D(1)/4/5000 + D(1)/2/10000 + D(1)/4/20000)
show("L03 R1 check: (1-p)^(1/s) x2 for p=1/2,x2=100,g=1/2 -> ", (D(1)-D("0.5"))**(1/(1-D("0.5")))*100)
show("L03 E3 (k+1)/2 for k=10", D(11)/2)
show("L03 mech1 r_A(4) for gamma=1/2", D(1)/2/4)

# L01 numbers
A = [(0,F(1,4)),(100,F(1,2)),(400,F(1,4))]
show("L01 Ex1.4 E X", sum(p*x for x,p in A))
show("L01 Ex1.4 E x^2", sum(p*x*x for x,p in A))
show("L01 Ex3.4 C E u(C) quad", sum(F(x*x,1)*p for x,p in [(0,F(1,3)),(150,F(1,3)),(300,F(1,3))]))
show("L01 M1 E X", F(1,5)*20+F(3,10)*50+F(1,2)*80)
show("L01 M1 E x^2", F(1,5)*400+F(3,10)*2500+F(1,2)*6400)
show("L01 M1 u(EX)=59^2", 59*59)
show("L01 M2 E u(L) and E u(M)", (F(1,2)*0+F(1,2)*100, F(1,4)*100+F(3,4)*200))
show("L01 R3 E u X", F(1,2)*100**2+F(1,2)*200**2 )
show("L01 R3 E u Y", 150**2)
show("L01 E1 diff", 45000-37500)

print("\n".join(out))
