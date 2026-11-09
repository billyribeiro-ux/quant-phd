"""Independent re-derivation of the LX1 slice-b numbers, with exact Fractions and 50-digit Decimals."""

from __future__ import annotations

import csv
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction as F

getcontext().prec = 50
ROOT = __import__("sys").argv[1]


def rhu(x: F) -> int:
    return math.floor(x + F(1, 2))


def dec(x: F, places: int) -> str:
    return str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


print("== L01")
d1, r, g = F(400), F(9, 100), F(3, 100)
F0 = d1 / (r - g)
print("F0 exact", F0, float(F0), "rounded", rhu(F0))
q = (1 + g) / (1 + r)
print("q", q, dec(q, 6))
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print("N", N, "S rounded", rhu(S), "identity", S == F0 * (1 - q**N), "F0 q^N rounded", rhu(F0 * q**N))
F2 = d1 * (1 + g) ** 2 / (r - g)
F3 = d1 * (1 + g) ** 3 / (r - g)
print("F2", dec(F2, 2), rhu(F2), "F3", dec(F3, 2), rhu(F3))
print("mech1 250/0.06", dec(F(250) / F(6, 100), 2), rhu(F(250) / F(6, 100)))
print("mech2 F3", dec(F(250) * F(104, 100) ** 3 / F(6, 100), 2), rhu(F(250) * F(104, 100) ** 3 / F(6, 100)))
S10 = sum(F(100) * (1 + F(5, 100)) ** (s - 1) / (1 + F(5, 100)) ** s for s in range(1, 11))
print("mech3 S10", S10, dec(S10, 2), "== 20000/21", S10 == F(20000, 21))
gstar = F(9, 100) - F(400, 6000)
print("research1 g*", gstar, dec(gstar, 6))
print("ratio F0 witness", F(400) / F(8, 100), F(400) / F(6, 100), "gap at 6000:", F(6000) - F(400) / F(8, 100), F(6000) - F(400) / F(6, 100))
# Lab Part B
rng_seed = 20261103
import random

rng = random.Random(rng_seed)
gaps = []
rows = []
for t in range(13):
    fund = F(400) * (1 + g) ** t / (r - g)
    w = F(rng.randint(-8, 25), 100)
    price = rhu(fund * (1 + w))
    fc = rhu(fund)
    gaps.append(price - fc)
    rows.append((t, fc, price, price - fc))
print("L01 gaps", [x[3] for x in rows])
print("positive", sum(1 for x in gaps if x > 0), "max", max(gaps), "at", gaps.index(max(gaps)))
rng = random.Random(rng_seed)
alt_pos = 0
for t in range(13):
    w = F(rng.randint(-8, 25), 100)
    fund = F(400) * (1 + g) ** t / (r - g)
    price = rhu(fund * (1 + w))
    alt = F(400) * (1 + F(1, 100)) ** t / (r - F(1, 100))
    alt_pos += (price - rhu(alt)) > 0
print("alt positive", alt_pos)
# Empirical 3: fundamental t=9 unrounded
f9 = F(400) * (1 + g) ** 9 / (r - g)
print("F9 exact", dec(f9, 4), "gap 0.25F", dec(F(1, 4) * f9, 4), "2175/8698", dec(F(2175, 8698), 6), dec(F(2175, 8698) * 100, 4))
print("F9 decimal", Decimal(f9.numerator) / Decimal(f9.denominator))
print("sqrt check 1.03^9", dec(F(103, 100) ** 9, 8))

print("== L03")
D, K0 = F(1_000_000), F(4_000_000)
delta = F(1, 50)
phi = beta = F(1)
C = K0 + D


def V(m: int, t: int) -> F:
    return D / (1 - delta) ** min(t, m)


def lam(x: F) -> F:
    return x / (C - x)


def depth_exact(m: int) -> F:
    return max(beta * phi * (lam(V(m, t)) - lam(D)) for t in range(13))


