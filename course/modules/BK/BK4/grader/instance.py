"""Per-learner instances for the BK4 project: the clearing-house simulator (clearing_house.py).

make_instance(seed) is deterministic. It returns a SIMULATED clearing house: N members with ids 1 to N (N from 4 to 6),
an initial margin and a default-fund contribution for each (integer cents, aligned with member_ids by position), a CCP
capital, one defaulting member, S scenario losses for that member's default (integer cents), and a target cover in
basis points. Every case is valid, and the seed changes the answers. Nothing here is market data or a real clearing
house.

Each case contains three scenarios that the page's rules must treat differently: one loss inside the defaulter's
initial margin, one that reaches the defaulter's default fund, and one that exhausts the defaulter's resources and
the CCP capital, so that the surviving members pay.

clearing_house.py never calls make_instance; a learner may call it only to read a case.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A SIMULATED clearing house and default for the given seed. Deterministic; every value is valid."""
    rng = random.Random(f"BK4-clearing-house/{int(seed)}")
    count = rng.randint(4, 6)
    member_ids = list(range(1, count + 1))
    initial_margin = [rng.randint(10_000, 60_000) for _ in member_ids]  # cents, initial margin of each member
    default_fund = [rng.randint(1_000, 8_000) for _ in member_ids]  # cents, default-fund contribution, at least 1 cent
    capital = rng.randint(0, 50_000)  # cents, the CCP's own capital
    defaulter_id = rng.randint(1, count)
    index = defaulter_id - 1
    margin_d, fund_d = initial_margin[index], default_fund[index]
    scenarios = rng.randint(40, 80)
    ceiling = margin_d + fund_d + capital + 30_000
    losses = [rng.randint(0, ceiling) for _ in range(scenarios)]
    losses[0] = margin_d // 2  # inside the defaulter's initial margin
    losses[1] = margin_d + fund_d // 2 + 1  # past the margin, inside the defaulter's default fund
    losses[2] = margin_d + fund_d + capital + 1 + rng.randint(0, 20_000)  # past every defaulter layer and the capital
    target_bps = rng.choice((9_000, 9_500, 9_750))
    return {
        "seed": int(seed),
        "label": f"SIMULATED clearing house, seed {int(seed)}: not market data",
        "member_ids": member_ids,
        "defaulter_id": defaulter_id,
        "initial_margin_cents": initial_margin,
        "default_fund_cents": default_fund,
        "ccp_capital_cents": capital,
        "losses_cents": losses,
        "target_bps": target_bps,
    }
