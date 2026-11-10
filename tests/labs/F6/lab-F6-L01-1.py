"""Lab F6-L01-1: Ridge vs. OLS Out-of-Sample R-squared in Low S/N Panels.

Compares unpenalized OLS against L2-regularized Ridge regression in high-dimensional
cross-sectional return prediction panels with low signal-to-noise ratio.
Demonstrates the Gu, Kelly & Xiu (2020) zero-benchmark R2_OOS.
"""

from __future__ import annotations

import math

import numpy as np


def run_lab(seed: int = 42) -> dict[str, float]:
    """Execute OLS vs. Ridge comparison on a simulated cross-sectional panel."""
    rng = np.random.default_rng(seed)

    n_assets = 30
    t_train = 24
    t_test = 24
    n_features = 35

    m_train = n_assets * t_train
    m_test = n_assets * t_test

    true_beta = np.zeros(n_features, dtype=np.float64)
    true_beta[:5] = np.array([0.030, -0.025, 0.020, -0.015, 0.010], dtype=np.float64)

    x_train = rng.normal(0.0, 1.0, size=(m_train, n_features))
    for p in range(n_features):
        x_train[:, p] = (np.argsort(np.argsort(x_train[:, p])) / (m_train - 1)) - 0.5

    x_test = rng.normal(0.0, 1.0, size=(m_test, n_features))
    for p in range(n_features):
        x_test[:, p] = (np.argsort(np.argsort(x_test[:, p])) / (m_test - 1)) - 0.5

    y_train = x_train @ true_beta + rng.normal(0.0, 0.075, size=m_train)
    y_test = x_test @ true_beta + rng.normal(0.0, 0.075, size=m_test)

    # 1. Unregularized OLS
    ols_beta = np.linalg.solve(x_train.T @ x_train, x_train.T @ y_train)
    pred_ols = x_test @ ols_beta

    # 2. L2 Penalized Ridge Regression (alpha = 0.25)
    ridge_alpha = 0.25
    ridge_beta = np.linalg.solve(
        x_train.T @ x_train + (m_train * ridge_alpha) * np.eye(n_features),
        x_train.T @ y_train,
    )
    pred_ridge = x_test @ ridge_beta

    # Compute out-of-sample R2 with zero return benchmark (Gu, Kelly, Xiu 2020)
    denom_zero = float(np.sum(y_test**2))
    r2_ols = float(1.0 - np.sum((y_test - pred_ols) ** 2) / denom_zero)
    r2_ridge = float(1.0 - np.sum((y_test - pred_ridge) ** 2) / denom_zero)

    # Evaluate long-short spread portfolio returns on test panel
    y_test_panel = y_test.reshape(t_test, n_assets).T
    pred_ols_panel = pred_ols.reshape(t_test, n_assets).T
    pred_ridge_panel = pred_ridge.reshape(t_test, n_assets).T

    k_quant = max(1, n_assets // 3)
    ols_spreads = np.zeros(t_test)
    ridge_spreads = np.zeros(t_test)

    for t in range(t_test):
        ord_ols = np.argsort(pred_ols_panel[:, t])
        ols_spreads[t] = np.mean(y_test_panel[ord_ols[-k_quant:], t]) - np.mean(y_test_panel[ord_ols[:k_quant], t])

        ord_ridge = np.argsort(pred_ridge_panel[:, t])
        ridge_spreads[t] = np.mean(y_test_panel[ord_ridge[-k_quant:], t]) - np.mean(
            y_test_panel[ord_ridge[:k_quant], t]
        )

    sharpe_ols = float(math.sqrt(12.0) * np.mean(ols_spreads) / np.std(ols_spreads, ddof=1))
    sharpe_ridge = float(math.sqrt(12.0) * np.mean(ridge_spreads) / np.std(ridge_spreads, ddof=1))

    return {
        "r2_ols_pct": r2_ols * 100.0,
        "r2_ridge_pct": r2_ridge * 100.0,
        "sharpe_ols": sharpe_ols,
        "sharpe_ridge": sharpe_ridge,
    }


def main() -> None:
    results = run_lab(seed=42)
    print("=== Lab F6-L01-1: Ridge vs. OLS Out-of-Sample Performance ===")
    print(f"OLS Out-of-Sample R2 (%):    {results['r2_ols_pct']:.4f}")
    print(f"Ridge Out-of-Sample R2 (%):  {results['r2_ridge_pct']:.4f}")
    print(f"OLS Spread Annual Sharpe:   {results['sharpe_ols']:.4f}")
    print(f"Ridge Spread Annual Sharpe: {results['sharpe_ridge']:.4f}")


main()
