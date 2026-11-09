"""Independent re-derivation of project Lab 3 (GBP, three windows) for LX1-c round 19.

Uses Decimal ln at 60 digits (not math.log), statistics.stdev (exact-fraction internals), and a
Decimal half-up quantize of the exact figures. Reads the CSV at a path given as argv[1] and
prints one line per figure. Run as: python -I -W error <this> course/assets/data/market/fx_monthly.csv
"""
import csv
import statistics
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 60
path = sys.argv[1]
with open(path, encoding="utf-8", newline="") as fh:
    rows = list(csv.reader(fh))
header = rows[0]
gi = header.index("GBP")
data = []
for r in rows[1:]:
    data.append((r[0], r[gi]))
# blank / gap checks
for m, c in data:
    assert c not in ("", None), m
def idx(m):
    y, mo = m.split("-")
    return int(y) * 12 + int(mo) - 1
for (a, _), (b, _) in zip(data, data[1:]):
    assert idx(b) == idx(a) + 1, (a, b)
print("months", len(data), data[0][0], data[-1][0])
changes = []
for (pm, pv), (m, v) in zip(data, data[1:]):
    ratio = Decimal(v) / Decimal(pv)
    changes.append((m, ratio.ln()))

def q2(x):
    return (x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def window(lo):
    return [(m, c) for m, c in changes if m >= lo]
w1 = changes
w2 = window("2000-01")
w3 = window("2025-10")
sds = {}
for name, w in (("w1", w1), ("w2", w2), ("w3", w3)):
    vals = [c for _, c in w]
    sd = Decimal(statistics.stdev([float(v) for v in vals]))  # float only for stdev input; exact pieces below
    # exact-decimal sd (two-pass) for an independent cross-check
    n = len(vals)
    mean = sum(vals, Decimal(0)) / n
    sd_dec = (sum(((v - mean) ** 2 for v in vals), Decimal(0)) / (n - 1)).sqrt()
    zeros = sum(1 for v in vals if v == 0)
    big_m, big_v = max(w, key=lambda t: abs(t[1]))
    sds[name] = sd_dec
    print(name, "n", n, "first", w[0][0], "last", w[-1][0], "zeros", zeros)
    print("  sd_dec", sd_dec.quantize(Decimal("0.000000000001")), "sd_stdev", sd)
    print("  sd percent two-dp", q2(100 * sd_dec), "largest", q2(100 * big_v), big_m, "sign", "+" if big_v > 0 else "-")
ratio = sds["w2"] / sds["w1"]
print("ratio w2/w1 unrounded", ratio.quantize(Decimal("0.000000001")), "two-dp", q2(ratio))
diff = 100 * (sds["w1"] - sds["w2"])
print("difference w1-w2 percent unrounded", diff.quantize(Decimal("0.000000001")), "two-dp", q2(diff))
