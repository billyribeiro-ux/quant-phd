"""Lab FI1-L08-1: Comparison of curve construction methods and the GSW specification.

SIMULATED: synthetic coupon Treasury bonds across maturities from 1 to 30 years.
Honest-pending note: official published GSW parameter time series are pending Board licence
redistribution clearance under Phase 2 Architect Ruling 5.
NumPy and standard library only; no network.
"""

from __future__ import annotations

import math

import numpy as np

NS_LAMBDA_GRID: tuple[float, ...] = tuple(float(x) * 0.25 for x in range(2, 41))
SVENSSON_LAMBDA1_GRID: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 3.0, 5.0)
SVENSSON_LAMBDA2_GRID: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0, 8.0, 12.0)


def ns_yield(tau: float, beta0: float, beta1: float, beta2: float, lam: float) -> float:
    """Continuous zero yield in Nelson-Siegel model."""
    x = tau / lam
    g = (1.0 - math.exp(-x)) / x
    return float(beta0 + beta1 * g + beta2 * (g - math.exp(-x)))


def svensson_yield(
    tau: float,
    beta0: float,
    beta1: float,
    beta2: float,
    beta3: float,
    lam1: float,
    lam2: float,
) -> float:
    """Continuous zero yield in Svensson extension."""
    ns_val = ns_yield(tau, beta0, beta1, beta2, lam1)
    x2 = tau / lam2
    g2 = (1.0 - math.exp(-x2)) / x2
    return float(ns_val + beta3 * (g2 - math.exp(-x2)))


def fit_ns(taus: np.ndarray, yields: np.ndarray) -> tuple[float, float, float, float]:
    best_ssr = float("inf")
    best_params = (0.0, 0.0, 0.0, 1.0)
    for lam in NS_LAMBDA_GRID:
        x = taus / lam
        g = (1.0 - np.exp(-x)) / x
        col2 = g - np.exp(-x)
        design = np.column_stack([np.ones_like(taus), g, col2])
        c = np.linalg.lstsq(design, yields, rcond=None)[0]
        ssr = float(np.sum((yields - design @ c) ** 2))
        if ssr < best_ssr:
            best_ssr = ssr
            best_params = (float(c[0]), float(c[1]), float(c[2]), lam)
    return best_params


def fit_sv(taus: np.ndarray, yields: np.ndarray) -> tuple[float, float, float, float, float, float]:
    best_ssr = float("inf")
    best_params = (0.0, 0.0, 0.0, 0.0, 1.0, 1.0)
    for l1 in SVENSSON_LAMBDA1_GRID:
        x1 = taus / l1
        g1 = (1.0 - np.exp(-x1)) / x1
        col2 = g1 - np.exp(-x1)
        for l2 in SVENSSON_LAMBDA2_GRID:
            x2 = taus / l2
            g2 = (1.0 - np.exp(-x2)) / x2
            col3 = g2 - np.exp(-x2)
            design = np.column_stack([np.ones_like(taus), g1, col2, col3])
            c = np.linalg.lstsq(design, yields, rcond=None)[0]
            ssr = float(np.sum((yields - design @ c) ** 2))
            if ssr < best_ssr:
                best_ssr = ssr
                best_params = (float(c[0]), float(c[1]), float(c[2]), float(c[3]), l1, l2)
    return best_params


def main() -> None:
    # 1. Market yields on 10 Treasury coupon bonds (0.5 to 30 years)
    # Generated from a two-hump term structure with small market noise
    maturities = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0], dtype=np.float64)

    # Underlying GSW / Svensson parameters + market noise
    b0_true, b1_true, b2_true, b3_true = 0.055, -0.025, 0.025, -0.018
    l1_true, l2_true = 1.5, 5.0
    true_curve = np.array([svensson_yield(t, b0_true, b1_true, b2_true, b3_true, l1_true, l2_true) for t in maturities])

    # Add realistic market noise (e.g. microstructure, liquidity premia)
    noise_bps = np.array([1.2, -0.8, 1.5, -1.0, 0.5, -0.7, 0.9, -1.2, 0.6, -0.4])  # in basis points
    market_yields = true_curve + noise_bps * 1e-4

    print("Market Yield Observations (SIMULATED Treasury Curve):")
    for t, y in zip(maturities, market_yields, strict=True):
        print(f"  Maturity = {t:4.1f} yr: Yield = {y:.4%}")

    # 2. Fit Nelson-Siegel model (4 parameters)
    ns_b0, ns_b1, ns_b2, ns_lam = fit_ns(maturities, market_yields)
    ns_fitted = np.array([ns_yield(t, ns_b0, ns_b1, ns_b2, ns_lam) for t in maturities])
    ns_rmse_bps = float(np.sqrt(np.mean((market_yields - ns_fitted) ** 2))) * 10_000

    # 3. Fit Svensson model (6 parameters, GSW specification)
    sv_b0, sv_b1, sv_b2, sv_b3, sv_l1, sv_l2 = fit_sv(maturities, market_yields)
    sv_fitted = np.array([svensson_yield(t, sv_b0, sv_b1, sv_b2, sv_b3, sv_l1, sv_l2) for t in maturities])
    sv_rmse_bps = float(np.sqrt(np.mean((market_yields - sv_fitted) ** 2))) * 10_000

    print("\nModel Fitting Summary:")
    print("Nelson-Siegel (4 params):")
    print(f"  beta0 = {ns_b0:.4f}, beta1 = {ns_b1:.4f}, beta2 = {ns_b2:.4f}, lam = {ns_lam:.2f}")
    print(f"  RMSE Pricing Error = {ns_rmse_bps:.2f} bps")

    print("\nSvensson / GSW (6 params):")
    print(
        f"  beta0 = {sv_b0:.4f}, beta1 = {sv_b1:.4f}, beta2 = {sv_b2:.4f}, beta3 = {sv_b3:.4f},"
        f" lam1 = {sv_l1:.2f}, lam2 = {sv_l2:.2f}"
    )
    print(f"  RMSE Pricing Error = {sv_rmse_bps:.2f} bps")

    # 4. Comparative evaluation
    print(f"\nSvensson error reduction over Nelson-Siegel: {ns_rmse_bps - sv_rmse_bps:.2f} bps")
    assert sv_rmse_bps < ns_rmse_bps
    print("GSW Svensson specification achieves superior fit on complex multi-hump curves.")


main()
