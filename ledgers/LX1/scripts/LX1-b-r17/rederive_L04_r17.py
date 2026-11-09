"""Independent re-derivation of the L04 GBP numbers (LX1-b round 17). Reads course/assets/data/market/fx_monthly.csv.

Uses Fraction for the rates and mpmath-free float math only where the page does (log changes)."""
import csv
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

PATH = sys.argv[1]
rows = []
with open(PATH, encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    print("header:", rd.fieldnames)
    for r in rd:
        rows.append((r["month"], r["GBP"]))
print("n rows:", len(rows), "first:", rows[0], "last:", rows[-1])
blank = [m for m, v in rows if not v.strip()]
print("blank GBP cells:", len(blank), blank[:5])
bad = [(m, v) for m, v in rows if v.strip() and not all(ch in "0123456789." for ch in v)]
print("non-decimal GBP cells:", bad[:5])
rates = [(m, Fraction(v)) for m, v in rows]
# consecutive months check
def idx(m):
    y, mo = int(m[:4]), int(m[5:7])
    return 12 * y + mo - 1
print("consecutive:", all(idx(rates[i][0]) + 1 == idx(rates[i + 1][0]) for i in range(len(rates) - 1)))

def show(v, places):
    return str(Decimal(v).quantize(Decimal(f"1e-{places}"), rounding=ROUND_HALF_UP))

def sd(vals):
    n = len(vals)
    mean = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mean) ** 2 for v in vals) / (n - 1))

def changes(seq):
    return [(seq[i][0], math.log(float(seq[i][1] / seq[i - 1][1]))) for i in range(1, len(seq))]

w1 = changes(rates)
w2_seq = [x for x in rates if x[0] >= "1999-12"]
w2 = [c for c in changes(rates) if c[0] >= "2000-01"]
print("window one n:", len(w1), "window two n:", len(w2))
zeros = [m for i, (m, r) in enumerate(rates) if i > 0 and r == rates[i - 1][1]]
print("exact zero months:", len(zeros), zeros)
s1 = sd([c for _, c in w1]); s2 = sd([c for _, c in w2])
print("sd1 raw:", repr(s1), "display:", show(s1, 6))
print("sd2 raw:", repr(s2), "display:", show(s2, 6))
print("diff raw:", repr(s2 - s1), "display:", show(s2 - s1, 6))
print("ratio raw:", repr(s2 / s1), "display 4dp:", show(s2 / s1, 4))
print("printed-difference from printed sds:", show(float("0.024700") - float("0.027935"), 6))
big1 = max(w1, key=lambda x: abs(x[1])); big2 = max(w2, key=lambda x: abs(x[1]))
print("largest w1:", big1, show(abs(big1[1]), 6), " largest w2:", big2, show(abs(big2[1]), 6))
print("simple change of w2 largest (exp-1), 6dp:", show(math.exp(big2[1]) - 1, 6))
print("simple change of w2 largest unrounded via Fraction ratio check:", show(math.exp(big2[1]) - 1, 8))
print("identity w1:", abs(math.fsum(c for _, c in w1) - math.log(float(rates[-1][1] / rates[0][1]))) <= 1e-12)
print("identity w2:", abs(math.fsum(c for _, c in w2) - math.log(float(rates[-1][1] / rates[idx_pos] [1]))) <= 1e-12 if False else "see below")
pos = [i for i, (m, _) in enumerate(rates) if m == "1999-12"][0]
print("identity w2 (start 1999-12):", abs(math.fsum(c for _, c in w2) - math.log(float(rates[-1][1] / rates[pos][1]))) <= 1e-12)
print("sum w1 raw:", repr(math.fsum(c for _, c in w1)), "ln ratio:", repr(math.log(float(rates[-1][1] / rates[0][1]))))
print("ln1.1:", show(math.log(1.1), 10), " ln1.1 6dp:", show(math.log(1.1), 6), " diff 0.1-ln1.1 6dp:", show(0.1 - math.log(1.1), 6))
for h in (Fraction(678, 10000),):
    hf = float(h)
    print("bound at h=0.0678:", repr(math.log((1 + hf) / (1 - hf))), show(math.log((1 + hf) / (1 - hf)), 6), show(math.log((1 + hf) / (1 - hf)), 4))
z = big1[1]
print("R2 z:", repr(z), " tanh(z/2):", repr(math.tanh(abs(z) / 2)), show(math.tanh(abs(z) / 2), 6))
print("R2 h 4dp:", show(math.tanh(abs(z) / 2), 4))
print("2008-10 signed:", big2)
print("Part A: sd of constant:", sd([0.0] * 11))
