"""Independent recomputation of every number on LX1 project.html (round 21), not using the lab code.

Usage: .venv/bin/python -I ledgers/LX1/scripts/LX1-c-r21/numbers_r21.py <repo_root>
Reads <repo_root>/course/assets/data/market/fx_monthly.csv only.
"""

import csv
import math
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
csv_path = root / "course/assets/data/market/fx_monthly.csv"


def half_up(x: Fraction, places: int) -> str:
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


# Lab 1 (independent)
D = Fraction(100000)
P_fall = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
P_rise = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
print("Lab1 real debt falling:", [half_up(D / p, 2) for p in P_fall])
print("Lab1 real debt rising :", [half_up(D / p, 2) for p in P_rise])
print("Lab1 burden falling   :", half_up(100 * (1 / P_fall[-1] - 1), 2), "exact", float(100 * (1 / P_fall[-1] - 1)))
print("Lab1 burden rising    :", half_up(100 * (1 / P_rise[-1] - 1), 2), "exact", float(100 * (1 / P_rise[-1] - 1)))
diff = D / P_fall[-1] - D / P_rise[-1]
print("Lab1 difference       :", half_up(diff, 2), "exact cents", float(diff * 100))

# Lab 2 (independent)
D2 = Fraction(40000)
P2 = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("Lab2 real debt        :", [half_up(D2 / p, 2) for p in P2])
print("Lab2 burden           :", half_up(100 * (1 / P2[-1] - 1), 2), "exact", float(100 * (1 / P2[-1] - 1)))
print("Lab2 inverted burden  :", half_up(100 * (P2[-1] - 1), 2))
print("Lab2 no-division real :", [half_up(D2 / 1, 2)] * 6)

# Lab 3 (independent): read the CSV with the csv module
with csv_path.open(encoding="utf-8", newline="") as fh:
    reader = csv.reader(fh)
    header = next(reader)
    rows = list(reader)
print("header:", header)
print("rows:", len(rows), "first:", rows[0][0], "last:", rows[-1][0])
col = header.index("GBP")
blank_counts = {h: sum(1 for r in rows if r[i].strip() == "") for i, h in enumerate(header) if h != "month"}
print("blank cells per column:", blank_counts)

# month gaps check
def mi(m: str) -> int:
    y, mo = m.split("-")
    return int(y) * 12 + int(mo)

gaps = [(rows[i][0], rows[i + 1][0]) for i in range(len(rows) - 1) if mi(rows[i + 1][0]) != mi(rows[i][0]) + 1]
print("month gaps:", gaps)

series = [(r[0], Fraction(r[col])) for r in rows]
changes = []
for (m0, s0), (m1, s1) in zip(series, series[1:]):
    changes.append((m1, math.log(float(s1 / s0)), s1 == s0))


def window(lo: str, hi: str):
    return [c for c in changes if lo <= c[0] <= hi]


w1 = window("1971-01", "9999-12")
w2 = window("2000-01", "9999-12")
w3 = window("2025-10", "9999-12")
res = {}
for name, w in (("w1", w1), ("w2", w2), ("w3", w3)):
    vals = [c[1] for c in w]
    sd = statistics.stdev(vals)  # denominator n - 1
    zeros = sum(1 for c in w if c[2])
    big = max(w, key=lambda c: abs(c[1]))
    res[name] = sd
    print(
        name,
        "first",
        w[0][0],
        "last",
        w[-1][0],
        "n",
        len(vals),
        "zeros",
        zeros,
        "sd%/mo",
        repr(100 * sd),
        "->",
        half_up(Fraction(100 * sd), 2),
        "largest",
        big[0],
        repr(100 * big[1]),
    )
print("ratio w2/w1 exact", repr(res["w2"] / res["w1"]), "->", half_up(Fraction(res["w2"] / res["w1"]), 2))
print("diff w1-w2 exact %/mo", repr(100 * (res["w1"] - res["w2"])), "->", half_up(Fraction(100 * (res["w1"] - res["w2"])), 2))
print("sd w1 decimal", repr(res["w1"]), "sd w2 decimal", repr(res["w2"]))
print("w2 - w1 (pure printed) =", round(res["w2"] - res["w1"], 6))
print("w3 change count and zeros", len(w3), sum(1 for c in w3 if c[2]))
# Lab3 sd check using exact rationals of log? (n/a) ; check that no change is within tie distance of a rounding boundary
for name, v in (("w1", 100 * res["w1"]), ("w2", 100 * res["w2"]), ("w3", 100 * statistics.stdev([c[1] for c in w3])), ("ratio", res["w2"] / res["w1"]), ("diff", 100 * (res["w1"] - res["w2"]))):
    frac = (v * 100) % 1
    print("boundary distance", name, abs(frac - 0.5))
