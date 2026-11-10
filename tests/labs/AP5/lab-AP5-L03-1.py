"""Lab AP5-L03-1: Predictive Regressions and Stambaugh Small-Sample Bias.

SIMULATED: generates predictive system under the null of no predictability (beta=0)
with a persistent predictor and negatively correlated innovations to quantify
the Stambaugh (1999) small-sample upward bias.
"""

from __future__ import annotations

import numpy as np


def newey_west_se(x: np.ndarray, e: np.ndarray, max_lags: int = 4) -> float:
    """Compute Newey-West HAC standard error for univariate OLS slope."""
    x_mean = np.mean(x)
    x_dev = x - x_mean
    sxx = np.sum(x_dev**2)

    # Autocovariance terms: gamma_j = sum_{t=j+1}^T (x_dev_t * e_t) * (x_dev_{t-j} * e_{t-j})
    u = x_dev * e
    omega = np.sum(u**2)
    for j in range(1, max_lags + 1):
        weight = 1.0 - j / (max_lags + 1.0)
        gamma = np.sum(u[j:] * u[:-j])
        omega += 2.0 * weight * gamma

    var_beta = omega / (sxx**2)
    return float(np.sqrt(max(1e-12, var_beta)))


def main() -> None:
    rng = np.random.default_rng(2026)
    n_obs = 200  # 200 periods (e.g. 50 years of quarterly data)
    phi = 0.95  # highly persistent valuation ratio (AR(1) parameter)
    mu = 0.05 * (1.0 - phi)
    beta_true = 0.0  # true slope is exactly zero under the null hypothesis

    # Covariance structure of innovations: [u, v]
    # u: return innovation (std = 0.18)
    # v: predictor innovation (std = 0.08)
    # corr(u, v) = -0.85 (price increase raises return and lowers dividend-price ratio)
    sigma_u = 0.18
    sigma_v = 0.08
    rho_uv = -0.85
    cov_uv = rho_uv * sigma_u * sigma_v

    cov_matrix = np.array([[sigma_u**2, cov_uv], [cov_uv, sigma_v**2]])
    innovations = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov_matrix, size=n_obs + 1)
    u = innovations[:, 0]
    v = innovations[:, 1]

    # Generate predictor path x_t
    x = np.zeros(n_obs + 1)
    x[0] = mu / (1.0 - phi)
    for t in range(n_obs):
        x[t + 1] = mu + phi * x[t] + v[t + 1]

    # Generate returns r_{t+1} = alpha + beta_true * x_t + u_{t+1}
    alpha = 0.02
    r = alpha + beta_true * x[:-1] + u[1:]
    x_pred = x[:-1]

    # Estimate OLS: r_{t+1} = a + b * x_t + e_{t+1}
    x_mean = float(np.mean(x_pred))
    r_mean = float(np.mean(r))
    sxx = float(np.sum((x_pred - x_mean) ** 2))
    sxy = float(np.sum((x_pred - x_mean) * (r - r_mean)))
    b_ols = sxy / sxx
    a_ols = r_mean - b_ols * x_mean

    residuals = r - (a_ols + b_ols * x_pred)
    sigma2_e = float(np.sum(residuals**2) / (n_obs - 2))
    se_ols = float(np.sqrt(sigma2_e / sxx))
    t_ols = b_ols / se_ols

    # Newey-West standard error with 4 lags
    se_nw = newey_west_se(x_pred, residuals, max_lags=4)
    t_nw = b_ols / se_nw

    # Estimate sample AR(1) of predictor: x_{t+1} = m + phi_hat * x_t + v_hat_{t+1}
    x_lag = x[:-1]
    x_lead = x[1:]
    s_lag_lag = float(np.sum((x_lag - np.mean(x_lag)) ** 2))
    s_lag_lead = float(np.sum((x_lag - np.mean(x_lag)) * (x_lead - np.mean(x_lead))))
    phi_hat = s_lag_lead / s_lag_lag
    v_hat = x_lead - (np.mean(x_lead) - phi_hat * np.mean(x_lag) + phi_hat * x_lag)

    # Sample covariance of residuals: cov(e, v_hat)
    sigma_uv_sample = float(np.mean(residuals * v_hat))
    sigma_v2_sample = float(np.mean(v_hat**2))

    # Analytical Stambaugh (1999) bias: E[b - beta] approx - (sigma_uv / sigma_v^2) * (1 + 3*phi) / T
    stambaugh_bias_analytical = -(sigma_uv_sample / sigma_v2_sample) * ((1.0 + 3.0 * phi_hat) / n_obs)
    b_corrected = b_ols - stambaugh_bias_analytical
    t_corrected = b_corrected / se_nw

    print("Stambaugh (1999) Predictive Regression Bias Analysis")
    print(f"Sample length T:             {n_obs}")
    print(f"True predictive slope beta:  {beta_true:.4f}")
    print(f"Predictor AR(1) phi (true):  {phi:.4f}")
    print(f"Predictor AR(1) phi (est):   {phi_hat:.4f}")
    print(f"Correlation corr(u, v):      {rho_uv:.4f}")
    print(f"Naive OLS slope b_ols:       {b_ols:.4f}")
    print(f"OLS std error (t-stat):      {se_ols:.4f} ({t_ols:.2f})")
    print(f"Newey-West std error (t):    {se_nw:.4f} ({t_nw:.2f})")
    print(f"Analytical Stambaugh bias:   {stambaugh_bias_analytical:.4f}")
    print(f"Bias-corrected slope b_adj:  {b_corrected:.4f}")
    print(f"Bias-corrected t-stat:       {t_corrected:.2f}")


main()
