"""Round 5 verifier (FC1-c): re-derive every project-page and test-docstring number with exact arithmetic."""
from fractions import Fraction as F
import math

def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w

y4 = F(400, 10000)
ev = [(1, 5000), (2, 5000), (3, 105000)]
pv = sum(F(a) / (1 + y4) ** t for t, a in ev)
print("L1 exact PV", pv, float(pv), "rounded", half_away(pv), "frac", float(pv - math.floor(pv)))
print("L1 trade", -1 * 10 * 9850 * 1)
r = [(1, 500), (2, 500), (3, 10500)]
pv3 = sum(F(a) / (1 + y4) ** t for t, a in r)
print("rounding fixture PV", float(pv3), "once", half_away(pv3), "termwise", sum(half_away(F(a) / (1 + y4) ** t) for t, a in r), [float(F(a) / (1 + y4) ** t) for t, a in r])
print("fixture A", half_away(F(10500) / F(105, 100)), F(10500) / F(105, 100))
print("fixture B exact", float(F(10500) / F(95, 100)), F(210000, 19), float(F(210000, 19)), half_away(F(210000, 19)))
print("fixture C coupon", F(10001 * 5000, 10000), half_away(F(10001 * 5000, 10000)))
print("fixture D coupon", F(1 * 5000, 10000), half_away(F(1 * 5000, 10000)))
print("fixture F price", F(1, 2), half_away(F(1, 2)), round(F(1, 2)))
print("fixture G price", F(10001, 2), half_away(F(10001, 2)))
print("E", -10 * 9850)
# test docstrings
print("496bps: coupon", F(1704285 * 179, 10000), half_away(F(1704285 * 179, 10000)))
face = 1734792
pv496 = F(face) / (F(10496, 10000))
print("496bps PV", pv496, float(pv496), half_away(pv496), "float", (1734792 / 1.0496))
print("3305625/2 check", pv496 == F(3305625, 2))
print("400bps 13 cents", F(13) / F(104, 100), float(F(13) / F(104, 100)), "float", (1 + 0.04) ** -1 * 13, "float as page", float((1 + 0.04) ** -1) * 13)
print("10**10+1 at 10000 bps", F(10**10 + 1, 2), half_away(F(10**10 + 1, 2)))
print("10**12+1", F(10**12 + 1, 2), half_away(F(10**12 + 1, 2)))
print("2^40+1 times 9851", (2**40 + 1) * 9851, (2**40 + 1) * 9851 > 2**53, ((2**40 + 1) * 9851) % 2)
print("float coupon 10**17+4999", F(10**17 + 4999, 10000), float(10**13 + F(4999, 10000)), half_away(F(10**17 + 4999, 10000)))
print("401 face 10^9 coupon", 10**9 * 500 // 10000)
print("yield -500 neg PV of 10500 at -500:", float(F(10500) / F(95, 100)))
print("fixture A 1-period par exact 10000:", F(10500, 1) / (1 + F(500, 10000)))
print("rounded 1 period 10001 at 50%", half_away(F(10001, 2)))
