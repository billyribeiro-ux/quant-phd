"""Round 20 independent re-derivation of the LX1 L04 numbers from the embedded fx_monthly.csv (GBP column).

Uses Fraction for the rates and the ratios and math.log only at the last step; the sample sd is computed with
exact-enough two-pass arithmetic via Fraction-of-floats (math.fsum), independent of the lab's helper functions.
Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/rederive_L04_r20.py
"""
import csv
import math
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

rows = []
with open("course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
blank = [m for m, v in rows if v.strip() == ""]
print("GBP blank cells", len(blank))
rates = [(m, F(v)) for m, v in rows]
ch = [(rates[i][0], math.log(float(rates[i][1] / rates[i - 1][1]))) for i in range(1, len(rates))]
zero = [rates[i][0] for i in range(1, len(rates)) if rates[i][1] == rates[i - 1][1]]
print("changes", len(ch), "first", ch[0][0], "last", ch[-1][0])
print("exact zero months", len(zero), zero)
w2 = [(m, c) for m, c in ch if m >= "2000-01"]
rate_1999_12 = dict(rates)["1999-12"]
print("window two changes", len(w2), "first", w2[0][0], "last", w2[-1][0])


def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))


def hu(x, p):
    return Decimal(x).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)


s1 = sd([c for _, c in ch])
s2 = sd([c for _, c in w2])
print("sd1", repr(s1), hu(s1, 6))
print("sd2", repr(s2), hu(s2, 6))
print("diff", repr(s2 - s1), hu(s2 - s1, 6), " printed-diff from rounded sds:", float(hu(s2, 6)) - float(hu(s1, 6)))
print("ratio", repr(s2 / s1), hu(s2 / s1, 4))
big1 = max(ch, key=lambda t: abs(t[1]))
big2 = max(w2, key=lambda t: abs(t[1]))
print("largest window one", big1, "window two", big2)
print("telescoping w1", abs(math.fsum(c for _, c in ch) - math.log(float(rates[-1][1] / rates[0][1]))))
print("telescoping w2", abs(math.fsum(c for _, c in w2) - math.log(float(rates[-1][1] / rate_1999_12))))
print("nonzero window one", len(ch) - len([1 for _, c in ch if c == 0.0]))

# Scale check on the number of distinct months: the file must be consecutive months
import itertools
def idx(m):
    y, mo = map(int, m.split("-"))
    return 12 * y + mo - 1
print("consecutive months:", all(idx(b[0]) == idx(a[0]) + 1 for a, b in itertools.pairwise(rates)))
