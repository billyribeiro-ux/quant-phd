"""Lab S5-L06-1: Gibbons-Ross-Shanken (GRS) test of portfolio efficiency.

SIMULATED: generates synthetic excess returns for N=10 test portfolios across T=120 months
under a K=1 factor asset pricing model, evaluates the exact finite-sample GRS F-statistic,
and verifies nominal size via 1000 Monte Carlo replications under the null hypothesis.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def compute_grs(returns: np.ndarray, factors: np.ndarray) -> tuple[float, float, float, float]:
    """Compute GRS F-statistic, factor Sharpe ratio, p-value, and critical value."""
    t_months, n_assets = returns.shape
    k_factors = factors.shape[1]

    # Time-series regressions
    x = np.column_stack([np.ones(t_months), factors])  # (T, K+1)
    # (X'X)^(-1) X' Y
    coefs = np.linalg.solve(x.T @ x, x.T @ returns)  # (K+1, N)
    alphas = coefs[0, :]  # (N,)
    resids = returns - x @ coefs  # (T, N)

    # Residual covariance matrix Sigma_hat (unbiased divisor T - K - 1)
    df_resid = t_months - k_factors - 1
    sigma_hat = (resids.T @ resids) / df_resid

    # Factor statistics
    f_bar = np.mean(factors, axis=0)  # (K,)
    f_cov = np.cov(factors, rowvar=False, ddof=1).reshape((k_factors, k_factors))
    sr2_f = float(f_bar.T @ np.linalg.solve(f_cov, f_bar))

    # GRS F-statistic:
    # F = [(T - N - K) / N] * [1 / (1 + SR_f^2)] * alpha' Sigma_hat^(-1) alpha
    d1 = n_assets
    d2 = t_months - n_assets - k_factors
    quad_alpha = float(alphas.T @ np.linalg.solve(sigma_hat, alphas))
    grs_stat = (float(d2) / float(d1)) * (1.0 / (1.0 + sr2_f)) * quad_alpha

    p_val = float(scipy.stats.f.sf(grs_stat, dfn=d1, dfd=d2))
    crit_val = float(scipy.stats.f.ppf(0.95, dfn=d1, dfd=d2))
    return grs_stat, sr2_f, p_val, crit_val


def main() -> None:
    seed = 505
    rng = np.random.default_rng(seed)
    n_assets = 10
    t_months = 120
    k_factors = 1
    d1 = n_assets
    d2 = t_months - n_assets - k_factors
    reps = 1000

    f_mean = 0.007
    f_sd = 0.045
    betas_true = rng.uniform(0.6, 1.4, size=n_assets)
    sigma_true = 0.04

    # Primary sample under the null: alpha_i = 0 for all i
    f_0 = rng.normal(f_mean, f_sd, size=(t_months, k_factors))
    e_0 = rng.normal(0.0, sigma_true, size=(t_months, n_assets))
    r_0 = f_0 @ betas_true.reshape(1, n_assets) + e_0

    grs_stat, sr2_f, p_val, crit_val = compute_grs(r_0, f_0)

    # Monte Carlo simulation of exact F test under null
    rejections = 0
    for _ in range(reps):
        f_r = rng.normal(f_mean, f_sd, size=(t_months, k_factors))
        e_r = rng.normal(0.0, sigma_true, size=(t_months, n_assets))
        r_r = f_r @ betas_true.reshape(1, n_assets) + e_r
        f_stat, _, _, _ = compute_grs(r_r, f_r)
        if f_stat > crit_val:
            rejections += 1

    emp_size = rejections / reps
    mc_se = float(np.sqrt(emp_size * (1.0 - emp_size) / reps))

    print("Lab S5-L06-1: Gibbons-Ross-Shanken (GRS) Portfolio Efficiency Test")
    print(f"  Test portfolios N: {n_assets}, Months T: {t_months}, Factors K: {k_factors} (SIMULATED, seed {seed})")
    print(f"  Degrees of freedom: df1={d1}, df2={d2}")
    print(f"  Factor Sharpe ratio squared (SR_f^2): {sr2_f:.4f}")
    print(f"  Primary sample GRS F-statistic: {grs_stat:.4f} (p-value: {p_val:.4f})")
    print(f"  F({d1}, {d2}) 95% critical threshold: {crit_val:.4f}")
    print(f"  Primary sample null accepted (F <= crit): {grs_stat <= crit_val}")
    print(f"  Monte Carlo empirical size under H_0 (R={reps}): {emp_size:.4f} (MC SE: {mc_se:.4f})")
    print(f"  Nominal 5% coverage within 2 SEs: {abs(emp_size - 0.05) <= 2.0 * mc_se}")


main()
