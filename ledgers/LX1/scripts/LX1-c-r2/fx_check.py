"""LX1-c round 2 verifier script: independent recomputation of the Lab 3 figures.

Reads course/assets/data/market/fx_monthly.csv given as argv[1] (run with python -I). Uses only the
standard library. Does not import the lab code. Rates are read as exact decimal strings.
"""
import csv
import math
import statistics
import sys
from decimal import Decimal
from fractions import Fraction

path = sys.argv[1]
with open(path, newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
print("rows:", len(rows), "first:", rows[0]["month"], "last:", rows[-1]["month"])
cols = [c for c in rows[0].keys() if c != "month"]
for c in cols:
    blanks = [r["month"] for r in rows if (r[c] or "").strip() == ""]
    print(f"column {c}: blanks={len(blanks)} first_blank={blanks[0] if blanks else None} last_blank={blanks[-1] if blanks else None}")

def months_ok(rs):
    def idx(m):
        y, mo = m.split("-")
        return int(y) * 12 + int(mo)
    for a, b in zip(rs, rs[1:]):
        assert idx(b["month"]) == idx(a["month"]) + 1, (a["month"], b["month"])
    return True
print("contiguous months:", months_ok(rows))

gbp = [(r["month"], Decimal(r["GBP"])) for r in rows]
changes = []  # (month, log change float, exact_zero bool)
for (pm, pv), (m, v) in zip(gbp, gbp[1:]):
    changes.append((m, math.log(float(v / pv)), v == pv))
print("total changes:", len(changes))

def window(lo, hi=None):
    return [c for c in changes if c[0] >= lo and (hi is None or c[0] <= hi)]

def report(name, w):
    vals = [c[1] for c in w]
    sd = statistics.stdev(vals)
    zeros_exact = sum(1 for c in w if c[2])
    zeros_float = sum(1 for c in w if c[1] == 0.0)
    big = max(w, key=lambda c: abs(c[1]))
    print(f"{name}: n={len(w)} months {w[0][0]}..{w[-1][0]} exact_zero={zeros_exact} float_zero={zeros_float} "
          f"sd_pct_per_month={100*sd:.10f} max_abs={100*abs(big[1]):.6f} at {big[0]} (signed {100*big[1]:.6f})")
    return sd

s1 = report("W1", window("1971-02"))
s2 = report("W2", window("2000-01"))
s3 = report("W3", window("2025-10"))
print("ratio W2/W1 =", f"{s2/s1:.10f}", "two decimals", f"{round(s2/s1, 2):.2f}")
print("W1 - W2 (percent per month, unrounded) =", f"{100*(s1-s2):.10f}")
print("sd decimals W1 =", f"{s1:.6f}", "W2 =", f"{s2:.6f}")
# Largest move in window one, outside window two?
w1_max = max(window("1971-02"), key=lambda c: abs(c[1]))
w2_max = max(window("2000-01"), key=lambda c: abs(c[1]))
print("W1 max month", w1_max[0], "W2 max month", w2_max[0])
# Sign of the largest move in window one
print("W1 max signed pct", f"{100*w1_max[1]:.6f}")
# Two rounding passes for W1 and W2 (Lab 3 rounds half up)
