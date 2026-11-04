"""Independent re-derivation of the BK4 project numbers (verifier BK4-c, round 2). Run from the checkout root.

Usage: .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/rederive.py
Computes with fractions and plain integers only; prints each checked value next to the value the page or test states.
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import ceil

out: list[str] = []


def check(name: str, got: object, stated: object) -> None:
    status = "OK" if got == stated else "MISMATCH"
    out.append(f"{status} {name}: derived={got} stated={stated}")


def layers(loss: int, im: int, fund: int, cap: int) -> tuple[int, int, int, int]:
    a1 = min(loss, im)
    a2 = min(loss - a1, fund)
    a3 = min(loss - a1 - a2, cap)
    return a1, a2, a3, loss - a1 - a2 - a3


def survivors(resid: int, funds: dict[int, int]) -> tuple[dict[int, int], int]:
    pool = sum(funds.values())
    if resid >= pool:
        return dict(funds), resid - pool
    sh = {m: resid * f // pool for m, f in funds.items()}
    left = resid - sum(sh.values())
    for m in sorted(funds):
        if left > 0 and funds[m] > 0:
            sh[m] += 1
            left -= 1
    assert left == 0
    return sh, 0


# Lab 1 / Lab 2 / Lab 3 reference instance (page constants)
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}
CAP = 20_000
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
check("lab scenarios: count", len(losses), 40)
check("lab scenarios: largest", max(losses), 118151)
a1, a2, a3, r = layers(80_000, MARGIN[2], FUND[2], CAP)
check("lab1 layers (margin, fund, capital, residual)", (a1, a2, a3, r), (50000, 6000, 20000, 4000))
sh, unc = survivors(r, {1: 4000, 3: 5000, 4: 3000})
check("lab1 survivor payments", sh, {1: 1334, 3: 1666, 4: 1000})
check("lab1 uncovered", unc, 0)
check("lab1 floored shares sum to residual minus 1", sum(r * f // 12000 for f in (4000, 5000, 3000)), 3999)
exact = Fraction(9550 * 40, 10000)
check("lab1 exact position", str(float(exact)), "38.2")
k = ceil(exact)
check("lab1 k", k, 39)
srt = sorted(losses)
check("lab1 margin (39th smallest)", srt[k - 1], 117088)
cov = 10000 * sum(1 for x in losses if x <= srt[k - 1]) // 40
below = 10000 * sum(1 for x in losses if x <= srt[k - 1] - 1) // 40
check("lab1 cover at margin", cov, 9750)
check("lab1 cover one cent below", below, 9500)
for tgt, stated_k, stated_m, stated_cov, stated_below in ((9000, 36, 105154, 9000, 8750), (9500, 38, 111074, 9500, 9250), (9750, 39, 117088, 9750, 9500)):
    kk = ceil(Fraction(tgt * 40, 10000))
    mm = srt[kk - 1]
    cc = 10000 * sum(1 for x in losses if x <= mm) // 40
    cb = 10000 * sum(1 for x in losses if x <= mm - 1) // 40
    check(f"lab3 target {tgt} k", kk, stated_k)
    check(f"lab3 target {tgt} margin", mm, stated_m)
    check(f"lab3 target {tgt} cover", cc, stated_cov)
    check(f"lab3 target {tgt} cover one cent below", cb, stated_below)
    # brute force least margin whose floored cover reaches target
    brute = next(m for m in range(max(losses) + 1) if 10000 * sum(1 for x in losses if x <= m) // 40 >= tgt)
    check(f"lab3 target {tgt} brute force", brute, mm)
for tgt, stated in ((9500, 111074), (9000, 105154)):
    mm = srt[ceil(Fraction(tgt * 40, 10000)) - 1]
    check(f"lab3 part C margin {tgt}", mm, stated)
    check(f"lab3 part C past margin {tgt}", sum(1 for x in losses if x > mm), 2 if tgt == 9500 else 4)
    check(f"lab3 part C past fund {tgt}", sum(1 for x in losses if x > mm + 6000), 2)
    check(f"lab3 part C past capital {tgt}", sum(1 for x in losses if x > mm + 6000 + CAP), 0)
    check(f"lab3 part C past survivors {tgt}", sum(1 for x in losses if x > mm + 6000 + CAP + 12000), 0)
check("exemplar B difference 111074-105154", 111074 - 105154, 5920)
check("exemplar B 38/40 is 95.00 percent (bps)", 10000 * 38 // 40, 9500)
# Lab 3 part A waterfall rows for defaulter margin 50000
rows = {}
for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
    a1, a2, a3, r = layers(loss, 50_000, 6_000, CAP)
    sh, unc = survivors(r, {1: 4000, 3: 5000, 4: 3000})
    rows[loss] = (a1, a2, a3, sh, unc, a1 + a2 + a3 + sum(sh.values()) + unc == loss)
check("lab3 part A 20000", rows[20_000], (20000, 0, 0, {1: 0, 3: 0, 4: 0}, 0, True))
check("lab3 part A 55000", rows[55_000], (50000, 5000, 0, {1: 0, 3: 0, 4: 0}, 0, True))
check("lab3 part A 70000", rows[70_000], (50000, 6000, 14000, {1: 0, 3: 0, 4: 0}, 0, True))
check("lab3 part A 80000", rows[80_000], (50000, 6000, 20000, {1: 1334, 3: 1666, 4: 1000}, 0, True))
check("lab3 part A 100000", rows[100_000], (50000, 6000, 20000, {1: 4000, 3: 5000, 4: 3000}, 12000, True))

# Layer-order fixture (page table)
FIX = {1: 40, 2: 60}
for loss, want in (
    (80, (80, 0, 0, (0, 0), 0)),
    (100, (100, 0, 0, (0, 0), 0)),
    (120, (100, 20, 0, (0, 0), 0)),
    (150, (100, 50, 0, (0, 0), 0)),
    (151, (100, 50, 1, (0, 0), 0)),
    (170, (100, 50, 20, (0, 0), 0)),
    (180, (100, 50, 30, (0, 0), 0)),
    (181, (100, 50, 30, (1, 0), 0)),
    (200, (100, 50, 30, (8, 12), 0)),
    (205, (100, 50, 30, (10, 15), 0)),
    (300, (100, 50, 30, (40, 60), 20)),
):
    a1, a2, a3, r = layers(loss, 100, 50, 30)
    sh, unc = survivors(r, FIX)
    check(f"fixture loss {loss}", (a1, a2, a3, (sh[1], sh[2]), unc), want)

# Remainder fixture
for loss, want in ((1, {1: 1, 2: 0, 3: 0}), (2, {1: 1, 2: 1, 3: 0}), (3, {1: 1, 2: 1, 3: 1}), (4, {1: 1, 2: 1, 3: 1})):
    sh, unc = survivors(loss, {1: 1, 2: 1, 3: 1})
    check(f"remainder loss {loss}", (sh, unc), (want, 1 if loss == 4 else 0))

# Sizing fixtures
def sized(losses_: list[int], tgt: int) -> int:
    return sorted(losses_)[ceil(Fraction(tgt * len(losses_), 10000)) - 1]

check("sizing 8000 bps", sized([10, 20, 30, 40, 50], 8000), 40)
check("sizing 8001 bps", sized([10, 20, 30, 40, 50], 8001), 50)
check("sizing 10000 bps", sized([10, 20, 30, 40, 50], 10000), 50)
check("sizing 5000 bps four", sized([10, 20, 30, 40], 5000), 20)
check("cover 1,5,9 margin 4", 10000 * sum(1 for x in [1, 5, 9] if x <= 4) // 3, 3333)
check("cover 1,2,9 margin 2", 10000 * sum(1 for x in [1, 2, 9] if x <= 2) // 3, 6666)

# Test fixture above 2**53: is the stated claim true?
L_BIG = 6_585_696_953_829_388
F1, F2 = 6_692_931_089_932_558, 585_467_024_498_971
pool = F1 + F2
sh1, sh2 = L_BIG * F1 // pool, L_BIG * F2 // pool
left = L_BIG - sh1 - sh2
check("big-case floored shares before leftover", (sh1, sh2), (6_055_950_114_045_319, 529_746_839_784_068))
check("big-case leftover", left, 1)
check("big-case payments after leftover to first survivor", (sh1 + left, sh2), (6_055_950_114_045_320, 529_746_839_784_068))
check("big-case payments sum to loss", sh1 + left + sh2, L_BIG)
out.append(f"INFO 2**53 = {2**53}; loss {L_BIG} < 2**53: {L_BIG < 2**53}; fund1 {F1} < 2**53: {F1 < 2**53}; pool {pool} < 2**53: {pool < 2**53}")
out.append(f"INFO product residual*fund1 = {L_BIG * F1} > 2**53: {L_BIG * F1 > 2**53}")
out.append(f"INFO float(loss*fund1)/pool floor check: {int(float(L_BIG * F1) / float(pool))} vs exact {sh1}")

# Seeded instances: target set, answer variety, validity (seeds 0-49)
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("inst", Path("course/modules/BK/BK4/grader/instance.py"))
assert spec and spec.loader
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
targets, answers, bad = set(), set(), []
for seed in range(50):
    c = inst.make_instance(seed)
    targets.add(c["target_bps"])
    ls = c["losses_cents"]
    answers.add(sorted(ls)[ceil(Fraction(c["target_bps"] * len(ls), 10000)) - 1])
    if not (4 <= len(c["member_ids"]) <= 6 and all(f >= 1 for f in c["default_fund_cents"]) and 40 <= len(ls) <= 80):
        bad.append(seed)
out.append(f"INFO seeds 0-49 target_bps values: {sorted(targets)}")
out.append(f"INFO seeds 0-49 distinct sizing answers (oracle): {len(answers)}")
out.append(f"INFO seeds 0-49 validity problems: {bad}")
print("\n".join(out))
