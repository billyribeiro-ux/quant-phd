"""LX1-a r1 independent recomputation of L01 prose numbers (Fraction and Decimal, not the lab code)."""
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import math
getcontext().prec = 50

def rhu(x):
    return math.floor(x + Fr(1, 2))

d1, r, g, g1 = Fr(400), Fr(9, 100), Fr(3, 100), Fr(1, 100)
F0 = d1 / (r - g)
q = (1 + g) / (1 + r)
print("F0", F0, float(F0), "rounded", rhu(F0), "q", q, float(q))
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    res = F0 * q ** N
    print("N", N, "S_N rounded", rhu(S), "identity", S == F0 * (1 - q ** N), "F0 q^N", float(res), "rounded", rhu(res))
# independent Decimal check of F0*q^10
qd = Decimal(103) / Decimal(109)
print("Decimal F0*q^10 =", Decimal(20000) / Decimal(3) * qd ** 10)
print("Decimal F0*q^60 =", Decimal(20000) / Decimal(3) * qd ** 60)
print("Decimal F0*q^200 =", Decimal(20000) / Decimal(3) * qd ** 200)
# fundamental path t=0..12 at g=3%
for t in range(13):
    f = d1 * (1 + g) ** t / (r - g)
    print("t", t, "fund", float(f), rhu(f))
print("q-threshold g*", Fr(9, 100) - Fr(400, 6000), float(Fr(9,100)-Fr(400,6000)))
print("prop2.2 F0(1%)", d1 / (r - g1), "F0(3%)", float(F0), "gap1", 6000 - d1 / (r - g1), "gap3", float(6000 - F0))
print("prose 400/1.09", float(Fr(400)/Fr(109,100)), "40000/109", float(Fr(40000,109)))
print("1.03^2 *400/0.06", float(Fr(400)*Fr(103,100)**2/Fr(6,100)))
print("250 Mech1", Fr(250)/Fr(6,100), float(Fr(250)/Fr(6,100)), "Mech2 F3", Fr(250)*Fr(104,100)**3/Fr(6,100), float(Fr(250)*Fr(104,100)**3/Fr(6,100)))
print("1.04^3", Fr(104,100)**3)
print("Mech3 S10", float(sum(Fr(100)*Fr(1)/Fr(105,100) for _ in range(10))), "20000/21", float(Fr(20000,21)))
print("9/13", round(9/13, 4), "2175/8698", float(Fr(2175, 8698)), "pct", round(float(Fr(2175,8698))*100, 2))
print("Pi check: 1000/1.05", float(Fr(1000)/Fr(105,100)))
print("lab threshold 2.33", float(Fr(9,100)-Fr(1,15)))
print("Quiz q2 6666.67", float(F0), "q3 7072.67", float(Fr(400)*Fr(103,100)**2/Fr(6,100)))
print("q5 0.023333", float(Fr(9,100)-Fr(400,6000)), "q4 103/109", float(q))
