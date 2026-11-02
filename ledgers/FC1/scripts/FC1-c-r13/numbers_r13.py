"""Round-13 recomputation of the numbers quoted on project.html and in test_project.py (exact Fractions and float)."""
from fractions import Fraction as F
import math


def half_away(x):
    m = abs(x)
    r = math.floor(m + F(1, 2))
    return r if x >= 0 else -r


def price(events, bps):
    y = F(bps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in events), F(0))


# Lab 1: bond 100000 face, 500 bps, 3 periods, yield 400 bps
ev1 = [(1, 5000), (2, 5000), (3, 105000)]
p1 = price(ev1, 400)
print("lab1 exact PV", float(p1), "rounded", half_away(p1))
print("lab1 terms", [float(F(a) / (F(1, 1) + F(400, 10000)) ** t) for t, a in ev1])
# Rounding fixture: 10000, 500 bps, 3 periods, 400 bps
ev_r = [(1, 500), (2, 500), (3, 10500)]
pr = price(ev_r, 400)
print("rounding exact", float(pr), "once", half_away(pr), "term terms", [float(F(a) / F(104, 100) ** t) for t, a in ev_r],
      "per-term rounded sum", sum(half_away(F(a) / F(104, 100) ** t) for t, a in ev_r))
# Fixture B
print("fixture B", float(F(10500) / F(95, 100)), half_away(price([(1, 10500)], -500)))
# Fixture C, D, F, G
print("C coupon", half_away(F(10001 * 5000, 10000)), "D", half_away(F(1 * 5000, 10000)))
print("F", price([(1, 1)], 10000), half_away(price([(1, 1)], 10000)))
print("G", half_away(price([(1, 10001)], 10000)))
# 496 bps case
ev_h = [(1, 1734792)]
ph = price(ev_h, 496)
print("496 case: coupon exact", F(1704285 * 179, 10000), "exact PV", ph, float(ph), "half_away", half_away(ph))
fl = 1734792 / (1 + 496 / 10000)
print("float PV", repr(fl), "float round", round(fl))
print("float discount then round half up (floor(x+0.5))", math.floor(fl + 0.5))
# 13-15 periods at 500 bps par check
for n in (13, 14, 15):
    ev = [(t, 500) for t in range(1, n + 1)]
    ev[-1] = (n, 500 + 10000)
    print("par", n, half_away(price(ev, 500)))
# Lab 3 fixture with 1 cent face
print("E seller", -(-1) * 10 * 9850)
print("A", price([(1, 10500)], 500), half_away(price([(1, 10500)], 500)))
