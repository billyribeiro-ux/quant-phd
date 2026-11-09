"""LX1-b round 15 independent re-derivation of every L03 and L04 number on the pin (no import of the twins).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r15/rederive_r15.py <checkout>
"""

import csv
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])


def half_up(x, places):
    return str(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)) if not isinstance(x, F) else str((x * 10**places + F(1, 2)).__floor__() / 10**places)


def rnd(x: F, places: int) -> str:
    scaled = x * 10**places
    n = math.floor(scaled + F(1, 2))
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}"


print("== L03 exact model values (Fraction)")
D = F(1_000_000)
A0 = F(4_000_000)
delta = F(1, 50)
C = A0 + D


def P(m, t):
    return (1 - delta) ** min(t, m)


def V(m, t):
    return D / P(m, t)


def lam(x):
    return x / (C - x)


def depth_path(m):
    L0 = D / A0
    out = []
    for t in range(13):
        v = V(m, t)
        a = A0 - (v - D)
        assert a > 0
        L = v / a
        out.append(1 * 1 * (L - L0))
    return out


def depth(m):
    return max(depth_path(m))


dX, dY = depth(12), depth(4)
print("depth X exact", float(dX), "->", rnd(100 * dX, 2))
print("depth Y exact", float(dY), "->", rnd(100 * dY, 2))
print("difference unrounded (pp)", float(100 * (dX - dY)), "->", rnd(100 * (dX - dY), 2))
print("printed difference of rounded depths", F(922, 100) - F(269, 100))
print("V_12 exact", float(V(12, 12)), "cents, rounds to", rnd(V(12, 12), 0))
print("V_4 exact", float(V(4, 4)), "rounds to", rnd(V(4, 4), 0))
print("P_4 exact", P(4, 4), float(P(4, 4)))
A4 = A0 - (V(4, 4) - D)
print("A_4 exact", float(A4), "rounds", rnd(A4, 0), "; rounded-first:", 4000000 - (1084166 - 1000000))
L4 = V(4, 4) / A4
print("L_4 exact", float(L4), "->", rnd(L4, 4))
print("L_4 rounded-first", 1084166 / 3915834)
print("V_12 vs C", float(V(12, 12)), float(C), V(12, 12) < C)
print("Part D ratios (phi*beta products)")
for phi, beta in ((F(1, 2), F(1)), (F(1), F(1)), (F(3), F(1))):
    dx = max(beta * phi * (lam(V(12, t)) - lam(D)) for t in range(13))
    dy = max(beta * phi * (lam(V(4, t)) - lam(D)) for t in range(13))
    print("  ratio exact", float(dx / dy), "->", rnd(dx / dy, 4))
# closed form check Prop 3.2(b)
for m in (4, 12):
    cf = lam(V(m, m)) - lam(D)
    print("closed form bracket m", m, float(cf), "depth", float(depth(m)), "equal", cf == depth(m))
print("Cor 3.4 ratio closed form", float((lam(V(12, 12)) - lam(D)) / (lam(V(4, 4)) - lam(D))))
# Part C monotonicity
ds = [depth(m) for m in range(13)]
print("Part C never falls", all(ds[i] <= ds[i + 1] for i in range(12)), "strict", all(ds[i] < ds[i + 1] for i in range(12)))
print("Part A X path rounded", [rnd(100 * x, 2) for x in depth_path(12)])
# Y index unchanged periods
idx_y = [P(4, t) for t in range(13)]
print("Y unchanged periods t=1..12:", sum(1 for t in range(1, 13) if idx_y[t] == idx_y[t - 1]))
# premium-square variant (lesson claim: ratio is square of Cor 3.4 ratio)
r = (lam(V(12, 12)) - lam(D)) / (lam(V(4, 4)) - lam(D))
print("square variant ratio", float(r * r), "vs linear", float(r))

print("== L04 exact checks")
M1_ratio = F(1375, 1000) / F(1250, 1000)
print("M1 ratio", M1_ratio, "ln", math.log(float(M1_ratio)), "diff", 0.1 - math.log(1.1))
print("M2 mean", F(2, 100) / 3, "dispersion", math.sqrt(float(F(19, 30000))))
print("M2 sum sq dev", F(14, 10000) - 3 * (F(1, 150)) ** 2, "=19/15000?", F(14, 10000) - 3 * (F(1, 150)) ** 2 == F(19, 15000))
print("M3 months", 26 * 12 + 9)
z = 0.135846
print("R2 tanh(z/2)", math.tanh(z / 2), "exact z from data below")
print("ln(1.0678/0.9322)", math.log(1.0678 / 0.9322))

rows = []
with (root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    print("header", rd.fieldnames)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
blank = [m for m, g in rows if not g.strip()]
print("GBP blanks", len(blank))
rates = [(m, F(g)) for m, g in rows]
# contiguity
def mi(s):
    y, mo = s.split("-")
    return int(y) * 12 + int(mo) - 1
assert all(mi(rates[i][0]) == mi(rates[i - 1][0]) + 1 for i in range(1, len(rates)))
changes = [(rates[i][0], math.log(float(rates[i][1] / rates[i - 1][1]))) for i in range(1, len(rates))]
print("changes", len(changes), changes[0][0], changes[-1][0])
zeros = [rates[i][0] for i in range(1, len(rates)) if rates[i][1] == rates[i - 1][1]]
print("exact zeros", len(zeros), zeros, "nonzero", len(changes) - len(zeros))


def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))


w1 = [c for _, c in changes]
w2_items = [(m, c) for m, c in changes if m >= "2000-01"]
w2 = [c for _, c in w2_items]
print("window2 changes", len(w2), w2_items[0][0], w2_items[-1][0])
s1, s2 = sd(w1), sd(w2)
print("sd1", s1, "->", round(s1, 6), "sd2", s2, "->", round(s2, 6))
print("diff exact", s2 - s1, "ratio", s2 / s1, "->", s2 / s1)
print("diff of printed", round(s2, 6) - round(s1, 6))
mx1 = max(changes, key=lambda it: abs(it[1]))
mx2 = max(w2_items, key=lambda it: abs(it[1]))
print("max1", mx1, "max2", mx2)
print("identity w1", abs(math.fsum(w1) - math.log(float(rates[-1][1] / rates[0][1]))))
rate_1999_12 = dict(rates)["1999-12"]
print("identity w2", abs(math.fsum(w2) - math.log(float(rates[-1][1] / rate_1999_12))))
print("E2 simple change of 2008-10", math.exp(mx2[1]) - 1, "ln->", mx2[1])
print("R2 h exact via z=max1", math.tanh(mx1[1] / 2), "half-width 0.0678 bound", math.log(1.0678 / 0.9322))
print("R2 exact h rounded 4dp", round(math.tanh(mx1[1] / 2), 4))
print("Part A model sd: 11 zero changes")
