"""Independent recomputation of the L05 Lab 1 numbers and the exact derivations (Fraction where exact)."""
import math
import random
from fractions import Fraction

rng = random.Random(2026)
years = [[rng.randint(-100000, 100000) for _ in range(12)] for _ in range(2000)]
minima = []
for y in years:
    s = 0
    lo = None
    for x in y:
        s += x
        lo = s if lo is None else min(lo, s)
    minima.append(lo)
for B in (0, 250000, 500000, 750000, 1000000, 1200000):
    c = sum(1 for m in minima if m < -B)
    p = Fraction(c, 2000)
    se = math.sqrt(float(p) * (1 - float(p)) / 2000)
    print("B", B, "count", c, "freq", f"{float(p):.4f}", "se", f"{se:.4f}")
srt = sorted(minima)
k = -((-5 * 2000) // 100)
q = srt[k - 1]
print("k", k, "q05", q, "cover", -q, "count_at_cover", sum(1 for m in minima if m < q), "freq", f"{sum(1 for m in minima if m < q)/2000:.4f}")
print("mean minima", f"{sum(minima)/2000:.2f}")
print("count_at_1200000", sum(1 for m in minima if m < -1200000))
# M2 exact
p = Fraction(356, 2000)
v = p * (1 - p) / 2000
print("M2 p(1-p)", p * (1 - p), "over2000", float(v), "sqrt", math.sqrt(float(v)), "round4", round(math.sqrt(float(v)), 4))
# R3
pp = Fraction(356, 2000)
print("R3 N_Y exact", (pp * (1 - pp)) / Fraction(2, 1000) ** 2, "ratio 0.0086/0.002", 0.0086 / 0.002)
# E1, E2, E3
print("E1 1676-356", 1676 - 356, "E2", Fraction(365525, 100), "99/2000", Fraction(99, 2000))
print("E3 750000-800000", 750000 - 800000)
