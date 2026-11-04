"""Independent re-derivation of every number on the BK4 project page (slice c, round 4).

Written from the page's rules alone, not from the lab code or the reference solution. Run: python rederive_r4.py <root>.
Prints OK/MISMATCH lines; exits 1 on any mismatch.
"""

import math
import random
import sys
from fractions import Fraction
from typing import Any

sys.path.insert(0, sys.argv[1] + "/course/modules/BK/BK4/grader")
import instance as inst  # noqa: E402

bad = 0


def check(name: str, got: Any, want: Any) -> None:
    global bad
    ok = got == want
    bad += not ok
    print(("OK " if ok else "MISMATCH ") + f"{name}: got {got!r} want {want!r}")


def waterfall_p(loss: int, d: int, im: dict[int, int], df: dict[int, int], cap: int) -> tuple[int, int, int, dict[int, int], int]:
    a1 = min(loss, im[d])
    a2 = min(loss - a1, df[d])
    a3 = min(loss - a1 - a2, cap)
    r = loss - a1 - a2 - a3
    surv = sorted(m for m in df if m != d)
    pool = sum(df[m] for m in surv)
    if r >= pool:
        return a1, a2, a3, {m: df[m] for m in surv}, r - pool
    pay = {m: r * df[m] // pool for m in surv}
    rem = r - sum(pay.values())
    for m in surv:
        if rem and df[m] > 0:
            pay[m] += 1
            rem -= 1
    return a1, a2, a3, pay, 0


# ---- Labs 1-3 instance: member 2 defaults; margins 30000/50000/40000/20000; funds 4000/6000/5000/3000; capital 20000
IM = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
DF = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAP = 20_000
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
check("S", S, 40)
check("largest loss", max(losses), 118151)
a1, a2, a3, pay, unc = waterfall_p(80_000, 2, IM, DF, CAP)
check("lab1 layers", (a1, a2, a3), (50_000, 6_000, 20_000))
check("residual 80000", 80_000 - a1 - a2 - a3, 4_000)
check("pool", sum(DF[m] for m in (1, 3, 4)), 12_000)
check("floored shares", {m: 4000 * DF[m] // 12000 for m in (1, 3, 4)}, {1: 1333, 3: 1666, 4: 1000})
check("survivor pay", pay, {1: 1334, 3: 1666, 4: 1000})
check("uncovered 80000", unc, 0)
check("conservation 80000", a1 + a2 + a3 + sum(pay.values()) + unc, 80_000)
k95_5 = -((-9550 * S) // 10_000)
check("exact position 9550", Fraction(9550 * S, 10_000), Fraction(382, 10))
check("k for 9550", k95_5, 39)
check("margin 9550 = 39th smallest", sorted(losses)[k95_5 - 1], 117_088)
m = 117_088
check("cover at 117088", 10_000 * sum(1 for x in losses if x <= m) // S, 9_750)
check("cover at 117087", 10_000 * sum(1 for x in losses if x <= m - 1) // S, 9_500)
check("38/40 as percent", Fraction(38, 40) * 100, Fraction(95, 1))
# Lab 1 interpretation "38.2 taken up to 39"
check("exact 38.2", float(Fraction(9550 * 40, 10_000)), 38.2)

# Lab 3 Part A
rows = {
    20_000: (20_000, 0, 0, 0),
    55_000: (50_000, 5_000, 0, 0),
    70_000: (50_000, 6_000, 14_000, 0),
    80_000: (50_000, 6_000, 20_000, 0),
    100_000: (50_000, 6_000, 20_000, 12_000),
}
for loss, want in rows.items():
    got = waterfall_p(loss, 2, IM, DF, CAP)
    check(f"partA layers+unc loss {loss}", (got[0], got[1], got[2], got[4]), want)
    check(f"partA conservation loss {loss}", got[0] + got[1] + got[2] + sum(got[3].values()) + got[4] == loss, True)
check("partA 80000 survivors", waterfall_p(80_000, 2, IM, DF, CAP)[3], {1: 1334, 3: 1666, 4: 1000})
check("partA 100000 survivors", waterfall_p(100_000, 2, IM, DF, CAP)[3], {1: 4000, 3: 5000, 4: 3000})

# Lab 3 Part B
def order_stat(ls: list[int], t: int) -> tuple[int, int]:
    k = math.ceil(Fraction(t * len(ls), 10_000))
    return k, sorted(ls)[k - 1]

def brute(ls: list[int], t: int) -> int:
    for cand in range(0, max(ls) + 1):
        if 10_000 * sum(1 for x in ls if x <= cand) // len(ls) >= t:
            return cand
    raise AssertionError

expect_b = {9_000: (36, 105_154, 8_750), 9_500: (38, 111_074, 9_250), 9_750: (39, 117_088, 9_500)}
for t, (kw, mw, below_w) in expect_b.items():
    k, mg = order_stat(losses, t)
    check(f"partB k {t}", k, kw)
    check(f"partB margin {t}", mg, mw)
    check(f"partB brute {t}", brute(losses, t), mw)
    check(f"partB cover at margin {t} >= t", 10_000 * sum(1 for x in losses if x <= mg) // S >= t, True)
    check(f"partB cover one below {t}", 10_000 * sum(1 for x in losses if x <= mg - 1) // S, below_w)
    check(f"partB cover at margin exact {t}", 10_000 * sum(1 for x in losses if x <= mg) // S, t)

# Lab 3 Part C (each margin taken as the defaulter's initial margin)
surv_fund = sum(DF[m] for m in (1, 3, 4))
for t, (mw_past_m, mw_past_f) in {9_500: (2, 2), 9_000: (4, 2)}.items():
    _, mg = order_stat(losses, t)
    past_m = sum(1 for x in losses if x > mg)
    past_f = sum(1 for x in losses if x > mg + DF[2])
    past_c = sum(1 for x in losses if x > mg + DF[2] + CAP)
    past_s = sum(1 for x in losses if x > mg + DF[2] + CAP + surv_fund)
    check(f"partC past margin {t}", past_m, mw_past_m)
    check(f"partC past fund {t}", past_f, mw_past_f)
    check(f"partC past capital {t}", past_c, 0)
    check(f"partC past survivors {t}", past_s, 0)
check("recommend 5920 difference", 111_074 - 105_154, 5_920)
check("500 bps", 9_500 - 9_000, 500)

# Layer-order fixture (defaulter 3: IM 100, DF 50; K 30; survivors 1:40, 2:60)
fixture = {
    80: (80, 0, 0, (0, 0), 0), 100: (100, 0, 0, (0, 0), 0), 120: (100, 20, 0, (0, 0), 0),
    150: (100, 50, 0, (0, 0), 0), 151: (100, 50, 1, (0, 0), 0), 170: (100, 50, 20, (0, 0), 0),
    180: (100, 50, 30, (0, 0), 0), 181: (100, 50, 30, (1, 0), 0), 200: (100, 50, 30, (8, 12), 0),
    205: (100, 50, 30, (10, 15), 0), 300: (100, 50, 30, (40, 60), 20),
}
for loss, (q1, q2, q3, (s1, s2), u) in fixture.items():
    got = waterfall_p(loss, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60, 3: 50}, 30)
    check(f"fixture loss {loss}", (got[0], got[1], got[2], (got[3][1], got[3][2]), got[4]), (q1, q2, q3, (s1, s2), u))

# Remainder fixture: survivors 1,2,3 DF 1; defaulter 4 with nothing
for loss, want in {1: {1: 1, 2: 0, 3: 0}, 2: {1: 1, 2: 1, 3: 0}, 3: {1: 1, 2: 1, 3: 1}}.items():
    got = waterfall_p(loss, 4, {1: 1, 2: 1, 3: 1, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
    check(f"remainder loss {loss}", got[3], want)
got4 = waterfall_p(4, 4, {1: 1, 2: 1, 3: 1, 4: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0)
check("remainder loss 4 uncovered", (got4[3], got4[4]), ({1: 1, 2: 1, 3: 1}, 1))

# Sizing fixtures
check("sizing 8000", order_stat([10, 20, 30, 40, 50], 8000)[1], 40)
check("sizing 8001", order_stat([10, 20, 30, 40, 50], 8001)[1], 50)
check("sizing 10000", order_stat([10, 20, 30, 40, 50], 10000)[1], 50)
check("sizing 5000 four", order_stat([10, 20, 30, 40], 5000)[1], 20)
# Cover fixtures
check("cover 1,5,9 @4", 10_000 * sum(1 for x in [1, 5, 9] if x <= 4) // 3, 3333)
check("cover 1,2,9 @2", 10_000 * sum(1 for x in [1, 2, 9] if x <= 2) // 3, 6666)
check("floor 20000/3", Fraction(20000, 3).__floor__(), 6666)

# Large-cent claim (page's test docstring says residual * fund exceeds 2**53)
TWO53 = 2**53
R = 6_585_696_953_829_388
F1, F2 = 6_692_931_089_932_558, 585_467_024_498_971
check("loss below 2**53", R < TWO53, True)
check("default funds below 2**53", (F1 < TWO53, F2 < TWO53), (True, True))
check("R*F1 exceeds 2**53", R * F1 > TWO53, True)
check("R*F2 exceeds 2**53", R * F2 > TWO53, True)
pool = F1 + F2
s1 = R * F1 // pool
s2 = R * F2 // pool
check("floor shares", (s1, s2), (6_055_950_114_045_319, 529_746_839_784_068))
check("with leftover", (s1 + (R - s1 - s2), s2), (6_055_950_114_045_320, 529_746_839_784_068))

# Instance validity and sizing answers over seeds 0-49 (plan 5.5)
answers = []
bad_seeds = []
for seed in range(50):
    c = inst.make_instance(seed)
    n = len(c["member_ids"])
    ok = (
        c["member_ids"] == list(range(1, n + 1)) and 4 <= n <= 6 and c["defaulter_id"] in c["member_ids"]
        and all(f >= 1 for f in c["default_fund_cents"]) and all(x >= 0 for x in c["initial_margin_cents"])
        and c["ccp_capital_cents"] >= 0 and 40 <= len(c["losses_cents"]) <= 80
        and all(isinstance(x, int) and x >= 0 for x in c["losses_cents"]) and c["target_bps"] in (9000, 9500, 9750)
    )
    if not ok:
        bad_seeds.append(seed)
    answers.append((order_stat(c["losses_cents"], c["target_bps"])[1], c["target_bps"]))
check("validity bad seeds", bad_seeds, [])
distinct = len({a for a, _ in answers})
print(f"INFO distinct sizing answers over seeds 0-49: {distinct}; distinct targets {sorted({t for _, t in answers})}")
check("distinct sizing answers >= 3", distinct >= 3, True)
print(f"INFO seeds whose sized margin differs from seed 0: {sum(1 for a, _ in answers if a != answers[0][0])} of 49")
print("TOTAL MISMATCHES", bad)
sys.exit(1 if bad else 0)
