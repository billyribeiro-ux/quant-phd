"""Deterministic instance generator for SC4 PDE pricer autograder. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:
* spot S0 in [85.0, 115.0];
* strike K in [90.0, 110.0];
* maturity T in [0.25, 1.50];
* risk-free rate r in [0.01, 0.06];
* volatility sigma in [0.15, 0.35];
* down-and-out barrier B in [0.70 * S0, 0.85 * S0];
* grid dimensions n_space in {120, 160, 200}, n_time in {60, 80, 100}.

The instance carries the seed and the label "SIMULATED".
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic SIMULATED option instance for ``seed``."""
    rng = random.Random(4_000_003 * int(seed) + 89_123)
    spot = round(rng.uniform(85.0, 115.0), 2)
    strike = round(rng.uniform(90.0, 110.0), 2)
    maturity = round(rng.uniform(0.25, 1.50), 3)
    rate = round(rng.uniform(0.01, 0.06), 3)
    vol = round(rng.uniform(0.15, 0.35), 3)
    barrier_fraction = rng.uniform(0.70, 0.85)
    barrier = round(spot * barrier_fraction, 2)
    n_space = rng.choice([120, 160, 200])
    n_time = rng.choice([60, 80, 100])
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "spot": spot,
        "strike": strike,
        "maturity": maturity,
        "rate": rate,
        "vol": vol,
        "barrier": barrier,
        "n_space": n_space,
        "n_time": n_time,
    }
