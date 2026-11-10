"""Instance generator for the FI3 term-premium and rates-RV autograder.

SIMULATED: generates synthetic zero-coupon yield panels, factor dynamics,
and relative-value curve trade specifications for testing the Atlas A13 contract.
Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = np.random.default_rng(seed)

    # 1. Base annual maturity grid (1y through 5y)
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    k = len(maturities)
    t_obs = 60  # 60 annual periods

    # 2. Simulate 3-factor VAR(1) state-space model for yields
    # Factors represent Level, Slope, Curvature
    phi_diag = np.array(
        [
            0.92 + 0.05 * rng.uniform(-1, 1),
            0.82 + 0.06 * rng.uniform(-1, 1),
            0.68 + 0.08 * rng.uniform(-1, 1),
        ],
        dtype=np.float64,
    )
    phi = np.diag(phi_diag)
    mu = np.array([0.045, -0.015, 0.005], dtype=np.float64) * (1.0 - phi_diag)

    # Innovation covariance
    sigma_v = np.diag([0.004, 0.006, 0.005]) ** 2
    l_v = np.linalg.cholesky(sigma_v)

    # Generate factors
    factors = np.zeros((t_obs, 3), dtype=np.float64)
    factors[0] = np.array([0.045, -0.015, 0.005], dtype=np.float64)
    for t in range(t_obs - 1):
        eps = rng.standard_normal(3)
        factors[t + 1] = mu + phi @ factors[t] + l_v @ eps

    # Factor loadings on yields: Level = 1, Slope = exp(-tau/2), Curvature = (tau/2)*exp(-tau/2)
    b_level = np.ones(k)
    b_slope = np.exp(-maturities / 2.5)
    b_curve = (maturities / 2.5) * np.exp(-maturities / 2.5)
    loadings = np.column_stack([b_level, b_slope, b_curve])

    # Intercept to ensure upward-sloping mean yield curve
    a_yields = 0.015 + 0.005 * np.log(maturities)
    yields = np.zeros((t_obs, k), dtype=np.float64)
    for t in range(t_obs):
        yields[t] = a_yields + loadings @ factors[t]

    # Clip to strictly positive realistic range (0.5% to 15%)
    yields = np.clip(yields, 0.005, 0.15)

    # 3. Carry and roll-down single curve instance
    base_curve = np.array([0.030, 0.036, 0.041, 0.045, 0.048], dtype=np.float64)
    curve_shift = rng.uniform(-0.005, 0.010, size=k)
    spot_curve = np.clip(base_curve + curve_shift, 0.010, 0.12)
    spot_maturities = maturities.copy()

    # 4. Relative-value curve trade instance
    trade_maturities = np.array([2.0, 5.0, 10.0], dtype=np.float64)
    # Butterfly weights (dollar-weighted -1, +2, -1)
    weights = np.array([-1.0, 2.0, -1.0], dtype=np.float64)
    yields_t0 = np.array([0.035, 0.042, 0.048], dtype=np.float64) + rng.uniform(-0.003, 0.003, size=3)
    # Curve movement: level shift + flattening/steepening
    delta_level = rng.uniform(-0.005, 0.005)
    delta_slope = rng.uniform(-0.004, 0.004)
    delta_curve = rng.uniform(-0.002, 0.002)
    delta_y = delta_level + np.array([-1.0, 0.0, 1.0]) * delta_slope + np.array([1.0, -2.0, 1.0]) * delta_curve
    yields_t1 = yields_t0 + delta_y

    financing_rate = float(np.clip(yields_t0[0] - 0.005, 0.01, 0.08))
    dt = float(rng.choice([0.25, 0.5, 1.0]))

    return {
        "seed": seed,
        "maturities": maturities.tolist(),
        "yields": yields.tolist(),
        "spot_maturities": spot_maturities.tolist(),
        "spot_curve": spot_curve.tolist(),
        "trade_maturities": trade_maturities.tolist(),
        "trade_weights": weights.tolist(),
        "trade_yields_t0": yields_t0.tolist(),
        "trade_yields_t1": yields_t1.tolist(),
        "financing_rate": financing_rate,
        "dt": dt,
    }
