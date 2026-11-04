"""Independent re-derivation of the BK4 project page numbers, written from the page's rules and not from the lab code.

Usage: python -I rederive_r5.py   (standard library only; prints every value the page quotes that it checks)
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

# Lab 1 / Lab 2 / Lab 3 instance: four members, defaulter 2, CCP capital 20000 cents.
IM = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
DF = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
K = 20_000
D = 2

# Scenario set: 40 losses from random.Random(1), each randint(0, 120000) (Lab 1 and Lab 3 generator).
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
print("S", S, "largest loss", max(losses))

# Lab 1 waterfall for loss 80000 (rules of the page, exact integers).
L = 80_000
a1 = min(L, IM[D])
a2 = min(L - a1, DF[D])
a3 = min(L - a1 - a2, K)
R = L - a1 - a2 - a3
surv = sorted(m for m in DF if m != D)
pool = sum(DF[m] for m in surv)
exact = {m: Fraction(R * DF[m], pool) for m in surv}
floors = {m: math.floor(exact[m]) for m in surv}
print("layers", a1, a2, a3, "residual", R, "pool", pool)
print("exact shares", {m: str(exact[m]) for m in surv}, "floors", floors, "sum floors", sum(floors.values()))
left = R - sum(floors.values())
pay = dict(floors)
for m in surv:
    if left > 0 and DF[m] > 0:
        pay[m] += 1
        left -= 1
print("payments", pay, "sum", sum(pay.values()), "== residual", sum(pay.values()) == R)

# Sizing: k = ceil(target * S / 10000) exactly.
for target in (9_550, 9_000, 9_500, 9_750):
    exact_pos = Fraction(target * S, 10_000)
    k = math.ceil(exact_pos)
    margin = sorted(losses)[k - 1]
    cover_at = Fraction(10_000 * sum(1 for x in losses if x <= margin), S)
    below = Fraction(10_000 * sum(1 for x in losses if x <= margin - 1), S)
    print(f"target {target}: exact position {exact_pos} k {k} margin {margin} cover_at {cover_at} cover_below_floor {math.floor(below)}")

# Brute force: least whole-cent margin with floor cover >= target.
def brute(target: int) -> int:
    for m in range(0, max(losses) + 1):
        if math.floor(Fraction(10_000 * sum(1 for x in losses if x <= m), S)) >= target:
            return m
    raise AssertionError

for target in (9_000, 9_500, 9_750):
    print("brute", target, brute(target))

# Lab 3 Part C counts for the margins of targets 9500 and 9000.
surv_fund = sum(DF[m] for m in DF if m != D)
for target in (9_500, 9_000):
    k = math.ceil(Fraction(target * S, 10_000))
    margin = sorted(losses)[k - 1]
    past_margin = sum(1 for x in losses if x > margin)
    past_fund = sum(1 for x in losses if x > margin + DF[D])
    past_cap = sum(1 for x in losses if x > margin + DF[D] + K)
    past_surv = sum(1 for x in losses if x > margin + DF[D] + K + surv_fund)
    print("partC", target, margin, past_margin, past_fund, past_cap, past_surv)
print("difference 111074 - 105154 =", 111074 - 105154)

# Lab 3 Part A waterfall rows for the defaulter margin 50000.
def wf(loss: int) -> tuple[int, int, int, dict[int, int], int]:
    m1 = min(loss, IM[D])
    f1 = min(loss - m1, DF[D])
    c1 = min(loss - m1 - f1, K)
    r = loss - m1 - f1 - c1
    if r >= pool:
        return m1, f1, c1, {m: DF[m] for m in surv}, r - pool
    sh = {m: r * DF[m] // pool for m in surv}
    lo = r - sum(sh.values())
    for m in surv:
        if lo > 0 and DF[m] > 0:
            sh[m] += 1
            lo -= 1
    return m1, f1, c1, sh, 0

for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    print("partA", loss, wf(loss))

# Page fixtures (hand computed on the page): layer-order table with defaulter margin 100, fund 50, capital 30, survivors 40 and 60.
def fx(loss: int) -> tuple[int, int, int, tuple[int, int], int]:
    im, df, cap = 100, 50, 30
    m1 = min(loss, im)
    f1 = min(loss - m1, df)
    c1 = min(loss - m1 - f1, cap)
    r = loss - m1 - f1 - c1
    funds = {1: 40, 2: 60}
    p = 100
    if r >= p:
        return m1, f1, c1, (40, 60), r - p
    sh = {m: r * funds[m] // p for m in funds}
    lo = r - sum(sh.values())
    for m in (1, 2):
        if lo > 0 and funds[m] > 0:
            sh[m] += 1
            lo -= 1
    return m1, f1, c1, (sh[1], sh[2]), 0

for loss in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    print("fixture", loss, fx(loss))

# Large-cent test values from test_project.py (oracle, exact).
fund1, fund2, loss_big = 6_692_931_089_932_558, 585_467_024_498_971, 6_585_696_953_829_388
pool_big = fund1 + fund2
print("big pool", pool_big, "residual<pool", loss_big < pool_big)
s1 = loss_big * fund1 // pool_big
s2 = loss_big * fund2 // pool_big
print("big shares", s1, s2, "leftover", loss_big - s1 - s2, "expected s1 6055950114045320 s2 529746839784068 ->", s1 == 6_055_950_114_045_320, s2 == 529_746_839_784_068)
print("loss exceeds 2**53:", loss_big * fund1 > 2**53)
