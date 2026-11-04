"""Re-derive every number on project.html (FC1-c round 7) in exact Fractions. Stdlib only. Run: python3 -I <this file>."""
from fractions import Fraction as F


def half_away(x):
    m = abs(x)
    whole = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return whole if x >= 0 else -whole


def events(face, cbps, n):
    c = half_away(F(face * cbps, 10_000))
    ev = [(t, c) for t in range(1, n + 1)]
    ev[-1] = (n, ev[-1][1] + face)
    return ev


def pv(ev, ybps):
    y = F(ybps, 10_000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))


ev1 = events(100_000, 500, 3)
p = pv(ev1, 400)
print("lab1 events", ev1)
print("lab1 exact pv", "%.6f" % float(p), "rounded", half_away(p))
print("fixtureA", events(10_000, 500, 1), half_away(pv(events(10_000, 500, 1), 500)))
b = pv(events(10_000, 500, 1), -500)
print("fixtureB exact", "%.4f" % float(b), "rounded", half_away(b))
print("fixtureC", events(10_001, 5_000, 2))
print("fixtureD", events(1, 5_000, 1))
r = events(10_000, 500, 3)
rp = pv(r, 400)
print("rounding events", r, "exact", "%.6f" % float(rp), "rounded once", half_away(rp))
terms = [half_away(F(a) / (1 + F(400, 10_000)) ** t) for t, a in r]
print("term-by-term", terms, sum(terms))
print("fixtureE", (2, -10 * 9_850))
print("fixtureF", half_away(pv(events(1, 0, 1), 10_000)), "exact", pv(events(1, 0, 1), 10_000))
print("fixtureG", half_away(pv(events(10_001, 0, 1), 10_000)), "exact", pv(events(10_001, 0, 1), 10_000))
print("lab2 count of blanks: 2; lab1 price line (cents):", half_away(p))
print("tolerance 1e-6*(1+102775) =", 1e-6 * (1 + 102775))
print("lab1 pv 102775.091033 check:", "%.6f" % float(p) == "102775.091033")
