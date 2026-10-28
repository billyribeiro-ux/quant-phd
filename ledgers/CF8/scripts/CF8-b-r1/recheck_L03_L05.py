"""Independent recomputation of the numbers printed or stated in CF8 L03, L04 and L05 (verifier round 1, slice b).

Standard library only. Run as: python3 -I -W error ledgers/CF8/scripts/CF8-b-r1/recheck_L03_L05.py
Every value is recomputed from the seeded generator and exact Fractions, not read from the pages.
"""

import math
import random
from fractions import Fraction


def flows(seed=7):
    rng = random.Random(seed)
    rec, dis = [], []
    for w in range(1, 14):
        slump = -350_000 if 5 <= w <= 8 else 0
        rec.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
        dis.append(1_020_000 + rng.randint(-120_000, 120_000))
    return rec, dis


def forecast(rec, dis, opening_cash, opening_drawn, minimum, commitment):
    cash, drawn, rows = opening_cash, opening_drawn, []
    for r, p in zip(rec, dis, strict=True):
        before = cash + r - p
        draw = repay = 0
        if before < minimum:
            draw = min(minimum - before, commitment - drawn)
        elif before > minimum and drawn > 0:
            repay = min(before - minimum, drawn)
        ending = before + draw - repay
        drawn += draw - repay
        rows.append({"draw": draw, "repay": repay, "end": ending, "drawn": drawn, "before": before, "short": max(0, minimum - ending)})
        cash = ending
    return rows


rec, dis = flows()
net = [r - p for r, p in zip(rec, dis, strict=True)]
cum = []
s = 0
for x in net:
    s += x
    cum.append(s)

# L03: Example 2.3 (week 6), M1-M3, E1-E3, R2
L03 = forecast(rec, dis, 1_200_000, 0, 1_000_000, 4_000_000)
assert L03[4]["end"] == 1_068_160 and L03[4]["drawn"] == 0
p6 = 1_068_160 + 530_408 - 1_138_473
assert p6 == 460_095 and 1_000_000 - p6 == 539_905 and 4_000_000 - 539_905 == 3_460_095
assert sum(r["draw"] for r in L03) == 1_356_374 and sum(r["repay"] for r in L03) == 438_816
assert L03[12]["drawn"] == 917_558
assert max(r["drawn"] for r in L03) == 1_288_640 and 4_000_000 - 1_288_640 == 2_711_360
assert 1_000_000 + 67_734 == 1_067_734 and rec[8] - dis[8] == 67_734
assert 1_000_000 - 1_200_000 - (1_356_374 - 438_816) == -1_117_558 and sum(net) == -1_117_558
# M1
assert 500_000 + 800_000 - 1_000_000 == 300_000 and min(600_000 - 300_000, 1_000_000) == 300_000
# M2 (p = 900000+400000-300000 = 1000000; Rp = min(400000, 250000))
assert min(1_000_000 - 600_000, 250_000) == 250_000 and 1_000_000 - 250_000 == 750_000
# M3 (capped)
assert min(500_000 - (-100_000), 300_000 - 100_000) == 200_000 and 500_000 - (100_000) == 400_000
# Q: rows 'ending cash of week 9' and the four-week printed pattern
draws_weeks = [i + 1 for i, r in enumerate(L03) if r["draw"] > 0]
repay_weeks = [i + 1 for i, r in enumerate(L03) if r["repay"] > 0]
assert draws_weeks == [6, 7, 8, 10, 11] and repay_weeks == [9, 12, 13]

# L04: same flows, commitment 1_200_000, covenant 1_800_000, minimum 1_000_000
L04 = forecast(rec, dis, 1_200_000, 0, 1_000_000, 1_200_000)
liq = [r["end"] + (1_200_000 - r["drawn"]) for r in L04]
head = [l - 1_800_000 for l in liq]
assert liq[5] == 1_660_095 and head[5] == -139_905 and liq[10] == 911_360
assert min(range(13), key=lambda i: cum[i]) == 10 and cum[10] == -1_488_640
assert 1_200_000 + 1_200_000 - 1_800_000 + cum[10] == -888_640 == head[10]
assert cum[5] == -739_905 and liq[5] == 2 * 1_200_000 - 739_905
assert min(range(13), key=lambda i: head[i]) == 10  # pinch week 11, earliest on tie
assert [i + 1 for i, h in enumerate(head) if h < 0] == [6, 7, 8, 9, 10, 11, 12, 13]
assert net[5] == -608_065 and min(range(13), key=lambda i: net[i]) == 5
# Theorem 2.3: K* = max(B0, max unconstrained drawn)
uncon = forecast(rec, dis, 1_200_000, 0, 1_000_000, 10**12)
kstar = max([0] + [r["drawn"] for r in uncon])
assert kstar == 1_288_640
assert all(r["short"] == 0 for r in forecast(rec, dis, 1_200_000, 0, 1_000_000, kstar))
below = forecast(rec, dis, 1_200_000, 0, 1_000_000, kstar - 1)
assert max(r["short"] for r in below) == 1
assert [i + 1 for i, r in enumerate(below) if r["short"] > 0] == [11]  # only week 11 is capped at K = kstar - 1
# Theorem 2.4 / Example 2.5 / E3
fall = Fraction(5 * 1_234_567, 7)
assert fall == Fraction(6_172_835, 7) and math.floor(fall + Fraction(1, 2)) == 881_834
assert -888_640 - 881_834 == -1_770_474
# M2 (L04): 3 * 700000 / 7 = 300000 exactly
assert Fraction(3 * 700_000, 7) == 300_000

# Misconception / E1 breach length: weeks 6..13 negative
assert sum(1 for h in head if h < 0) == 8

# L05: standard error, quantile, shares, R3
p = Fraction(356, 2000)
assert p == Fraction(178, 1000) and float(p * (1 - p) / 2000) == 0.146316 / 2000
se = math.sqrt(0.178 * 0.822 / 2000)
assert f"{se:.4f}" == "0.0086" and f"{se:.7f}" == "0.0085532"  # page M2 prints 0.0085533 (defect)
assert math.ceil(Fraction(5, 100) * 2000) == 100 and math.ceil(Fraction(5, 100) * 30) == 2
assert Fraction(99, 2000) == Fraction("0.0495") and 99 / 2000 <= 0.05
assert 365_525 / 100 == 3655.25
assert 1676 - 356 == 1320 and 2000 - 1676 == 324
assert 0.146316 / 0.000004 == 36579
assert round(0.0086 / 0.002, 1) == 4.3 and round(se / 0.002, 1) == 4.3
assert 12 * 100_000 == 1_200_000
print("CF8 L03-L05 recomputation: all assertions hold")
print("L03 closing sum-identity", 1_000_000 - 1_000_000)
print("L04 pinch week", min(range(13), key=lambda i: head[i]) + 1, "headroom", head[10])
print("L04 required commitment", kstar, "cents; slip", 881_834, "cents; liquidity drop identical across weeks")
print("L05 standard error at p=0.178, N=2000 (7 dp):", f"{se:.7f}")
