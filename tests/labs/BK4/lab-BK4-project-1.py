"""Rung 1 worked example: one default on a four-member clearing house, every step annotated, in integer cents.

Standard library only. The inputs are SIMULATED: illustrative values, not market data. No file is read, and the
scenario losses come from a seeded generator, so every run prints the same lines.
"""

import random

MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}  # initial margin of each member, in cents (SIMULATED)
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}  # default-fund contribution of each member, in cents (SIMULATED)
CAPITAL = 20_000  # the CCP's own capital, in cents (SIMULATED)
DEFAULTER = 2
LOSS = 80_000  # the loss from this one default, in cents


def main() -> None:
    # Step 1. The three layers, in order. Each layer pays what the loss still needs, up to its own size, so the
    # layers never pay the same cent twice. The defaulter's margin is used before its default fund, and the
    # default fund before the CCP capital.
    from_margin = min(LOSS, MARGIN[DEFAULTER])
    from_fund = min(LOSS - from_margin, FUND[DEFAULTER])
    from_capital = min(LOSS - from_margin - from_fund, CAPITAL)
    residual = LOSS - from_margin - from_fund - from_capital
    print(f"layers: margin {from_margin} | default fund {from_fund} | CCP capital {from_capital} | residual {residual}")
    # Step 2. The surviving members are every member except the defaulter. Their default funds form the pool that
    # pays the residual, and the pool is the sum of their contributions.
    survivors = sorted(m for m in FUND if m != DEFAULTER)
    pool = sum(FUND[m] for m in survivors)
    print(f"survivors {survivors} | default funds {[FUND[m] for m in survivors]} | pool {pool}")
    # Step 3. The residual is below the pool, so each survivor pays its pro rata share. The share is floored to a
    # whole cent, which can leave a few cents unpaid. Those cents are given out one each, to the first survivors in
    # ascending id order that have a positive contribution, so the shares add up to the residual exactly.
    uncovered = 0
    if residual >= pool:
        shares = {m: FUND[m] for m in survivors}
        uncovered = residual - pool
    else:
        shares = {m: residual * FUND[m] // pool for m in survivors}
        leftover = residual - sum(shares.values())
        print(f"floored shares {shares} | leftover cents {leftover}")
        for m in survivors:
            if leftover > 0 and FUND[m] > 0:
                shares[m] += 1
                leftover -= 1
    print(f"survivor payments {shares} | uncovered {uncovered}")
    # Step 4. The conservation check. The layers, the survivors' payments and the uncovered loss add to the loss.
    total = from_margin + from_fund + from_capital + sum(shares.values()) + uncovered
    print(f"conservation: {total} == {LOSS} is {total == LOSS}")
    # Step 5. Sizing. The scenario set is 40 losses drawn from a seeded generator, each between 0 and 120000 cents.
    rng = random.Random(1)
    losses = [rng.randint(0, 120_000) for _ in range(40)]
    count = len(losses)
    target = 9_550  # basis points: the cover we want, 95.50 % of scenarios
    # The exact position of the target in the sorted losses is target * count / 10000, which is 38.2 here. The
    # margin must cover at least that many scenarios, so the position is rounded up: k = 39.
    exact_position = target * count / 10_000
    k = -((-target * count) // 10_000)
    print(f"target {target} bps of {count} scenarios: exact position {exact_position:.1f} | k {k}")
    margin = sorted(losses)[k - 1]
    print(f"margin: the {k}th smallest loss = {margin}")
    # Step 6. The cover at the margin, and one cent below it. Both are floored counts in basis points.
    covered = sum(1 for loss in losses if loss <= margin)
    below = sum(1 for loss in losses if loss <= margin - 1)
    cover_at = 10_000 * covered // count
    cover_below = 10_000 * below // count
    print(f"cover at the margin: {cover_at} bps | reaches the target: {cover_at >= target}")
    print(f"cover one cent below: {cover_below} bps | reaches the target: {cover_below >= target}")


main()
