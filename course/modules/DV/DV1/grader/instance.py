"""Instance generator for DV1: Hedging-Error Study.

Generates deterministic market instances for option parameters, rebalancing frequencies,
and transaction cost structures under geometric Brownian motion.
All instances are labeled SIMULATED.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    spot = round(85.0 + rng.random() * 30.0, 2)
    moneyness = round(0.90 + rng.random() * 0.20, 2)
    strike = round(spot * moneyness, 2)
    rate = round(0.02 + rng.random() * 0.04, 3)
    vol = round(0.15 + rng.random() * 0.15, 3)
    maturity = round(0.25 + rng.random() * 0.75, 2)
    cost_rate = round(0.001 + rng.random() * 0.003, 4)  # 10 bps to 40 bps
    steps_list = [12, 52, 252]
    n_paths = 1000

    return {
        "spot": spot,
        "strike": strike,
        "rate": rate,
        "vol": vol,
        "maturity": maturity,
        "cost_rate": cost_rate,
        "steps_list": steps_list,
        "n_paths": n_paths,
        "seed": seed,
    }
