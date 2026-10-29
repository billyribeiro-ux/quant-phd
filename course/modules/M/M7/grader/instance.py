"""Per-learner instances for the M7 constrained allocator (constrained_allocator.py).

make_instance(seed) is deterministic. It returns a SIMULATED case of three to five assets in two sectors: expected
returns, a covariance matrix equal to (A-transpose A plus the identity) over 1000, a starting portfolio, box bounds,
sector caps and a turnover limit. Every case is feasible by construction: the starting portfolio sums to one, lies in
its box and within every sector cap, and the turnover limit is not negative. Nothing here is a real portfolio or a
real return series.

All inputs are decimals with at most three digits after the point, so the grader can read each one exactly. The case is
returned as a JSON string under ``payload``. The grader decodes it, and constrained_allocator.py never calls
make_instance; a learner may call it only to read a case, as the project page shows.
"""

from __future__ import annotations

import json
import random
from typing import Any

SECTOR_COUNT = 2  # fixed, so the collected test count is the same on every seed
ASSET_COUNTS = (3, 4, 5)


def _integers_summing_to_100(rng: random.Random, n: int) -> list[int]:
    """Hundredths of a unit: non-negative integers that sum to exactly 100, so the starting portfolio sums to one."""
    draws = [rng.randint(5, 40) for _ in range(n)]
    total = sum(draws)
    weights = [value * 100 // total for value in draws]
    largest = max(range(n), key=lambda i: weights[i])
    weights[largest] += 100 - sum(weights)
    return weights


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(f"M7-constrained-allocator/{int(seed)}")
    n = rng.choice(ASSET_COUNTS)
    gamma = rng.randint(2, 8)  # risk aversion; the objective is (gamma / 2) w' Sigma w - mu' w
    factor = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    # Sigma = (A'A + I) / 1000: symmetric, and positive definite because the identity is added.
    sigma = [
        [(sum(factor[k][i] * factor[k][j] for k in range(n)) + (1 if i == j else 0)) / 1000 for j in range(n)]
        for i in range(n)
    ]
    mu = [rng.randint(-10, 40) / 1000 for _ in range(n)]  # expected return in one period, -1.0% to 4.0%
    w0_units = _integers_summing_to_100(rng, n)
    w0 = [value / 100 for value in w0_units]
    lower = [rng.choice((-10, -5, 0)) / 100 for _ in range(n)]  # -10% to 0%: short selling is allowed in some cases
    upper = [max(w0_units[i], rng.choice((35, 60, 100))) / 100 for i in range(n)]  # never below the starting weight
    labels = [i % SECTOR_COUNT for i in range(n)]
    rng.shuffle(labels)
    sector_caps = []
    for k in range(SECTOR_COUNT):
        in_sector = sum(w0_units[i] for i in range(n) if labels[i] == k)
        sector_caps.append((in_sector + rng.choice((0, 5, 10, 20, 40))) / 100)  # never below the starting sector weight
    turnover_limit = rng.choice(range(5, 41, 5)) / 100  # 5% to 40% of the portfolio, one period
    case: dict[str, Any] = {
        "label": f"SIMULATED constrained allocation, seed {int(seed)}: {n} assets, not a real portfolio",
        "gamma": gamma,
        "mu": mu,
        "sigma": sigma,
        "w0": w0,
        "lower": lower,
        "upper": upper,
        "sector": labels,
        "sector_caps": sector_caps,
        "turnover_limit": turnover_limit,
    }
    return {"seed": int(seed), "label": case["label"], "payload": json.dumps(case, sort_keys=True)}
