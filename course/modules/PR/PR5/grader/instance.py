"""Instance generator for PR5 Pod Allocation Simulator.

Deterministic instance generation from integer seed.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic parameters for a multi-manager pod platform.

    Args:
        seed: Random seed derived from learner workspace.

    Returns:
        Dictionary containing platform configuration and pod parameters as numeric lists.
    """
    rng = random.Random(seed)

    n_pods = 10
    n_skilled = 6
    n_unskilled = 4

    mus: list[float] = []
    sigmas: list[float] = []
    skills: list[int] = []
    soft_stops: list[float] = []
    hard_stops: list[float] = []

    # 6 Skilled pods: positive annualized drift (8% to 18%), vol (12% to 22%)
    for _ in range(n_skilled):
        mu = round(0.08 + 0.10 * rng.random(), 4)
        sigma = round(0.12 + 0.10 * rng.random(), 4)
        soft_stop = round(0.04 + 0.02 * rng.random(), 4)
        hard_stop = round(soft_stop + 0.03 + 0.03 * rng.random(), 4)
        mus.append(mu)
        sigmas.append(sigma)
        skills.append(1)
        soft_stops.append(soft_stop)
        hard_stops.append(hard_stop)

    # 4 Unskilled pods: noise or negative drift (-4% to +3%), vol (14% to 25%)
    for _ in range(n_unskilled):
        mu = round(-0.04 + 0.07 * rng.random(), 4)
        sigma = round(0.14 + 0.11 * rng.random(), 4)
        soft_stop = round(0.04 + 0.02 * rng.random(), 4)
        hard_stop = round(soft_stop + 0.03 + 0.03 * rng.random(), 4)
        mus.append(mu)
        sigmas.append(sigma)
        skills.append(0)
        soft_stops.append(soft_stop)
        hard_stops.append(hard_stop)

    # Average pairwise correlation across pods (0.08 to 0.24)
    corr_rho = round(0.08 + 0.16 * rng.random(), 4)
    risk_free_rate = round(0.02 + 0.02 * rng.random(), 4)
    platform_budget_mdd = round(0.08 + 0.04 * rng.random(), 4)

    return {
        "seed": seed,
        "n_pods": n_pods,
        "mus": mus,
        "sigmas": sigmas,
        "skills": skills,
        "soft_stops": soft_stops,
        "hard_stops": hard_stops,
        "corr_rho": corr_rho,
        "n_days": 252,
        "t_years": 1.0,
        "risk_free_rate": risk_free_rate,
        "platform_budget_mdd": platform_budget_mdd,
    }
