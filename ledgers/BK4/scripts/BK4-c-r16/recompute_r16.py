"""Round-16 independent recomputation of every number on the BK4 project page (slice c). Written from the page's rules.

Run: python -I recompute_r16.py (from any directory; standard library only; writes nothing).
"""

import math
import random
from fractions import Fraction

# Reference instance of Labs 1-3 (page :54)
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAP = 20_000
D = 2


def layers(loss):
    a1 = min(loss, MARGIN[D])
    a2 = min(loss - a1, FUND[D])
    a3 = min(loss - a1 - a2, CAP)
    return a1, a2, a3, loss - a1 - a2 - a3


def survivors(residual):
    ids = sorted(m for m in FUND if m != D)
    pool = sum(FUND[m] for m in ids)
    if residual >= pool:
        return {m: FUND[m] for m in ids}, residual - pool
    sh = {m: residual * FUND[m] // pool for m in ids}
    left = residual - sum(sh.values())
    for m in ids:
        if left > 0 and FUND[m] > 0:
            sh[m] += 1
            left -= 1
    return sh, 0


print("Lab 1 layers at 80000:", layers(80_000))
print("pool survivors", sum(FUND[m] for m in (1, 3, 4)))
print("floored shares at residual 4000:", {m: 4000 * FUND[m] // 12000 for m in (1, 3, 4)}, "sum", sum(4000 * FUND[m] // 12000 for m in (1, 3, 4)))
print("Lab1 survivors:", survivors(4000))
print("Lab1 conservation:", sum(layers(80_000)[:3]) + sum(survivors(4000)[0].values()) + survivors(4000)[1] == 80_000)
print("Lab 2 completed shares 1334/1666/1000:", survivors(4000)[0] == {1: 1334, 3: 1666, 4: 1000})

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
print("S", S, "max loss", max(losses))
print("exact position 9550:", Fraction(9550 * S, 10_000), "9500:", Fraction(9500 * S, 10_000), "9000:", Fraction(9000 * S, 10_000), "9750:", Fraction(9750 * S, 10_000))


def k_of(t):
    return math.ceil(Fraction(t * S, 10_000))


def margin_of(t):
    return sorted(losses)[k_of(t) - 1]


def cover(m):
    return 10_000 * sum(1 for x in losses if x <= m) // S


def brute(t):
    for m in range(0, 200_000):
        if cover(m) >= t:
            return m
    raise AssertionError


for t in (9_000, 9_500, 9_550, 9_750):
    m = margin_of(t)
    print(f"target {t}: k {k_of(t)} margin {m} cover {cover(m)} cover-1 {cover(m - 1)} brute {brute(t)} agrees {brute(t) == m}")

for t in (9_500, 9_000):
    m = margin_of(t)
    past_m = sum(1 for x in losses if x > m)
    past_f = sum(1 for x in losses if x > m + FUND[D])
    past_c = sum(1 for x in losses if x > m + FUND[D] + CAP)
    past_s = sum(1 for x in losses if x > m + FUND[D] + CAP + 12_000)
    print(f"Part C target {t} margin {m}: past margin {past_m} past fund {past_f} past capital {past_c} past survivors {past_s}")

print("difference 111074-105154 =", 111074 - 105154)
print("1e-6*(1+117088) =", 1e-6 * (1 + 117088), "< 1 cent:", 1e-6 * (1 + 117088) < 1)
print("38/40 =", Fraction(38, 40), "as percent", float(Fraction(38, 40)) * 100)
print("15/50 hours =", Fraction(15, 50))
print("Lab1 Part A rows:")
for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    a1, a2, a3, r = layers(loss)
    sh, unc = survivors(r)
    print(f"  loss {loss}: layers {(a1, a2, a3)} survivors {sh} uncovered {unc} conservation {a1 + a2 + a3 + sum(sh.values()) + unc == loss}")

# Hand fixtures from the page (:230-251), recomputed with the page's rules
FIXM = {1: 500, 2: 500, 3: 100}
FIXF = {1: 40, 2: 60, 3: 50}
FIXC = 30
for loss in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    a1 = min(loss, FIXM[3]); a2 = min(loss - a1, FIXF[3]); a3 = min(loss - a1 - a2, FIXC); r = loss - a1 - a2 - a3
    pool = 100
    if r >= pool:
        sh, unc = {1: 40, 2: 60}, r - pool
    else:
        sh = {1: r * 40 // pool, 2: r * 60 // pool}
        left = r - sum(sh.values())
        for m in (1, 2):
            if left > 0 and FIXF[m] > 0:
                sh[m] += 1; left -= 1
        unc = 0
    print(f"fixture {loss}: {(a1, a2, a3)} {sh} {unc}")
print("remainder fixture 1,2,4:", [1, 2, 4])
print("sizing fixtures:", [sorted([10,20,30,40,50])[math.ceil(Fraction(8000*5,10000))-1], sorted([10,20,30,40,50])[math.ceil(Fraction(8001*5,10000))-1], sorted([10,20,30,40,50])[math.ceil(Fraction(10000*5,10000))-1], sorted([10,20,30,40])[math.ceil(Fraction(5000*4,10000))-1]])
print("cover fixtures:", 10_000 * 1 // 3, 10_000 * 2 // 3, "floor 20000/3", 20_000 // 3)

# Large-cent test (test_project.py :450-459)
f1, f2 = 6_692_931_089_932_558, 585_467_024_498_971
loss = 6_585_696_953_829_388
pool = f1 + f2
print("large-cent: residual<pool", loss < pool, "shares", loss * f1 // pool, loss * f2 // pool, "leftover", loss - loss * f1 // pool - loss * f2 // pool)
print("large-cent expected in test: 6055950114045320, 529746839784068; products exceed 2**53:", loss * f1 > 2**53)

# Seeded cases: validity over seeds 0-49 and the test's sizing-answer diversity (independent of the grader)
import sys
sys.path.insert(0, "course/modules/BK/BK4/grader")
