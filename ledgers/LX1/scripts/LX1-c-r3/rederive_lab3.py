"""Independent re-derivation of LX1 project Lab 3 figures with Decimal (50 digits) and a separate sd routine."""
import csv, sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
months = [r["month"] for r in rows]
def idx(m): return int(m[:4]) * 12 + int(m[5:7])
for a, b in zip(months, months[1:]):
    assert idx(b) == idx(a) + 1, (a, b)
print("rows", len(rows), months[0], months[-1])
for col in ["GBP", "EUR", "CAD", "JPY"]:
    blanks = [r["month"] for r in rows if r[col].strip() == ""]
    first = next((r["month"] for r in rows if r[col].strip()), None)
    print(col, "blanks", len(blanks), "first obs", first, "last blank", blanks[-1] if blanks else None)
def ln(x): return x.ln()
vals = [(rows[i]["month"], Decimal(rows[i]["GBP"]), Decimal(rows[i-1]["GBP"])) for i in range(1, len(rows))]
changes = [(m, ln(s / p)) for m, s, p in vals]
def sd(xs):
    n = len(xs); mu = sum(xs) / n
    return (sum((x - mu) ** 2 for x in xs) / (n - 1)).sqrt()
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
w3 = [c for c in changes if c[0] >= "2025-10"]
res = {}
for name, w in [("w1", w1), ("w2", w2), ("w3", w3)]:
    xs = [c for _, c in w]
    s = sd(xs)
    zeros = sum(1 for x in xs if x == 0)
    big = max(w, key=lambda t: abs(t[1]))
    res[name] = s
    q = (100 * s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    print(name, "n", len(xs), "first", w[0][0], "last", w[-1][0], "zeros", zeros, "sd%", q, "unrounded sd%", (100*s).quantize(Decimal("0.000001")), "largest", (100*big[1]).quantize(Decimal("0.01")), big[0])
print("ratio w2/w1", (res["w2"] / res["w1"]).quantize(Decimal("0.0001")))
print("diff sd w1-w2 %/month unrounded", (100 * (res["w1"] - res["w2"])).quantize(Decimal("0.000001")))
print("sd decimals w1, w2", res["w1"].quantize(Decimal("0.000001")), res["w2"].quantize(Decimal("0.000001")))
print("w1 minus w2 rounded-figures", Decimal("2.79") - Decimal("2.47"))
print("biggest abs in w1 excludes w2 check: max abs w1 date", max(w1, key=lambda t: abs(t[1]))[0])
