"""Lab CAP3-project-1 (Completion Solution): Shanken Correction & Taylor Determinacy."""

from __future__ import annotations

import numpy as np


def compute_shanken_adjustment(risk_premia: np.ndarray, factor_cov: np.ndarray) -> float:
    """Compute the quadratic Shanken correction factor c_shanken = 1 + lambda' Sigma_f^{-1} lambda."""
    inv_factor_cov = np.linalg.inv(factor_cov)
    quadratic_term = float(risk_premia @ inv_factor_cov @ risk_premia)
    c_shanken = 1.0 + quadratic_term
    return c_shanken


def evaluate_new_keynesian_determinacy(
    phi_pi: float,
    phi_y: float,
    beta: float,
    kappa: float,
) -> tuple[float, bool]:
    """Evaluate the Taylor principle determinacy condition phi_pi + ((1 - beta)/kappa) * phi_y > 1.0."""
    slope_ratio = (1.0 - beta) / kappa
    taylor_metric = phi_pi + slope_ratio * phi_y
    is_determinate = bool(taylor_metric > 1.0)
    return taylor_metric, is_determinate


def main() -> None:
    # 1. Shanken adjustment test case
    lambdas = np.array([0.008, 0.004])
    f_cov = np.array([[0.0025, 0.0005], [0.0005, 0.0016]])
    shanken_factor = compute_shanken_adjustment(lambdas, f_cov)

    # 2. Taylor principle determinacy test case
    beta_val = 0.99
    kappa_val = 0.12
    metric, determinate = evaluate_new_keynesian_determinacy(1.5, 0.5, beta_val, kappa_val)

    print(f"Shanken Correction Factor: {shanken_factor:.4f}")
    print(f"Taylor Determinacy Metric: {metric:.4f}")
    print(f"System Is Determinate: {determinate}")


main()
