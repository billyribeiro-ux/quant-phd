"""LX1 project lab 3 (rung 3 check) alternative correct implementation (verifier round 17): log changes as differences
of logarithms, dispersion by statistics.variance, Decimal rounding of the exact binary value of each float.

Written for the page as it stands at 700bf33f: no agreement check is printed, because the page claims none.
"""
import csv
import math
import statistics
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path


def show(value, places):
    return str(Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def main():
    with Path("data/fx_monthly.csv").open(encoding="utf-8", newline="") as fh:
        rows = [(r["month"], Decimal(r["GBP"])) for r in csv.DictReader(fh)]
    print("GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
    print(f"months in file: {len(rows)}, {rows[0][0]} to {rows[-1][0]}")
    changes = [(m, math.log(float(b)) - math.log(float(a))) for (_, a), (m, b) in zip(rows, rows[1:])]

    def report(window):
        vals = [v for _, v in window]
        sd = math.sqrt(statistics.variance(vals))
        zeros = sum(1 for v in vals if v == 0.0)
        big_m, big = max(window, key=lambda it: abs(it[1]))
        print(f"  changes: {len(vals)}")
        print(f"  exact zero changes: {zeros}")
        print(f"  sample sd, percent per month: {show(100 * sd, 2)}")
        print(f"  largest monthly log change by size, percent, with its sign: {show(100 * big, 2)} ({big_m})")
        return sd

    w1 = changes
    w2 = [c for c in changes if c[0] >= "2000-01"]
    w3 = [c for c in changes if c[0] >= "2025-10"]
    print(f"Window one, {w1[0][0]} to {w1[-1][0]}:")
    sd1 = report(w1)
    print(f"Window two, {w2[0][0]} to {w2[-1][0]}:")
    sd2 = report(w2)
    print(f"Window three, {w3[0][0]} to {w3[-1][0]}:")
    report(w3)
    print(f"ratio of window two to window one sd, two decimals: {show(sd2 / sd1, 2)}")
    print(f"difference of window one minus window two sd, percent per month, two decimals: {show(100 * (sd1 - sd2), 2)}")


main()
