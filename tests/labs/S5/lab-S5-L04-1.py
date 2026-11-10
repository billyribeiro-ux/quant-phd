"""Lab S5-L04-1: Fama-MacBeth two-pass cross-sectional regression.

SIMULATED: generates synthetic asset returns and factor returns for N=20 assets across T=180 months,
executes time-series regressions to obtain factor loadings, runs monthly cross-sectional regressions,
and computes Fama-MacBeth risk premia, naive standard errors, and t-statistics.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 303
    rng = np.random.default_rng(seed)
    n_assets = 20
    t_months = 180
    k_factors = 2

    # Factor excess returns (T, K)
    f_mean = np.array([0.006, 0.004])  # 60 bps and 40 bps monthly
    f_cov = np.array([[0.0016, 0.0004], [0.0004, 0.0009]])
    factors = rng.multivariate_normal(f_mean, f_cov, size=t_months)

    # True asset loadings (N, K) and pricing errors
    true_betas = rng.uniform(0.5, 1.5, size=(n_assets, k_factors))
    true_alpha = np.zeros(n_assets)
    resid_sd = rng.uniform(0.02, 0.04, size=n_assets)

    # Generate asset excess returns: R_it = alpha_i + beta_i' f_t + e_it
    excess_returns = np.empty((t_months, n_assets))
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess_returns[t] = true_alpha + true_betas @ factors[t] + e_t

    # Step 1: First-pass time-series regressions for each asset
    # Design: [1, factors] (T, K+1)
    x_ts = np.column_stack([np.ones(t_months), factors])
    betas_est = np.empty((n_assets, k_factors + 1))
    for i in range(n_assets):
        y_i = excess_returns[:, i]
        coef = np.linalg.solve(x_ts.T @ x_ts, x_ts.T @ y_i)
        betas_est[i] = coef

    # Step 2: Second-pass monthly cross-sectional regressions
    # For each month t, regress R_t (N,) on [1, beta_est[:, 1:]] (N, K+1)
    z_cs = np.column_stack([np.ones(n_assets), betas_est[:, 1:]])
    monthly_slopes = np.empty((t_months, k_factors + 1))
    for t in range(t_months):
        r_t = excess_returns[t]
        gamma_t = np.linalg.solve(z_cs.T @ z_cs, z_cs.T @ r_t)
        monthly_slopes[t] = gamma_t

    # Fama-MacBeth estimates: mean and standard error of monthly slopes
    fm_premia = np.mean(monthly_slopes, axis=0)
    slope_sd = np.std(monthly_slopes, axis=0, ddof=1)
    fm_naive_se = slope_sd / np.sqrt(t_months)
    fm_t_stats = fm_premia / fm_naive_se

    # Check that premium equals average of monthly slopes exactly
    diff_premia = np.max(np.abs(fm_premia - np.sum(monthly_slopes, axis=0) / t_months))

    print("Lab S5-L04-1: Fama-MacBeth Two-Pass Cross-Sectional Regression")
    print(f"  Test assets N: {n_assets}, Months T: {t_months}, Factors K: {k_factors} (SIMULATED, seed {seed})")
    print(f"  Max absolute difference between mean and manual sum/T: {diff_premia:.2e}")
    print("  Parameter | Estimated Premium | Naive SE    | t-statistic | Significant (|t| > 1.96)?")
    print("  " + "-" * 72)
    names = ["Zero-Beta Intercept", "Factor 1 Premium", "Factor 2 Premium"]
    for idx, name in enumerate(names):
        sig = "Yes" if abs(fm_t_stats[idx]) > 1.96 else "No"
        p_str = f"{fm_premia[idx]:+.6f}"
        se_str = f"{fm_naive_se[idx]:.6f}"
        t_str = f"{fm_t_stats[idx]:+7.3f}"
        print(f"  {name:<20} | {p_str}        | {se_str}   | {t_str}     | {sig}")


main()
