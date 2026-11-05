"""LX1-b round 11: independent re-derivation of every prose number in L03 and L04 (own code, not the twins).

Usage: python -I ledgers/LX1/scripts/LX1-b-r11/rederive_r11.py <checkout>
"""

import csv
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
D = Fraction(1_000_000)
N0 = Fraction(4_000_000)
delta = Fraction(1, 50)
H = 12
C = N0 + D


def P(m, t):
    return (1 - delta) ** min(t, m)


def V(m, t):
    return D / P(m, t)


def ell(x):
    return x / (C - x)


def L(m, t):
    return V(m, t) / (N0 - (V(m, t) - D))


def depth_exact(m):
    # phi = beta = 1; f_t = L_t - L_0
    return max(L(m, t) - L(m, 0) for t in range(H + 1))


def r(x, places):
    q = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fraction) else Decimal(x)
    return q.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


print("L03 real debt V_12 exact (cents):", float(V(12, 12)), "rounded:", math.floor(V(12, 12) + Fraction(1, 2)))
print("L03 V_12 exact decimal 1274345.2124? ->", r(V(12, 12), 4))
print("L03 V_4 exact:", r(V(4, 4), 4), "P_4 =", P(4, 4), float(P(4, 4)))
print("L03 depth X exact:", float(depth_exact(12)), "percent:", float(100 * depth_exact(12)))
print("L03 depth Y exact:", float(depth_exact(4)), "percent:", float(100 * depth_exact(4)))
print("L03 X-Y exact (percentage points):", float(100 * (depth_exact(12) - depth_exact(4))))
print("L03 printed X-Y from rounded:", Decimal("9.20") - Decimal("2.69"))
print("L03 ratio X/Y:", float(depth_exact(12) / depth_exact(4)))
for bp in [Fraction(1, 2), Fraction(1), Fraction(3)]:
    # depth scales with beta*phi; ratio independent (Corollary 3.4). Compute with phi=bp, beta=1
    pass
# Closed-form check of Prop 3.2(b): depth(m) = beta*phi*(ell(V_m)-ell(D))
for m in (4, 12):
    cf = ell(V(m, m)) - ell(D)
    print("L03 closed form m=%d: %.10f  vs direct %.10f" % (m, float(cf), float(depth_exact(m))))
# Part C: depths per m, monotone checks
ds = [depth_exact(m) for m in range(H + 1)]
print("L03 monotone non-decreasing:", all(ds[i] <= ds[i + 1] for i in range(H)), "strict:", all(ds[i] < ds[i + 1] for i in range(H)))
# Part D ratio for any phi,beta: depth ~ beta*phi*g(m)
g = lambda m: ell(V(m, m)) - ell(D)  # noqa: E731
print("L03 ratio g(12)/g(4) exact:", float(g(12) / g(4)), "squared ratio:", float((g(12) / g(4)) ** 2))
# M1-M3 numbers
P4 = (Fraction(49, 50)) ** 4
print("M1 P4 =", P4, "=", float(P4), "V4 =", float(D / P4))
V4 = D / P4
N4 = N0 - (V4 - D)
print("M2 N4 =", float(N4), "rounded", math.floor(N4 + Fraction(1, 2)))
print("M3 L4 =", float(V4 / N4), "4dp", r(V4 / N4, 4))
# E1 exact depth Y
print("E1 depth Y exact percent:", float(100 * depth_exact(4)))
# Quiz numeric: V_12 rounds to 1274345
print("quiz real debt X t=12 rounded:", math.floor(V(12, 12) + Fraction(1, 2)), "exact:", float(V(12, 12)))
# Premium at t=12 displayed 0.0920 etc
print("premium X t=12 exact:", float(L(12, 12) - L(12, 0)), "leverage X t=12:", float(L(12, 12)))
print("premium Y t=4 exact:", float(L(4, 4) - L(4, 0)), "leverage Y t=4:", float(L(4, 4)))
# Misconception: squared premium claim, ratio of squares
print("squared-premium ratio would be", float((g(12) / g(4)) ** 2))

# -------- L04 --------
rows = []
with (root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("L04 csv rows:", len(rows), "first", rows[0][0], "last", rows[-1][0])
blank = [m for m, v in rows if not v.strip()]
print("L04 blank GBP cells:", len(blank))
fr = [(m, Fraction(v)) for m, v in rows]
# month consecutive
def mi(s):
    y, mo = s.split("-")
    return int(y) * 12 + int(mo) - 1
print("L04 consecutive months:", all(mi(fr[i + 1][0]) == mi(fr[i][0]) + 1 for i in range(len(fr) - 1)))
zeros = [fr[i][0] for i in range(1, len(fr)) if fr[i][1] == fr[i - 1][1]]
print("L04 exact zero changes:", zeros)
logs = [(fr[i][0], math.log(float(fr[i][1] / fr[i - 1][1]))) for i in range(1, len(fr))]
print("L04 window one n:", len(logs), "first", logs[0][0], "last", logs[-1][0])
w2 = [(m, c) for m, c in logs if m >= "2000-01"]
idx_1999_12 = [i for i, (m, _) in enumerate(fr) if m == "1999-12"][0]
print("L04 window two n:", len(w2), "first", w2[0][0], "last", w2[-1][0], "rate before:", fr[idx_1999_12][0], fr[idx_1999_12][1])


def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))


s1 = sd([c for _, c in logs])
s2 = sd([c for _, c in w2])
print("L04 sd1 =", repr(s1), "sd2 =", repr(s2))
print("L04 sd1 4/6dp:", r(Fraction(s1), 6), "sd2:", r(Fraction(s2), 6))
print("L04 difference unrounded:", repr(s2 - s1), "rounded:", r(Fraction(s2 - s1), 6))
print("L04 ratio:", repr(s2 / s1), "4dp:", r(Fraction(s2 / s1), 4))
big1 = max(logs, key=lambda it: abs(it[1]))
big2 = max(w2, key=lambda it: abs(it[1]))
print("L04 largest window one:", big1, "window two:", big2)
print("L04 simple change at largest window two:", math.exp(big2[1]) - 1)
print("L04 telescoping w1:", abs(math.fsum(c for _, c in logs) - math.log(float(fr[-1][1] / fr[0][1]))))
print("L04 telescoping w2:", abs(math.fsum(c for _, c in w2) - math.log(float(fr[-1][1] / fr[idx_1999_12][1]))))
# Part A model: 12 rates at 2 -> 11 changes zero
print("L04 model sd:", sd([0.0] * 11))
# R2 numbers
Lh = 0.135846
h = math.tanh(Lh / 2)
print("R2 h = tanh(L/2) =", repr(h), "=> 0.067819?", round(h, 6))
print("R2 bound at h=0.0678:", repr(math.log(1.0678 / 0.9322)))
print("R2 check bound at exact unrounded L:", repr(math.log((1 + h) / (1 - h))))
print("E2 simple change exp(-0.0965747)-1:", math.exp(-0.0965747) - 1)
print("M1 ln1.1:", math.log(1.1), 0.1 - math.log(1.1))
