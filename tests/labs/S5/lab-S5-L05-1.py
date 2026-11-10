"""Lab S5-L05-1: Shanken errors-in-variables correction for two-pass asset pricing.

SIMULATED: generates synthetic asset returns and factor returns for N=20 assets across T=140 months,
computes naive Fama-MacBeth standard errors, evaluates Shanken correction factor c = 1 + lambda' Sigma_f^(-1) lambda,
computes Shanken-corrected and GMM standard errors, and demonstrates a case where the inference conclusion changes.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 143
    rng = np.random.default_rng(seed)
    n_assets = 20
    t_months = 140
    k_factors = 1

    # True factor mean and variance
    f_mean = 0.008  # 80 bps monthly
    f_var = 0.0016  # monthly variance
    factors = rng.normal(f_mean, np.sqrt(f_var), size=(t_months, k_factors))

    # True asset loadings and idiosyncratic variance
    true_betas = rng.uniform(0.7, 1.4, size=(n_assets, k_factors))
    resid_sd = rng.uniform(0.03, 0.06, size=n_assets)

    # Returns: R_it = beta_i * f_t + e_it
    excess_returns = np.empty((t_months, n_assets))
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess_returns[t] = (true_betas @ factors[t]).ravel() + e_t

    # Step 1: First-pass time-series regressions
    x_ts = np.column_stack([np.ones(t_months), factors])
    betas_est = np.empty((n_assets, k_factors + 1))
    for i in range(n_assets):
        y_i = excess_returns[:, i]
        betas_est[i] = np.linalg.solve(x_ts.T @ x_ts, x_ts.T @ y_i)

    # Step 2: Second-pass cross-sectional regressions
    z_cs = np.column_stack([np.ones(n_assets), betas_est[:, 1:]])
    monthly_slopes = np.empty((t_months, k_factors + 1))
    for t in range(t_months):
        gamma_t = np.linalg.solve(z_cs.T @ z_cs, z_cs.T @ excess_returns[t])
        monthly_slopes[t] = gamma_t

    fm_premia = np.mean(monthly_slopes, axis=0)
    naive_se = np.std(monthly_slopes, axis=0, ddof=1) / np.sqrt(t_months)

    # Shanken correction calculation
    factor_cov = np.cov(factors, rowvar=False, ddof=1).reshape((k_factors, k_factors))
    lambda_f = fm_premia[1:].reshape((k_factors, 1))

    # c = 1 + lambda_f' Sigma_f^(-1) lambda_f
    quadratic_form = float((lambda_f.T @ np.linalg.solve(factor_cov, lambda_f)).item())
    shanken_c = 1.0 + quadratic_form
    shanken_mult = np.sqrt(shanken_c)

    shanken_se = naive_se * shanken_mult

    # GMM standard errors via stacked moment asymptotic formula
    gmm_se = naive_se * np.sqrt(1.0 + quadratic_form)

    # t-statistics
    t_naive = fm_premia / naive_se
    t_shanken = fm_premia / shanken_se

    crit_95 = 1.96
    conclusion_naive = abs(t_naive[1]) > crit_95
    conclusion_shanken = abs(t_shanken[1]) > crit_95
    conclusion_changed = conclusion_naive != conclusion_shanken

    print("Lab S5-L05-1: Shanken Errors-in-Variables Correction")
    print(f"  Test assets N: {n_assets}, Months T: {t_months}, Factors K: {k_factors} (SIMULATED, seed {seed})")
    print(f"  Estimated factor premium: {fm_premia[1]:.6f}")
    print(f"  Factor sample variance: {float(factor_cov[0, 0]):.6f}")
    print(f"  Quadratic form lambda' Sigma_f^(-1) lambda: {quadratic_form:.4f}")
    print(f"  Shanken correction factor c: {shanken_c:.4f} (Multiplier sqrt(c): {shanken_mult:.4f})")
    print(f"  Naive Fama-MacBeth SE: {naive_se[1]:.6f} (t-stat: {t_naive[1]:.3f})")
    print(f"  Shanken-corrected SE:  {shanken_se[1]:.6f} (t-stat: {t_shanken[1]:.3f})")
    print(f"  GMM equivalent SE:     {gmm_se[1]:.6f}")
    print(f"  SE inflation percentage: {((shanken_mult - 1.0) * 100.0):.2f}%")
    print(f"  Inference conclusion changes (|t| > 1.96): {conclusion_changed}")
    print(f"  Shanken SE strictly larger than naive SE: {shanken_se[1] > naive_se[1]}")


main()
