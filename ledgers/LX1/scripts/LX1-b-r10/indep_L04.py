"""Independent recomputation of the L04 GBP-column statistics (exact Decimal parse, math.log, statistics by hand).

Usage: python3 -I indep_L04.py <checkout>
"""
import csv
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

root = Path(sys.argv[1])
rows = list(csv.DictReader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8")))
months = [r["month"] for r in rows]
gbp_text = [r["GBP"] for r in rows]
blanks = [m for m, v in zip(months, gbp_text) if v.strip() == ""]
print("rows", len(rows), "first", months[0], "last", months[-1], "GBP blank cells", len(blanks))
x = [Decimal(v) for v in gbp_text]
assert all(v > 0 for v in x)
ell = [(months[t], math.log(float(x[t] / x[t - 1]))) for t in range(1, len(x))]
zeros = [m for m, v in ell if x[months.index(m)] == x[months.index(m) - 1]]
print("changes", len(ell), "first change", ell[0][0], "last", ell[-1][0])
print("exactly zero changes (decimal equality):", zeros)


def sd(vals):
    n = len(vals)
    mean = sum(vals) / n
    return math.sqrt(sum((v - mean) ** 2 for v in vals) / (n - 1))


w1 = [v for m, v in ell]
w2 = [v for m, v in ell if m >= "2000-01"]
print("window two changes", len(w2), "first", [m for m, v in ell if m >= "2000-01"][0])
s1, s2 = sd(w1), sd(w2)
print("sd w1 %.9f  sd w2 %.9f" % (s1, s2))
print("diff w2-w1 %.9f  ratio %.9f" % (s2 - s1, s2 / s1))
print("diff of printed 6dp values:", round(s2, 6) - round(s1, 6))
mx1 = max(ell, key=lambda p: abs(p[1]))
mx2 = max([p for p in ell if p[0] >= "2000-01"], key=lambda p: abs(p[1]))
print("max abs w1", mx1, "max abs w2", mx2)
print("telescoping w1 err", abs(sum(w1) - math.log(float(x[-1] / x[0]))))
print("telescoping w2 err", abs(sum(w2) - math.log(float(x[-1] / x[months.index('1999-12')]))))
print("ln 1.1", math.log(1.1), "diff from 0.10", 0.10 - math.log(1.1))
