"""Alternative correct lab 3 (verifier round 9): Welford online mean/M2 for the sample sd, log change via
math.log(v) - math.log(prev), window selection by index, and the stdev agreement check against statistics.stdev.
A correct implementation: its printed output must equal the page block exactly."""
import csv, math, statistics
from decimal import Decimal, ROUND_HALF_UP

def q(x, p):
    return str(Decimal(x).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP))

def welford_sd(vals):
    mean, m2, n = 0.0, 0.0, 0
    for x in vals:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    return math.sqrt(m2 / (n - 1))

with open("data/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rows = list(csv.reader(h))
header = rows[0]
gi = header.index("GBP")
data = [(r[0], float(r[gi])) for r in rows[1:]]
print(f"GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
print(f"months in file: {len(data)}, {data[0][0]} to {data[-1][0]}")
changes = [(data[i][0], math.log(data[i][1]) - math.log(data[i - 1][1])) for i in range(1, len(data))]
def win(start_idx):
    return changes[start_idx:]
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
w3 = [c for c in changes if c[0] >= "2025-10"]
def rep(name, w):
    vals = [c for _, c in w]
    s = welford_sd(vals)
    assert abs(100 * (s - statistics.stdev(vals))) <= 1e-9, "disagree"
    zeros = sum(1 for v in vals if v == 0.0)
    big = max(w, key=lambda t: abs(t[1]))
    print(f"Window {name}, {w[0][0]} to {w[-1][0]}:")
    print(f"  changes: {len(vals)}")
    print(f"  exact zero changes: {zeros}")
    print(f"  sample sd, percent per month: {q(100 * s, 2)}")
    print(f"  largest monthly log change by size, percent, with its sign: {q(100 * big[1], 2)} ({big[0]})")
    return s
s1 = rep("one", w1)
s2 = rep("two", w2)
rep("three", w3)
print(f"ratio of window two to window one sd, two decimals: {q(s2 / s1, 2)}")
print(f"difference of window one minus window two sd, percent per month, two decimals: {q(100 * (s1 - s2), 2)}")
print("two-pass and statistics.stdev agree in all three windows: True")
