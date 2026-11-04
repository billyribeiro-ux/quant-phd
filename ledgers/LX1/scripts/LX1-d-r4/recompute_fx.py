"""Independent recomputation of the L04 GBP figures in cards c054-c058, c059, c065, c068, c069 (no lab code reused)."""
import csv
import math
import sys
from fractions import Fraction

path = sys.argv[1]
with open(path, encoding="utf-8", newline="") as h:
    rows = list(csv.DictReader(h))
print("rows", len(rows), "first", rows[0]["month"], "last", rows[-1]["month"], "columns", list(rows[0].keys()))
months = [r["month"] for r in rows]
gbp = [r["GBP"] for r in rows]
bad = [(m, v) for m, v in zip(months, gbp) if not v.replace(".", "", 1).isdigit()]
print("non-decimal GBP cells:", bad[:5], len(bad))
# consecutive months
def idx(m):
    y, mm = m.split("-")
    return int(y) * 12 + int(mm) - 1
print("consecutive:", all(idx(months[i + 1]) == idx(months[i]) + 1 for i in range(len(months) - 1)))
x = [Fraction(v) for v in gbp]
# log changes (float from exact ratio)
ch = [(months[i], math.log(float(x[i] / x[i - 1]))) for i in range(1, len(x))]
print("changes:", len(ch), ch[0][0], ch[-1][0])
zeros = [m for i, (m, c) in enumerate(ch) if x[months.index(m)] == x[months.index(m) - 1]]
print("exact zero months:", zeros, len(zeros))
print("exact zero months via fraction equality over all rows:", [months[i] for i in range(1, len(x)) if x[i] == x[i - 1]])
print("zero changes (float == 0):", sum(1 for _, c in ch if c == 0.0))
w1 = ch
w2 = [(m, c) for m, c in ch if m >= "2000-01"]
print("window2 changes:", len(w2), w2[0][0], "first uses rate of", months[months.index(w2[0][0]) - 1])


def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))


s1 = sd([c for _, c in w1])
s2 = sd([c for _, c in w2])
print(f"sd1 = {s1!r}  -> {s1:.6f}")
print(f"sd2 = {s2!r}  -> {s2:.6f}")
print(f"diff = {s2 - s1!r} -> {s2 - s1:.6f}")
print(f"ratio = {s2 / s1!r} -> {s2 / s1:.4f}")
print(f"nonzero in window1: {sum(1 for _, c in w1 if c != 0.0)} of {len(w1)}")
big1 = max(w1, key=lambda it: abs(it[1]))
big2 = max(w2, key=lambda it: abs(it[1]))
print("largest abs w1:", big1, "w2:", big2)
print("largest abs w2 ties:", sorted([(abs(c), m) for m, c in w2], reverse=True)[:3])
# telescoping
print("telescoping w1:", abs(math.fsum(c for _, c in w1) - math.log(float(x[-1] / x[0]))) <= 1e-12)
print("telescoping w2:", abs(math.fsum(c for _, c in w2) - math.log(float(x[-1] / x[months.index("1999-12")]))) <= 1e-12)
# ln 1.1
print("ln1.1", math.log(1.1), "1-ln", 0.1 - math.log(1.1))
