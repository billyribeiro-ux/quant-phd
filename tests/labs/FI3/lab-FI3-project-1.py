"""Lab FI3-project-1 (Rung 1, Worked Example): Fully solved term-premium and rates-RV workflow.

SIMULATED: 5-year Treasury yield panel demonstrating the complete Atlas A13 pipeline:
forward rates, excess returns, Cochrane-Piazzesi factor, carry and roll-down,
and relative-value curve trade P&L attribution.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 1. Yield panel (T = 5 observations, K = 5 maturities)
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    yields = np.array(
        [
            [0.030, 0.035, 0.040, 0.044, 0.047],
            [0.032, 0.036, 0.041, 0.045, 0.048],
            [0.029, 0.034, 0.039, 0.043, 0.046],
            [0.033, 0.038, 0.042, 0.046, 0.049],
            [0.035, 0.040, 0.044, 0.047, 0.050],
        ],
        dtype=np.float64,
    )

    print("Step 1 · Discrete 1-Year Forward Rates f_t^{(n-1, n)}:")
    fwd = np.empty_like(yields)
    fwd[:, 0] = yields[:, 0]
    for k in range(1, 5):
        fwd[:, k] = (maturities[k] * yields[:, k] - maturities[k - 1] * yields[:, k - 1]) / (
            maturities[k] - maturities[k - 1]
        )
    print("  Initial forward curve (t=0):", np.round(fwd[0], 4))

    print("\nStep 2 · 1-Year Holding Period Excess Returns rx_{t+1}^{(n)}:")
    rx = np.empty((4, 4), dtype=np.float64)
    for k in range(1, 5):
        n = maturities[k]
        rx[:, k - 1] = -(n - 1.0) * yields[1:, k - 1] + n * yields[:-1, k] - yields[:-1, 0]
    print("  Excess return matrix (T-1 x K-1):")
    for row in rx:
        print("    " + "  ".join(f"{val:7.4f}" for val in row))

    print("\nStep 3 · Carry & Roll-Down on Initial Curve (1-Year Horizon):")
    spot_0 = yields[0]
    carry = 1.0 * spot_0
    roll = np.zeros(5, dtype=np.float64)
    for i in range(1, 5):
        tau_rem = maturities[i] - 1.0
        y_rem = float(np.interp(tau_rem, maturities, spot_0))
        roll[i] = tau_rem * (spot_0[i] - y_rem)
    total_cr = carry + roll
    for i, m in enumerate(maturities):
        print(f"  {m:.0f}y: Carry = {carry[i]:.4%}, Roll = {roll[i]:.4%}, Total = {total_cr[i]:.4%}")

    print("\nStep 4 · 2s10s Flattener P&L Attribution:")
    # 2s10s Flattener: Long 2y (weight +5.0), Short 10y (weight -1.0) -> DV01 neutral
    w = np.array([5.0, -1.0])
    m_trade = np.array([2.0, 10.0])
    y_t0 = np.array([0.035, 0.047])
    # 10y yield drops 20 bps, 2y yield drops 5 bps (flattening)
    y_t1 = np.array([0.0345, 0.0450])
    dt = 0.25
    repo = 0.030

    dy = y_t1 - y_t0
    d_level = float(np.mean(dy))
    carry_pnl = float(np.sum(w * (y_t0 - repo) * dt))
    level_pnl = float(-np.sum(w * m_trade * d_level))
    slope_pnl = float(-np.sum(w * m_trade * (dy - d_level)))
    convexity_pnl = float(0.5 * np.sum(w * (m_trade**2) * (dy**2)))

    p0 = np.exp(-m_trade * y_t0)
    p1 = np.exp(-(m_trade - dt) * y_t1)
    ret_bonds = (p1 - p0) / p0 - repo * dt
    total_pnl = float(np.sum(w * ret_bonds))

    print(f"  Carry P&L     = {carry_pnl:.5f} ({carry_pnl * 10000:.1f} bps)")
    print(f"  Level P&L     = {level_pnl:.5f} ({level_pnl * 10000:.1f} bps)")
    print(f"  Slope P&L     = {slope_pnl:.5f} ({slope_pnl * 10000:.1f} bps)")
    print(f"  Convexity P&L = {convexity_pnl:.5f} ({convexity_pnl * 10000:.1f} bps)")
    print(f"  Total P&L     = {total_pnl:.5f} ({total_pnl * 10000:.1f} bps)")


main()
