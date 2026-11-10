"""Per-learner instances for the CS1 Atlas A1 returns autograder.

make_instance(seed) is deterministic: the same seed always produces the same instance,
and different seeds produce different price paths.
Every valid price path consists of strictly positive, finite float numbers.
All price series are SIMULATED: generated synthetic trajectories, not market data.
"""

from __future__ import annotations

import json
import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given workspace seed."""
    rng = random.Random(seed)

    # 1. Valid price path: length between 10 and 60, starting price 50 to 500
    n_steps = rng.randint(10, 60)
    p0 = round(rng.uniform(50.0, 500.0), 2)
    prices: list[float] = [p0]
    p_curr = p0
    for _ in range(n_steps - 1):
        # Geometric random walk step
        pct_change = rng.uniform(-0.04, 0.04)
        p_curr = max(0.01, round(p_curr * (1.0 + pct_change), 4))
        prices.append(p_curr)

    # 2. Fixed probe path for invariant checks across known steps
    probe_base = round(rng.uniform(80.0, 150.0), 3)
    probe_prices = [probe_base, round(probe_base * 1.05, 4), round(probe_base * 0.98, 4), round(probe_base * 1.02, 4)]

    # 3. Invalid cases to check exception raising
    invalid_cases = [
        {"desc": "single_price", "prices": [100.0]},
        {"desc": "empty_list", "prices": []},
        {"desc": "contains_zero", "prices": [100.0, 0.0, 105.0]},
        {"desc": "contains_negative", "prices": [100.0, -5.0, 105.0]},
        {"desc": "contains_nan", "prices": [100.0, float("nan"), 105.0]},
        {"desc": "contains_inf", "prices": [100.0, float("inf"), 105.0]},
    ]

    # Pre-calculated reference returns for the seed's price path to test against
    ref_simple: list[float] = [prices[i] / prices[i - 1] - 1.0 for i in range(1, len(prices))]
    ref_log: list[float] = [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]

    payload = {
        "prices": prices,
        "probe_prices": probe_prices,
        "ref_simple": ref_simple,
        "ref_log": ref_log,
        "invalid_cases": invalid_cases,
    }

    return {
        "seed": seed,
        "label": f"SIMULATED returns instance {seed}",
        "payload": json.dumps(payload, sort_keys=True),
    }
