"""Independent recomputation of project lab 3 figures (LX1-c round 1).

Usage: python3 -I recompute_gbp.py <path-to-fx_monthly.csv>
Uses Decimal for the log-free checks and math for logs; prints unrounded values.
"""
import csv, math, statistics, sys
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50
path = sys.argv[1]
with open(path, encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    cols = rd.fieldnames
    rows = list(rd)
print("columns:", cols)
print("data rows:", len(rows), "first:", rows[0]["month"], "last:", rows[-1]["month"])
blank = {c: sum(1 for r in rows if not (r.get(c) or "").strip()) for c in cols if c != "month"}
print("blank counts:", blank)
gbp = [(r["month"], r["GBP"]) for r in rows]
bad = [m for m, v in gbp if not v.replace(".", "", 1).isdigit()]
print("non-decimal GBP cells:", bad)
# month gap check
def idx(m):
    y, mo = m.split("-")
    return int(y) * 12 + int(mo) - 1
gaps = [(a[0], b[0]) for a, b in zip(gbp, gbp[1:]) if idx(b[0]) != idx(a[0]) + 1]
print("month gaps:", gaps)
# exact rational log-change proxies: exact-zero changes are rate equality
zeros_all = [m for (a, va), (m, vb) in zip(gbp, gbp[1:]) if Fraction(va) == Fraction(vb)]
print("exact equal consecutive rates (zero log change), all:", zeros_all)
# log changes using Fraction ratio then float log (same as the lab's method)
changes = []
for (a, va), (m, vb) in zip(gbp, gbp[1:]):
    r = Fraction(vb) / Fraction(va)
    changes.append((m, math.log(float(r))))
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
print("n w1", len(w1), "n w2", len(w2), "first w2 change month", w2[0][0], "last", w1[-1][0])
def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))
s1 = sd([v for _, v in w1]); s2 = sd([v for _, v in w2])
print("sd w1 unrounded pct/month:", repr(100 * s1))
print("sd w2 unrounded pct/month:", repr(100 * s2))
print("statistics.stdev w1 pct:", repr(100 * statistics.stdev([v for _, v in w1])))
print("statistics.stdev w2 pct:", repr(100 * statistics.stdev([v for _, v in w2])))
print("difference w1-w2 pct (unrounded):", repr(100 * (s1 - s2)))
print("ratio w2/w1:", repr(s2 / s1))
mx1 = max(w1, key=lambda c: abs(c[1])); mx2 = max(w2, key=lambda c: abs(c[1]))
print("max abs w1:", mx1, repr(100 * mx1[1]))
print("max abs w2:", mx2, repr(100 * mx2[1]))
print("zero changes w1:", sum(1 for _, v in w1 if v == 0.0), "w2:", sum(1 for _, v in w2 if v == 0.0))
print("GBP 1999-12 and 2000-01:", [r for r in gbp if r[0] in ("1999-12", "2000-01")])
