"""Re-derive every number on FC1 project.html (slice c) with exact fractions."""
from fractions import Fraction as F


def half_away(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def events(face, cb, n):
    c = half_away(F(face * cb, 10000))
    ev = [(t, c) for t in range(1, n + 1)]
    ev[-1] = (n, ev[-1][1] + face)
    return ev


def pv(ev, ybps):
    y = F(ybps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))


ev = events(100000, 500, 3)
p = pv(ev, 400)
print("lab1 events", ev)
print("lab1 exact PV float", f"{float(p):.6f}", "rounded", half_away(p))
print("lab1 trade", (2, -1 * 10 * 9850))
print("fixA events", events(10000, 500, 1), "price", half_away(pv(events(10000, 500, 1), 500)))
print("fixB exact", float(F(10500) / F(95, 100)), "price", half_away(pv(events(10000, 500, 1), -500)))
print("fixC events", events(10001, 5000, 2))
print("fixD events", events(1, 5000, 1))
r = events(10000, 500, 3)
print("rounding events", r, "exact", f"{float(pv(r, 400)):.6f}", "once", half_away(pv(r, 400)))
terms = [half_away(F(a) / (1 + F(400, 10000)) ** t) for t, a in r]
print("term-by-term", terms, sum(terms))
print("fixE", (2, -10 * 9850))
print("fixF events", events(1, 0, 1), "price", half_away(pv(events(1, 0, 1), 10000)), "exact", pv(events(1, 0, 1), 10000), "py round", round(pv(events(1, 0, 1), 10000)))
print("fixG events", events(10001, 0, 1), "price", half_away(pv(events(10001, 0, 1), 10000)), "exact", pv(events(10001, 0, 1), 10000))
print("hours sum", 1 + 2 + 5 + 4 + 2 + 3 + 3 + 0)
print("hub: 20 of 70 ; check index later")
print("10**18 bps as pct:", F(10**18, 100), "% ; 10**7 bps as pct:", F(10**7, 100), "%")
print("10**18 bps yield test:", half_away(pv([(1, 10**30)], 10**18)), "vs expected 9999999999999900")
print("exact of 10**30 at 1e18 bps:", float(pv([(1, 10**30)], 10**18)))
print("exact half cent Bond(10**40+1,0,1) at 10000 bps:", half_away(pv(events(10**40 + 1, 0, 1), 10000)), "expect", 5 * 10**39 + 1)
