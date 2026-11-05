"""Independent recomputation of L04 Part B-D numbers from the embedded CSV (LX1-b r7). Uses Decimal for display."""
import csv, math, sys
from decimal import Decimal, ROUND_HALF_UP
path = sys.argv[1]
with open(path, newline="", encoding="utf-8") as fh:
    rows = list(csv.reader(fh))
hdr = rows[0]; gi = hdr.index("GBP"); mi = hdr.index("month")
data = [(r[mi], r[gi]) for r in rows[1:]]
print("header:", hdr, "n rows:", len(data), data[0][0], data[-1][0])
vals = []
for m, s in data:
    assert s.replace(".", "", 1).isdigit(), (m, s)
    vals.append((m, float(s)))
chg = [(vals[i][0], math.log(vals[i][1] / vals[i-1][1])) for i in range(1, len(vals))]
zeros = [m for m, c in chg if c == 0.0]
print("changes:", len(chg), "zeros:", zeros, "nonzero:", len(chg) - len(zeros))
def sd(xs):
    n = len(xs); mu = sum(xs) / n
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
w1 = [c for _, c in chg]; w2 = [c for m, c in chg if m >= "2000-01"]
s1, s2 = sd(w1), sd(w2)
print("n w1", len(w1), "n w2", len(w2), "first w2", [m for m, _ in chg if m >= "2000-01"][0])
print("sd1 %.12f sd2 %.12f diff %.12f ratio %.12f" % (s1, s2, s2 - s1, s2 / s1))
print("printed sd1 6dp:", Decimal(s1).quantize(Decimal("1e-6"), ROUND_HALF_UP), "sd2:", Decimal(s2).quantize(Decimal("1e-6"), ROUND_HALF_UP))
print("diff printed:", Decimal(s2 - s1).quantize(Decimal("1e-6"), ROUND_HALF_UP), "ratio 4dp:", Decimal(s2 / s1).quantize(Decimal("1e-4"), ROUND_HALF_UP))
print("printed-sds diff:", round(0.024700 - 0.027935, 6))
b1 = max(chg, key=lambda x: abs(x[1])); b2 = max([x for x in chg if x[0] >= "2000-01"], key=lambda x: abs(x[1]))
print("largest w1:", b1, "largest w2:", b2)
print("sum identity w1:", abs(sum(w1) - math.log(vals[-1][1] / vals[0][1])))
print("sum identity w2:", abs(sum(w2) - math.log(vals[-1][1] / dict(vals)["1999-12"])))
print("MIN/MAX rate:", min(v for _, v in vals), max(v for _, v in vals))
