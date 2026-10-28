# Independent recomputation for E3 L07-L08 (decimal, 40 digits; fractions where exact).
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
import math
getcontext().prec = 40

def om(p, eta=D("0.5")):
    p = D(p)
    return p**eta / ((p**eta) + ((1 - p)**eta)) ** (1 / eta)

def om_closed(p):
    p = D(p)
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())

print("omega(3/10) =", om(D(3)/10))
print("omega(3/5)  =", om(D(3)/5))
print("omega(1/2)  =", om(D("0.5")), " 1/(2sqrt2)=", 1/(2*D(2).sqrt()))
print("omega(1/4)  =", om_closed(D("0.25")), " 2-sqrt3=", 2-D(3).sqrt())
print("2*omega(3/10)=", 2*om(D(3)/10), " omega(3/5)=", om(D(3)/5))
r = om(D(3)/10)/om(D(3)/5)
print("ratio =", r)
for a in (D(1), D("0.5")):
    thr = 1/(1+D(2)**(-a))
    print("alpha", a, "threshold", thr, "ratio>thr", r > thr)
# weighted values
A = [(0, F(2,5)), (50, F(3,10)), (100, F(3,10))]
B = [(0, F(2,5)), (100, F(3,5))]
def V(L, a):
    return sum((om(D(p.numerator)/p.denominator) * (D(x) ** D(a) if x > 0 else D(0)) for x, p in L), D(0))
for a in (D(1), D("0.5")):
    va, vb = V(A, a), V(B, a)
    print("alpha", a, "V(A)=", va, "V(B)=", vb, "diff=", va-vb)
va, vb = V(A, D(1)), V(B, D(1))
print("printed difference of rounded values:", round(va,4)-round(vb,4), " unrounded diff to 4dp:", (va-vb).quantize(D("0.0001")))
# misconception counterexample
w01, w099 = om(D("0.01")), om(D("0.99"))
print("omega(0.01)=", w01, " omega(0.99)=", w099)
wv = w01*100 + w099*50
ev = D("0.01")*100 + D("0.99")*50
print("weighted", wv, "EV", ev, "net", wv-ev, "over-part", (w01-D("0.01"))*100, "under-part", (D("0.99")-w099)*50)
# crossing of omega(p)=p in (0,1)
lo, hi = D("0.2"), D("0.3")
for _ in range(200):
    mid = (lo+hi)/2
    if om(mid) > mid: lo = mid
    else: hi = mid
print("crossing ~", (lo+hi)/2)
# grid check on 1001 points (floats as in lab)
def omf(p):
    return p**0.5 / (p**0.5 + (1-p)**0.5) ** 2
grid = [i/1000 for i in range(1001)]
interior = grid[1:-1]
above = [omf(p) > p for p in interior]
changes = sum(1 for a,b in zip(above, above[1:]) if a != b)
last = max(p for p in interior if omf(p) > p)
print("grid sign changes", changes, "last above", last)
print("grid 0.279 omega-p", omf(0.279)-0.279)
# M2, M1, M3, lesson 8 numbers
def ce(pairs):  # pairs (prob_red, W_red, W_black)
    return None
W1, W0 = D(110000), D(95000)
def cep(p):  # EU CE, p = P(red)
    return 1/(p/W1 + (1-p)/W0)
print("EU CE at 1/2 =", cep(D("0.5")), " 4180000/41=", D(4180000)/41)
print("M1 CE at 1/4:", cep(D(1)/4), " expected wealth 98750")
print("M2 maxmin {1/4,3/4} = min:", min(cep(D(1)/4), cep(D(3)/4)), " larger prior", cep(D(3)/4))
print("M3 alpha=0 =", 1/(D(3)/4/W1 + D(1)/4/W0))
print("maxmin 1/3:", cep(D(1)/3), " P=2/3", cep(D(2)/3))
print("prem EU", D(102500) - cep(D("0.5")), " in CU", (D(102500)-cep(D("0.5")))/100)
# known and ambiguous urn
Wp, Wl = D(110000), D(100000)
def ceb(p): return 1/(p/Wp + (1-p)/Wl)
print("known red 1/3", ceb(D(1)/3), " known black", ceb(D(2)/3))
print("R2 set 30-60 red worst 1/3 CE", ceb(D(1)/3))
# Model 2 prospect
import math
V2 = 0.5*math.sqrt(100) + 0.5*(-2*math.sqrt(50))
print("prospect V", V2, "inverse", -((-V2/2)**2), "wealth", 100000 + 100*(-((-V2/2)**2)))
print("prospect CE check 2dp:", round(100000 + 100*(-((-V2/2)**2)),2))
# Model 4 extra: alpha-MEU alpha=1/2
g = lambda p: p/W1 + (1-p)/W0
print("alpha-MEU 1/2 CE:", 1/(D(1)/2*g(D(1)/3) + D(1)/2*g(D(2)/3)))
# Prop 1.3 example: EU at midpoint of 30..60
print("mean of k/90 for k in 30..60:", sum(F(k,90) for k in range(30,61))/31)
# premium 102500 - 101951.2195 in cents
print("premium", D(102500)-D(4180000)/41)
# 2dp rounding of quiz answers
print("maxmin 2dp", (1/(D(1)/3/W1 + D(2)/3/W0)).quantize(D("0.01")))
print("EU 1/4 2dp", cep(D(1)/4).quantize(D("0.01")))
print("omega(1/2) 5dp", om(D("0.5")).quantize(D("0.00001")), "omega(1/4) 5dp", om_closed(D("0.25")).quantize(D("0.00001")))
