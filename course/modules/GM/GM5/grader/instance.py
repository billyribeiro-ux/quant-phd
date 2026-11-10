"""Instance generator for GM5 project autograder.

Generates deterministic, per-seed balance sheet states, shock trajectories,
market depth parameters, and policy intervention thresholds for crisis simulation.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic synthetic crisis instance for seed.

    Parameters
    ----------
    seed : int
        RNG seed derived from learner workspace.

    Returns
    -------
    dict[str, Any]
        Instance dictionary containing initial balance sheets, market depth,
        exogenous shock paths, and backstop parameters.
    """
    rng = np.random.default_rng(seed)

    # Initial price and position
    p0 = float(100.0 + rng.uniform(-5.0, 10.0))
    q0 = float(1000.0 + rng.uniform(-100.0, 200.0))

    # Haircut requirement (10% to 15%)
    haircut0 = float(0.10 + rng.uniform(0.0, 0.05))

    # Debt sized to produce realistic high leverage (e.g., 6x to 9x initial leverage)
    asset_val = p0 * q0
    leverage_target = float(6.0 + rng.uniform(0.0, 2.5))
    equity0 = asset_val / leverage_target
    cash0 = float(0.05 * equity0)
    debt0 = float(asset_val + cash0 - equity0)

    # Exogenous negative fundamental shocks across 5 periods (e.g. -2% to -6% per round)
    n_steps = 5
    base_shocks = rng.uniform(-0.05, -0.015, size=n_steps)
    exogenous_shocks = [float(s) for s in base_shocks]

    # Market depth (Kyle's lambda) in range [0.002, 0.008]
    lambda_impact = float(0.003 + rng.uniform(0.0005, 0.004))

    # Haircut sensitivity to volatility in range [0.15, 0.35]
    haircut_sensitivity = float(0.20 + rng.uniform(0.0, 0.15))

    # Central bank policy backstop price floor (e.g., set at 75% of initial price)
    price_floor = float(p0 * (0.72 + rng.uniform(0.0, 0.06)))
    policy_enabled = True
    policy_price_floor = price_floor

    target_leverage = float(1.0 / haircut0)

    return {
        "seed": seed,
        "p0": p0,
        "q0": q0,
        "cash0": cash0,
        "debt0": debt0,
        "haircut0": haircut0,
        "exogenous_shocks": exogenous_shocks,
        "lambda_impact": lambda_impact,
        "haircut_sensitivity": haircut_sensitivity,
        "policy_enabled": policy_enabled,
        "policy_price_floor": policy_price_floor,
        "target_leverage": target_leverage,
    }
