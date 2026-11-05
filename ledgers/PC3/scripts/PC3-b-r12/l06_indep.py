"""Independent recomputation of every L06 number (stdlib only; does not import lab code).

Usage: python -I l06_indep.py
"""
from fractions import Fraction as F
import statistics

def annuity(r, n=3):
    return sum(F(1) / (1 + r) ** t for t in range(1, n + 1))

def npv(cfs, r):
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))

I, m = 15_000_000, 5_000
A10 = annuity(F(1, 10))
print("A(10%) =", A10, float(A10), "expected 3310/1331:", A10 == F(3310, 1331))
be10 = F(I, m) / A10
print("u*(10%) =", be10, float(be10), "== 399300/331:", be10 == F(399300, 331))
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A = annuity(r)
    be = F(I, m) / A
    lo = npv([F(-I)] + [F(200) * m] * 3, r)
    hi = npv([F(-I)] + [F(1600) * m] * 3, r)
    print(f"r={float(r)*100:.0f}%: A={float(A):.9f} u*={float(be):.6f} NPV(200)={float(lo):.4f} NPV(1600)={float(hi):.4f}")
    print("   half-up whole cents NPV(200), NPV(1600):",
          int((lo + F(1, 2)).__floor__()), int((hi + F(1, 2)).__floor__()), "break-even 2dp:", float(be))
# Remark 4.3 numbers
b8 = F(I, m) / annuity(F(8, 100)); b10 = be10; b12 = F(I, m) / annuity(F(12, 100))
print("unrounded: 8%", float(b8), "10%", float(b10), "12%", float(b12))
print("diff 10-8:", float(b10 - b8), "diff 12-10:", float(b12 - b10), "avg slope:", float((b12 - b8) / 4))
print("printed diffs 1206.34-1164.10 =", round(1206.34 - 1164.10, 2), "1249.05-1206.34 =", round(1249.05 - 1206.34, 2))
# Example 4.2 bounds of units and NPV signs
print("NPV(200)=", float(npv([F(-I)] + [F(200 * m)] * 3, F(1, 10))), "exact", npv([F(-I)] + [F(200 * m)] * 3, F(1, 10)))
print("NPV(1600)=", float(npv([F(-I)] + [F(1600 * m)] * 3, F(1, 10))))
# E2 grid
grid = [F(u) for u in range(200, 1601, 100)]
pos = [u for u in grid if npv([F(-I)] + [u * m] * 3, F(1, 10)) > 0]
neg = [u for u in grid if npv([F(-I)] + [u * m] * 3, F(1, 10)) < 0]
print("grid positive count", len(pos), [int(u) for u in pos], "largest negative", int(max(neg)))
v1200 = npv([F(-I)] + [F(1200 * m)] * 3, F(1, 10)); v1300 = npv([F(-I)] + [F(1300 * m)] * 3, F(1, 10))
print("NPV(1200) exact", v1200, "== -105000000/1331:", v1200 == F(-105000000, 1331), float(v1200))
print("NPV(1300) exact", v1300, "== 1550000000/1331:", v1300 == F(1550000000, 1331), float(v1300))
# E1 at 12%
print("E1 annuity 12% =", float(annuity(F(12, 100))), "break-even", float(F(3000) / annuity(F(12, 100))))
# R3 margin
mstar = F(I) / (1600 * annuity(F(1, 10)))
print("R3 m* =", float(mstar), "fraction of 5000 =", float(mstar / 5000), "fall % =", float((1 - mstar / 5000) * 100))
# M3
print("M3 u* =", F(100000, 400) / annuity(F(1, 10)), float(F(100000, 400) / annuity(F(1, 10))), "== 33275/331:",
      F(100000, 400) / annuity(F(1, 10)) == F(33275, 331))
# M2
print("M2 NPV at 10% of -100,60,60 =", npv([F(-100), F(60), F(60)], F(1, 10)), "about", float(npv([F(-100), F(60), F(60)], F(1, 10))))
# E3 values
print("E3 width", float(F(1249.0469) - F(1164.1005)) if False else "", float(b12 - b8))
# Fermi product bounds
print("P3 bounds", F(2000) * 1 * F(1, 10), F(4000) * 2 * F(1, 5))
print("NPV at 1600 rate 8% printed 5616776? recompute:", round(float(npv([F(-I)] + [F(1600 * m)] * 3, F(8, 100)))))
print("E3 average slope 2dp:", round(float((b12 - b8) / 4), 2), "8-10 diff 2dp:", round(float(b10 - b8), 2), "10-12 diff 2dp:", round(float(b12 - b10), 2))
# Remark 4.3: NPV at 1200 units and 8% (card c124)
print("card c124 NPV(1200, 8%) =", float(npv([F(-I)] + [F(1200 * m)] * 3, F(8, 100))))
# z-value for the L04 E2 critical value
print("z 0.975 =", statistics.NormalDist().inv_cdf(0.975))
