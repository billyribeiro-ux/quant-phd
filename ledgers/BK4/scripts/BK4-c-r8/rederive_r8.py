"""Round 8 independent re-derivation of every number the project page and its labs state (Fraction and plain integers).

Does not import the lab twins or the grader; it re-computes from the page's stated inputs only.
"""
from fractions import Fraction
import math
import random

fails = []


def check(label, got, want):
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got!r}, page says {want!r}")
    if not ok:
        fails.append(label)


# Lab 1 / Lab 2 inputs (page lines 56-139, 141-190)
MARGIN_D, FUND_D, CAP, LOSS = 50_000, 6_000, 20_000, 80_000
surv_funds = {1: 4_000, 3: 5_000, 4: 3_000}
pool = sum(surv_funds.values())
check("pool", pool, 12_000)
a1 = min(LOSS, MARGIN_D); a2 = min(LOSS - a1, FUND_D); a3 = min(LOSS - a1 - a2, CAP); R = LOSS - a1 - a2 - a3
check("layers margin/fund/capital/residual", (a1, a2, a3, R), (50_000, 6_000, 20_000, 4_000))
floored = {m: R * f // pool for m, f in surv_funds.items()}
check("floored shares", floored, {1: 1333, 3: 1666, 4: 1000})
left = R - sum(floored.values())
check("leftover cent", left, 1)
pay = dict(floored); pay[1] += left
check("survivor payments", pay, {1: 1334, 3: 1666, 4: 1000})
check("conservation", a1 + a2 + a3 + sum(pay.values()) + 0, LOSS)

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
check("largest loss of the seeded set (Lab 3 Part B says 118151)", max(losses), 118_151)
for target, margin_want, cover_want, below_want in [(9_000, 105_154, 9_000, 8_750), (9_500, 111_074, 9_500, 9_250), (9_750, 117_088, 9_750, 9_500), (9_550, 117_088, None, None)]:
    k = math.ceil(Fraction(target * 40, 10_000))
    m = sorted(losses)[k - 1]
    cov = Fraction(10_000 * sum(1 for x in losses if x <= m), 40).__floor__()
    below = Fraction(10_000 * sum(1 for x in losses if x <= m - 1), 40).__floor__()
    check(f"target {target}: margin", m, margin_want)
    if cover_want is not None:
        check(f"target {target}: cover at margin", cov, cover_want)
        check(f"target {target}: cover one cent below", below, below_want)
        check(f"target {target}: cover below target", below < target, True)
check("Lab 1 exact position for 9550", Fraction(9_550 * 40, 10_000), Fraction(382, 10))
check("Lab 1 index k for 9550", math.ceil(Fraction(9_550 * 40, 10_000)), 39)
check("Part C margin count past margin (9500)", sum(1 for x in losses if x > 111_074), 2)
check("Part C past default fund (9500)", sum(1 for x in losses if x > 111_074 + FUND_D), 2)
check("Part C past CCP capital (9500)", sum(1 for x in losses if x > 111_074 + FUND_D + CAP), 0)
check("Part C past survivors (9500)", sum(1 for x in losses if x > 111_074 + FUND_D + CAP + pool), 0)
check("Part C past margin (9000)", sum(1 for x in losses if x > 105_154), 4)
check("Part C past default fund (9000)", sum(1 for x in losses if x > 105_154 + FUND_D), 2)
check("exemplar B difference 111074-105154", 111_074 - 105_154, 5_920)

# Layer-order fixture table (page lines 229-250): defaulter margin 100, fund 50, capital 30, survivors 40 and 60
def wf(loss, margin=100, fund=50, cap=30, s1=40, s2=60):
    m = min(loss, margin); f = min(loss - m, fund); c = min(loss - m - f, cap); r = loss - m - f - c
    D = s1 + s2
    if r >= D:
        return m, f, c, (s1, s2), r - D
    sh1, sh2 = r * s1 // D, r * s2 // D
    lo = r - sh1 - sh2
    if lo >= 1:
        sh1 += 1; lo -= 1
    if lo >= 1:
        sh2 += 1; lo -= 1
    assert lo == 0
    return m, f, c, (sh1, sh2), 0

table = {80: (80, 0, 0, (0, 0), 0), 100: (100, 0, 0, (0, 0), 0), 120: (100, 20, 0, (0, 0), 0), 150: (100, 50, 0, (0, 0), 0),
         151: (100, 50, 1, (0, 0), 0), 170: (100, 50, 20, (0, 0), 0), 180: (100, 50, 30, (0, 0), 0),
         181: (100, 50, 30, (1, 0), 0), 200: (100, 50, 30, (8, 12), 0), 205: (100, 50, 30, (10, 15), 0),
         300: (100, 50, 30, (40, 60), 20)}
for loss, want in table.items():
    check(f"fixture row {loss}", wf(loss), want)
# remainder fixture: defaulter 4 with nothing, survivors 1,2,3 with 1 cent each
def rem(r):
    D = 3
    if r >= D:
        return [1, 1, 1], r - D
    sh = [r * 1 // D] * 3; lo = r - sum(sh); out = list(sh)
    for i in range(3):
        if lo > 0:
            out[i] += 1; lo -= 1
    return out, max(0, r - D)
check("remainder 1 cent", rem(1), ([1, 0, 0], 0))
check("remainder 2 cents", rem(2), ([1, 1, 0], 0))
check("remainder 4 cents", rem(4), ([1, 1, 1], 1))
# sizing fixtures
def size(losses, t):
    return sorted(losses)[math.ceil(Fraction(t * len(losses), 10_000)) - 1]
check("sizing 8000 on 10..50", size([10, 20, 30, 40, 50], 8000), 40)
check("sizing 8001 on 10..50", size([10, 20, 30, 40, 50], 8001), 50)
check("sizing 10000 on 10..50", size([10, 20, 30, 40, 50], 10000), 50)
check("sizing 5000 on 10..40", size([10, 20, 30, 40], 5000), 20)
check("cover 1 of 3 at margin 4", 10_000 * sum(1 for x in [1, 5, 9] if x <= 4) // 3, 3333)
check("cover 2 of 3 at margin 2", 10_000 * sum(1 for x in [1, 2, 9] if x <= 2) // 3, 6666)
check("20000/3 to two places", round(20000 / 3, 2), 6666.67)

# test_large_cent_shares_are_floored_in_integers numbers
R_big = 6_585_696_953_829_388
F1, F2 = 6_692_931_089_932_558, 585_467_024_498_971
D_big = F1 + F2
floor1, floor2 = R_big * F1 // D_big, R_big * F2 // D_big
check("large-cent floor share 1 (before leftover)", floor1, 6_055_950_114_045_319)
check("large-cent floor share 2 (before leftover)", floor2, 529_746_839_784_068)
lo_big = R_big - floor1 - floor2
check("large-cent leftover cents", lo_big, 1)
check("large-cent share 1 after leftover to member 1", floor1 + lo_big, 6_055_950_114_045_320)
check("large-cent share 2 after leftover", floor2, 529_746_839_784_068)
check("large-cent payments sum to residual", floor1 + lo_big + floor2, R_big)
check("large-cent products exceed 2**53", R_big * F1 > 2 ** 53, True)

print("FAILS:", fails if fails else "none")
