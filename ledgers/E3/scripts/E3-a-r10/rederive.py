from fractions import Fraction as F
from decimal import Decimal, getcontext
import math
getcontext().prec = 50
# L02 Example 1.5
EU = Decimal(1)/4*Decimal(40).sqrt() + Decimal(1)/2*Decimal(100).sqrt() + Decimal(1)/4*Decimal(160).sqrt()
print("L02 Ex1.5 E sqrt W =", str(EU)[:12])
CE = EU*EU
print("CE =", str(CE)[:14], "premium =", str(100-CE)[:12])
# L02 Part B: sqrt utility, W = 100 + eps X, X = -60,0,60 w.p. 1/4,1/2,1/4
def ce_sqrt(eps):
    e = Decimal(0)
    for x,p in [(-60,Decimal(1)/4),(0,Decimal(1)/2),(60,Decimal(1)/4)]:
        e += p*Decimal(100+eps*x).sqrt()
    return e*e
limit = Decimal(1)/2 * (Decimal(1)/(2*100)) * 1800
print("limit", limit)
for eps in (Decimal(1), Decimal("0.5"), Decimal("0.25"), Decimal("0.1"), Decimal("0.01")):
    prem = 100 - ce_sqrt(eps)
    r = prem/(eps*eps)
    print("eps", eps, "ratio", round(r,6), "gap", round(abs(r-limit),6))
# L03 CE values for lottery 5000,10000,20000 w.p. 1/4,1/2,1/4
P = [Decimal(1)/4, Decimal(1)/2, Decimal(1)/4]
X = [5000,10000,20000]
for g in ["0","0.25","0.5","1","2","4"]:
    g = Decimal(g)
    if g == 1:
        ce = (sum(p*Decimal(x).ln() for p,x in zip(P,X))).exp()
    else:
        s = 1-g
        M = sum(p*(Decimal(x)**s) for p,x in zip(P,X))
        ce = M**(1/s)
    print("gamma", g, "CE", round(ce,4), "half-up cents", int((ce+Decimal("0.5")).to_integral_value(rounding="ROUND_FLOOR")))
print("80000/9 =", Decimal(80000)/9)
M = sum(p/Decimal(x) for p,x in zip(P,X)); print("M =", M, "1/M =", 1/M, "9/80000=", Decimal(9)/80000)
# L02 Example 2.3 at w=100
print("r_A(100)=", 1/(2*100))
# 2.5 of L03
print("CE at scale 10, 10*CE(X) bound check not needed")
