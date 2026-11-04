"""Independent re-derivation of L06 numbers with fractions.Fraction (own code, page formulas only).

Usage: python -I recompute_L06.py. Stdlib only.
"""
from fractions import Fraction as F
import math

def A(r):
    return sum((F(1) / (1 + r) ** t for t in range(1, 4)), F(0))

def npv(u, r, outlay=15_000_000, margin=5_000):
    return -outlay + sum(F(u) * margin / (1 + r) ** t for t in range(1, 4))

def half_up(x, places):
    s = 10 ** places
    return math.floor(x * s + F(1, 2)) / s

print("A(10%) exact", A(F(1, 10)), "= 3310/1331?", A(F(1, 10)) == F(3310, 1331))
for r in (F(8, 100), F(1, 10), F(12, 100)):
    be = F(15_000_000, 5_000) / A(r)
    print("rate", r, "break-even exact", float(be), "2dp", half_up(be, 2), "unrounded 4dp", round(float(be), 4))
    print("   NPV lower(200) exact", float(npv(200, r)), "rounded", half_up(npv(200, r), 0),
          " NPV upper(1600) rounded", half_up(npv(1600, r), 0))
be10 = F(399300, 331)
print("399300/331 exact check", be10 == F(15_000_000, 5_000) / A(F(1, 10)))
print("NPV(1200) at 10% exact", npv(1200, F(1, 10)), "=", float(npv(1200, F(1, 10))))
print("NPV(1300) at 10% exact", npv(1300, F(1, 10)), "=", float(npv(1300, F(1, 10))))
print("NPV(1200) 2dp", half_up(npv(1200, F(1, 10)), 2), " NPV(1300) 2dp", half_up(npv(1300, F(1, 10)), 2))
# grid
grid = list(range(200, 1601, 100))
pos = [u for u in grid if npv(u, F(1, 10)) > 0]
neg = [u for u in grid if npv(u, F(1, 10)) < 0]
print("grid positive", pos, "count", len(pos), "largest negative", max(neg))
# E3 differences from unrounded values
b8 = float(F(15_000_000, 5_000) / A(F(8, 100)))
b10 = float(F(15_000_000, 5_000) / A(F(1, 10)))
b12 = float(F(15_000_000, 5_000) / A(F(12, 100)))
print("unrounded", round(b8, 4), round(b10, 4), round(b12, 4))
print("width 8->12", round(b12 - b8, 4), "avg per point", round((b12 - b8) / 4, 4))
print("8->10", round(b10 - b8, 4), "10->12", round(b12 - b10, 4))
print("displayed difference 1249.05-1206.34 =", round(1249.05 - 1206.34, 2))
# E1: annuity at 12%
print("E1 annuity 12% float", float(A(F(12, 100))), "break-even", float(F(3000) / A(F(12,100))))
# Remark 4.3 change
print("change 8->10 and 10->12 two decimals", round(b10 - b8, 2), round(b12 - b10, 2))
# R3 margin
m_star = F(15_000_000) / (F(1600) * A(F(1, 10)))
print("R3 m* exact float", float(m_star), "ratio", float(m_star / 5000), "fall %", float((1 - m_star / 5000) * 100))
# M3
print("M3 u*", F(100000, 400) / A(F(1, 10)), float(F(100000, 400) / A(F(1, 10))))
# P1/Prop 1.1 spot checks not needed; M2
print("M2 NPV", -100 + F(60) / F(11, 10) + F(60) / F(11, 10) ** 2, float(-100 + F(60) / F(11, 10) + F(60) / F(11, 10) ** 2))
# Misconception: average slope
print("slope avg", (b12 - b8) / 4)
# Fermi ratios
print("log ratios", math.log(4000 / 2000), math.log(2 / 1), math.log((1/5) / (1/10)))
# Part 1
D = F(97, 100)
print("F=", F(9700) / D)