dx, dy = depth_exact(12), depth_exact(4)
print("depth X exact", dec(dx * 100, 6), "rounded 2dp", dec(dx * 100, 2))
print("depth Y exact", dec(dy * 100, 6), "rounded 2dp", dec(dy * 100, 2))
print("diff exact", dec((dx - dy) * 100, 6), "rounded 2dp", dec((dx - dy) * 100, 2))
print("diff of printed", F(920, 100) - F(269, 100))
print("ratio X/Y exact", dec(dx / dy, 6), "rounded 4dp", dec(dx / dy, 4))
print("V12 exact", dec(V(12, 12), 4), "rounded", rhu(V(12, 12)))
print("V4 exact", dec(V(4, 4), 7), "rounded", rhu(V(4, 4)))
P4 = (F(49, 50)) ** 4
print("P4", P4, dec(P4, 8), "5764801/6250000", P4 == F(5764801, 6250000))
K4 = K0 - (V(4, 4) - D)
print("K4", dec(K4, 4), rhu(K4), "L4", dec(V(4, 4) / K4, 7), dec(V(4, 4) / K4, 4))
print("ratio of depth Y for product 1/2 equal?", depth_exact(12) / depth_exact(4) == F(1,2) * 0 + dx / dy)
# depth for phi=1/2 and phi=3, check cancellation
for ph in (F(1, 2), F(3)):
    dxp = max(ph * (lam(V(12, t)) - lam(D)) for t in range(13))
    dyp = max(ph * (lam(V(4, t)) - lam(D)) for t in range(13))
    print("ratio phi", ph, dec(dxp / dyp, 6))
# E1 depth Y first reached at 4, check monotone
print("Y path", [dec(100 * (lam(V(4, t)) - lam(D)), 4) for t in range(13)])
# Part C depths
depths = [depth_exact(m) for m in range(13)]
print("Part C depths 2dp", [dec(x * 100, 2) for x in depths])
print("never falls", all(depths[m] <= depths[m + 1] for m in range(12)), "strict", all(depths[m] < depths[m + 1] for m in range(12)))

print("== L04")
rows = []
with open(f"{ROOT}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as fh:
    rd = csv.DictReader(fh)
    print("header", rd.fieldnames)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
zero = [rows[i][0] for i in range(1, len(rows)) if F(rows[i][1]) == F(rows[i - 1][1])]
print("zero months", zero)
ch_all = [(rows[i][0], math.log(float(F(rows[i][1]) / F(rows[i - 1][1])))) for i in range(1, len(rows))]
print("n changes", len(ch_all))
w2 = [c for c in ch_all if c[0] >= "2000-01"]
print("window two n", len(w2), w2[0][0])
import statistics

def sd(vals):
    m = math.fsum(vals) / len(vals)
    return math.sqrt(math.fsum((v - m) ** 2 for v in vals) / (len(vals) - 1))

s1 = sd([c for _, c in ch_all])
s2 = sd([c for _, c in w2])
print("s1", repr(s1), "s2", repr(s2), "diff", repr(s2 - s1), "ratio", repr(s2 / s1))
print("s1 6dp", dec(Decimal(s1), 6) if False else f"{s1:.6f}", "s2", f"{s2:.6f}", "diff", f"{s2 - s1:.6f}", "ratio", f"{s2 / s1:.4f}")
big1 = max(ch_all, key=lambda c: abs(c[1]))
big2 = max(w2, key=lambda c: abs(c[1]))
print("largest w1", big1, "largest w2", big2)
print("ln ratio 2008-10 simple", math.exp(big2[1]) - 1)
print("tanh check", math.tanh(big1[1] / 2), "h rounded", round(math.tanh(big1[1] / 2), 4))
print("bound at 0.0678", math.log(1.0678 / 0.9322), "bound at exact h", math.log((1 + math.tanh(big1[1] / 2)) / (1 - math.tanh(big1[1] / 2))))
print("ln 1.1", math.log(1.1), "diff", 0.1 - math.log(1.1))
print("M2 dispersion", math.sqrt((0.0001 + 0.0009 + 0.0004 - 3 * (0.02 / 3) ** 2) / 2))
print("M1 log 1.1 from 1.25->1.375", math.log(1.375 / 1.25))
