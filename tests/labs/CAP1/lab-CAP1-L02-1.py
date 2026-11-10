"""Lab 2: Specification curve generator and Shanken (1992) correction calculator."""

from __future__ import annotations

import numpy as np


def compute_shanken_adjustment(
    lambda_vec: np.ndarray,
    factor_cov: np.ndarray,
    naive_se: np.ndarray,
    t_obs: int,
) -> tuple[float, np.ndarray]:
    """Compute Shanken (1992) asymptotic correction factor for factor risk premia.

    Correction factor: c = 1 + lambda' * Sigma_f^(-1) * lambda
    Shanken SE = sqrt(naive_var * c + diag(Sigma_f) / T)
    """
    inv_factor_cov = np.linalg.pinv(factor_cov)
    quad_form = float(lambda_vec.T @ inv_factor_cov @ lambda_vec)
    shanken_factor = 1.0 + quad_form

    naive_var = naive_se**2
    shanken_var = naive_var * shanken_factor + np.diag(factor_cov) / float(t_obs)
    shanken_se = np.sqrt(shanken_var)
    return shanken_factor, shanken_se


def main() -> None:
    rng = np.random.default_rng(2026)
    t_obs = 360

    # 2 Factors: Market and Value
    f_returns = rng.multivariate_normal(mean=[0.006, 0.003], cov=[[0.0020, 0.0004], [0.0004, 0.0016]], size=t_obs)
    factor_cov = np.cov(f_returns, rowvar=False)

    # Estimated risk premia lambda (annualized ~ 7.2% and 3.6%)
    lambda_hat = np.array([0.0060, 0.0030])
    naive_se = np.array([0.0023, 0.0020])

    shanken_factor, shanken_se = compute_shanken_adjustment(lambda_hat, factor_cov, naive_se, t_obs)

    print("Shanken (1992) Factor Premium Inference:")
    print(f"  T = {t_obs} observations")
    print(f"  Quadratic form lambda' Sigma_f^(-1) lambda: {shanken_factor - 1.0:.4f}")
    print(f"  Shanken multiplicative factor (1 + q): {shanken_factor:.4f}")
    r0 = shanken_se[0] / naive_se[0]
    r1 = shanken_se[1] / naive_se[1]
    t0_naive = lambda_hat[0] / naive_se[0]
    t0_shanken = lambda_hat[0] / shanken_se[0]
    print(f"  Factor 1: Naive SE = {naive_se[0]:.5f} -> Shanken SE = {shanken_se[0]:.5f} (SE ratio = {r0:.2f})")
    print(f"  Factor 2: Naive SE = {naive_se[1]:.5f} -> Shanken SE = {shanken_se[1]:.5f} (SE ratio = {r1:.2f})")
    print(f"  Naive t-stat Factor 1: {t0_naive:.2f} -> Shanken t-stat: {t0_shanken:.2f}")


main()
