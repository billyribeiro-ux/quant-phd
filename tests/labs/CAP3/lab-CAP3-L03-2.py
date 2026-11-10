"""Lab CAP3-L03-2: Field Prelim II, Problem B: Fama-MacBeth & Shanken Correction.

Performs two-pass cross-sectional regression, computes the Shanken (1992)
asymptotic standard error adjustment, and evaluates the GRS (1989) test statistic.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(202)
    t_obs = 180
    n_assets = 5
    n_factors = 2

    # Simulate factor series and test assets
    factor_means = np.array([0.007, 0.003])
    factor_cov = np.array([[0.0020, 0.0004], [0.0004, 0.0016]])
    factors = np.random.multivariate_normal(factor_means, factor_cov, size=t_obs)

    true_betas = np.array([[0.8, -0.1], [1.1, 0.3], [0.9, 0.0], [1.2, -0.2], [0.7, 0.4]])
    true_alphas = np.array([0.001, -0.001, 0.0005, 0.002, -0.0015])
    noise = np.random.normal(0.0, 0.02, size=(t_obs, n_assets))
    returns = np.zeros((t_obs, n_assets))
    for t in range(t_obs):
        returns[t] = true_alphas + true_betas @ factors[t] + noise[t]

    # Pass 1: Time-series OLS to estimate factor loadings
    x_mat = np.column_stack([np.ones(t_obs), factors])
    x_inv = np.linalg.inv(x_mat.T @ x_mat)
    alphas = np.zeros(n_assets)
    betas = np.zeros((n_assets, n_factors))
    residuals = np.zeros((t_obs, n_assets))

    for i in range(n_assets):
        y = returns[:, i]
        coeff = x_inv @ (x_mat.T @ y)
        alphas[i] = coeff[0]
        betas[i, :] = coeff[1:]
        residuals[:, i] = y - x_mat @ coeff

    # Covariance matrices
    sigma_eps = (residuals.T @ residuals) / float(t_obs)
    f_bar = np.mean(factors, axis=0)
    f_dev = factors - f_bar
    sigma_f = (f_dev.T @ f_dev) / float(t_obs)
    sigma_f_inv = np.linalg.inv(sigma_f)

    # Pass 2: Cross-sectional regression of mean returns on betas
    mean_ret = np.mean(returns, axis=0)
    beta_cov_inv = np.linalg.inv(betas.T @ betas)
    lambda_premia = beta_cov_inv @ (betas.T @ mean_ret)

    # Naive vs Shanken standard errors
    c_shanken = float(1.0 + lambda_premia @ sigma_f_inv @ lambda_premia)
    v_naive = (1.0 / float(t_obs)) * (sigma_f + (beta_cov_inv @ (betas.T @ sigma_eps @ betas) @ beta_cov_inv))
    v_shanken = (1.0 / float(t_obs)) * (
        sigma_f + c_shanken * (beta_cov_inv @ (betas.T @ sigma_eps @ betas) @ beta_cov_inv)
    )

    se_naive = np.sqrt(np.diag(v_naive))
    se_shanken = np.sqrt(np.diag(v_shanken))

    # GRS (1989) statistic
    eps_inv = np.linalg.inv(sigma_eps)
    alpha_form = float(alphas @ eps_inv @ alphas)
    curvature = float(1.0 + f_bar @ sigma_f_inv @ f_bar)
    grs_stat = float(((t_obs - n_assets - n_factors) / n_assets) * (alpha_form / curvature))

    print(
        f"Factor 1 Risk Premium: {lambda_premia[0]:.4f} | Naive SE: {se_naive[0]:.4f} | Shanken SE: {se_shanken[0]:.4f}"
    )
    print(
        f"Factor 2 Risk Premium: {lambda_premia[1]:.4f} | Naive SE: {se_naive[1]:.4f} | Shanken SE: {se_shanken[1]:.4f}"
    )
    print(f"Shanken Correction Factor (1 + lambda' Sigma_f^{{-1}} lambda): {c_shanken:.4f}")
    print(f"GRS Test Statistic F: {grs_stat:.4f}")


main()
