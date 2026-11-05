"""Independent re-derivation of L04 Lab 1 numbers from the embedded fx_monthly.csv (stdlib only)."""
import csv, math, sys
from fractions import Fraction as Fr
path = sys.argv[1]
rows = []
with open(path, newline='', encoding='utf-8') as h:
    rd = csv.DictReader(h)
    print("header:", rd.fieldnames[:4], "...", len(rd.fieldnames), "cols")
    for rec in rd:
        rows.append((rec['month'], rec['GBP']))
print("rows", len(rows), rows[0][0], rows[-1][0])
rates = [(m, Fr(v)) for m, v in rows]
zeros = [m for (m0, a), (m, b) in zip(rates, rates[1:]) if a == b]
print("exact zero months:", len(zeros), zeros)
chg = [(m, math.log(float(b / a))) for (m0, a), (m, b) in zip(rates, rates[1:])]
print("changes:", len(chg), chg[0][0], chg[-1][0])
nz = sum(1 for m, c in chg if c != 0.0)
print("nonzero changes (all):", nz)
def sd(vals):
    n = len(vals); mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))
w1 = [c for m, c in chg]
w2_items = [(m, c) for m, c in chg if m >= "2000-01"]
w2 = [c for m, c in w2_items]
s1, s2 = sd(w1), sd(w2)
print("window1 n", len(w1), "sd", repr(s1), "window2 n", len(w2), "sd", repr(s2))
print("ratio s2/s1 =", repr(s2 / s1), round(s2 / s1, 4))
print("difference s2-s1 =", repr(s2 - s1), round(s2 - s1, 6), "printed-diff", round(round(s2, 6) - round(s1, 6), 6))
big1 = max(chg, key=lambda t: abs(t[1])); big2 = max(w2_items, key=lambda t: abs(t[1]))
print("largest window1", big1, "largest window2", big2)
# ratio check of first change in window2 and before-window rate
print("rate 1999-12", dict(rows)["1999-12"], "rate 1971-01", rows[0][1])
