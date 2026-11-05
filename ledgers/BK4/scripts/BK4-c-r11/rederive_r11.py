"""Round-11 independent re-derivation for BK4-c (project page numbers, fixtures, exemplar B numbers).

Written by the round-11 verifier from the rules on project.html (spec, Conventions, Hand-computed fixtures), with
exact Fraction arithmetic where a rule is a fraction. It does not import or copy the grader, the reference or the page
code. Usage: python -I rederive_r11.py <repo_root>   (stdlib only; prints OK / MISMATCH lines and exits 1 on a mismatch)
"""

import random
import sys
from fractions import Fraction
from math import ceil

fails: list[str] = []


def check(label: str, got: object, want: object) -> None:
    status = "OK" if got == want else "MISMATCH"
    if got != want:
        fails.append(label)
    print(f"{status} {label}: got {got!r} want {want!r}")


def pay(loss: int, im_d: int, df_d: int, k_cap: int, survivors: dict[int, int]) -> tuple[int, int, int, dict[int, int], int]:
    """The rules of the page: layers, then survivors pro rata with the leftover by ascending id, or whole funds."""
    a1 = min(loss, im_d)
    a2 = min(loss - a1, df_d)
    a3 = min(loss - a1 - a2, k_cap)
    r = loss - a1 - a2 - a3
    total = sum(survivors.values())
    if r >= total:
        return a1, a2, a3, dict(survivors), r - total
    shares = {i: Fraction(r * d, total) for i, d in survivors.items()}
    floors = {i: (r * d) // total for i, d in survivors.items()}
    rem = r - sum(floors.values())
    assert 0 <= rem
    for i in sorted(survivors):
        if rem > 0 and survivors[i] > 0:
            floors[i] += 1
            rem -= 1
    del shares
    return a1, a2, a3, floors, 0


# Lab 1 / Lab 2 / Lab 3 shared inputs: member 2 defaults; survivors 1, 3, 4.
IM = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
DF = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
K = 20_000
surv = {1: DF[1], 3: DF[3], 4: DF[4]}

a1, a2, a3, sh, unc = pay(80_000, IM[2], DF[2], K, surv)
check("lab1 layers 50000/6000/20000 residual 4000", (a1, a2, a3, 80_000 - a1 - a2 - a3), (50_000, 6_000, 20_000, 4_000))
check("lab1 survivor payments 1334/1666/1000 uncovered 0", (sh, unc), ({1: 1334, 3: 1666, 4: 1000}, 0))
check("lab1 conservation", a1 + a2 + a3 + sum(sh.values()) + unc, 80_000)
check("lab1 floored shares sum 3999 (one cent short)", sum((4_000 * d) // 12_000 for d in surv.values()), 3_999)

rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
S = len(losses)
check("lab1/lab3 seeded scenario count", S, 40)
check("lab3 largest loss 118151", max(losses), 118_151)


def k_of(t: int) -> int:
    return ceil(Fraction(t * S, 10_000))


def margin_of(t: int) -> int:
    return sorted(losses)[k_of(t) - 1]


def cover(m: int) -> int:
    return (10_000 * sum(1 for x in losses if x <= m)) // S


def brute(t: int) -> int:
    for m in range(0, max(losses) + 1):
        if Fraction(10_000 * sum(1 for x in losses if x <= m), S) >= t:
            return m
    raise AssertionError


check("lab1 exact position 38.2 (9550 bps)", Fraction(9_550 * S, 10_000), Fraction(191, 5))
check("lab1 k 39, margin 117088 for 9550", (k_of(9_550), margin_of(9_550)), (39, 117_088))
check("lab1 cover at 117088 is 9750, one cent below 9500", (cover(117_088), cover(117_087)), (9_750, 9_500))
check("lab1 38 of 40 is 95.00 pct", Fraction(38, 40), Fraction(19, 20))

for t, k_want, m_want, c_want, cb_want in (
    (9_000, 36, 105_154, 9_000, 8_750),
    (9_500, 38, 111_074, 9_500, 9_250),
    (9_750, 39, 117_088, 9_750, 9_500),
):
    m = margin_of(t)
    check(f"lab3 part B target {t}: k, margin", (k_of(t), m), (k_want, m_want))
    check(f"lab3 part B target {t}: cover at, one cent below", (cover(m), cover(m - 1)), (c_want, cb_want))
    check(f"lab3 part B target {t}: brute force agrees", brute(t), m)

for t, past_m, past_f in ((9_500, 2, 2), (9_000, 4, 2)):
    m = margin_of(t)
    pm = sum(1 for x in losses if x > m)
    pf = sum(1 for x in losses if x > m + DF[2])
    pc = sum(1 for x in losses if x > m + DF[2] + K)
    ps = sum(1 for x in losses if x > m + DF[2] + K + sum(surv.values()))
    check(f"lab3 part C target {t}: past margin, fund, capital, survivors", (pm, pf, pc, ps), (past_m, past_f, 0, 0))

# Lab 3 part A rows (defaulter margin 50000).
rows = {
    20_000: (20_000, 0, 0, 0),
    55_000: (50_000, 5_000, 0, 0),
    70_000: (50_000, 6_000, 14_000, 0),
    80_000: (50_000, 6_000, 20_000, 0),
    100_000: (50_000, 6_000, 20_000, 12_000),
}
for loss, (wm, wf, wc, wu) in rows.items():
    a1, a2, a3, sh, unc = pay(loss, IM[2], DF[2], K, surv)
    check(f"lab3 part A loss {loss}: layers and uncovered", (a1, a2, a3, unc), (wm, wf, wc, wu))
    check(f"lab3 part A loss {loss}: conservation", a1 + a2 + a3 + sum(sh.values()) + unc, loss)
a1, a2, a3, sh, unc = pay(80_000, IM[2], DF[2], K, surv)
check("lab3 part A 80000 survivors", sh, {1: 1334, 3: 1666, 4: 1000})
a1, a2, a3, sh, unc = pay(100_000, IM[2], DF[2], K, surv)
check("lab3 part A 100000 survivors whole funds", sh, {1: 4000, 3: 5000, 4: 3000})

# Layer-order fixture (page table): defaulter margin 100, fund 50, capital 30; survivors {1: 40, 2: 60}.
table = {
    80: (80, 0, 0, 0, 0, 0), 100: (100, 0, 0, 0, 0, 0), 120: (100, 20, 0, 0, 0, 0), 150: (100, 50, 0, 0, 0, 0),
    151: (100, 50, 1, 0, 0, 0), 170: (100, 50, 20, 0, 0, 0), 180: (100, 50, 30, 0, 0, 0),
    181: (100, 50, 30, 1, 0, 0), 200: (100, 50, 30, 8, 12, 0), 205: (100, 50, 30, 10, 15, 0),
    300: (100, 50, 30, 40, 60, 20),
}
for loss, want in table.items():
    a1, a2, a3, sh, unc = pay(loss, 100, 50, 30, {1: 40, 2: 60})
    check(f"fixture layer order loss {loss}", (a1, a2, a3, sh.get(1, 0), sh.get(2, 0), unc), want)

# Remainder fixture: defaulter 4 with nothing; survivors 1, 2, 3 with 1 cent each.
for loss, want in ((1, {1: 1, 2: 0, 3: 0}), (2, {1: 1, 2: 1, 3: 0}), (4, {1: 1, 2: 1, 3: 1})):
    a1, a2, a3, sh, unc = pay(loss, 0, 0, 0, {1: 1, 2: 1, 3: 1})
    check(f"fixture remainder loss {loss}", sh, want)
check("fixture remainder loss 4 uncovered", pay(4, 0, 0, 0, {1: 1, 2: 1, 3: 1})[4], 1)


def margin_for(losses_c: list[int], t: int) -> int:
    n = len(losses_c)
    return sorted(losses_c)[ceil(Fraction(t * n, 10_000)) - 1]


check("sizing fixture 8000->40", margin_for([10, 20, 30, 40, 50], 8_000), 40)
check("sizing fixture 8001->50", margin_for([10, 20, 30, 40, 50], 8_001), 50)
check("sizing fixture 10000->50", margin_for([10, 20, 30, 40, 50], 10_000), 50)
check("sizing fixture 5000 of four ->20", margin_for([10, 20, 30, 40], 5_000), 20)
check("cover fixture 3333", (10_000 * sum(1 for x in [1, 5, 9] if x <= 4)) // 3, 3_333)
check("cover fixture 6666", (10_000 * sum(1 for x in [1, 2, 9] if x <= 2)) // 3, 6_666)

# Exemplar B numbers (memo passage): 9500 bps of 40 scenarios.
check("exemplar B exact position 38.0 for 9500", Fraction(9_500 * 40, 10_000), Fraction(38))
check("exemplar B difference 5920 cents and 500 bps", (111_074 - 105_154, 9_500 - 9_000), (5_920, 500))

# Hours.
hours = [2, 2, 3, 3, 2, 2, 1]
check("hours components sum to 15", sum(hours), 15)
check("hub 5 lessons x 7 h plus 15 h project = 50; 15/50 = 30 pct", (5 * 7 + 15, Fraction(15, 50)), (50, Fraction(3, 10)))

print("ROUND11 REDERIVE", "FAIL" if fails else "PASS", len(fails))
sys.exit(1 if fails else 0)
