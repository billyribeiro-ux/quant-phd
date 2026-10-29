"""Independent recomputation of the numbers printed in E3 slice a (L01-L03 prose and lab outputs)."""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def half_up(x):
    return int(Decimal(repr(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP))

# L02 Example 1.5
EU = 0.25*math.sqrt(40) + 0.5*math.sqrt(100) + 0.25*math.sqrt(160)
CE = EU*EU
print("L02 Ex1.5 EU", round(EU, 6), "CE", round(CE, 6), "premium", round(100-CE, 6), "cents CE", half_up(CE*100) if False else half_up(CE*100), "premium cents", half_up((100-CE)*100))

# L02 lab: X in {-60,0,60} p 1/4,1/2,1/4; w=100
var = F(1,4)*3600 + F(1,4)*3600
print("var", var)
def ce_sqrt(eps):
    e = sum(float(p)*math.sqrt(100+eps*float(x)) for x, p in [(-60,F(1,4)),(0,F(1,2)),(60,F(1,4))])
    return e*e
def ce_lin(eps):
    return sum(float(p)*(100+eps*float(x)) for x,p in [(-60,F(1,4)),(0,F(1,2)),(60,F(1,4))])
r_a = 1/(2*100)
approx = 0.5*r_a*float(var)
print("approx", approx, "pratt error at eps1", (100-ce_sqrt(1.0))-approx, "pct of premium", ((100-ce_sqrt(1.0))-approx)/(100-ce_sqrt(1.0))*100, "pct of approx", ((100-ce_sqrt(1.0))-approx)/approx*100)
print("ce cents eps1", half_up(ce_sqrt(1.0)*100), "premium cents", half_up((100-ce_sqrt(1.0))*100))
for eps in (1.0,0.5,0.25,0.1,0.01):
    ratio = (100-ce_sqrt(eps))/eps**2
    print("eps", eps, "ratio", round(ratio,6), "gap", round(abs(ratio-4.5),6))
print("linear premium", 100-ce_lin(1.0), 100-ce_lin(0.5), 100-ce_lin(0.1))
print("half variance", 0.5*float(var), "ratio to exact", 0.5*float(var)/(100-ce_sqrt(1.0)))

# L03 lab: prizes 5000,10000,20000 p 1/4,1/2,1/4
prizes=[5000,10000,20000]; probs=[0.25,0.5,0.25]
def ce(g):
    if g==1.0: return math.exp(sum(p*math.log(x) for p,x in zip(probs,prizes)))
    s=1-g
    return sum(p*x**s for p,x in zip(probs,prizes))**(1/s)
for g in (0,0.25,0.5,1,2,4):
    print("gamma", g, "CE", f"{ce(g):.4f}", "rounded", half_up(ce(g)))
print("gamma2 exact", 1/(0.25/5000+0.5/10000+0.25/20000), 80000/9)
print("falls", all(ce(a)>=ce(b) for a,b in zip((0,0.25,0.5,1,2),(0.25,0.5,1,2,4))))
# L03 M1 mech-1 (gamma 1/2 at w=4)
u=lambda w: (w**0.5-1)/0.5
h=1e-6
print("mech1 r_A(4)=", 0.5/4, "numeric", -((u(4+h)-2*u(4)+u(4-h))/h**2)/((u(4+h)-u(4-h))/(2*h)))
# L02 E1: gap at 0.1 and factor
print("E1 gap", 4.504565-4.5, "factor 0.028811/0.004565", 0.028811/0.004565, "eps^2 ratio", (0.25/0.1)**2)
# L02 E2 numbers
print("E2", 0.565835/5.065835, 0.565835/4.5)
# L01 numbers
print("L01 A EU", sum(float(p)*x for x,p in [(0,F(1,4)),(100,F(1,2)),(400,F(1,4))]))
