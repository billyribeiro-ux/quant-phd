"""Lab FI1-L07-1: Nelson-Siegel and Svensson curve fitting and the nesting property.

SIMULATED: two-hump yield curve generated from known Svensson parameters.
Estimates parameters via variable projection (grid search over decay parameters
and linear least squares for beta coefficients).
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
    ns_part = ns_yield(tau, beta0, beta1, beta2, lam1)
    x2 = tau / lam2
    g2 = (1.0 - math.exp(-x2)) / x2
    return float(ns_part + beta3 * (g2 - math.exp(-x2)))


def fit_svensson(maturities: np.ndarray, yields: np.ndarray) -> tuple[float, float, float, float, float, float]:
    """Fit Svensson model parameters (beta0, beta1, beta2, beta3, lam1, lam2)."""
    best_ssr = float("inf")
    best_params = (0.0, 0.0, 0.0, 0.0, 1.0, 1.0)

    for l1 in SVENSSON_LAMBDA1_GRID:
        x1 = maturities / l1
        g1 = (1.0 - np.exp(-x1)) / x1
        col2 = g1 - np.exp(-x1)
        for l2 in SVENSSON_LAMBDA2_GRID:
            x2 = maturities / l2
            g2 = (1.0 - np.exp(-x2)) / x2
            col3 = g2 - np.exp(-x2)
            design = np.column_stack([np.ones_like(maturities), g1, col2, col3])
            c = np.linalg.lstsq(design, yields, rcond=None)[0]
            ssr = float(np.sum((yields - design @ c) ** 2))
            if ssr < best_ssr:
                best_ssr = ssr
                best_params = (float(c[0]), float(c[1]), float(c[2]), float(c[3]), l1, l2)

    return best_params


def main() -> None:
    # 1. Generating parameters (True curve)
    true_b0 = 0.060
    true_b1 = -0.030
    true_b2 = 0.020
    true_b3 = -0.015
    true_l1 = 1.5
    true_l2 = 5.0

    maturities = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0], dtype=np.float64)
    yields = np.array(
        [svensson_yield(tau, true_b0, true_b1, true_b2, true_b3, true_l1, true_l2) for tau in maturities],
        dtype=np.float64,
    )

    print("True Svensson Generating Parameters:")
    print(f"  beta0 = {true_b0:.4f} (asymptotic long-term rate)")
    print(f"  beta1 = {true_b1:.4f} (short-to-long spread)")
    print(f"  beta2 = {true_b2:.4f} (medium hump 1)")
    print(f"  beta3 = {true_b3:.4f} (medium hump 2)")
    print(f"  lam1  = {true_l1:.2f} yr, lam2 = {true_l2:.2f} yr")

    # 2. Fit Svensson model
    fit_b0, fit_b1, fit_b2, fit_b3, fit_l1, fit_l2 = fit_svensson(maturities, yields)
    print("\nRecovered Svensson Parameters:")
    print(f"  beta0 = {fit_b0:.6f} (recovered within 1e-6: {abs(fit_b0 - true_b0) < 1e-6})")
    print(f"  beta1 = {fit_b1:.6f} (recovered within 1e-6: {abs(fit_b1 - true_b1) < 1e-6})")
    print(f"  beta2 = {fit_b2:.6f} (recovered within 1e-6: {abs(fit_b2 - true_b2) < 1e-6})")
    print(f"  beta3 = {fit_b3:.6f} (recovered within 1e-6: {abs(fit_b3 - true_b3) < 1e-6})")
    print(f"  lam1  = {fit_l1:.2f} yr (exact match: {fit_l1 == true_l1})")
    print(f"  lam2  = {fit_l2:.2f} yr (exact match: {fit_l2 == true_l2})")

    assert abs(fit_b0 - true_b0) < 1e-4
    assert abs(fit_b1 - true_b1) < 1e-4
    assert abs(fit_b2 - true_b2) < 1e-4
    assert abs(fit_b3 - true_b3) < 1e-4

    # 3. Nesting Property Check: Svensson with beta3 = 0 identically equals Nelson-Siegel
    print("\nNesting Property Verification (beta3 = 0 => Svensson equals Nelson-Siegel):")
    max_nest_diff = 0.0
    for tau in maturities:
        sv_zero_b3 = svensson_yield(tau, true_b0, true_b1, true_b2, 0.0, true_l1, true_l2)
        ns_val = ns_yield(tau, true_b0, true_b1, true_b2, true_l1)
        diff = abs(sv_zero_b3 - ns_val)
        if diff > max_nest_diff:
            max_nest_diff = diff
    print(f"  Max absolute difference across all tenors < 1e-12: {max_nest_diff < 1e-12}")
    assert max_nest_diff < 1e-15
    print("Nesting identity proved: Svensson model nests Nelson-Siegel exactly.")


main()
