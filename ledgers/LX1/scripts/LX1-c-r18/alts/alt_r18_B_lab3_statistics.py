"""Alternative correct implementation (verifier, round 18): project lab 3 (rung 3 check) with statistics.stdev, math.log1p on the exact ratio minus one, and index-based windows.

Reads data/fx_monthly.csv, GBP column, fails on a blank or non-decimal cell and on a month gap.
"""
import csv
import math
import re
import statistics
from decimal import ROUND_HALF_UP, Decimal

with open("data/fx_monthly.csv", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
for prev, cur in zip(rows, rows[1:]):
    y0, m0 = map(int, prev["month"].split("-"))
    y1, m1 = map(int, cur["month"].split("-"))
    if (y1 * 12 + m1) - (y0 * 12 + m0) != 1:
        raise ValueError(f"month gap at {cur['month']}")
for r in rows:
    if not re.fullmatch(r"\d+(\.\d+)?", r["GBP"]):
        raise ValueError(f"bad GBP cell at {r['month']}")
changes = []
for prev, cur in zip(rows, rows[1:]):
    ratio = Decimal(cur["GBP"]) / Decimal(prev["GBP"])
    changes.append((cur["month"], math.log1p(float(ratio - 1)), ratio == 1))
first_two = next(i for i, c in enumerate(changes) if c[0] >= "2000-01")
first_three = next(i for i, c in enumerate(changes) if c[0] >= "2025-10")
windows = [("Window one", changes), ("Window two", changes[first_two:]), ("Window three", changes[first_three:])]


def r2(x: float) -> str:
    return str(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


print("GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
print(f"months in file: {len(rows)}, {rows[0]['month']} to {rows[-1]['month']}")
sds = {}
for label, w in windows:
    vals = [v for _, v, _ in w]
    sd = statistics.stdev(vals)
    sds[label] = sd
    big_month, big_val, _ = max(w, key=lambda c: abs(c[1]))
    print(f"{label}, {w[0][0]} to {w[-1][0]}:")
    print(f"  changes: {len(vals)}")
    print(f"  exact zero changes: {sum(1 for _, _, z in w if z)}")
    print(f"  sample sd, percent per month: {r2(100 * sd)}")
    print(f"  largest monthly log change by size, percent, with its sign: {r2(100 * big_val)} ({big_month})")
print(f"ratio of window two to window one sd, two decimals: {r2(sds['Window two'] / sds['Window one'])}")
print(f"difference of window one minus window two sd, percent per month, two decimals: {r2(100 * (sds['Window one'] - sds['Window two']))}")
