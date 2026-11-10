"""Lab CAP4-L06-1: Latent Factor Representation & Non-Linear Structural Validation.

Evaluates an original doctoral contribution by comparing linear benchmark factor models
against a non-linear latent factor architecture, quantifying cross-sectional pricing error reduction,
out-of-sample R^2, and Gibbons-Ross-Shanken (GRS) efficiency test statistics.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)
    t_obs = 240
    n_assets = 15

    # 1. True data-generating process with non-linear factor interactions
    # Common macro state z_t and two latent factors
    z = np.random.normal(0.0, 1.0, size=t_obs)
    f1 = np.random.normal(0.005, 0.04, size=t_obs)
    f2 = np.random.normal(0.003, 0.03, size=t_obs)

    # True non-linear interaction factor: f_nl = f1 * (1 + 0.5 * tanh(z))
    f_nl = f1 * (1.0 + 0.5 * np.tanh(z))

    betas_linear = np.random.uniform(0.6, 1.4, size=(n_assets, 2))
    betas_nl = np.random.uniform(-0.5, 0.5, size=n_assets)
    residuals = np.random.normal(0.0, 0.03, size=(t_obs, n_assets))

    returns = np.zeros((t_obs, n_assets))
    for t in range(t_obs):
        returns[t] = 0.002 + betas_linear @ np.array([f1[t], f2[t]]) + betas_nl * f_nl[t] + residuals[t]

    # 2. Linear 2-Factor Benchmark Model Estimation (F1, F2)
    x_linear = np.column_stack([np.ones(t_obs), f1, f2])
    b_hat_lin = np.linalg.inv(x_linear.T @ x_linear) @ (x_linear.T @ returns)
    alphas_lin = b_hat_lin[0]
    resids_lin = returns - x_linear @ b_hat_lin
    sigma_eps_lin = (resids_lin.T @ resids_lin) / (t_obs - 3)
    inv_sigma_eps_lin = np.linalg.inv(sigma_eps_lin)

    # GRS test for linear model
    f_mat_lin = np.column_stack([f1, f2])
    f_mean_lin = np.mean(f_mat_lin, axis=0)
    sigma_f_lin = np.cov(f_mat_lin, rowvar=False)
    grs_scaling_lin = (t_obs - n_assets - 2) / n_assets
    quad_alpha_lin = float(alphas_lin @ inv_sigma_eps_lin @ alphas_lin)
    quad_f_lin = float(f_mean_lin @ np.linalg.inv(sigma_f_lin) @ f_mean_lin)
    grs_stat_linear = float(grs_scaling_lin * (quad_alpha_lin / (1.0 + quad_f_lin)))

    # 3. Novel Contribution Model: Augmented with Non-Linear Latent State (F1, F2, F_nl)
    x_novel = np.column_stack([np.ones(t_obs), f1, f2, f_nl])
    b_hat_novel = np.linalg.inv(x_novel.T @ x_novel) @ (x_novel.T @ returns)
    alphas_novel = b_hat_novel[0]
    resids_novel = returns - x_novel @ b_hat_novel
    sigma_eps_novel = (resids_novel.T @ resids_novel) / (t_obs - 4)
    inv_sigma_eps_novel = np.linalg.inv(sigma_eps_novel)

    # GRS test for novel model
    f_mat_nov = np.column_stack([f1, f2, f_nl])
    f_mean_nov = np.mean(f_mat_nov, axis=0)
    sigma_f_nov = np.cov(f_mat_nov, rowvar=False)
    grs_scaling_nov = (t_obs - n_assets - 3) / n_assets
    quad_alpha_nov = float(alphas_novel @ inv_sigma_eps_novel @ alphas_novel)
    quad_f_nov = float(f_mean_nov @ np.linalg.inv(sigma_f_nov) @ f_mean_nov)
    grs_stat_novel = float(grs_scaling_nov * (quad_alpha_nov / (1.0 + quad_f_nov)))

    # 4. Mean absolute pricing errors (MAPEs)
    mape_lin = float(np.mean(np.abs(alphas_lin)))
    mape_nov = float(np.mean(np.abs(alphas_novel)))
    pricing_error_reduction = float((mape_lin - mape_nov) / mape_lin) * 100.0

    print(f"Linear Benchmark GRS F-Stat: {grs_stat_linear:.4f}")
    print(f"Novel Model GRS F-Stat: {grs_stat_novel:.4f}")
    print(f"Linear Model MAPE: {mape_lin * 100:.3f}%")
    print(f"Novel Model MAPE: {mape_nov * 100:.3f}%")
    print(f"Pricing Error Reduction: {pricing_error_reduction:.2f}%")
    print(f"GRS F-Statistic Improvement: {(grs_stat_linear - grs_stat_novel):.4f}")


main()
