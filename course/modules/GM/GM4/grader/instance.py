"""Instance generator for GM4: Macro Strategy Construction (Atlas A20)."""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for seed across 0-49."""
    rng = np.random.default_rng(seed)

    # Yield curve / DV01 parameters
    dv01_1 = float(35.0 + rng.uniform(5.0, 20.0))
    dv01_2 = float(75.0 + rng.uniform(10.0, 30.0))
    notional_1 = float(10_000_000.0 + rng.integers(1, 10) * 1_000_000.0)

    # Carry and roll-down
    spot_yield = float(0.038 + rng.uniform(0.005, 0.020))
    duration = float(6.5 + rng.uniform(0.5, 3.0))
    roll_down_bps = float(12.0 + rng.uniform(2.0, 15.0))
    repo_rate = float(0.032 + rng.uniform(0.002, 0.015))
    horizon_years = float(rng.choice([0.25, 0.50, 1.0]))

    # Options expression parameters
    spot = float(100.0 + rng.uniform(-10.0, 25.0))
    strikes = np.array([spot * 0.95, spot * 1.0, spot * 1.05], dtype=np.float64)
    vols = np.array([0.22, 0.20, 0.24], dtype=np.float64)
    expiry = float(0.5 + rng.uniform(0.1, 0.5))
    rate = float(0.040 + rng.uniform(0.005, 0.015))
    weights = np.array([-1.0, 2.0, -1.0], dtype=np.float64)  # Butterfly structure
    is_call = np.array([1, 1, 1], dtype=int)

    # Kelly sizing parameters
    mu = float(0.05 + rng.uniform(0.01, 0.08))
    var = float(0.025 + rng.uniform(0.005, 0.020))
    fraction = 0.25
    max_leverage = 4.0

    # Macro view
    view_move_bps = float(20.0 + rng.uniform(5.0, 30.0))
    confidence = float(0.65 + rng.uniform(0.05, 0.25))

    # Scenario grid parameters
    spot_shocks = np.array([-0.10, -0.05, 0.0, 0.05, 0.10], dtype=np.float64)
    vol_shocks = np.array([-0.04, -0.02, 0.0, 0.02, 0.04], dtype=np.float64)

    # Discrete P&L distribution for asymmetry calculation
    raw_pnl = rng.normal(0.02, 0.08, size=1000)
    pnl_dist = np.ascontiguousarray(raw_pnl, dtype=np.float64)

    return {
        "seed": seed,
        "dv01_1": dv01_1,
        "dv01_2": dv01_2,
        "notional_1": notional_1,
        "spot_yield": spot_yield,
        "duration": duration,
        "roll_down_bps": roll_down_bps,
        "repo_rate": repo_rate,
        "horizon_years": horizon_years,
        "opt_spot": spot,
        "opt_strikes": strikes,
        "opt_vols": vols,
        "opt_expiry": expiry,
        "opt_rate": rate,
        "opt_weights": weights,
        "opt_is_call": is_call,
        "kelly_mu": mu,
        "kelly_var": var,
        "kelly_fraction": fraction,
        "kelly_max_leverage": max_leverage,
        "scen_spot_shocks": spot_shocks,
        "scen_vol_shocks": vol_shocks,
        "pnl_dist": pnl_dist,
        "view_id": f"VIEW-{seed:03d}",
        "view_type": "curve_steepener",
        "view_expected_move_bps": view_move_bps,
        "view_confidence": confidence,
        "view_horizon_days": int(horizon_years * 365),
    }
