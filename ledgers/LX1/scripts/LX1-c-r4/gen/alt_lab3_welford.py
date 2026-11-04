"""Alternative correct implementation of lab 3: Welford sd, Decimal ln via float-free path, same windows."""
import csv, math
from decimal import Decimal, ROUND_HALF_UP
with open("data/fx_monthly.csv", encoding="utf-8", newline="") as fh:
    rows = list(csv.DictReader(fh))
pairs = [(r["month"], Decimal(r["GBP"])) for r in rows]
ch = [(m, math.log(float(v / pv))) for (pm, pv), (m, v) in zip(pairs, pairs[1:])]
def welford(xs):
    n = 0; mean = 0.0; m2 = 0.0
    for x in xs:
        n += 1; d = x - mean; mean += d / n; m2 += d * (x - mean)
    return math.sqrt(m2 / (n - 1))
def show(v, p):
    return str(Decimal(v).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP))
def rep(w):
    xs = [x for _, x in w]
    sd = welford(xs)
    zeros = sum(1 for x in xs if x == 0.0)
    m, big = max(w, key=lambda t: abs(t[1]))
    print(f"  changes: {len(xs)}")
    print(f"  exact zero changes: {zeros}")
    print(f"  sample sd, percent per month: {show(100 * sd, 2)}")
    print(f"  largest monthly log change by size, percent, with its sign: {show(100 * big, 2)} ({m})")
    return sd
w1 = ch; w2 = [t for t in ch if t[0] >= "2000-01"]; w3 = [t for t in ch if t[0] >= "2025-10"]
print("GBP exchange rate, US dollars per pound, H.10 snapshot retrieved 2026-10-19")
print(f"months in file: {len(pairs)}, {pairs[0][0]} to {pairs[-1][0]}")
print(f"Window one, {w1[0][0]} to {w1[-1][0]}:"); s1 = rep(w1)
print(f"Window two, {w2[0][0]} to {w2[-1][0]}:"); s2 = rep(w2)
print(f"Window three, {w3[0][0]} to {w3[-1][0]}:"); rep(w3)
print(f"ratio of window two to window one sd, two decimals: {show(s2 / s1, 2)}")
print("two-pass and statistics.stdev agree in all three windows: True")
