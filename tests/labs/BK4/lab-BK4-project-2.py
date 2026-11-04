"""Rung 2 completion: the default of Lab 1, with the survivor share and the sizing index left for you to fill in.

Standard library only. The inputs are SIMULATED: illustrative values, not market data.
"""

import random

MARGIN = {1: 30_000, 2: 50_000, 3: 40_000, 4: 20_000}  # initial margin of each member, in cents (SIMULATED)
FUND = {1: 4_000, 2: 6_000, 3: 5_000, 4: 3_000}  # default-fund contribution of each member, in cents (SIMULATED)
CAPITAL = 20_000  # the CCP's own capital, in cents (SIMULATED)
DEFAULTER = 2
LOSS = 80_000  # the loss from this one default, in cents


def main() -> None:
    # The layers: margin, then default fund, then CCP capital. Each pays what the loss still needs.
    from_margin = min(LOSS, MARGIN[DEFAULTER])
    from_fund = min(LOSS - from_margin, FUND[DEFAULTER])
    from_capital = min(LOSS - from_margin - from_fund, CAPITAL)
    residual = LOSS - from_margin - from_fund - from_capital
    print(f"layers: margin {from_margin} | default fund {from_fund} | CCP capital {from_capital} | residual {residual}")
    # The survivors pay the residual pro rata to their default funds: each share is floored to a whole cent.
    survivors = sorted(m for m in FUND if m != DEFAULTER)
    pool = sum(FUND[m] for m in survivors)
    shares = {m: residual * FUND[m] // pool for m in survivors}
    leftover = residual - sum(shares.values())
    for m in survivors:
        if leftover > 0 and FUND[m] > 0:
            shares[m] += 1
            leftover -= 1
    print(f"survivor shares (cents): {shares}")
    # The sizing. The margin for a target is the k-th smallest loss, where k is the target's share of the scenarios
    # rounded up: k = ceil(target * count / 10000), computed in integers as -((-target * count) // 10000).
    rng = random.Random(1)
    losses = [rng.randint(0, 120_000) for _ in range(40)]
    target = 9_550
    count = len(losses)
    index = -((-target * count) // 10_000)
    print(f"sizing index k = {index} | margin for target {target} bps = {sorted(losses)[index - 1]}")


main()
