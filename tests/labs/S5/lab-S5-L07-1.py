"""Lab S5-L07-1: Panel fixed effects within transformation vs LSDV regression.

SIMULATED: generates synthetic panel data with unobserved entity fixed effects correlated
with persistent regressors and serially correlated errors. Verifies exact numerical equivalence
between the within estimator and LSDV, and compares naive versus entity-clustered standard errors.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 606
    rng = np.random.default_rng(seed)
    n_entities = 40
    t_periods = 10
    total_obs = n_entities * t_periods
    beta_true = 2.40

    # Unobserved entity fixed effects alpha_i
    alpha_entities = rng.normal(0.0, 1.5, size=n_entities)

    # Regressors x_it correlated with alpha_i and persistent across time
    x = np.empty((n_entities, t_periods))
    y = np.empty((n_entities, t_periods))

    rho_x = 0.70
    rho_e = 0.60
    for i in range(n_entities):
        x_curr = 0.8 * alpha_entities[i] + rng.normal(0.0, 0.8)
        e_curr = rng.normal(0.0, 0.8)
        for t in range(t_periods):
            x_curr = rho_x * x_curr + rng.normal(0.0, 0.5)
            e_curr = rho_e * e_curr + rng.normal(0.0, 0.5)
            x[i, t] = x_curr
            y[i, t] = alpha_entities[i] + beta_true * x_curr + e_curr

    # Flatten for regression
    y_flat = y.ravel()
    x_flat = x.ravel()

    # 1. Within (demeaning) estimator
    y_mean = np.mean(y, axis=1, keepdims=True)
    x_mean = np.mean(x, axis=1, keepdims=True)
    y_tilde = (y - y_mean).ravel()
    x_tilde = (x - x_mean).ravel()

    s_xx = float(np.sum(x_tilde**2))
    s_xy = float(np.sum(x_tilde * y_tilde))
    beta_within = s_xy / s_xx

    # 2. Least Squares Dummy Variable (LSDV) regression
    # Design matrix: [x_flat, D_1, ..., D_N] (total_obs, 1 + N)
    d_dummies = np.zeros((total_obs, n_entities))
    for i in range(n_entities):
        d_dummies[i * t_periods : (i + 1) * t_periods, i] = 1.0

    z_lsdv = np.column_stack([x_flat, d_dummies])
    coef_lsdv = np.linalg.lstsq(z_lsdv, y_flat, rcond=None)[0]
    beta_lsdv = float(coef_lsdv[0])

    abs_diff = abs(beta_within - beta_lsdv)

    # 3. Standard errors for within estimator
    # Residuals
    e_within = y_tilde - beta_within * x_tilde
    df_resid = total_obs - n_entities - 1  # NT - N - K
    sigma2_naive = float(np.sum(e_within**2)) / df_resid
    se_naive = np.sqrt(sigma2_naive / s_xx)

    # Entity-clustered standard errors (sandwich estimator)
    e_within_mat = e_within.reshape((n_entities, t_periods))
    x_tilde_mat = x_tilde.reshape((n_entities, t_periods))
    # Score for entity i: u_i = sum_t (x_tilde_it * e_it)
    scores = np.sum(x_tilde_mat * e_within_mat, axis=1)  # (N,)
    meat = float(np.sum(scores**2))

    # Small-sample cluster adjustment: (N / (N-1)) * ((NT - 1) / (NT - N - K))
    adj = (n_entities / (n_entities - 1)) * ((total_obs - 1) / df_resid)
    var_cluster = (1.0 / (s_xx**2)) * meat * adj
    se_cluster = np.sqrt(var_cluster)

    print("Lab S5-L07-1: Panel Fixed Effects Within Transformation vs LSDV")
    print(f"  Entities N: {n_entities}, Periods T: {t_periods}, Total obs: {total_obs} (SIMULATED, seed {seed})")
    print(f"  True slope beta: {beta_true:.4f}")
    print(f"  Within (demeaned) estimator: {beta_within:.8f}")
    print(f"  LSDV dummy-variable slope:  {beta_lsdv:.8f}")
    print(f"  Absolute difference (|Within - LSDV|): {abs_diff:.2e}")
    print(f"  FWL exact equivalence (|diff| < 1e-10): {abs_diff < 1e-10}")
    print(f"  Naive OLS standard error:     {se_naive:.6f}")
    print(f"  Entity-clustered standard error: {se_cluster:.6f}")
    print(f"  Clustered SE strictly larger than naive SE: {se_cluster > se_naive}")


main()
