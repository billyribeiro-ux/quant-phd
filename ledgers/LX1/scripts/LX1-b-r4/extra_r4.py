"""Round-4 extra numbers for LX1-b: unrounded window difference, window-start sensitivity, R2 band, E2 simple change.
Independent of the twins. Usage: python -I extra_r4.py <fx_monthly.csv>"""
import csv
import sys
from decimal import Decimal, getcontext

getcontext().prec = 60
rows = [(r["month"], Decimal(r["GBP"])) for r in csv.DictReader(open(sys.argv[1], encoding="utf-8", newline=""))]
ch = [(rows[i][0], (rows[i][1] / rows[i - 1][1]).ln()) for i in range(1, len(rows))]


def sd(vals):
    n = len(vals)
    mu = sum(vals, Decimal(0)) / n
    return (sum(((v - mu) ** 2 for v in vals), Decimal(0)) / (n - 1)).sqrt()


w1 = [c for _, c in ch]
w2 = [c for m, c in ch if m >= "2000-01"]
diff = sd(w2) - sd(w1)
print("unrounded window two minus window one sd:", diff, "-> 6dp", diff.quantize(Decimal("0.000001")))
for start in ("1990-01", "2000-01", "2010-01"):
    w = [c for m, c in ch if m >= start]
    print("window start", start, "n", len(w), "sd 6dp", sd(w).quantize(Decimal("0.000001")))
L = [c for _, c in ch if abs(c) == max(abs(x) for _, x in ch)][0]
eL = L.exp()
h = (eL - 1) / (eL + 1)
print("R2 h = (e^L-1)/(e^L+1) =", h, "-> 6dp", h.quantize(Decimal("0.000001")), "4dp", h.quantize(Decimal("0.0001")))
print("bound at h=0.0678:", ((1 + Decimal("0.0678")) / (1 - Decimal("0.0678"))).ln().quantize(Decimal("0.000001")))
simple = next(c for m, c in ch if m == "2008-10").exp() - 1
print("E2 simple change 2008-10 6dp:", simple.quantize(Decimal("0.000001")))
