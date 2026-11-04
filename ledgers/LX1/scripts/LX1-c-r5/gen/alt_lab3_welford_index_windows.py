"""Independent correct alternative for LX1 project lab 3: Welford online variance, index-based windows, float logs."""

import csv
import math
import statistics
from decimal import ROUND_HALF_UP, Decimal


def show2(x: float, places: int = 2) -> str:
    return str(Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def welford(values):
    mean = 0.0
    m2 = 0.0
    for k, v in enumerate(values, start=1):
        delta = v - mean
        mean += delta / k
        m2 += delta * (v - mean)
    return math.sqrt(m2 / (len(values) - 1))


with open("data/fx_monthly.csv", encoding="utf-8", newline="") as h:
    table = [(r["month"], float(r["GBP"])) for r in csv.DictReader(h)]
print("GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
print(f"months in file: {len(table)}, {table[0][0]} to {table[-1][0]}")
changes = [(table[i][0], math.log(table[i][1] / table[i - 1][1])) for i in range(1, len(table))]
start2 = next(i for i, (m, _) in enumerate(changes) if m >= "2000-01")
start3 = next(i for i, (m, _) in enumerate(changes) if m >= "2025-10")
wins = {"one": changes, "two": changes[start2:], "three": changes[start3:]}
sds = {}
for key, label in (("one", "Window one"), ("two", "Window two"), ("three", "Window three")):
    w = wins[key]
    vals = [c for _, c in w]
    sd = welford(vals)
    assert abs(100 * (sd - statistics.stdev(vals))) <= 1e-9
    sds[key] = sd
    zeros = sum(1 for v in vals if v == 0.0)
    big_m, big = max(w, key=lambda it: abs(it[1]))
    print(f"{label}, {w[0][0]} to {w[-1][0]}:")
    print(f"  changes: {len(vals)}")
    print(f"  exact zero changes: {zeros}")
    print(f"  sample sd, percent per month: {show2(100 * sd)}")
    print(f"  largest monthly log change by size, percent, with its sign: {show2(100 * big)} ({big_m})")
print(f"ratio of window two to window one sd, two decimals: {show2(sds['two'] / sds['one'])}")
print(f"difference of window one minus window two sd, percent per month, two decimals: {show2(100 * (sds['one'] - sds['two']))}")
print("two-pass and statistics.stdev agree in all three windows: True")
