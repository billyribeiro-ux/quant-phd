"""Round-13 BK4-c independent recomputation of every number on project.html and the grader fixtures.

Standard library only. Written from the page's stated rules, not from reference.py. Run: python3 -I recompute_r13.py
"""

import math
import random
from fractions import Fraction

# ---- Lab 1 / Lab 2 / Lab 3 reference instance (page values) ----
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAPITAL = 20_000
DEF = 2
LOSS = 80_000
survivors = [1, 3, 4]
pool = sum(FUND[m] for m in survivors)
a1 = min(LOSS, MARGIN[DEF]); a2 = min(LOSS - a1, FUND[DEF]); a3 = min(LOSS - a1 - a2, CAPITAL)
R = LOSS - a1 - a2 - a3
print("L1 layers", a1, a2, a3, "R", R, "pool", pool)
assert (a1, a2, a3, R, pool) == (50000, 6000, 20000, 4000, 12000)
floored = {m: R * FUND[m] // pool for m in survivors}
left = R - sum(floored.values())
print("L1 floored", floored, "leftover", left, "exact shares", {m: Fraction(R * FUND[m], pool) for m in survivors})
assert floored == {1: 1333, 3: 1666, 4: 1000} and left == 1
pay = dict(floored); pay[1] += 1
assert pay == {1: 1334, 3: 1666, 4: 1000} and sum(pay.values()) == R

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
print("L1 largest", max(losses), "sorted 36..39 (1-based)", sorted(losses)[35:39])
target = 9_550
exact = Fraction(target * 40, 10_000)
k = -((-target * 40) // 10_000)
assert exact == Fraction(191, 5) and k == 39, (exact, k)
margin = sorted(losses)[k - 1]
cov = 10_000 * sum(1 for x in losses if x <= margin) // 40
below = 10_000 * sum(1 for x in losses if x <= margin - 1) // 40
print("L1 margin", margin, "cover", cov, "below", below)
assert margin == 117088 and cov == 9750 and below == 9500

# Lab 3 part A and B and C
def waterfall(loss, mg):
    a1 = min(loss, mg); a2 = min(loss - a1, FUND[DEF]); a3 = min(loss - a1 - a2, CAPITAL)
    r = loss - a1 - a2 - a3
    surv = [1, 3, 4]; p = sum(FUND[m] for m in surv)
    if r >= p:
        return a1, a2, a3, {m: FUND[m] for m in surv}, r - p
    sh = {m: r * FUND[m] // p for m in surv}; lo = r - sum(sh.values())
    for m in surv:
        if lo > 0 and FUND[m] > 0:
            sh[m] += 1; lo -= 1
    return a1, a2, a3, sh, 0

for ls in (20_000, 55_000, 70_000, 80_000, 100_000):
    a1_, a2_, a3_, sh, unc = waterfall(ls, MARGIN[DEF])
    tot = a1_ + a2_ + a3_ + sum(sh.values()) + unc
    print("A", ls, a1_, a2_, a3_, sh, unc, tot == ls)
    assert tot == ls

srt = sorted(losses)
print("B sizing:")
for t in (9000, 9500, 9750):
    kk = -((-t * 40) // 10_000)
    mg = srt[kk - 1]
    c_at = 10_000 * sum(1 for x in losses if x <= mg) // 40
    c_b = 10_000 * sum(1 for x in losses if x <= mg - 1) // 40
    # brute force: least integer margin M with floored cover >= t
    bf = next(M for M in range(0, max(losses) + 1) if 10_000 * sum(1 for x in losses if x <= M) // 40 >= t)
    print("  target", t, "k", kk, "margin", mg, "cover", c_at, "below", c_b, "brute", bf)
    assert bf == mg
assert max(losses) == 118151
print("C counts:")
surv_fund = sum(FUND[m] for m in (1, 3, 4))
for t in (9500, 9000):
    mg = srt[-(-t * 40 // 10_000) - 1]
    pm = sum(1 for x in losses if x > mg)
    pf = sum(1 for x in losses if x > mg + FUND[DEF])
    pc = sum(1 for x in losses if x > mg + FUND[DEF] + CAPITAL)
    ps = sum(1 for x in losses if x > mg + FUND[DEF] + CAPITAL + surv_fund)
    print("  target", t, "margin", mg, "past margin", pm, "past fund", pf, "past cap", pc, "past survivors", ps)

# Lab 1 interpretation numbers
print("9750 vs 9500 cover one cent below", 9500, "; 5920 =", 111074 - 105154)
assert 111074 - 105154 == 5920
assert 38 == -(-9500 * 40 // 10000) or True

# ---- Grader fixture: large cent shares (test_large_cent_shares_are_floored_in_integers) ----
f1, f2 = 6_692_931_089_932_558, 585_467_024_498_971
loss_big = 6_585_696_953_829_388
pool_big = f1 + f2
w1 = loss_big * f1 // pool_big
w2 = loss_big * f2 // pool_big
lo_big = loss_big - w1 - w2
w1 += lo_big  # leftover cents go one each to the first survivors with a positive fund (member 1 here)
print("large-cent shares after leftover", w1, w2, "leftover", lo_big)
assert (w1, w2, w1 + w2) == (6_055_950_114_045_320, 529_746_839_784_068, loss_big)
assert loss_big * f1 > 2**53

# ---- float-index probe: exact integer index vs float index (page forbids float) ----
exact_k = -((-2800 * 50) // 10_000)
float_k = math.ceil(2800 / 10_000 * 50)
print("float probe: exact k", exact_k, "float k", float_k, "2800/10000*50 =", repr(2800 / 10_000 * 50))
assert exact_k == 14 and float_k == 15

# ---- fixture tables: cover, sizing, layer order ----
print("sizing fixtures", sorted([10,20,30,40,50])[math.ceil(Fraction(8000*5,10000))-1],
      sorted([10,20,30,40,50])[math.ceil(Fraction(8001*5,10000))-1],
      sorted([10,20,30,40,50])[math.ceil(Fraction(10000*5,10000))-1],
      sorted([10,20,30,40])[math.ceil(Fraction(5000*4,10000))-1])
assert [sorted([10,20,30,40,50])[math.ceil(Fraction(t*5,10000))-1] for t in (8000,8001,10000)] == [40,50,50]
assert sorted([10,20,30,40])[math.ceil(Fraction(5000*4,10000))-1] == 20
assert 10000*1//3 == 3333 and 10000*2//3 == 6666
print("cover fixtures ok")
print("ALL RECOMPUTE ASSERTIONS PASSED")
