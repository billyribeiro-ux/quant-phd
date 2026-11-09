"""Round-14 BK4-c: independent recomputation of every number the project page prints or derives (no lab code reused)."""

import random
from fractions import Fraction
from math import ceil

rng = random.Random(1)
L = [rng.randint(0, 120_000) for _ in range(40)]
S = len(L)
print("S", S, "max", max(L), "sorted[:3]", sorted(L)[:3])
for t in (9000, 9500, 9750, 9550):
    pos = Fraction(t * S, 10000)
    k = ceil(pos)
    m = sorted(L)[k - 1]
    cov = 10000 * sum(x <= m for x in L) // S
    cov_b = 10000 * sum(x <= m - 1 for x in L) // S
    past = sum(x > m for x in L)
    print(f"t={t} pos={pos} k={k} margin={m} cover={cov} cover_minus1={cov_b} past_margin={past}")
# Lab 1 layer arithmetic: IM_d 50000, DF_d 6000, K 20000, loss 80000, survivors 4000,5000,3000
loss, im, df, K = 80000, 50000, 6000, 20000
a1 = min(loss, im)
a2 = min(loss - a1, df)
a3 = min(loss - a1 - a2, K)
R = loss - a1 - a2 - a3
pool = 4000 + 5000 + 3000
sh = [R * f // pool for f in (4000, 5000, 3000)]
print("layers", a1, a2, a3, "R", R, "pool", pool, "floored", sh, "leftover", R - sum(sh))
# Lab 3 Part A rows
def row(loss, mg):
    a1 = min(loss, mg); a2 = min(loss - a1, df); a3 = min(loss - a1 - a2, K); R = loss - a1 - a2 - a3
    if R >= pool:
        return a1, a2, a3, (4000, 5000, 3000), R - pool
    s = [R * f // pool for f in (4000, 5000, 3000)]
    left = R - sum(s)
    for i, f in enumerate((4000, 5000, 3000)):
        if left > 0 and f > 0:
            s[i] += 1; left -= 1
    return a1, a2, a3, tuple(s), 0
for loss in (20000, 55000, 70000, 80000, 100000):
    print("A", loss, row(loss, 50000))
# Part C: margin as defaulter IM; thresholds
for t in (9500, 9000):
    k = ceil(Fraction(t * S, 10000)); m = sorted(L)[k - 1]
    print("C", t, m, sum(x > m for x in L), sum(x > m + df for x in L), sum(x > m + df + K for x in L), sum(x > m + df + K + pool for x in L))
# Exemplar B arithmetic
print("diff", 111074 - 105154, "bps", 9500 - 9000)
# Layer fixture (page table) for defaulter margin 100, fund 50, K 30, survivors 40,60
for l in (80,100,120,150,151,170,180,181,200,205,300):
    a1 = min(l, 100); a2 = min(l - a1, 50); a3 = min(l - a1 - a2, 30); R = l - a1 - a2 - a3
    if R >= 100:
        s = (40, 60); u = R - 100
    else:
        s = [R * 40 // 100, R * 60 // 100]; left = R - sum(s)
        if left > 0: s[0] += 1; left -= 1
        s = tuple(s); u = 0
    print("F", l, a1, a2, a3, s, u)
# Large-cent test values
R = 6_585_696_953_829_388; f1 = 6_692_931_089_932_558; f2 = 585_467_024_498_971
D = f1 + f2
print("large", R * f1 // D, R * f2 // D, R * f1 // D + R * f2 // D, (R * f1 // D + R * f2 // D) == R, R < D, R * f1 > 2**53)
print("expected", 6_055_950_114_045_320, 529_746_839_784_068)
# 50 scenarios, 2800 bps
print("pos50", ceil(Fraction(2800 * 50, 10000)))
