"""Independent recomputation of every number in BK4 slice b (L04, L05) with exact fractions.

Does not import the lab twins. Usage: python -I -W error recompute_r5.py
"""

import math
from fractions import Fraction as F
from itertools import product

print("== L04: reserve coverage")
# Remark 1.3 and Remark 2.8, worked values
claims = 2_000_000
print("reserves at 19/20:", F(19, 20) * claims, " at 21/20:", F(21, 20) * claims)
for rho, x in [(F(19, 20), F(1, 2)), (F(21, 20), F(1, 2)), (F(19, 20), F(1, 7))]:
    th = (rho - x) / (1 - x)
    print(f"rho={rho} x={x} theta={th} bps_floor={math.floor(10000 * th)}")
# E1 / E2 / M3 / R2 / E3 / Prop 2.4 / 2.5 / 2.6 checks on a grid of admissible shares
def cov(rho, x):
    assert 0 <= x < 1 and x <= rho
    return (rho - x) / (1 - x)

# the printed path (checked by hand in the review): shares 7/100 1/10 1/5 21/50 51/100 21/25 99/100
path = [F(7, 100), F(1, 10), F(1, 5), F(21, 50), F(51, 100), F(21, 25)]
for rho in (F(19, 20), F(21, 20)):
    rows = []
    for x in path + [F(99, 100)]:
        if x > rho:
            print(f"  rho={rho} x={x} omitted (x > rho)")
            continue
        res = rho * claims - x * claims
        cl = claims - x * claims
        assert res.denominator == 1 and cl.denominator == 1
        th = cov(rho, x)
        assert th == F(int(res), int(cl))
        rows.append((x, int(res), int(cl), th, math.floor(10000 * th)))
    for r in rows:
        print(f"  rho={rho} x={r[0]} res={r[1]} claims={r[2]} cov={r[3]} bps={r[4]} below1={r[3] < 1}")
    below = sum(1 for r in rows if r[3] < 1)
    print(f"  rho={rho}: computed {len(rows)} below1 {below} pairs {len(rows) * (len(rows) - 1) // 2}")
    ok_sign = all((r[3] < 1) == (rho < 1) for r in rows)
    ok_diff = True
    dir_ok = True
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            lhs = b[3] - a[3]
            rhs = (b[0] - a[0]) * (rho - 1) / ((1 - a[0]) * (1 - b[0]))
            ok_diff &= lhs == rhs
            dir_ok &= (lhs * (rho - 1) > 0)
    print(f"  rho={rho}: sign rule {ok_sign}, difference identity {ok_diff}, direction {dir_ok}")
# E1: lowest bps for rho=19/20 among computed shares
# E2: first share at >= 10600 bps for rho=21/20
# R2 example, E3 example
x_star = (F(19, 20) - F(9, 10)) / (1 - F(9, 10))
print("R2 x* for rho=19/20, c=9/10:", x_star, "check theta:", cov(F(19, 20), x_star))
lhs = F(44, 49) - F(15, 16)
rhs = (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100)))
print("E3 lhs", lhs, "rhs", rhs, "equal", lhs == rhs)
# Remark 4.1 / R1 threshold and haircut check
h = F(1, 20)
thr = 1 / (1 - h)
print("threshold", thr, "decimal 10dp", f"{float(thr):.10f}", "exact-to-10dp check", abs(float(thr) - 1.0526315789) < 1e-9)
for rho in (F(21, 20), thr):
    eff = rho * (1 - h)
    v = (eff - F(1, 2)) / (1 - F(1, 2))
    print("haircut rho", rho, "eff", eff, "x=1/2 cov", v, "bps", math.floor(10000 * v))
# Prop 2.7 spot check over a grid: floor(y)>=10000 iff y>=10000
import random
rng = random.Random(1)
bad = 0
for _ in range(20000):
    y = F(rng.randint(0, 2 * 10**8), 10**4)
    if (math.floor(y) >= 10000) != (y >= 10000):
        bad += 1
