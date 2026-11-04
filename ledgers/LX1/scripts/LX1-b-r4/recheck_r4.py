"""Independent recheck (no twin import). Usage: python -I recheck_r4.py <csv> <manifest.json>"""
import csv, json, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
import math

getcontext().prec = 60
csv_path, manifest_path = sys.argv[1], sys.argv[2]

def q(x, places):
    return x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)

# ---- L04 data
rows = []
with open(csv_path, encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    for r in rd:
        rows.append((r["month"], r["GBP"]))
print("fieldnames", rd.fieldnames)
print("rows", len(rows), rows[0][0], rows[-1][0])
blank = [m for m, v in rows if not v.strip()]
nondec = [m for m, v in rows if v.strip() and not all(ch.isdigit() or ch == "." for ch in v)]
print("blank GBP", len(blank), "non-decimal GBP", len(nondec))
vals = [(m, Decimal(v)) for m, v in rows]
zero_months = [vals[i][0] for i in range(1, len(vals)) if vals[i][1] == vals[i-1][1]]
print("exact zero months (decimal equality)", len(zero_months), zero_months)
changes = []
for i in range(1, len(vals)):
    m, x = vals[i]
    p = vals[i-1][1]
    ratio = x / p  # Decimal division at 60 digits
    changes.append((m, ratio.ln()))
print("changes", len(changes), changes[0][0], changes[-1][0])
def sd(xs):
    n = len(xs)
    mean = sum(xs, Decimal(0)) / n
    ss = sum(((x - mean) ** 2 for x in xs), Decimal(0))
    return (ss / (n - 1)).sqrt()
w1 = [c for _, c in changes]
w2_items = [(m, c) for m, c in changes if m >= "2000-01"]
w2 = [c for _, c in w2_items]
s1, s2 = sd(w1), sd(w2)
print("window one n", len(w1), "sd", q(s1, 6))
print("window two n", len(w2), "sd", q(s2, 6))
print("window two first change month", w2_items[0][0], "last", w2_items[-1][0])
big1 = max(changes, key=lambda t: abs(t[1]))
big2 = max(w2_items, key=lambda t: abs(t[1]))
print("largest abs w1", big1[0], q(abs(big1[1]), 6), "signed", q(big1[1], 6))
print("largest abs w2", big2[0], q(abs(big2[1]), 6), "signed", q(big2[1], 6))
print("diff sd (w2-w1)", q(s2 - s1, 6), "ratio", q(s2 / s1, 4), "ratio unrounded", s2 / s1)
print("sum identity w1 diff", float(sum(w1, Decimal(0)) - (vals[-1][1] / vals[0][1]).ln()))
print("sum identity w2 diff", float(sum(w2, Decimal(0)) - (vals[-1][1] / vals[vals.index(next(v for v in vals if v[0]=='1999-12'))][1]).ln()))
# model
print("ln 1.1", q(Decimal("1.1").ln(), 10), "1 - ln1.1", q(Decimal("0.1") - Decimal("1.1").ln(), 10))
# -- L03 fractions
DEBT, N0, DELTA, H, PX, PY = 1_000_000, 4_000_000, Fraction(1, 50), 12, 12, 4
def pidx(m, t): return (1 - DELTA) ** min(t, m)
def V(m, t): return Fraction(DEBT) / pidx(m, t)
def lev(v): return v / (N0 + DEBT - v)
L0 = lev(Fraction(DEBT))
def fall(m, t, phi=Fraction(1), beta=Fraction(1)): return beta * phi * (lev(V(m, t)) - L0)
def depth(m, phi=Fraction(1), beta=Fraction(1)): return max(fall(m, t, phi, beta) for t in range(H + 1))
def rnd(x, places):
    scaled = x * 10 ** places
    return Fraction(math.floor(scaled + Fraction(1, 2)), 10 ** places)
dX, dY = depth(PX), depth(PY)
print("depth X exact", float(dX * 100), "round", rnd(dX * 100, 2))
print("depth Y exact", float(dY * 100), "round", rnd(dY * 100, 2))
print("first t X", [t for t in range(H+1) if fall(PX, t) == dX], "first t Y", [t for t in range(H+1) if fall(PY, t) == dY])
print("diff exact", float((dX - dY) * 100), "round", rnd((dX - dY) * 100, 2), "printed-diff", rnd(dX*100,2)-rnd(dY*100,2))
print("ratio exact", float(dX / dY), "round4", rnd(dX / dY, 4))
for phi, beta in ((Fraction(1,2), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(3), Fraction(1))):
    print("ratio phi", phi, "beta", beta, rnd(depth(PX, phi, beta) / depth(PY, phi, beta), 4), float(depth(PX, phi, beta)/depth(PY,phi,beta)))
ds = [depth(m) for m in range(H + 1)]
print("never falls", all(ds[m] <= ds[m+1] for m in range(H)), "strict", all(ds[m] < ds[m+1] for m in range(H)))
print("depth list pct", [str(rnd(d*100, 2)) for d in ds])
print("V_12 X", float(V(12, 12)), "round", rnd(V(12,12), 0))
print("M1 P_4", pidx(4, 4), float(pidx(4,4)), "V_4 float", float(V(4,4)))
print("depth(4) exact pct", float(depth(4)*100))
print("leverage values", float(lev(V(4,4))), "X ratio", float(depth(12)/depth(4)))
print("E2 unrounded diff", float(depth(12)*100), float(depth(4)*100), float((depth(12)-depth(4))*100))
print("squared-ratio", float((depth(12)/depth(4))**2))
