# Independent recomputation for L23 and L22 numbers. Does not import the lab twins.
import math
from decimal import Decimal, getcontext
from fractions import Fraction as Fr
getcontext().prec = 80

def cf(t):
    return 5000 + (100000 if t == 10 else 0)

def P(y):
    v = 1 + y
    return sum(Fr(cf(t)) / v**t for t in range(1, 11))

def P1(y):
    v = 1 + y
    return -sum(Fr(t * cf(t)) / v**(t + 1) for t in range(1, 11))

def P2(y):
    v = 1 + y
    return sum(Fr(t * (t + 1) * cf(t)) / v**(t + 2) for t in range(1, 11))

def P3(y):
    v = 1 + y
    return -sum(Fr(t * (t + 1) * (t + 2) * cf(t)) / v**(t + 3) for t in range(1, 11))

y0 = Fr(4, 100)
p0 = P(y0)
print("P(0.04) exact-rational float", float(p0), "rounded cents", round(p0))
print("P(0.04) decimal 60 digits", Decimal(p0.numerator) / Decimal(p0.denominator))
print("P'(0.04)", float(P1(y0)), " P''(0.04)", float(P2(y0)), " P'''(0.04)", float(P3(y0)))
print("-P'/P =", float(-P1(y0) / p0), " P''/P =", float(P2(y0) / p0))
# printed closed forms from floats as the lab computes them
pf1 = float(P1(Fr(0.04)))
pf2 = float(P2(Fr(0.04)))
print("float closed forms P' %.6f P'' %.6f" % (pf1, pf2))
# shifts
for dy in (Fr(1, 100), Fr(5, 1000), Fr(25, 10000), Fr(-1, 100)):
    ex = P(y0 + dy)
    e1 = ex - (p0 + P1(y0) * dy)
    e2 = ex - (p0 + P1(y0) * dy + Fr(1, 2) * P2(y0) * dy * dy)
    print("dy", float(dy), "e1 %.6e e2 %.6e" % (float(e1), float(e2)))
# ratios
ex = {}
for dy in (Fr(1, 100), Fr(5, 1000), Fr(25, 10000)):
    ex[dy] = (P(y0 + dy) - (p0 + P1(y0) * dy), P(y0 + dy) - (p0 + P1(y0) * dy + Fr(1, 2) * P2(y0) * dy * dy))
ks = [Fr(1, 100), Fr(5, 1000), Fr(25, 10000)]
for a, b in ((ks[0], ks[1]), (ks[1], ks[2])):
    print("ratio e1 %.4f e2 %.4f" % (float(ex[a][0] / ex[b][0]), float(ex[a][1] / ex[b][1])))
# cents at +/-0.01
for dy in (Fr(1, 100), Fr(-1, 100)):
    exact = P(y0 + dy)
    approx = p0 + P1(y0) * dy + Fr(1, 2) * P2(y0) * dy * dy
    print("shift", float(dy), "exact cents", round(exact), "approx cents", round(approx), "diff", round(exact) - round(approx), "unrounded exact-approx %.4f" % float(exact - approx))
# E3: float yield 0.04+0.01 vs 0.05
yf = 0.04 + 0.01
off = Decimal(yf) - Decimal("0.05")
print("float 0.04+0.01 repr", repr(yf), "exact offset from 0.05 =", off, "%.4e" % float(off))
Pp05 = P1(Fr(1, 20))
print("P'(0.05) =", float(Pp05))
eff = Pp05 * (Fr(yf) - Fr(1, 20))
print("effect on unrounded price = %.4e cents" % float(eff))
print("P(float 0.05) =", float(P(Fr(yf))), " rounded", round(P(Fr(yf))))
print("second-order expansion at 0.05 float =", float(P(Fr(yf))), "approx", float(p0 + P1(y0) * Fr(0.01) + Fr(1, 2) * P2(y0) * Fr(0.01)**2))
# Two cash flows c1 = -1, c2 = 1000 at y = 0.04
c = {1: -1, 2: 1000}
v = 1 + y0
pp = -sum(Fr(t * c[t]) / v**(t + 1) for t in c)
print("two-cash-flow P'(0.04) = %.4f" % float(pp))
# L22 numbers
print("L22 f_xx at a=1.5, x=0.5:", -1.5 / (1.5) ** 2, " half f_xx e^2 with e=1e-8:", 0.5 * (1.5 / 2.25) * 1e-16)
print("sqrt(eps) =", math.sqrt(2.220446049250313e-16))
