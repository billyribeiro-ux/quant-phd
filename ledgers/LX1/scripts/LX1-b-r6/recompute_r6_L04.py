# Independent re-derivation of the L04 statistics from the CSV, 60-digit Decimal. Imports nothing from the twin.
import csv, math
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
getcontext().prec = 60
CSV = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b/course/assets/data/market/fx_monthly.csv"
rows = []
with open(CSV, encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    print("header", rd.fieldnames)
    for r in rd:
        rows.append((r["month"], r["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
bad = [m for m, v in rows if not v.replace(".", "", 1).isdigit()]
print("non-decimal GBP cells", len(bad))
# month consecutiveness
def mi(s):
    y, mo = s.split("-"); return int(y) * 12 + int(mo) - 1
print("consecutive", all(mi(rows[i+1][0]) == mi(rows[i][0]) + 1 for i in range(len(rows)-1)))
X = [(m, Decimal(v)) for m, v in rows]
ch = []
for (pm, pv), (m, v) in zip(X, X[1:]):
    ch.append((m, (v / pv).ln()))
def rnd(d, places):
    return d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
def sd(vals):
    n = len(vals); mean = sum(vals) / n
    return (sum((x - mean) ** 2 for x in vals) / (n - 1)).sqrt(), n, mean
w1 = ch
w2 = [c for c in ch if c[0] >= "2000-01"]
s1, n1, mu1 = sd([c for _, c in w1])
s2, n2, mu2 = sd([c for _, c in w2])
print("window one n", n1, "sd", s1, rnd(s1, 6))
print("window two n", n2, "sd", s2, rnd(s2, 6))
print("diff unrounded", s2 - s1, rnd(s2 - s1, 6), "printed-subtraction", Decimal("0.024700") - Decimal("0.027935"))
print("ratio", s2 / s1, rnd(s2 / s1, 4))
zeros = [m for (m, c) in ch if c == 0]
print("zero changes", len(zeros), zeros, "nonzero", n1 - len(zeros))
mx1 = max(w1, key=lambda t: abs(t[1])); mx2 = max(w2, key=lambda t: abs(t[1]))
print("max |change| w1", mx1[0], mx1[1], rnd(abs(mx1[1]), 6))
print("max |change| w2", mx2[0], mx2[1], rnd(abs(mx2[1]), 6))
# telescoping identity
for name, w, start in (("w1", w1, X[0][1]), ("w2", w2, [v for m, v in X if m == "1999-12"][0])):
    tot = sum(c for _, c in w)
    print("identity", name, float(tot - (X[-1][1] / start).ln()))
# the rate before window two
print("1999-12 present", any(m == "1999-12" for m, _ in X))
# derived numbers
print("ln 1.1", rnd((Decimal("1.1")).ln(), 6), "diff", rnd(Decimal("0.1") - Decimal("1.1").ln(), 6))
L = mx1[1]
print("L unrounded", L, "h closed form tanh(L/2)", (L.exp() - 1) / (L.exp() + 1), rnd((L.exp() - 1) / (L.exp() + 1), 6))
h = Decimal("0.0678")
print("bound at h=0.0678", ((1 + h) / (1 - h)).ln(), rnd(((1 + h) / (1 - h)).ln(), 6), rnd(((1 + h) / (1 - h)).ln(), 4))
print("E2 simple change", (mx2[1].exp() - 1), rnd(mx2[1].exp() - 1, 6))
print("M2 mean 1/150 check", Decimal(0.02)/3)
mc = [Decimal("0.01"), Decimal("0.03"), Decimal("-0.02")]
mu = sum(mc)/3; ss = sum((x-mu)**2 for x in mc)
print("M2", mu, ss, ss/2, (ss/2).sqrt(), rnd((ss/2).sqrt(), 6), Fraction(19,15000))
print("M1 simple", Decimal("1.3750")/Decimal("1.2500") - 1)
print("window one start 1971-01 rate", X[0])
print("window one first change month", w1[0][0], "last", w1[-1][0], "w2 first", w2[0][0], "n w2", len(w2))
print("identity residual window two (sum minus ln(last/1999-12))", sum(c for _, c in w2) - (X[-1][1]/[v for m, v in X if m == "1999-12"][0]).ln())
