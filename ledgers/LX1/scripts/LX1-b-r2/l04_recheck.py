"""Independent recomputation of LX1 L04 numbers from the CSV, without importing the lab twin.

Uses Decimal for the rates (exact parse) and math for logs. Run with: python -I this.py <csv>
"""
import csv, math, sys
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction
getcontext().prec = 60
rows = []
with open(sys.argv[1], encoding="utf-8", newline="") as h:
    r = csv.reader(h)
    header = next(r)
    gi = header.index("GBP"); mi = header.index("month")
    for rec in r:
        rows.append((rec[mi], Fraction(rec[gi])))
print("header", header)
print("n rows", len(rows), rows[0][0], rows[-1][0])
def mi_(s):
    y, m = s.split("-"); return int(y) * 12 + int(m) - 1
for a, b in zip(rows, rows[1:]):
    assert mi_(b[0]) == mi_(a[0]) + 1, (a, b)
print("consecutive months ok")
ch = [(rows[i][0], math.log(float(rows[i][1] / rows[i - 1][1]))) for i in range(1, len(rows))]
zeros = [m for i, m in [(i, rows[i][0]) for i in range(1, len(rows))] if rows[i][1] == rows[i - 1][1]]
print("zero changes", len(zeros), zeros)
print("nonzero", len(ch) - len(zeros))
def sd(vals):
    n = len(vals); mean = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mean) ** 2 for v in vals) / (n - 1))
w1 = [c for _, c in ch]
w2_items = [(m, c) for m, c in ch if m >= "2000-01"]
w2 = [c for _, c in w2_items]
s1, s2 = sd(w1), sd(w2)
print("n1", len(w1), "n2", len(w2))
print("sd1 exact", repr(s1), "sd2", repr(s2))
print("diff", repr(s2 - s1), "ratio", repr(s2 / s1))
q = lambda x, p: Decimal(x).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)
print("sd1 6dp", q(s1, 6), "sd2 6dp", q(s2, 6), "diff 6dp", q(s2 - s1, 6), "ratio 4dp", q(s2 / s1, 4))
mx1 = max(ch, key=lambda t: abs(t[1])); mx2 = max(w2_items, key=lambda t: abs(t[1]))
print("max1", mx1, "max2", mx2)
print("first change window2 dated", w2_items[0][0], "last", w2_items[-1][0], "rate before", [x for x in rows if x[0]=="1999-12"])
print("rows 1971-01 first", rows[0])
# telescoping
print("telescope w1", abs(math.fsum(w1) - math.log(float(rows[-1][1] / rows[0][1]))))
print("telescope w2", abs(math.fsum(w2) - math.log(float(rows[-1][1] / [x for x in rows if x[0]=="1999-12"][0][1]))))
# P2/R2/quiz
L = mx1[1]
print("L exact", repr(L))
h = (math.exp(L) - 1) / (math.exp(L) + 1)
print("h exact", repr(h), "tanh(L/2)", repr(math.tanh(L / 2)), "h 4dp", q(h, 4), "6dp", q(h,6))
print("bound at 0.0678", repr(math.log(1.0678 / 0.9322)), q(math.log(1.0678/0.9322), 6), q(math.log(1.0678/0.9322), 4))
print("bound at 0.0678 vs L", math.log(1.0678/0.9322) - L)
# E2 simple change
print("simple change 2008-10", repr(math.exp(mx2[1]) - 1), q(math.exp(mx2[1]) - 1, 6))
print("ln1.1", repr(math.log(1.1)), q(math.log(1.1), 6), "diff", repr(0.1 - math.log(1.1)), q(0.1 - math.log(1.1), 6))
print("M1 ln", repr(math.log(1.375/1.25)))
print("sum sq check M2", sd([0.01, 0.03, -0.02]), q(sd([0.01,0.03,-0.02]),6), q(math.sqrt(19/30000),6), 19/15000)
