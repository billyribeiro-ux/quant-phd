"""Instance generator for DV6: Exotics, Structured Products & Dealer Hedging.

Generates deterministic market instances across seeds 0-49:
- Underlying asset spot, interest rate, dividend yield, and notional.
- Multi-period autocallable schedule (observation dates, autocall barriers, coupon barriers).
- Downside knock-in barrier with continuous or maturity-only monitoring.
- Parametric local volatility surface parameters (base volatility, skew, curvature).
- Analysis spot grid for dealer gamma exposure profiling.
All simulated data is labeled SIMULATED.
All dictionary values are numeric primitives or lists of numeric primitives for deterministic reproducibility.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    spot = round(95.0 + rng.random() * 15.0, 2)  # 95.0 to 110.0
    strike = spot  # At-the-money initial strike
    rate = round(0.02 + rng.random() * 0.03, 4)  # 2.0% to 5.0%
    div_yield = round(0.01 + rng.random() * 0.02, 4)  # 1.0% to 3.0%
    notional = 1000.0

    # Observation schedule: 4 semi-annual dates over 2 years
    observation_dates = [0.5, 1.0, 1.5, 2.0]
    n_obs = len(observation_dates)

    # Step-down autocall barrier schedule (e.g. 100%, 98%, 96%, 94% of spot)
    step_down = round(rng.random() * 0.02, 3)
    autocall_levels = [round(spot * (1.0 - i * step_down), 2) for i in range(n_obs)]

    # Coupon schedule: 2.0% to 3.5% per semi-annual period (4% to 7% annualized)
    coupon_rate = round(0.025 + rng.random() * 0.015, 4)
    coupon_barrier = round(spot * (0.75 + rng.random() * 0.05), 2)  # 75% to 80% of spot
    memory_coupon = True

    # Knock-in barrier: 60% to 70% of spot
    knock_in_barrier = round(spot * (0.60 + rng.random() * 0.08), 2)
    barrier_type = "continuous"

    # Parametric local volatility surface: sigma(S, t) = base / sqrt(1 + 0.5 t) * (1 - skew * tanh(m) + curvature * m^2)
    base_vol = round(0.18 + rng.random() * 0.08, 4)  # 18% to 26%
    skew = round(0.10 + rng.random() * 0.08, 4)  # 10% to 18%
    curvature = round(0.03 + rng.random() * 0.04, 4)  # 3% to 7%

    # Spot grid for dealer hedging profiling: from 50% spot to 130% spot
    spot_grid = [round(spot * factor, 2) for factor in [0.55, 0.62, 0.68, 0.75, 0.85, 0.95, 1.00, 1.05, 1.15, 1.25]]

    return {
        "spot": spot,
        "strike": strike,
        "rate": rate,
        "div_yield": div_yield,
        "notional": notional,
        "observation_dates": observation_dates,
        "autocall_levels": autocall_levels,
        "coupon_rate": coupon_rate,
        "coupon_barrier": coupon_barrier,
        "memory_coupon": memory_coupon,
        "knock_in_barrier": knock_in_barrier,
        "barrier_type": barrier_type,
        "base_vol": base_vol,
        "skew": skew,
        "curvature": curvature,
        "n_steps": 40,
        "spot_grid": spot_grid,
    }