print("Prop 2.7 grid violations:", bad)
# Prop 2.6 sign checks on a grid
bad = 0
for rho_n in range(0, 41):
    rho = F(rho_n, 20)
    for x_n in range(0, 20):
        x = F(x_n, 20)
        if x > rho:
            continue
        th = cov(rho, x)
        d = x * (rho - 1) / (1 - x)
        if th - rho != d:
            bad += 1
        if rho <= 1 and th > rho:
            bad += 1
        if rho >= 1 and th < rho:
            bad += 1
print("Prop 2.6 grid violations:", bad)

print("\n== L05: operational risk, three trades")
PATTERNS = list(product((0, 1), repeat=3))
ell = (1, 2, 4)
kappa = 2500
p = F(1, 8)
def prob(pat, p):
    out = F(1)
    for x in pat:
        out *= p if x else 1 - p
    return out
cost = lambda pat, ells, k: sum(k * e * x for x, e in zip(pat, ells))
tot = sum(prob(pt, p) for pt in PATTERNS)
mean = sum(prob(pt, p) * cost(pt, ell, kappa) for pt in PATTERNS)
closed = p * kappa * sum(ell)
print("sum of probabilities", tot, "mean", mean, "closed", closed, "equal", mean == closed)
print("round half up:", math.floor(mean + F(1, 2)))
for pt in PATTERNS:
    print("  pattern", pt, "prob", prob(pt, p), "cost", cost(pt, ell, kappa))
no_fail = prob((0, 0, 0), p)
print("no fail A3", no_fail, "at least one", 1 - no_fail, "3p", 3 * p, "below", 1 - no_fail < 3 * p)
eq = (2, 2, 2)
mean_eq = sum(prob(pt, p) * cost(pt, eq, kappa) for pt in PATTERNS)
print("equal delays enumeration", mean_eq, "3 p kappa l", 3 * p * kappa * 2)

def mean_var(outcomes):
    m = sum(pr * c for pr, c in outcomes)
    v = sum(pr * c * c for pr, c in outcomes) - m * m
    return m, v

indep = [(prob(pt, p), cost(pt, ell, kappa)) for pt in PATTERNS]
comono = [(1 - p, 0), (p, kappa * sum(ell))]
mi, vi = mean_var(indep)
mc, vc = mean_var(comono)
print("indep mean", mi, "var", vi, "=", vi, "(57421875/4 =", F(57421875, 4), ")", vi == F(57421875, 4))
print("comono mean", mc, "var", vc, "(133984375/4 =", F(133984375, 4), ")", vc == F(133984375, 4))
print("no-cost prob indep", sum(pr for pr, c in indep if c == 0), "comono", sum(pr for pr, c in comono if c == 0))
print("E2 diff", vc - vi, "Prop 2.5 value", 2 * kappa**2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4))
print("Prop 2.5 identity", vc - vi == 2 * kappa**2 * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3)))
print("Example 2.8 mean", F(1, 8) * 2500 * 7, "rounded", math.floor(F(17500, 8) + F(1, 2)))
print("M1 mean", F(1, 4) * 1000 * (2 + 3 + 1))
print("M3 mean", 3 * F(1, 8) * 2500 * 2)
# R1: n trades, ratio of variances under A4 to A3 equals n
for n in (2, 3, 4):
    l, k, pp = 2, 1000, F(1, 3)
    v3 = n * pp * (1 - pp) * (k * l) ** 2
    v4 = (n * k * l) ** 2 * pp * (1 - pp)
    print("R1 n", n, "ratio", v4 / v3)
# R2 interval: bounds
print("R2 no-fail range [5/8, 7/8]:", F(5, 8), F(7, 8), "3p", 3 * p)
# Misconception 3 and 2: p general identity p^2(3-p)
for pp in (F(1, 10), F(1, 3), F(3, 4)):
    lhs = 3 * pp - (1 - (1 - pp) ** 3)
    print("Example 2.7 identity at p", pp, lhs == pp**2 * (3 - pp), lhs > 0)
# Prop 2.6
print("P(C=0) A3", (1 - p) ** 3, "A4", 1 - p, "strictly smaller", (1 - p) ** 3 < 1 - p)
# M1 numeric answer: single trade 1/4, 1000 c/day, 3 days
print("quiz single trade", F(1, 4) * 1000 * 3)
print("quiz 512-343", 512 - 343, "one minus", 1 - F(343, 512) == F(169, 512))
