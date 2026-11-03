"""Independent re-derivation of every number in project.html and the new tests (FC1-c round 4)."""
from fractions import Fraction as F
import math


def half_away(x):
    m = abs(x)
    w = math.floor(m + F(1, 2))
    return w if x >= 0 else -w


def events(face, cbps, n):
    c = half_away(F(face * cbps, 10000))
    rows = [(t, c) for t in range(1, n + 1)]
    rows[-1] = (n, rows[-1][1] + face)
    return rows


def price(ev, ybps):
    y = F(ybps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))


# Lab 1 / Lab 2
ev1 = events(100000, 500, 3)
pv1 = price(ev1, 400)
print("lab1 events", ev1, "exact pv", float(pv1), "price", half_away(pv1), "pv6dp", f"{float(pv1):.6f}")
print("lab1 frac of pv", float(pv1) - math.floor(float(pv1)))
print("trade", (2, -10 * 9850))
# Rounding fixture
ev3 = events(10000, 500, 3)
pv3 = price(ev3, 400)
print("rounding events", ev3, "exact", float(pv3), "once", half_away(pv3),
      "terms", [float(F(a) / (F(104, 100)) ** t) for t, a in ev3],
      "terms rounded", [half_away(F(a) / (F(104, 100)) ** t) for t, a in ev3],
      "sum", sum(half_away(F(a) / (F(104, 100)) ** t) for t, a in ev3))
# Fixtures
print("A", events(10000, 500, 1), half_away(price(events(10000, 500, 1), 500)))
print("B", half_away(price(events(10000, 500, 1), -500)), float(F(10500) / F(95, 100)), F(210000, 19))
print("C", events(10001, 5000, 2), F(10001 * 5000, 10000))
print("D", events(1, 5000, 1), F(5000, 10000))
print("E", (2, -10 * 9850))
print("F", events(1, 0, 1), price(events(1, 0, 1), 10000), half_away(price(events(1, 0, 1), 10000)))
print("G", events(10001, 0, 1), price(events(10001, 0, 1), 10000), half_away(price(events(10001, 0, 1), 10000)))
# Hand fixture for 496 bps half
c = half_away(F(1704285 * 179, 10000))
ev = events(1704285, 179, 1)
print("496 coupon", F(1704285 * 179, 10000), float(F(1704285 * 179, 10000)), "c", c, ev)
exact496 = price(ev, 496)
print("496 exact", exact496, "float", float(exact496), half_away(exact496))
# float discounting at 496
fl = sum(a / (1 + 496 / 10000) ** t for t, a in ev)
print("496 float discounting", repr(fl), round(fl))
print("1734792/1.0496", F(1734792) / F(10496, 10000), F(3305625, 2))
# 400 bps half at 13
print("13/1.04", F(13) / F(104, 100), "float", repr((1 + 0.04) ** -1 * 13), round((1 + 0.04) ** -1 * 13))
print("13 float discount", repr(13 * (1 + 0.04) ** -1))
# 10 significant digits halves
print("10**10+1", half_away(price(events(10**10 + 1, 0, 1), 10000)), price(events(10**10 + 1, 0, 1), 10000))
print("10**12+1", half_away(price(events(10**12 + 1, 0, 1), 10000)), price(events(10**12 + 1, 0, 1), 10000))
# float-face hand check
face = 10**17 + 4999
print("face coupon", F(face, 10000), half_away(F(face, 10000)), 10**13, events(face, 1, 1))
# trade exact
print("2**40+1 trade", (2**40 + 1) * 9851, 2**53, (2**40 + 1) * 9851 > 2**53, ((2**40 + 1) * 9851) % 2)
print("trade 501", 501 * 9850, "1001", 1001 * 9850)
print("10**9 face coupon", half_away(F(10**9 * 500, 10000)), 5 * 10**7)
# 24-period check values
print("24 events", events(10000, 500, 24)[-2:], half_away(price(events(10000, 500, 24), 400)))
# 13-15 par
for n in (13, 14, 15):
    print("par", n, half_away(price(events(10000, 500, n), 500)))
# 12
print("n=12 events len", len(events(10000, 500, 12)))
