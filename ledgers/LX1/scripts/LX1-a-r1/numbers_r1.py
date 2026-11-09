"""Independent Fraction recomputation of every number changed in the L01/L02 delta."""
from fractions import Fraction as Fr
import math

def rhu(x):
    return math.floor(x + Fr(1, 2))

r, g = Fr(9, 100), Fr(3, 100)
d1 = 400
F0 = Fr(d1) / (r - g)
print("F0 =", F0, "=", float(F0), "rounded", rhu(F0))
q = (1 + g) / (1 + r)
print("q =", q)
# Prop 2.2 witness
F_1 = Fr(d1) / (r - Fr(1, 100))
F_3 = Fr(d1) / (r - Fr(3, 100))
print("F0(1%) =", F_1, " F0(3%) =", F_3, float(F_3))
print("gap at 6000 under 1%:", 6000 - F_1, " under 3%:", 6000 - F_3, float(6000 - F_3))
# canon-breaks: d1=400, d2=0, ds=0 for s>=3, r=9%
pv = Fr(400) / (1 + r)
print("PV single dividend =", pv, "=", float(pv), "rounded", rhu(pv))
# misconception 3: g=10%, r=9%
print("closed form at g=10%:", Fr(400) / (Fr(9, 100) - Fr(10, 100)))
# Mech 3: d1=100, r=g=5%, S_10
s10 = sum(Fr(100) * ((Fr(105, 100)) ** 0 * 1) / (1 + Fr(5, 100)) for _ in range(10))
print("S10 (q=1) =", s10, "=", float(s10), "; 20000/21 =", Fr(20000, 21), float(Fr(20000, 21)))
# Research 1: g*
gstar = Fr(9, 100) - Fr(400, 6000)
print("g* =", gstar, float(gstar), "percent:", float(gstar * 100))
# Lab L01 Part A checks
for n in (10, 60, 200):
    sn = sum(Fr(d1) * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, n + 1))
    print("N", n, "S_N rounded", rhu(sn), "identity", sn == F0 * (1 - q ** n), "F0 q^N rounded", rhu(F0 * q ** n))
# Quiz 6: each discounted term at least d1/(1+r)
print("d1/(1+r) =", Fr(d1) / (1 + r), float(Fr(d1) / (1 + r)))
# Proof 3 / Prop 1.4: q>=1 when g>=r
print("q>=1 when g=r:", ((1 + r) / (1 + r)) >= 1)
