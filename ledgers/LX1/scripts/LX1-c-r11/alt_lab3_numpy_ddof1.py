"""Alternative correct lab 3 (verifier round 11): numpy std with ddof=1 for the sample sd, the stdev agreement check
with a looser 1e-6 tolerance, and log changes from numpy log of the ratio. A correct implementation: its printed
output must equal the page expected block exactly."""
import csv
import statistics
from decimal import Decimal, ROUND_HALF_UP

import numpy as np


def q(x, p):
    return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP))


rows = []
with open("data/fx_monthly.csv", encoding="utf-8", newline="") as h:
    for r in csv.DictReader(h):
        rows.append((r["month"], float(r["GBP"])))
months = [m for m, _ in rows]
vals = np.array([v for _, v in rows])
chg = np.log(vals[1:] / vals[:-1])
labels = months[1:]
print("GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
print(f"months in file: {len(rows)}, {months[0]} to {months[-1]}")


def win(lo, hi=None):
    idx = [i for i, m in enumerate(labels) if m >= lo and (hi is None or m < hi)]
    return idx


def report(idx):
    x = chg[idx]
    sd = float(np.std(x, ddof=1))
    assert abs(sd - statistics.stdev(x.tolist())) < 1e-6 / 100, "disagree"
    zeros = int(np.sum(x == 0.0))
    k = int(np.argmax(np.abs(x)))
    print(f"  changes: {len(x)}")
    print(f"  exact zero changes: {zeros}")
    print(f"  sample sd, percent per month: {q(100 * sd, 2)}")
    print(f"  largest monthly log change by size, percent, with its sign: {q(100 * x[k], 2)} ({labels[idx[k]]})")
    return sd


w1 = win("0000-00")
w2 = win("2000-01")
w3 = win("2025-10")
print(f"Window one, {labels[w1[0]]} to {labels[w1[-1]]}:")
s1 = report(w1)
print(f"Window two, {labels[w2[0]]} to {labels[w2[-1]]}:")
s2 = report(w2)
print(f"Window three, {labels[w3[0]]} to {labels[w3[-1]]}:")
report(w3)
print(f"ratio of window two to window one sd, two decimals: {q(s2 / s1, 2)}")
print(f"difference of window one minus window two sd, percent per month, two decimals: {q(100 * (s1 - s2), 2)}")
print("two-pass and statistics.stdev agree in all three windows: True")
