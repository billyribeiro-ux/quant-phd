"""Independent recomputation of every number the BK4 project page prints or states (round 12).

Written from the page's rules alone, with Fraction for exact arithmetic. Run: python3 -I recompute_r12.py <checkout>
"""

import math
import random
import sys
from fractions import Fraction


def layers(loss, im, df, cap):
    a1 = min(loss, im)
    a2 = min(loss - a1, df)
    a3 = min(loss - a1 - a2, cap)
    return a1, a2, a3, loss - a1 - a2 - a3


def survivors(residual, funds):
    pool = sum(funds.values())
    if residual >= pool:
        return dict(funds), residual - pool
    floors = {m: math.floor(Fraction(residual * f, pool)) for m, f in funds.items()}
    left = residual - sum(floors.values())
    for m in sorted(funds):
        if left and funds[m] > 0:
            floors[m] += 1
            left -= 1
    assert left == 0
    return floors, 0


def ceil_index(target, count):
    return math.ceil(Fraction(target * count, 10000))


def out(tag, value):
    print(f"{tag}: {value}")


# Page's reference instance: four members, defaulter 2
IM = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
DF = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
K = 20_000
d = 2
surv_df = {m: DF[m] for m in DF if m != d}
out("pool", sum(surv_df.values()))

a1, a2, a3, R = layers(80_000, IM[d], DF[d], K)
out("lab1 layers (margin, fund, capital, residual)", (a1, a2, a3, R))
out("lab1 survivors (sv, uncovered)", survivors(R, surv_df))
out("exemplar B sum 1334+1666+1000", 1334 + 1666 + 1000)

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
out("scenario largest loss", max(losses))
for target in (9_000, 9_500, 9_550, 9_750):
    k = ceil_index(target, 40)
    m = sorted(losses)[k - 1]
    cov = math.floor(Fraction(10000 * sum(1 for x in losses if x <= m), 40))
    cov_below = math.floor(Fraction(10000 * sum(1 for x in losses if x <= m - 1), 40))
    print(f"target {target}: exact {Fraction(target * 40, 10000)} k {k} margin {m} cover {cov} cover_minus_1c {cov_below}")

for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    a1, a2, a3, R = layers(loss, IM[d], DF[d], K)
    sv, unc = survivors(R, surv_df)
    out(f"partA loss {loss}", (a1, a2, a3, sv, unc, a1 + a2 + a3 + sum(sv.values()) + unc == loss))

for target in (9_500, 9_000):
    m = sorted(losses)[ceil_index(target, 40) - 1]
    past_m = sum(1 for x in losses if x > m)
    past_f = sum(1 for x in losses if x > m + DF[d])
    past_c = sum(1 for x in losses if x > m + DF[d] + K)
    past_s = sum(1 for x in losses if x > m + DF[d] + K + sum(surv_df.values()))
    out(f"partC target {target}", (m, past_m, past_f, past_c, past_s))
out("exemplar B difference 111074-105154", 111_074 - 105_154)

fix_surv = {1: 40, 2: 60}
fixture_rows = [(80, (80, 0, 0), (0, 0), 0), (100, (100, 0, 0), (0, 0), 0), (120, (100, 20, 0), (0, 0), 0),
                (150, (100, 50, 0), (0, 0), 0), (151, (100, 50, 1), (0, 0), 0), (170, (100, 50, 20), (0, 0), 0),
                (180, (100, 50, 30), (0, 0), 0), (181, (100, 50, 30), (1, 0), 0), (200, (100, 50, 30), (8, 12), 0),
                (205, (100, 50, 30), (10, 15), 0), (300, (100, 50, 30), (40, 60), 20)]
for loss, layer_want, surv_want, unc_want in fixture_rows:
    a1, a2, a3, R = layers(loss, 100, 50, 30)
    sv, unc = survivors(R, fix_surv)
    ok = (a1, a2, a3) == layer_want and (sv[1], sv[2]) == surv_want and unc == unc_want
    out(f"fixture loss {loss}", "OK" if ok else f"MISMATCH {(a1, a2, a3, sv, unc)}")

for loss, want in [(1, {1: 1, 2: 0, 3: 0}), (2, {1: 1, 2: 1, 3: 0}), (3, {1: 1, 2: 1, 3: 1}), (4, {1: 1, 2: 1, 3: 1})]:
    sv, unc = survivors(loss, {1: 1, 2: 1, 3: 1})
    out(f"remainder loss {loss}", ("OK" if sv == want and unc == (1 if loss == 4 else 0) else "MISMATCH", sv, unc))

base = [10, 20, 30, 40, 50]
out("sizing 8000 on 10..50", sorted(base)[ceil_index(8000, 5) - 1])
out("sizing 8001 on 10..50", sorted(base)[ceil_index(8001, 5) - 1])
out("sizing 10000 on 10..50", sorted(base)[ceil_index(10000, 5) - 1])
out("sizing 5000 on 10..40", sorted([10, 20, 30, 40])[ceil_index(5000, 4) - 1])
out("cover [1,5,9] at 4", math.floor(Fraction(10000 * 1, 3)))
out("cover [1,2,9] at 2", math.floor(Fraction(10000 * 2, 3)))
out("20000/3 to two places", round(20000 / 3, 2))

fund1, fund2 = 6_692_931_089_932_558, 585_467_024_498_971
loss_big = 6_585_696_953_829_388
pool_big = fund1 + fund2
s1, s2 = loss_big * fund1 // pool_big, loss_big * fund2 // pool_big
out("big fixture shares, leftover", (s1, s2, loss_big - s1 - s2))
out("big fixture shares match test", (s1, s2) == (6_055_950_114_045_320, 529_746_839_784_068))
out("big fixture product exceeds 2**53", loss_big * fund1 > 2**53)
