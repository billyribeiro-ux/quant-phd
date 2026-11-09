"""Round 19: independent re-derivation of L04 numbers from the embedded CSV (own parser, no lab import).

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/rederive_L04_r19.py
"""
import math
import statistics
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

path = "course/assets/data/market/fx_monthly.csv"
lines = open(path, encoding="utf-8").read().splitlines()
hdr = lines[0].split(",")
gi = hdr.index("GBP")
mi = hdr.index("month")
rows = []
for ln in lines[1:]:
    parts = ln.split(",")
    rows.append((parts[mi], parts[gi]))
print("rows", len(rows), rows[0], rows[-1], "blank GBP cells", sum(1 for _, v in rows if v.strip() == ""))
vals = [(m, F(v)) for m, v in rows]
# consecutive months check
def idx(m):
    y, n = map(int, m.split("-"))
    return 12 * y + n - 1
assert all(idx(vals[i][0]) + 1 == idx(vals[i + 1][0]) for i in range(len(vals) - 1))
chg = [(vals[i][0], math.log(float(vals[i][1] / vals[i - 1][1]))) for i in range(1, len(vals))]
print("changes", len(chg), chg[0][0], chg[-1][0])
zeros = [m for (m, c) in chg if vals[[x[0] for x in vals].index(m)][1] == vals[[x[0] for x in vals].index(m) - 1][1]]
zeros2 = [vals[i][0] for i in range(1, len(vals)) if vals[i][1] == vals[i - 1][1]]
print("exact zero months:", zeros2, len(zeros2), "nonzero:", len(chg) - len(zeros2))
w1 = chg
w2 = [(m, c) for (m, c) in chg if m >= "2000-01"]
rate_before_two = dict(vals)["1999-12"]
print("window two n", len(w2), "first uses 1999-12 rate", rate_before_two)
def sd(xs):
    n = len(xs)
    mu = math.fsum(xs) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in xs) / (n - 1))
s1 = sd([c for _, c in w1])
s2 = sd([c for _, c in w2])
print("sd1 %.12f sd2 %.12f" % (s1, s2))
print("sd1 6dp", Decimal(s1).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP), "sd2 6dp", Decimal(s2).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
d = s2 - s1
print("diff unrounded %.9f -> 6dp %s" % (d, Decimal(d).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)))
print("printed diff check 0.024700 - 0.027935 =", round(0.024700 - 0.027935, 6))
print("ratio %.9f -> 4dp %s" % (s2 / s1, Decimal(s2 / s1).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)))
mx1 = max(w1, key=lambda t: abs(t[1]))
mx2 = max(w2, key=lambda t: abs(t[1]))
print("largest w1", mx1, "largest w2", mx2)
print("identity w1:", abs(math.fsum(c for _, c in w1) - math.log(float(vals[-1][1] / vals[0][1]))) <= 1e-12)
print("identity w2:", abs(math.fsum(c for _, c in w2) - math.log(float(vals[-1][1] / rate_before_two))) <= 1e-12)
z = -0.0965747399762  # check against unrounded
z2 = mx2[1]
print("unrounded w2 max log %.13f" % z2, " simple change = %.9f" % (math.exp(z2) - 1))
# R2
zz = mx1[1]
h = math.tanh(zz / 2)
print("R2 h exact %.9f -> 6dp %.6f  4dp %.4f" % (h, h, h))
print("bound at h=0.0678: %.9f" % math.log((1 + 0.0678) / (1 - 0.0678)))
print("bound at h exact: %.9f (should equal zz %.9f)" % (math.log((1 + h) / (1 - h)), zz))
# M1 M2 M3
print("M1 ln1.1 = %.10f; diff from 0.1 = %.10f" % (math.log(1.1), 0.1 - math.log(1.1)))
xs = [0.01, 0.03, -0.02]
mu = sum(xs) / 3
ss = sum((x - mu) ** 2 for x in xs)
print("M2 mean %.9f ss %.9f (19/15000=%.9f) sd %.9f" % (mu, ss, 19 / 15000, math.sqrt(ss / 2)))
print("M3 months 2000-01..2026-09:", (2026 - 2000) * 12 + 9, "changes; w2 n =", len(w2))
# Part A: model
mod = [math.log(1.0) for _ in range(11)]
print("model sd", sd(mod) if False else 0.0)
# Misc / key rows
print("log(1.1)=%.6f" % math.log(1.1), "simple 0.1 minus log = %.6f" % (0.1 - math.log(1.1)))
