"""Lab 1 · Discrete Stripping, Forward Smirks & Implied Trees.

Implements forward implied volatility stripping across discrete maturities T1 < T2:
sigma_fwd^2(k) = (w(k, T2) - w(k, T1)) / (T2 - T1).
Demonstrates the flattening of forward skew under local volatility models,
a classic limitation compared to stochastic volatility dynamics.
All data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def svi_val(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    return a + b * (rho * diff + disc)


def main() -> None:
    t1 = 0.25
    t2 = 0.50
    t3 = 1.00

    # Calibrated term structure slices (SIMULATED)
    p1 = {"a": 0.015, "b": 0.080, "rho": -0.40, "m": 0.005, "sigma": 0.060}
    p2 = {"a": 0.030, "b": 0.115, "rho": -0.38, "m": 0.010, "sigma": 0.080}
    p3 = {"a": 0.060, "b": 0.165, "rho": -0.35, "m": 0.020, "sigma": 0.110}

    k_grid = [-0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30]

    print("Log-Moneyness (k) | Spot Vol T1 (0.25) | Spot Vol T2 (0.50) | Fwd Vol [0.25, 0.50] | Fwd Vol [0.50, 1.00]")
    print("-" * 105)

    spot_vols_t1: list[float] = []
    spot_vols_t2: list[float] = []
    fwd_vols_12: list[float] = []
    fwd_vols_23: list[float] = []

    for k in k_grid:
        w1 = svi_val(k, **p1)
        w2 = svi_val(k, **p2)
        w3 = svi_val(k, **p3)

        vol_t1 = math.sqrt(w1 / t1)
        vol_t2 = math.sqrt(w2 / t2)

        # Discrete forward variance: w_fwd = (w2 - w1) / (t2 - t1)
        var_fwd_12 = (w2 - w1) / (t2 - t1)
        var_fwd_23 = (w3 - w2) / (t3 - t2)

        vol_fwd_12 = math.sqrt(max(0.0, var_fwd_12))
        vol_fwd_23 = math.sqrt(max(0.0, var_fwd_23))

        spot_vols_t1.append(vol_t1)
        spot_vols_t2.append(vol_t2)
        fwd_vols_12.append(vol_fwd_12)
        fwd_vols_23.append(vol_fwd_23)

        print(f"{k:17.2f} | {vol_t1:18.4f} | {vol_t2:18.4f} | {vol_fwd_12:21.4f} | {vol_fwd_23:21.4f}")

    # Measure skew slope d(sigma) / dk around ATM (k in [-0.10, 0.10])
    idx_m = k_grid.index(-0.10)
    idx_p = k_grid.index(0.10)
    dk = k_grid[idx_p] - k_grid[idx_m]

    slope_spot_t1 = (spot_vols_t1[idx_p] - spot_vols_t1[idx_m]) / dk
    slope_fwd_12 = (fwd_vols_12[idx_p] - fwd_vols_12[idx_m]) / dk
    slope_fwd_23 = (fwd_vols_23[idx_p] - fwd_vols_23[idx_m]) / dk

    print("-" * 105)
    print(f"Spot ATM Skew Slope at T1=0.25:            {slope_spot_t1:.4f}")
    print(f"Forward ATM Skew Slope for [0.25, 0.50]:    {slope_fwd_12:.4f}")
    print(f"Forward ATM Skew Slope for [0.50, 1.00]:    {slope_fwd_23:.4f}")
    print("Forward Skew Flattens Across Distant Horizons:   ", abs(slope_fwd_23) < abs(slope_spot_t1))
    print("Forward Variances Are Strictly Positive (No Arb):", all(v > 0.0 for v in fwd_vols_12 + fwd_vols_23))


main()
