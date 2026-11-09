"""FC1-c round 17: independent exact re-derivation of the page and test numbers (Fractions only)."""

import math
from fractions import Fraction


def half_away(x):
    m = abs(x)
    whole = math.floor(m + Fraction(1, 2))
    return whole if x >= 0 else -whole


def events(face, bps, n):
    c = half_away(Fraction(face * bps, 10000))
    rows = [(t, c) for t in range(1, n + 1)]
    rows[-1] = (n, rows[-1][1] + face)
    return rows


def pv(ev, yield_bps):
    y = Fraction(yield_bps, 10000)
    return sum((Fraction(a) / (1 + y) ** t for t, a in ev), Fraction(0))


a = pv(events(10000, 500, 1), 500)
print("A events", events(10000, 500, 1), "exact", a, "rounded", half_away(a), "expected 10000")
b = pv(events(10000, 500, 1), -500)
print("B exact", float(b), "equals 210000/19:", b == Fraction(210000, 19), "rounded", half_away(b), "expected 11053")
print("C events", events(10001, 5000, 2), "coupon exact", Fraction(10001 * 5000, 10000), "expected [(1,5001),(2,15002)]")
print("D events", events(1, 5000, 1), "expected [(1,2)]")
print("E buyer", -1 * 10 * 9850, "seller", 1 * 10 * 9850, "expected -98500 / 98500")
f = pv([(1, 1)], 10000)
print("F exact", f, "half-away", half_away(f), "python round", round(float(f)), "expected 1 and 0")
g = pv(events(10001, 0, 1), 10000)
print("G events", events(10001, 0, 1), "exact", g, "rounded", half_away(g), "expected 5001")
rc = events(10000, 500, 3)
p = pv(rc, 400)
terms = [half_away(Fraction(am) / Fraction(10400, 10000) ** t) for t, am in rc]
print("rounding events", rc, "exact", float(p), "rounded", half_away(p), "termwise", terms, sum(terms), "expected 10278 and 10277")
lab1 = events(100000, 500, 3)
p1 = pv(lab1, 400)
print("lab1 events", lab1, "exact 6dp", f"{float(p1):.6f}", "rounded", half_away(p1), "expected 102775")
print("150pct", half_away(pv(events(10000, 500, 1), 15000)), "expected 4200; exact 4200:", pv(events(10000, 500, 1), 15000) == 4200)
print("20001 coupon events", events(10000, 20001, 1), "expected [(1,30001)]")
print("10^18 coupon events", events(10000, 10**18, 1) == [(1, 10**18 + 10000)])
print("10^18 trade", -10 * 10**18, "expected -(10*10**18)")
val = pv([(1, 10**30)], 10**18)
print("10^30 at 10^18 bps: exact-minus-9999999999999900 =", val - 9_999_999_999_999_900, "rounded", half_away(val), "expected 9999999999999900")
print("10^30 identity 10^30 == (10^14+1)(10^16-100)+100:", 10**30 == (10**14 + 1) * (10**16 - 100) + 100)
h = pv([(1, 10**40 + 1)], 10000)
print("half cent of Bond(10**40+1,0,1) at 10000 bps rounded", half_away(h), "expected", 5 * 10**39 + 1)
print("2^40+1 trade cash flow", (2**40 + 1) * 9851, "exceeds 2^53:", (2**40 + 1) * 9851 > 2**53)
print("10^18 bps as percent:", Fraction(10**18, 100), "% per period")
