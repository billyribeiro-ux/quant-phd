"""Rung 3 check: the reference instance of the project page, its waterfall rows and its sizing table.

Standard library only. The inputs are SIMULATED: illustrative values, not market data. Every amount is an int in cents,
and every cover is an int in basis points, floored. The scenario losses are the seeded set of Lab 1. The brute-force
search below is a check on the sizing rule, not a proof of it.
"""

import random

MEMBERS = [1, 2, 3, 4]
MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}  # initial margin of each member, in cents (SIMULATED)
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}  # default-fund contribution of each member, in cents (SIMULATED)
CAPITAL = 20_000  # the CCP's own capital, in cents (SIMULATED)
DEFAULTER = 2
TARGETS = (9_000, 9_500, 9_750)  # basis points


def waterfall(loss: int, margin_d: int) -> tuple[int, int, int, dict[int, int], int]:
    """Pay one loss in cents: the defaulter's margin (margin_d), its default fund, the CCP capital, then survivors."""
    from_margin = min(loss, margin_d)
    from_fund = min(loss - from_margin, FUND[DEFAULTER])
    from_capital = min(loss - from_margin - from_fund, CAPITAL)
    residual = loss - from_margin - from_fund - from_capital
    survivors = [m for m in MEMBERS if m != DEFAULTER]
    pool = sum(FUND[m] for m in survivors)
    if residual >= pool:
        return from_margin, from_fund, from_capital, {m: FUND[m] for m in survivors}, residual - pool
    shares = {m: residual * FUND[m] // pool for m in survivors}
    leftover = residual - sum(shares.values())
    for m in survivors:
        if leftover > 0 and FUND[m] > 0:
            shares[m] += 1
            leftover -= 1
    return from_margin, from_fund, from_capital, shares, 0


def margin_for_target(losses: list[int], target: int) -> int:
    """The k-th smallest loss in cents, with k = ceil(target * count / 10000) in integers."""
    k = -((-target * len(losses)) // 10_000)
    return sorted(losses)[k - 1]


def brute_force_margin(losses: list[int], target: int) -> int:
    """The least whole-cent margin whose floored cover in basis points reaches the target, found by scanning margins."""
    top = max(losses)
    tally = [0] * (top + 1)
    for loss in losses:
        tally[loss] += 1
    covered = 0
    for margin in range(top + 1):
        covered += tally[margin]
        if 10_000 * covered // len(losses) >= target:
            return margin
    return top


def main() -> None:
    # Part A. Five losses on the reference instance, each with its layers, survivor payments and uncovered loss.
    print("part A: the waterfall rows, with the defaulter's margin as set")
    for loss in (20_000, 55_000, 70_000, 80_000, 100_000):
        a1, a2, a3, shares, uncovered = waterfall(loss, MARGIN[DEFAULTER])
        total = a1 + a2 + a3 + sum(shares.values()) + uncovered
        print(
            f"loss {loss} | margin {a1} | fund {a2} | capital {a3} | survivors {shares} | "
            f"uncovered {uncovered} | conservation {total == loss}"
        )
    # Part B. Sizing for three targets on the 40 seeded scenario losses.
    rng = random.Random(1)
    losses = [rng.randint(0, 120_000) for _ in range(40)]
    print(f"part B: {len(losses)} scenarios, largest loss {max(losses)}")
    for target in TARGETS:
        k = -((-target * len(losses)) // 10_000)
        margin = margin_for_target(losses, target)
        cover_at = 10_000 * sum(1 for x in losses if x <= margin) // len(losses)
        cover_below = 10_000 * sum(1 for x in losses if x <= margin - 1) // len(losses)
        brute = brute_force_margin(losses, target)
        print(
            f"target {target} | k {k} | margin {margin} | cover {cover_at} | cover one cent below {cover_below} | "
            f"brute force {brute} | agrees {brute == margin}"
        )
    # Part C. The margin for two targets, taken as the defaulter's initial margin. Each count is the number of
    # scenarios that get past one more layer: past the margin, past the default fund, past the CCP capital (so the
    # surviving members pay), and past the surviving members' total (so a loss is uncovered).
    surviving_fund = sum(FUND[m] for m in MEMBERS if m != DEFAULTER)
    print("part C: the scenarios that get past each layer, for each margin taken as the defaulter's margin")
    for target in (9_500, 9_000):
        margin = margin_for_target(losses, target)
        past_margin = sum(1 for x in losses if x > margin)
        past_fund = sum(1 for x in losses if x > margin + FUND[DEFAULTER])
        past_capital = sum(1 for x in losses if x > margin + FUND[DEFAULTER] + CAPITAL)
        past_survivors = sum(1 for x in losses if x > margin + FUND[DEFAULTER] + CAPITAL + surviving_fund)
        print(
            f"target {target} | margin {margin} | past margin {past_margin} | past default fund {past_fund} | "
            f"past CCP capital {past_capital} | past survivors (uncovered) {past_survivors}"
        )


main()
