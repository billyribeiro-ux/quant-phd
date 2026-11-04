# Independent re-derivation for L04 (no import of the twin). Decimal at 60 digits, Fraction for exact ratios.
import csv, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction
getcontext().prec = 60
rows = []
with open(sys.argv[1], newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    header = next(rd)
    gi = header.index("GBP")
    for r in rd:
        rows.append((r[0], r[gi]))
print("rows", len(rows), "first", rows[0][0], "last", rows[-1][0], "header", header[:3], "...")
def months(s):
    y, m = s.split("-"); return int(y) * 12 + int(m) - 1
def mlabel(i):
    return f"{i//12:04d}-{i%12+1:02d}"
# consecutive check and exact positive decimal check
for k in range(1, len(rows)):
    assert months(rows[k][0]) == months(rows[k-1][0]) + 1, rows[k]
bad = [r for r in rows if not r[1].replace(".", "", 1).isdigit()]
print("non-decimal GBP cells:", len(bad), "blank:", sum(1 for r in rows if r[1].strip() == ""))
rates = [(m, Fraction(v)) for m, v in rows]
changes = []
for (pm, pr), (m, r) in zip(rates, rates[1:]):
    ratio = r / pr
    # exact ln via Decimal: ln(num/den) with high precision
    lnv = (Decimal(ratio.numerator) / Decimal(ratio.denominator)).ln()
    changes.append((m, lnv, r == pr))
print("changes", len(changes), "first", changes[0][0], "last", changes[-1][0])
zeros = [m for m, _, z in changes if z]
print("exact zero changes", len(zeros), zeros)
def q(x, p):
    return Decimal(x).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)
def sd(vals):
    n = len(vals)
    mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()
w1 = [c for c in changes]
w2 = [c for c in changes if c[0] >= "2000-01"]
rate_1999_12 = dict(rates)["1999-12"]
print("window2 changes", len(w2), "first", w2[0][0], "last", w2[-1][0])
res = {}
for name, w in (("w1", w1), ("w2", w2)):
    vals = [c for _, c, _ in w]
    s = sd(vals)
    res[name] = s
    big = max(w, key=lambda c: abs(c[1]))
    print(name, "n", len(vals), "sd", s, "->", q(s, 6), "| 4dp:", q(s, 4))
    print(name, "largest |change|", q(abs(big[1]), 6), "at", big[0], "signed", q(big[1], 6))
    # telescoping residual
    start = rates[0][1] if name == "w1" else rate_1999_12
    tot = sum(vals)
    target = (Decimal(rates[-1][1].numerator) / Decimal(rates[-1][1].denominator) / (Decimal(start.numerator) / Decimal(start.denominator))).ln() if False else None
    lr = (rates[-1][1] / start)
    tgt = (Decimal(lr.numerator) / Decimal(lr.denominator)).ln()
    print(name, "telescoping residual", abs(tot - tgt))
d = res["w2"] - res["w1"]
print("difference", d, "->", q(d, 6))
print("ratio", res["w2"] / res["w1"], "->", q(res["w2"] / res["w1"], 4))
# nonzero counts and the first-window largest-move detail
print("nonzero w1:", len([c for c in w1 if not c[2]]))
