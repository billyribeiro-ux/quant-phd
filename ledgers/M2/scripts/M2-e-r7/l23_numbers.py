# Independent re-derivation of L23 numbers (exact Fractions and Decimal, no lab code).
from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 80
N = 10
c = {t: (5000 + (100000 if t == 10 else 0)) for t in range(1, N + 1)}
def P(y):  # y as Fraction
    return sum(F(c[t]) / (1 + y) ** t for t in range(1, N + 1))
def P1(y):
    return sum(F(t * c[t]) / (1 + y) ** (t + 1) for t in range(1, N + 1)) * -1
def P2(y):
    return sum(F(t * (t + 1) * c[t]) / (1 + y) ** (t + 2) for t in range(1, N + 1))
def P3(y):
    return -sum(F(t * (t + 1) * (t + 2) * c[t]) / (1 + y) ** (t + 3) for t in range(1, N + 1))
y0 = F(4, 100)
p0 = P(y0); d1 = P1(y0); d2 = P2(y0)
print("P(0.04) =", float(p0), "P'=", float(d1), "P''=", float(d2))
print("-P'/P =", float(-d1 / p0), "P''/P =", float(d2 / p0))
# float sensitivities as the lab uses
print("P'(0.04) float", float(d1), "P''(0.04) float", float(d2))
def T1(dy):
    return p0 + F(float(d1)) * dy
def T2(dy):
    return T1(dy) + F(1, 2) * F(float(d2)) * dy * dy
for dy in [F(1, 100), F(5, 1000), F(25, 10000)]:
    e1 = P(y0 + dy) - T1(dy)
    e2 = P(y0 + dy) - T2(dy)
    print("dy", float(dy), "e1", float(e1), "e2", float(e2))
# ratios, using exact rational errors
es = []
for dy in [F(1, 100), F(5, 1000), F(25, 10000)]:
    es.append((P(y0 + dy) - T1(dy), P(y0 + dy) - T2(dy)))
print("ratio1", float(es[0][0] / es[1][0]), float(es[1][0] / es[2][0]))
print("ratio2", float(es[0][1] / es[1][1]), float(es[1][1] / es[2][1]))
for dy in [F(1, 100), F(-1, 100)]:
    ex = P(y0 + dy)
    print("shift", float(dy), "exact unrounded", float(ex), "second-order unrounded", float(T2(dy)), "diff", float(ex - T2(dy)))
# Part D checks from the text: float 0.04+0.01 vs 0.05
s = 0.04 + 0.01
print("float 0.04+0.01 =", repr(s), "exact minus 1/20 =", float(F(s) - F(1, 20)), "as Decimal:", Decimal(s) - Decimal(1) / Decimal(20))
print("P'(0.05) =", float(P1(F(1, 20))), "P(0.05) =", float(P(F(1, 20))))
print("P'(0.05)*offset =", float(P1(F(1, 20)) * (F(s) - F(1, 20))))
print("Price at 0.05 exact:", P(F(1, 20)))
# quiz: c1=-1, c2=1000, N=2, y=0.04
y = F(4, 100)
q = -(1 * F(-1) / (1 + y) ** 2 + 2 * F(1000) / (1 + y) ** 3)
print("quiz P' =", float(q))
# zero-coupon 100 cents at year 2 at y=0
print("zero coupon P'(0) =", float(-200 / (1 + 0) ** 3))
# Problem M1 check
print("M1 terms:", float(F(50) / F(105, 100) + F(1050) / F(105, 100) ** 2))
print("M3 P'(0.04) = -200/1.04^3 =", float(F(-200) / F(104, 100) ** 3))
# P'(0.05) closed-form
print("P'(0.05) float check", float(P1(F(5, 100))))
# 2nd order ratios from float T1/T2 in lab style are checked above
# R1: P'(y) negative; R2 M bound not computed
# Part A central difference checks
import math
