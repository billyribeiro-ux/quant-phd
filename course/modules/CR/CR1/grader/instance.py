"""Instance generator for the CR1 credit module autograder.

SIMULATED: generates synthetic firm asset parameters, debt structures, hazard rates,
and market spread observations for testing the Atlas A14 credit engine.
Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = np.random.default_rng(seed)

    # 1. Firm asset and debt parameters for structural pricing
    asset_value = float(80.0 + rng.uniform(20.0, 100.0))
    debt_face = float(50.0 + rng.uniform(10.0, 40.0))
    maturity = float(rng.choice([1.0, 2.0, 3.0, 5.0, 7.0, 10.0]))
    risk_free_rate = float(0.02 + rng.uniform(0.01, 0.04))
    asset_volatility = float(0.15 + rng.uniform(0.05, 0.25))

    # 2. Black-Cox barrier and recovery
    # Barrier K must be <= debt_face and < asset_value
    barrier = float(min(debt_face * rng.uniform(0.6, 0.95), asset_value * 0.9))
    recovery_rate = float(rng.choice([0.3, 0.4, 0.5, 0.6]))

    # 3. Reduced-form parameters
    hazard_rate = float(0.005 + rng.uniform(0.005, 0.05))

    # 4. KMV / Distance to default observables
    equity_value = float(30.0 + rng.uniform(10.0, 50.0))
    equity_volatility = float(0.25 + rng.uniform(0.10, 0.35))
    expected_return = float(0.06 + rng.uniform(0.02, 0.08))

    # 5. Market spread decomposition parameters
    market_spread = float(0.0080 + rng.uniform(0.0040, 0.0250))
    default_prob = float(0.0020 + rng.uniform(0.0010, 0.0150))
    risk_premium_ratio = float(0.40 + rng.uniform(0.10, 0.50))

    return {
        "asset_value": asset_value,
        "debt_face": debt_face,
        "maturity": maturity,
        "risk_free_rate": risk_free_rate,
        "asset_volatility": asset_volatility,
        "barrier": barrier,
        "recovery_rate": recovery_rate,
        "hazard_rate": hazard_rate,
        "equity_value": equity_value,
        "equity_volatility": equity_volatility,
        "expected_return": expected_return,
        "market_spread": market_spread,
        "default_prob": default_prob,
        "risk_premium_ratio": risk_premium_ratio,
    }
