"""Test instance generator for CS5 Monte Carlo pricing project.

Generates reproducible pseudo-random market parameters and invalid test cases.
Data is purely SIMULATED for testing and benchmarking purposes.
"""

from __future__ import annotations

import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance from an integer seed.

    SIMULATED: Parameters are sampled uniformly within standard financial ranges:
      - s0: [50.0, 150.0]
      - strike: [0.6 * s0, 1.4 * s0]
      - rate: [0.01, 0.08]
      - vol: [0.10, 0.50]
      - maturity: [0.25, 2.00]
      - n_paths: [2000, 5000]
      - seed: 64-bit integer
    """
    rng = random.Random(seed)
    s0 = round(rng.uniform(50.0, 150.0), 4)
    strike = round(rng.uniform(0.6 * s0, 1.4 * s0), 4)
    rate = round(rng.uniform(0.01, 0.08), 4)
    vol = round(rng.uniform(0.10, 0.50), 4)
    maturity = round(rng.uniform(0.25, 2.00), 4)
    n_paths = rng.randint(2000, 5000)
    mc_seed = rng.randint(0, (1 << 64) - 1)

    mutation_idx = rng.randint(0, 6)
    invalid_data: dict[str, Any] = {
        "s0": s0,
        "strike": strike,
        "rate": rate,
        "vol": vol,
        "maturity": maturity,
        "n_paths": n_paths,
        "seed": mc_seed,
        "mutation": mutation_idx,
    }

    return {
        "s0": s0,
        "strike": strike,
        "rate": rate,
        "vol": vol,
        "maturity": maturity,
        "n_paths": n_paths,
        "seed": mc_seed,
        "invalid_json": json.dumps(invalid_data, sort_keys=True),
    }
