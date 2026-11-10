"""Deterministic instance generator for the S1 project autograder.

All instances are SIMULATED and generated from a seed.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid parameter set and sample returns from seed."""
    rng = random.Random(seed)

    # Grid of annualized Sharpe ratios from 0.30 to 1.50 in steps of 0.05
    sr_ann_choices = [round(0.30 + 0.05 * i, 2) for i in range(25)]
    sr_ann = sr_ann_choices[rng.randrange(len(sr_ann_choices))]

    # Periods per year: monthly (12), weekly (52), or daily (252)
    k_choices = [12, 52, 252]
    periods_per_year = k_choices[rng.randrange(len(k_choices))]

    # Significance levels alpha and power targets
    alpha_choices = [0.01, 0.05, 0.10]
    alpha = alpha_choices[rng.randrange(len(alpha_choices))]

    power_choices = [0.80, 0.90]
    power = power_choices[rng.randrange(len(power_choices))]

    # Per-period Sharpe ratio
    sr_per_period = sr_ann / math.sqrt(periods_per_year)

    # 30 simulated returns for testing sample Sharpe ratio
    returns = [rng.gauss(sr_per_period, 1.0) for _ in range(30)]

    return {
        "label": "SIMULATED",
        "seed": seed,
        "sr_ann": sr_ann,
        "periods_per_year": periods_per_year,
        "alpha": alpha,
        "power": power,
        "sr_per_period": sr_per_period,
        "returns": returns,
    }
