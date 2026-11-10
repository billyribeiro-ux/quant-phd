"""Lab F4-project-2: Project Rung 2 Completion Problem - Crash-Risk Dynamic Overlay.

Completed reference twin for the Project Rung 2 completion exercise. Implements
Daniel & Moskowitz (2016) panic state detection and crash-risk overlay exposure
adjustment to truncate tail losses during market rebounds.
"""

from __future__ import annotations

import numpy as np


def identify_panic_states(
    market_returns: np.ndarray,
    lookback_months: int = 24,
) -> np.ndarray:
    """Identify panic / bear market states (trailing cumulative market return < 0)."""
    t_len = len(market_returns)
    panic = np.zeros(t_len, dtype=bool)
    for t in range(lookback_months, t_len):
        if np.sum(market_returns[t - lookback_months : t]) < 0.0:
            panic[t] = True
    return panic


def apply_crash_overlay(
    vol_scaled_weights: np.ndarray,
    panic_states: np.ndarray,
    panic_multiplier: float = 0.20,
) -> np.ndarray:
    """Scale down exposure during panic states to eliminate rebound crash optionality."""
    dynamic_weights = vol_scaled_weights.copy()
    dynamic_weights[panic_states] *= panic_multiplier
    return dynamic_weights


def main() -> None:
    rng = np.random.default_rng(456)
    n_months = 120

    # Simulate market returns with a crisis at months 40..60 and rebound at 61..64
    mkt = rng.normal(0.007, 0.04, size=n_months)
    mkt[40:61] = -0.04 + rng.normal(0.0, 0.02, size=21)
    mkt[61:65] = 0.12  # explosive rebound

    # WML raw returns: positive drift, severe crash during rebound
    wml = rng.normal(0.008, 0.04, size=n_months)
    wml[61:65] = -0.25  # short squeeze on loser leg

    # Base vol-scaled weights
    vol_weights = np.ones(n_months) * 1.50

    # Apply panic overlay
    panic = identify_panic_states(mkt, lookback_months=24)
    dm_weights = apply_crash_overlay(vol_weights, panic, panic_multiplier=0.20)

    # Returns during the rebound months (61..64)
    rebound_ret_vol = np.sum(vol_weights[61:65] * wml[61:65])
    rebound_ret_dm = np.sum(dm_weights[61:65] * wml[61:65])

    print("=== PROJECT RUNG 2: CRASH OVERLAY COMPLETION TWIN ===")
    print(f"Total Panic Months Detected: {int(np.sum(panic))}")
    print(f"Rebound Gross Loss (Vol-Scaled): {rebound_ret_vol:+.2%}")
    print(f"Rebound Gross Loss (Dynamic DM): {rebound_ret_dm:+.2%}")
    print(f"Capital Saved by Overlay:       {rebound_ret_dm - rebound_ret_vol:+.2%}")


main()
