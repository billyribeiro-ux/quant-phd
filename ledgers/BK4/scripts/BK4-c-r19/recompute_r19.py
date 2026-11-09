"""Round 19 (BK4 slice c): independent recomputation of every number the project page and its tests state.

Standard library only; written from the page's rules, not from reference.py. Usage: python -I recompute_r19.py <checkout-root>
"""

import pathlib
import random
import sys
from fractions import Fraction

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "course/modules/BK/BK4/grader"))
import instance  # noqa: E402  (the suite's generator; read only)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def sized(losses, target):
    k = ceil_div(target * len(losses), 10_000)
    return k, sorted(losses)[k - 1]


def cover(losses, margin):
    return 10_000 * sum(1 for x in losses if x <= margin) // len(losses)


def waterfall(loss, dfl, margins, funds, cap):
    a1 = min(loss, margins[dfl])
    a2 = min(loss - a1, funds[dfl])
    a3 = min(loss - a1 - a2, cap)
    r = loss - a1 - a2 - a3
    surv = sorted(m for m in funds if m != dfl)
    pool = sum(funds[m] for m in surv)
    if r >= pool:
        return a1, a2, a3, {m: funds[m] for m in surv}, r - pool
    sh = {m: r * funds[m] // pool for m in surv}
    left = r - sum(sh.values())
    for m in surv:
        if left > 0 and funds[m] > 0:
            sh[m] += 1
            left -= 1
    assert sum(sh.values()) == r
    return a1, a2, a3, sh, 0


# Lab 1 / Lab 3 instance (the page's four-member clearing house)
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAP = 20_000
D = 2
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
print("count", len(losses), "largest", max(losses), "sum", sum(losses))
print("Lab1 exact position", Fraction(9_550 * 40, 10_000), "k", ceil_div(9_550 * 40, 10_000))
k1, m1 = sized(losses, 9_550)
print("Lab1 margin for 9550", k1, m1, "cover at", cover(losses, m1), "cover below", cover(losses, m1 - 1))
for t in (9_000, 9_500, 9_750):
    k, m = sized(losses, t)
    print(f"target {t}: k {k} margin {m} cover {cover(losses, m)} below {cover(losses, m - 1)}")
for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    print("waterfall", loss, waterfall(loss, D, MARGIN, FUND, CAP))
print("Lab1 layers", waterfall(80_000, D, MARGIN, FUND, CAP))
# Part C: past counts for the margins of 9500 and 9000 taken as the defaulter's margin
sf = sum(FUND[m] for m in MARGIN if m != D)
for t in (9_500, 9_000):
    _, m = sized(losses, t)
    print(
        "partC", t, m,
        "past margin", sum(x > m for x in losses),
        "past fund", sum(x > m + FUND[D] for x in losses),
        "past capital", sum(x > m + FUND[D] + CAP for x in losses),
        "past survivors", sum(x > m + FUND[D] + CAP + sf for x in losses),
    )
print("difference 111074-105154 =", 111_074 - 105_154, "; 9500-9000 =", 9_500 - 9_000)
# Remainder and fixture values on the page
print("share check 4000 residual:", [4000 * FUND[m] // 12000 for m in (1, 3, 4)], "leftover", 4000 - sum(4000 * FUND[m] // 12000 for m in (1, 3, 4)))
print("fixture 181 (1,0):", waterfall(181, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60, 3: 50}, 30))
for L in (80, 100, 120, 150, 151, 170, 180, 181, 200, 205, 300):
    print("layer fixture", L, waterfall(L, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60, 3: 50}, 30))
print("remainder", [waterfall(L, 4, {1: 1, 2: 1, 3: 1, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0) for L in (1, 2, 3, 4)])
print("sizing fixtures", sized([10, 20, 30, 40, 50], 8000), sized([10, 20, 30, 40, 50], 8001), sized([10, 20, 30, 40, 50], 10000), sized([10, 20, 30, 40], 5000))
print("cover fixtures", cover([1, 5, 9], 4), 10_000 * 2 // 3, "20000/3 =", 20_000 / 3)
# Float claim in test_exact_position_is_an_integer_index_not_a_rounded_float
print("float 2800/10000*50 =", repr(2800 / 10000 * 50), "ceil", -((-2800 / 10000 * 50) // 1))
print("float target/10000*count for 9500 and 40:", repr(9500 / 10000 * 40))
# Large-cent test values
funds = {1: 6_692_931_089_932_558, 2: 585_467_024_498_971, 3: 0}
loss = 6_585_696_953_829_388
pool = funds[1] + funds[2]
s1 = loss * funds[1] // pool
s2 = loss * funds[2] // pool
left = loss - s1 - s2
print("large-cent shares", s1, s2, "leftover", left, "products exceed 2^53:", loss * funds[1] > 2**53)
print("large-cent test expects", {1: 6_055_950_114_045_320, 2: 529_746_839_784_068})
# Instance facts across seeds 0-49
answers = []
margins_by_seed = []
uncov = []
for seed in range(50):
    c = instance.make_instance(seed)
    answers.append(sized(c["losses_cents"], c["target_bps"])[1])
    margins_by_seed.append(c)
print("distinct sizing answers over seeds 0-49:", len(set(answers)))
print("distinct target-sized margins across seeds (target as set):", len(set(answers)))
print("seeds where the 9000/9500/9750 answers all differ:", sum(1 for seed in range(50) if len({sized(instance.make_instance(seed)['losses_cents'], t)[1] for t in (9000, 9500, 9750)}) == 3))
print("seed 0 instance:", {k: v for k, v in instance.make_instance(0).items() if k != "losses_cents"})
for seed in range(50):
    c = instance.make_instance(seed)
    assert 4 <= len(c["member_ids"]) <= 6 and 40 <= len(c["losses_cents"]) <= 80
    assert all(f >= 1 for f in c["default_fund_cents"]) and c["target_bps"] in (9000, 9500, 9750)
print("instance validity ranges: pass on seeds 0-49")
