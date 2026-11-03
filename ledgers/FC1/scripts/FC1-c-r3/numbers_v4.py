"""Re-derive every number stated on project.html (Lab 1, Lab 3, fixtures A-G, rounding case, test docstrings)."""
from fractions import Fraction
import math


def half_away(x: Fraction) -> int:
    m = abs(x)
    w = math.floor(m + Fraction(1, 2))
    return w if x >= 0 else -w


def events(face, bps, n):
    c = half_away(Fraction(face * bps, 10_000))
    rows = [(t, c) for t in range(1, n + 1)]
    rows[-1] = (n, rows[-1][1] + face)
    return rows


def pv(ev, yield_bps):
    y = Fraction(yield_bps, 10_000)
    return sum((Fraction(a) / (1 + y) ** t for t, a in ev), Fraction(0))


def fl(x):
    return f"{float(x):.6f}"


ev1 = events(100_000, 500, 3)
print("Lab1 events", ev1)
print("Lab1 exact PV", fl(pv(ev1, 400)), "rounded", half_away(pv(ev1, 400)))
print("Lab1 trade", (2, -10 * 9850))
ev3 = events(10_000, 500, 3)
print("Rounding case events", ev3, "exact", fl(pv(ev3, 400)), "once", half_away(pv(ev3, 400)))
print("Rounding case terms", [str(Fraction(a) / (1 + Fraction(400, 10000)) ** t) for t, a in ev3],
      [float(Fraction(a) / (1 + Fraction(400, 10000)) ** t) for t, a in ev3])
print("term-by-term", sum(half_away(Fraction(a) / (1 + Fraction(400, 10000)) ** t) for t, a in ev3))
print("A events", events(10000, 500, 1), "A price", half_away(pv(events(10000, 500, 1), 500)))
print("B exact", Fraction(10500) / Fraction(95, 100), fl(Fraction(10500) / Fraction(95, 100)), half_away(pv(events(10000, 500, 1), -500)))
print("C events", events(10001, 5000, 2))
print("D events", events(1, 5000, 1))
print("F events", events(1, 0, 1), "F price", half_away(pv(events(1, 0, 1), 10000)), "exact", pv(events(1, 0, 1), 10000))
print("G events", events(10001, 0, 1), "G price", half_away(pv(events(10001, 0, 1), 10000)), "exact", pv(events(10001, 0, 1), 10000))
print("E", (2, -98500))
# test docstring claims
ev496 = events(1_704_285, 179, 1)
print("496bps event", ev496, "coupon exact", fl(Fraction(1_704_285 * 179, 10_000)))
ex496 = pv(ev496, 496)
print("496bps exact PV", ex496, float(ex496), "rounded", half_away(ex496), "claimed 1652812.5 =", Fraction(3305625, 2) == ex496)
print("496bps float discount", float(1734792) * (1 + 0.0496) ** -1, "float-rounded",
      round(float(1734792) * (1 + 0.0496) ** -1))
print("496 float form Fraction? 1734792/1.0496 float =", 1734792 / 1.0496)
print("400 bps Bond(13,0,1): exact", pv(events(13, 0, 1), 400), "float (1+0.04)**-1*13 =", 13 * (1 + 0.04) ** -1,
      "13/(1+0.04)=", 13 / (1 + 0.04), "round", round(13 * (1 + 0.04) ** -1))
print("trade 2**40+1 * 9851", (2**40 + 1) * 9851)
print("float(10**17+4999)", float(10**17 + 4999) == 10**17 + 4999)
print("rung1 'rounding each term first' 102775?", sum(half_away(Fraction(a) / (1 + Fraction(400, 10000)) ** t) for t, a in ev1))
print("hand fixture 1 fixed: 1000 coupon stuff ok")
print("13-15 periods at 500bps par:", [half_away(pv(events(10000, 500, n), 500)) for n in (13, 14, 15)])
print("12-period bond 400 bps price:", half_away(pv(events(10000, 500, 12), 400)), " 24:", half_away(pv(events(10000,500,24),400)))
print("Bond(10**12+1,0,1) at 10000:", half_away(pv(events(10**12+1,0,1),10000)))
print("Trade 501*9850", 501*9850, "1001*9850", 1001*9850)
