"""Lab F6-L05-1: Double Descent and the Virtue of Complexity in Asset Pricing.

Simulates random feature regressions across complexity ratios gamma = P / N in [0.25, 4.0].
Demonstrates the Kelly, Malamud & Zhou (2024) double descent phenomenon for ridgeless
minimum-norm interpolators and tests the Nagel (2025) critique on explicit regularization.
"""

from __future__ import annotations

import math

import numpy as np


def run_lab(seed: int = 42) -> dict[str, list[float]]:
    """Execute double-descent complexity sweep across parameter ratios."""
    rng = np.random.default_rng(seed)

    n_samples_train = 300
    n_samples_test = 300
    n_features_base = 8

    # Generate underlying predictive signals
    x_train = rng.normal(0.0, 1.0, size=(n_samples_train, n_features_base))
    x_test = rng.normal(0.0, 1.0, size=(n_samples_test, n_features_base))

    beta_sparse = np.zeros(n_features_base, dtype=np.float64)
    beta_sparse[:3] = np.array([0.030, -0.020, 0.020], dtype=np.float64)

    y_train = x_train @ beta_sparse + rng.normal(0.0, 0.050, size=n_samples_train)
    y_test = x_test @ beta_sparse + rng.normal(0.0, 0.050, size=n_samples_test)

    gammas = [0.25, 0.50, 0.90, 1.00, 1.50, 2.50, 4.00]
    ridgeless_mse: list[float] = []
    regularized_mse: list[float] = []

    for gamma in gammas:
        d_proj = max(2, int(gamma * n_samples_train))
        w_mat = rng.normal(0.0, 1.0 / math.sqrt(n_features_base), size=(n_features_base, d_proj))

        z_train = np.maximum(0.0, x_train @ w_mat)
        z_test = np.maximum(0.0, x_test @ w_mat)

        # 1. Ridgeless minimum-norm interpolator
        if d_proj <= n_samples_train:
            gram = z_train.T @ z_train + 1e-5 * np.eye(d_proj)
            beta_rl = np.linalg.solve(gram, z_train.T @ y_train)
        else:
            dual = z_train @ z_train.T + 1e-5 * np.eye(n_samples_train)
            alpha_dual = np.linalg.solve(dual, y_train)
            beta_rl = z_train.T @ alpha_dual

        pred_rl = z_test @ beta_rl
        mse_rl = float(np.mean((y_test - pred_rl) ** 2))
        ridgeless_mse.append(mse_rl)

        # 2. Explicitly regularized ridge estimator (optimal shrinkage per Nagel 2025)
        reg_penalty = 0.05 * n_samples_train
        gram_reg = z_train.T @ z_train + reg_penalty * np.eye(d_proj)
        beta_reg = np.linalg.solve(gram_reg, z_train.T @ y_train)
        pred_reg = z_test @ beta_reg
        mse_reg = float(np.mean((y_test - pred_reg) ** 2))
        regularized_mse.append(mse_reg)

    return {
        "gammas": gammas,
        "ridgeless_mse": ridgeless_mse,
        "regularized_mse": regularized_mse,
    }


def main() -> None:
    res = run_lab(seed=42)
    print("=== Lab F6-L05-1: Double Descent & Virtue of Complexity ===")
    for g, rl, reg in zip(res["gammas"], res["ridgeless_mse"], res["regularized_mse"], strict=True):
        print(f"gamma = {g:4.2f} | Ridgeless MSE: {rl:.5f} | Regularized Ridge MSE: {reg:.5f}")


main()
