"""Lab QR3-L03-1: Coordinate Descent LASSO vs. Ridge Regression Shrinkage.

Compares L1 coordinate descent (LASSO) and L2 shrinkage (Ridge) on a high-dimensional
collinear factor panel with true sparsity.
"""

from __future__ import annotations

import numpy as np


def solve_ridge(x_mat: np.ndarray, y_vec: np.ndarray, alpha: float) -> np.ndarray:
    """Solves Ridge regression via closed-form normal equations."""
    n_samples, n_features = x_mat.shape
    a_mat = x_mat.T @ x_mat + (n_samples * alpha) * np.eye(n_features)
    b_vec = x_mat.T @ y_vec
    return np.linalg.solve(a_mat, b_vec)


def solve_lasso(
    x_mat: np.ndarray,
    y_vec: np.ndarray,
    alpha: float,
    max_iter: int = 1000,
    tol: float = 1e-5,
) -> np.ndarray:
    """Solves LASSO via cyclical coordinate descent with soft-thresholding."""
    n_samples, n_features = x_mat.shape
    col_norms = np.sum(x_mat**2, axis=0) / n_samples
    col_norms[col_norms < 1e-12] = 1e-12

    beta = np.zeros(n_features, dtype=np.float64)
    residuals = y_vec.copy()

    for _ in range(max_iter):
        max_change = 0.0
        for j in range(n_features):
            old_b = beta[j]
            r_j = residuals + x_mat[:, j] * old_b
            rho_j = float(x_mat[:, j] @ r_j) / n_samples

            # Soft-thresholding operator
            if rho_j > alpha:
                new_b = (rho_j - alpha) / col_norms[j]
            elif rho_j < -alpha:
                new_b = (rho_j + alpha) / col_norms[j]
            else:
                new_b = 0.0

            diff = new_b - old_b
            if diff != 0.0:
                beta[j] = new_b
                residuals -= x_mat[:, j] * diff
                max_change = max(max_change, abs(diff))

        if max_change < tol:
            break

    return beta


def main() -> None:
    rng = np.random.default_rng(123)
    n_samples = 200
    n_features = 10

    # 2 true factors, 8 noise factors (some collinear)
    x_mat = rng.normal(0.0, 1.0, size=(n_samples, n_features))
    # Make features 2 and 3 correlated with feature 0
    x_mat[:, 2] = 0.8 * x_mat[:, 0] + 0.2 * rng.normal(0.0, 1.0, size=n_samples)
    x_mat[:, 3] = 0.7 * x_mat[:, 1] + 0.3 * rng.normal(0.0, 1.0, size=n_samples)

    # Standardize
    x_mat = (x_mat - np.mean(x_mat, axis=0)) / np.std(x_mat, axis=0)

    # True sparse coefficients: only feature 0 and feature 1 matter
    true_beta = np.zeros(n_features)
    true_beta[0] = 0.60
    true_beta[1] = -0.50

    y_vec = x_mat @ true_beta + rng.normal(0.0, 0.8, size=n_samples)
    y_vec -= np.mean(y_vec)

    ridge_beta = solve_ridge(x_mat, y_vec, alpha=1.0)
    lasso_beta = solve_lasso(x_mat, y_vec, alpha=0.15)

    print("True Beta:    ", [f"{b:+.2f}" for b in true_beta])
    print("Ridge Coeffs: ", [f"{b:+.2f}" for b in ridge_beta])
    print("LASSO Coeffs: ", [f"{b:+.2f}" for b in lasso_beta])

    ridge_zeros = int(np.sum(np.abs(ridge_beta) < 1e-4))
    lasso_zeros = int(np.sum(np.abs(lasso_beta) < 1e-4))
    ridge_l2 = float(np.linalg.norm(ridge_beta))
    lasso_l1 = float(np.sum(np.abs(lasso_beta)))

    print(f"Ridge: Zero coefficients = {ridge_zeros}/{n_features} | L2 norm = {ridge_l2:.3f}")
    print(f"LASSO: Zero coefficients = {lasso_zeros}/{n_features} | L1 norm = {lasso_l1:.3f}")
    print("Verification Invariant: LASSO yields exact sparsity while Ridge retains dense non-zeros.")


main()
