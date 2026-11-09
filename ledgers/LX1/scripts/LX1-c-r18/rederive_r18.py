"""Round-18 LX1-c rederivation (written by the verifier). Independent of the lab twins: exact Fractions, math only.

Usage: python -I rederive_r18.py <checkout_root>
"""
import csv
import math
import pathlib
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

ROOT = pathlib.Path(sys.argv[1]).resolve()
CSV = ROOT / "course/assets/data/market/fx_monthly.csv"

with CSV.open(encoding="utf-8", newline="") as h:
    rdr = csv.DictReader(h)
    fields = rdr.fieldnames
    rows = list(rdr)
print("fields:", fields)
print("rows:", len(rows), rows[0]["month"], rows[-1]["month"])
gbp = [r["GBP"] for r in rows]
blank = [r["month"] for r in rows if not r["GBP"].strip()]
print("GBP blank cells:", len(blank))
print("EUR blank cells:", sum(1 for r in rows if not r["EUR"].strip()), "first EUR nonblank:", next(r["month"] for r in rows if r["EUR"].strip()))

def ym(m):
    y, mo = m.split("-")
    return int(y) * 12 + int(mo) - 1

# exact log changes are not exact; zero test on exact ratio
changes = []  # (month, exact ratio Fraction, float log change)
for prev, cur in zip(rows, rows[1:]):
    a = Fraction(Decimal(prev["GBP"]))
    b = Fraction(Decimal(cur["GBP"]))
    assert ym(cur["month"]) == ym(prev["month"]) + 1, (prev["month"], cur["month"])
    changes.append((cur["month"], b / a, math.log(float(b / a))))
print("changes total:", len(changes), changes[0][0], changes[-1][0])

def window(lo):
    return [c for c in changes if c[0] >= lo]

def stats(w):
    vals = [c[2] for c in w]
    n = len(vals)
    mean = math.fsum(vals) / n
    sd = math.sqrt(math.fsum((v - mean) ** 2 for v in vals) / (n - 1))
    zeros_exact = [c[0] for c in w if c[1] == 1]
    zeros_float = [c[0] for c in w if c[2] == 0.0]
    big = max(w, key=lambda c: abs(c[2]))
    return n, sd, zeros_exact, zeros_float, big

w1 = changes
w2 = window("2000-01")
w3 = window("2025-10")
s1 = stats(w1); s2 = stats(w2); s3 = stats(w3)
for name, s, w in (("w1", s1, w1), ("w2", s2, w2), ("w3", s3, w3)):
    n, sd, ze, zf, big = s
    print(name, "first", w[0][0], "last", w[-1][0], "n", n, "sd%/mo", 100 * sd, "zeros exact", len(ze), ze, "zeros float", len(zf))
    print(name, "largest by size", big[0], 100 * big[2])
print("sd decimals w1 w2:", round(s1[1], 6), round(s2[1], 6), "exact", s1[1], s2[1])
ratio = s2[1] / s1[1]
print("ratio unrounded:", repr(ratio), "2dp:", Decimal(ratio).quantize(Decimal("0.01"), ROUND_HALF_UP))
diff = 100 * (s1[1] - s2[1])
print("difference unrounded (pct/mo):", repr(diff), "2dp:", Decimal(diff).quantize(Decimal("0.01"), ROUND_HALF_UP))
print("percent fall in dispersion from ratio: 100*(1-ratio) =", 100 * (1 - ratio))
print("ratio from rounded inputs 2.47/2.79 =", 2.47 / 2.79)
print("w2 zero-change months float:", s2[3])
print("w3 sd%:", 100 * s3[1])
# cross-check with statistics module (independent algorithm)
print("statistics.stdev w1 %:", 100 * statistics.stdev([c[2] for c in w1]), " w2 %:", 100 * statistics.stdev([c[2] for c in w2]), " w3 %:", 100 * statistics.stdev([c[2] for c in w3]))
