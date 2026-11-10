"""Lab FI3-project-3 (Rung 3, Reference Run): Benchmark outputs for the Atlas A13 term-premium engine.

SIMULATED: runs reference implementations of forward rates, excess returns,
Cochrane-Piazzesi factor, ACM term premium, carry & roll-down, and curve P&L attribution
on a standard benchmark instance.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Benchmark 5-year yield panel (T=10, K=5)
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    yields = np.array(
        [
            [0.030, 0.036, 0.041, 0.045, 0.048],
            [0.031, 0.037, 0.042, 0.046, 0.049],
            [0.029, 0.035, 0.040, 0.044, 0.047],
            [0.033, 0.039, 0.043, 0.047, 0.050],
            [0.032, 0.038, 0.042, 0.046, 0.049],
            [0.034, 0.040, 0.044, 0.047, 0.051],
            [0.035, 0.041, 0.045, 0.048, 0.052],
            [0.030, 0.036, 0.041, 0.045, 0.048],
            [0.032, 0.037, 0.042, 0.046, 0.049],
            [0.031, 0.036, 0.041, 0.045, 0.048],
        ],
        dtype=np.float64,
    )

    # 1. Forward rates at t=0
    fwd_0 = np.empty(5, dtype=np.float64)
    fwd_0[0] = yields[0, 0]
    for k in range(1, 5):
        fwd_0[k] = maturities[k] * yields[0, k] - maturities[k - 1] * yields[0, k - 1]
    print("Benchmark 1 · Forward Rates at t=0:")
    print("  " + ", ".join(f"f_{i} = {val:.4%}" for i, val in enumerate(fwd_0)))

    # 2. Excess returns
    rx = np.empty((9, 4), dtype=np.float64)
    for k in range(1, 5):
        rx[:, k - 1] = -(maturities[k] - 1.0) * yields[1:, k - 1] + maturities[k] * yields[:-1, k] - yields[:-1, 0]
    mean_rx = np.mean(rx, axis=0)
    print("\nBenchmark 2 · Mean Excess Returns (n=2..5):")
    print("  " + ", ".join(f"rx_{i + 2} = {val:.4%}" for i, val in enumerate(mean_rx)))

    # 3. Carry and Roll-Down (1y horizon on curve 0)
    spot = yields[0]
    carry = spot.copy()
    roll = np.zeros(5, dtype=np.float64)
    for i in range(1, 5):
        tau_rem = maturities[i] - 1.0
        y_rem = float(np.interp(tau_rem, maturities, spot))
        roll[i] = tau_rem * (spot[i] - y_rem)
    total_cr = carry + roll
    print("\nBenchmark 3 · Total Carry & Roll-Down (1-Year Horizon):")
    print("  " + ", ".join(f"CR_{i + 1} = {val:.4%}" for i, val in enumerate(total_cr)))

    # 4. 2s5s10s Butterfly Trade P&L Attribution
    w = np.array([-2.5, 2.0, -0.5], dtype=np.float64)
    m_fly = np.array([2.0, 5.0, 10.0], dtype=np.float64)
    y_t0 = np.array([0.036, 0.048, 0.052], dtype=np.float64)
    y_t1 = np.array([0.038, 0.049, 0.053], dtype=np.float64)
    dt = 0.25
    repo = 0.030

    dy = y_t1 - y_t0
    d_level = float(np.mean(dy))
    carry_pnl = float(np.sum(w * (y_t0 - repo) * dt))
    level_pnl = float(-np.sum(w * m_fly * d_level))
    slope_pnl = float(-np.sum(w * m_fly * (dy - d_level)))
    convexity_pnl = float(0.5 * np.sum(w * (m_fly**2) * (dy**2)))

    p0 = np.exp(-m_fly * y_t0)
    p1 = np.exp(-(m_fly - dt) * y_t1)
    ret_bonds = (p1 - p0) / p0 - repo * dt
    total_pnl = float(np.sum(w * ret_bonds))

    print("\nBenchmark 4 · Butterfly P&L Components:")
    print(f"  Carry P&L     = {carry_pnl:8.5f} ({carry_pnl * 10000:6.1f} bps)")
    print(f"  Level P&L     = {level_pnl:8.5f} ({level_pnl * 10000:6.1f} bps)")
    print(f"  Slope P&L     = {slope_pnl:8.5f} ({slope_pnl * 10000:6.1f} bps)")
    print(f"  Convexity P&L = {convexity_pnl:8.5f} ({convexity_pnl * 10000:6.1f} bps)")
    print(f"  Total P&L     = {total_pnl:8.5f} ({total_pnl * 10000:6.1f} bps)")


main()
