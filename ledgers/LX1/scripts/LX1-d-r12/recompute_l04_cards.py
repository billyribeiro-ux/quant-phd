"""Independent recomputation of the L04 numbers cited by LX1 cards (c054-c058, c063-c065, c068).

Reads course/assets/data/market/fx_monthly.csv (path given as argv[1]) with exact Fractions for the
zero test and the float path for dispersion, and prints every figure the cards cite.
Run with: python3 -I -W error recompute_l04_cards.py <path-to-fx_monthly.csv>
"""

import csv
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

path = sys.argv[1]
with open(path, encoding="utf-8", newline="") as handle:
    rows = [(r["month"], r["GBP"]) for r in csv.DictReader(handle)]

months = [m for m, _ in rows]
texts = [t for _, t in rows]
assert all(t and t.replace(".", "", 1).isdigit() for t in texts), "non-decimal GBP cell"
rates = [Fraction(t) for t in texts]
print("rows", len(rows), months[0], months[-1])


def y(m: str) -> int:
    return int(m[:4]) * 12 + int(m[5:7]) - 1


def month_of(i: int) -> str:
    return f"{i // 12:04d}-{i % 12 + 1:02d}"


# Monthly log changes dated by the later month.
changes = []
for i in range(1, len(rows)):
    changes.append((months[i], math.log(float(rates[i] / rates[i - 1])), rates[i] == rates[i - 1]))
print("changes", len(changes), changes[0][0], changes[-1][0])
zeros = [m for m, _, z in changes if z]
print("exact zero months", len(zeros), zeros, "nonzero", len(changes) - len(zeros))


def sample_sd(vals):
    n = len(vals)
    mean = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mean) ** 2 for v in vals) / (n - 1))


w1 = [c for _, c, _ in changes]
w2 = [c for m, c, _ in changes if m >= "2000-01"]
w2_months = [m for m, _, _ in changes if m >= "2000-01"]
sd1 = sample_sd(w1)
sd2 = sample_sd(w2)
print("window one n", len(w1), "sd", sd1)
print("window two n", len(w2), "sd", sd2, "first change dated", w2_months[0])
print("ratio sd2/sd1", sd2 / sd1)
print("difference sd2-sd1 unrounded", sd2 - sd1)
print("difference of printed 6dp", round(sd2, 6) - round(sd1, 6))


def half_up(x: float, places: int) -> str:
    return str(Decimal(x).quantize(Decimal(f"1e-{places}"), rounding=ROUND_HALF_UP))


print("sd1 6dp", half_up(sd1, 6), "sd2 6dp", half_up(sd2, 6))
print("ratio 4dp", half_up(sd2 / sd1, 4), "diff 6dp", half_up(sd2 - sd1, 6))
big1 = max(changes, key=lambda t: abs(t[1]))
print("largest abs overall", big1[0], big1[1])
big2 = max([t for t in changes if t[0] >= "2000-01"], key=lambda t: abs(t[1]))
print("largest abs window two", big2[0], big2[1])
big1w = max([t for t in changes], key=lambda t: abs(t[1]))
print("largest abs window one", big1w[0], big1w[1])
print("ln1.1", math.log(1.1), "simple-log", 0.1 - math.log(1.1))
