"""Round-9 verifier re-derivation (independent of the lab code): GBP windows, zero counts, blanks, months,
Lab 1 and Lab 2 numbers, Lesson-4 decimals, and the EUR blank count. Reads only the repository CSV."""
import csv
import math
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

CSV = sys.argv[1]
rows = list(csv.DictReader(open(CSV, encoding="utf-8", newline="")))
print("rows", len(rows), "first", rows[0]["month"], "last", rows[-1]["month"])
months = [r["month"] for r in rows]
def idx(m):
    y, mm = m.split("-")
    return int(y) * 12 + int(mm) - 1
gaps = [(months[i - 1], months[i]) for i in range(1, len(months)) if idx(months[i]) != idx(months[i - 1]) + 1]
print("month gaps", gaps)
for col in ["GBP", "EUR"]:
    blanks = [r["month"] for r in rows if r[col].strip() == ""]
    print(col, "blank count", len(blanks), "first blank", blanks[:1], "last blank", blanks[-1:])
gbp = [(r["month"], Decimal(r["GBP"])) for r in rows]
changes = []
for (pm, pv), (m, v) in zip(gbp, gbp[1:]):
    changes.append((m, math.log(float(v / pv))))
def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in vals) / (n - 1))
def q(x, p):
    return Decimal(repr(x)).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)
W = {
    "one": changes,
    "two": [c for c in changes if c[0] >= "2000-01"],
    "three": [c for c in changes if c[0] >= "2025-10"],
}
sds = {}
for k, w in W.items():
    vals = [c for _, c in w]
    s = sd(vals)
    sds[k] = s
    big = max(w, key=lambda t: abs(t[1]))
    zeros = sum(1 for v in vals if v == 0.0)
    print(f"window {k}: first {w[0][0]} last {w[-1][0]} n={len(vals)} zeros={zeros} sd_pct={q(100*s,2)} "
          f"sd_raw={s:.9f} stdev_check_diff={abs(100*(s-statistics.stdev(vals))):.3e} "
          f"largest={q(100*big[1],2)} at {big[0]}")
print("ratio two/one", q(sds['two']/sds['one'], 2), "raw", sds['two']/sds['one'])
print("diff one-two pct", q(100*(sds['one']-sds['two']), 2), "raw", 100*(sds['one']-sds['two']))
# Lesson 4 decimals check
print("sd one decimal (6dp)", f"{sds['one']:.6f}", "sd two decimal (6dp)", f"{sds['two']:.6f}")
# Lab 1 numbers with exact fractions
D = Fraction(100000)
fall = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rise = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
print("lab1 falling end real", float(D / fall[-1]), "rising end real", float(D / rise[-1]))
print("lab1 burden falling", float(100 * (fall[0] / fall[-1] - 1)), "rising", float(100 * (rise[0] / rise[-1] - 1)))
print("lab1 diff", float(D / fall[-1] - D / rise[-1]))
print("lab1 real debt at t=1 falling", float(D / fall[1]), "t=3 falling", float(D/fall[3]), "t=4 falling", float(D/fall[4]))
for name, p in (("falling", fall), ("rising", rise)):
    print("lab1", name, [f"{float(D / x):.4f}" for x in p])
# Lab 2
D2 = Fraction(40000)
path = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("lab2 real", [f"{float(D2/x):.6f}" for x in path])
print("lab2 burden", float(100 * (path[0] / path[-1] - 1)))
print("lab1 about-cents", float(Fraction(10000000) / Fraction(85, 100)), float(Fraction(10000000)/Fraction(85,100) - Fraction(10000000)/Fraction(115,100)))
