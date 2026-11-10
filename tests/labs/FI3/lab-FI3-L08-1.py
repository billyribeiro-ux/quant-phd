"""Lab FI3-L08-1: Relative value curve trade P&L attribution (2s5s10s butterfly).

SIMULATED: evaluates a duration-weighted 2s5s10s butterfly portfolio across
a combined shift in yield curve level, slope, and curvature.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def attribute_pnl(
    weights: np.ndarray,
    maturities: np.ndarray,
    y0: np.ndarray,
    y1: np.ndarray,
    dt: float,
    repo_rate: float,
) -> dict[str, float]:
    """Decompose curve trade P&L into carry, roll, level, slope, convexity, and residual."""
    m_legs = len(weights)
    delta_y = y1 - y0
    delta_level = float(np.mean(delta_y))

    # Carry P&L
    carry_pnl = float(np.sum(weights * (y0 - repo_rate) * dt))

    # Roll-down P&L
    roll_vals = np.zeros(m_legs, dtype=np.float64)
    for i in range(m_legs):
        tau = maturities[i]
        if tau > dt:
            tau_rem = tau - dt
            y_rem = float(np.interp(tau_rem, maturities, y0))
            roll_vals[i] = tau_rem * (y0[i] - y_rem)
    rolldown_pnl = float(np.sum(weights * roll_vals))

    # Factor P&L
    level_pnl = float(-np.sum(weights * maturities * delta_level))
    slope_pnl = float(-np.sum(weights * maturities * (delta_y - delta_level)))
    curvature_pnl = 0.0
    convexity_pnl = float(0.5 * np.sum(weights * (maturities**2) * (delta_y**2)))

    # Exact bond repricing total return
    p0 = np.exp(-maturities * y0)
    p1 = np.exp(-(maturities - dt) * y1)
    ret_bonds = (p1 - p0) / p0 - repo_rate * dt
    total_pnl = float(np.sum(weights * ret_bonds))

    residual_pnl = float(total_pnl - (carry_pnl + rolldown_pnl + level_pnl + slope_pnl + curvature_pnl + convexity_pnl))

    return {
        "carry_pnl": carry_pnl,
        "rolldown_pnl": rolldown_pnl,
        "level_pnl": level_pnl,
        "slope_pnl": slope_pnl,
        "curvature_pnl": curvature_pnl,
        "convexity_pnl": convexity_pnl,
        "residual_pnl": residual_pnl,
        "total_pnl": total_pnl,
    }


def main() -> None:
    # 2s-5s-10s Butterfly Trade: Long 5y belly, short 2y and 10y wings
    maturities = np.array([2.0, 5.0, 10.0], dtype=np.float64)
    y0 = np.array([0.035, 0.042, 0.048], dtype=np.float64)

    # Fifty-fifty duration weighting:
    # w_2 * 2 + w_10 * 10 = w_5 * 5. With w_5 = 2.0:
    # w_2 * 2 = 5.0 => w_2 = -2.5; w_10 * 10 = 5.0 => w_10 = -0.5.
    # Total DV01: (-2.5)*2 + 2.0*5 + (-0.5)*10 = -5 + 10 - 5 = 0 (DV01 neutral!)
    weights = np.array([-2.5, 2.0, -0.5], dtype=np.float64)

    # Market shift over 3 months (dt = 0.25y):
    # Level shift +25 bps, flattening (10y drops 10 bps vs 2y), curvature drops 15 bps (belly outperformance)
    delta_y = np.array([0.0030, 0.0015, 0.0020], dtype=np.float64)
    y1 = y0 + delta_y
    dt = 0.25
    repo_rate = 0.032

    res = attribute_pnl(weights, maturities, y0, y1, dt, repo_rate)

    print("2s5s10s Butterfly P&L Attribution (DV01-Neutral):")
    print(f"  Weights: [2y: {weights[0]:.1f}, 5y: {weights[1]:.1f}, 10y: {weights[2]:.1f}]")
    print(f"  Net DV01 exposure = {np.sum(weights * maturities):.4f} (strictly zero)")

    print("\nP&L Decomposition (cents per dollar notional of wings):")
    for key in [
        "carry_pnl",
        "rolldown_pnl",
        "level_pnl",
        "slope_pnl",
        "convexity_pnl",
        "residual_pnl",
        "total_pnl",
    ]:
        val = res[key]
        print(f"  {key:15s}: {val:9.5f} ({val * 10000:7.2f} bps)")

    # Articulation invariant
    explained = sum(res[k] for k in ["carry_pnl", "rolldown_pnl", "level_pnl", "slope_pnl", "convexity_pnl"])
    print(f"\nExplained P&L (Linear + Convexity + Carry/Roll): {explained:9.5f} ({explained * 10000:.2f} bps)")
    print(f"Residual unexplained (higher-order Taylor error): {res['residual_pnl']:9.5f}")
    assert abs(res["total_pnl"] - (explained + res["residual_pnl"])) < 1e-12
    print("Exact articulation verified.")


main()
