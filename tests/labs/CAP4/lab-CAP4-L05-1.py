"""Lab CAP4-L05-1: Two-Stage IV Identification & Weak Instrument Diagnostic.

Evaluates causal identification by comparing OLS vs 2SLS estimates under endogenous factor loadings,
computing first-stage Montiel Olea-Pflueger / Stock-Yogo F-statistics, and verifying the Sargan overidentification test.
"""

from __future__ import annotations

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def main() -> None:
    np.random.seed(42)
    n_obs = 300

    # 1. Structural model: Y = alpha + beta * X + epsilon
    # True causal parameter beta = 0.50
    # Endogeneity: Cov(X, epsilon) > 0 (e.g. unobserved managerial skill or confounding shock)
    true_beta = 0.50
    u_confound = np.random.normal(0.0, 1.0, size=n_obs)
    epsilon = 0.6 * u_confound + np.random.normal(0.0, 0.8, size=n_obs)

    # 2. Instruments Z = [Z1, Z2] (two exogenous instruments)
    # Z1 is strong, Z2 is moderately strong
    z1 = np.random.normal(0.0, 1.0, size=n_obs)
    z2 = np.random.normal(0.0, 1.0, size=n_obs)
    z_matrix = np.column_stack([np.ones(n_obs), z1, z2])

    # Endogenous regressor X = gamma0 + gamma1 * Z1 + gamma2 * Z2 + 0.8 * u_confound + v
    gamma = np.array([0.2, 0.7, 0.4])
    v_noise = np.random.normal(0.0, 0.5, size=n_obs)
    x = z_matrix @ gamma + 0.7 * u_confound + v_noise

    y = 0.1 + true_beta * x + epsilon

    # 3. Naive OLS Estimation
    x_mat = np.column_stack([np.ones(n_obs), x])
    beta_ols = np.linalg.inv(x_mat.T @ x_mat) @ (x_mat.T @ y)
    ols_causal_slope = float(beta_ols[1])

    # 4. First-Stage Regression: X on Z
    gamma_hat = np.linalg.inv(z_matrix.T @ z_matrix) @ (z_matrix.T @ x)
    x_hat = z_matrix @ gamma_hat
    resid_first = x - x_hat
    # F-statistic for excluded instruments (Z1, Z2)
    k_excl = 2
    r2_first = float(1.0 - np.var(resid_first) / np.var(x))
    f_stat_first = float((r2_first / k_excl) / ((1.0 - r2_first) / (n_obs - 3)))

    # 5. Second-Stage Regression (2SLS): Y on [1, X_hat]
    x_hat_mat = np.column_stack([np.ones(n_obs), x_hat])
    beta_2sls = np.linalg.inv(x_hat_mat.T @ x_hat_mat) @ (x_hat_mat.T @ y)
    iv_causal_slope = float(beta_2sls[1])

    # 6. Sargan Overidentification Test
    # Residuals computed with actual X: e_iv = y - beta_0 - beta_1 * X
    resid_2sls = y - (x_mat @ beta_2sls)
    # Regress e_iv on Z
    gamma_sargan = np.linalg.inv(z_matrix.T @ z_matrix) @ (z_matrix.T @ resid_2sls)
    fitted_sargan = z_matrix @ gamma_sargan
    r2_sargan = float(np.var(fitted_sargan) / np.var(resid_2sls))
    sargan_stat = float(n_obs * r2_sargan)
    # Degrees of freedom = L - K = 2 - 1 = 1
    sargan_p = float(1.0 - stats.chi2.cdf(sargan_stat, df=1))

    is_weak = bool(f_stat_first < 10.0)

    print(f"True Causal Beta: {true_beta:.4f}")
    print(f"Naive OLS Beta: {ols_causal_slope:.4f}")
    print(f"2SLS Identified Beta: {iv_causal_slope:.4f}")
    print(f"First-Stage F-Statistic: {f_stat_first:.2f}")
    print(f"Weak Instrument Flag (F < 10): {is_weak}")
    print(f"Sargan Overid Stat (df=1): {sargan_stat:.4f}")
    print(f"Sargan p-value: {sargan_p:.4f}")


main()
