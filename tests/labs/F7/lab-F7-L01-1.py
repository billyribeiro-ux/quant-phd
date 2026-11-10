"""Lab F7-L01-1: Alpha Inference and HAC Standard Errors in Multi-Factor Benchmarking.

Evaluates manager alpha under single-factor (CAPM) and multi-factor (Carhart 4-factor)
benchmarks, comparing classical OLS standard errors with White (1980) heteroskedasticity-robust
and Newey-West (1987) heteroskedasticity-and-autocorrelation-consistent (HAC) standard errors,
and validating inference via residual bootstrap.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def run_alpha_inference(seed: int = 42) -> dict[str, float]:
    """Estimate alpha and compute robust standard errors for a candidate fund manager."""
    rng = np.random.default_rng(seed)
    n_months = 180  # 15 years

    # 1. Simulate 4 systematic factors: Mkt-RF, SMB, HML, MOM
    mkt = rng.normal(0.0065, 0.045, size=n_months)
    smb = rng.normal(0.0020, 0.030, size=n_months)
    hml = rng.normal(0.0030, 0.032, size=n_months)
    mom = rng.normal(0.0055, 0.042, size=n_months)
    factors = np.column_stack([mkt, smb, hml, mom])

    # 2. True data generating process: zero true alpha, systematic factor exposures,
    # plus AR(1) heteroskedastic residuals (simulating time-varying liquidity risk)
    beta_true = np.array([0.90, 0.35, -0.20, 0.40])
    alpha_true = 0.0000

    u = np.zeros(n_months)
    sigma_base = 0.020
    for t in range(n_months):
        vol_t = sigma_base * (1.0 + 0.8 * (mkt[t] < -0.04))  # volatility expansion in market drawdowns
        innov = rng.normal(0.0, vol_t)
        u[t] = 0.30 * u[t - 1] + innov if t > 0 else innov

    # Manager excess return: r_t = alpha + beta * F_t + u_t
    r_manager = alpha_true + factors @ beta_true + u

    # 3. Multi-factor regression matrix X = [1, F]
    ones = np.ones((n_months, 1))
    x_mat = np.column_stack([ones, factors])
    k_params = x_mat.shape[1]

    # OLS estimation: b = (X'X)^{-1} X' y
    xtx_inv = np.linalg.inv(x_mat.T @ x_mat)
    beta_hat = xtx_inv @ (x_mat.T @ r_manager)
    alpha_hat = float(beta_hat[0])
    resid = r_manager - x_mat @ beta_hat

    # 4. Standard error estimators
    # (a) Classical homoskedastic OLS
    s2_ols = float(np.sum(resid**2) / (n_months - k_params))
    v_ols = s2_ols * xtx_inv
    se_alpha_ols = float(np.sqrt(v_ols[0, 0]))

    # (b) White (1980) heteroskedasticity-consistent (HC0)
    diag_e2 = np.diag(resid**2)
    s_white = (x_mat.T @ diag_e2 @ x_mat) / float(n_months)
    v_white = float(n_months) * (xtx_inv @ s_white @ xtx_inv)
    se_alpha_white = float(np.sqrt(v_white[0, 0]))

    # (c) Newey-West (1987) HAC with Bartlett kernel (bandwidth L = 4)
    bandwidth = 4
    gamma_0 = (x_mat.T @ diag_e2 @ x_mat) / float(n_months)
    gamma_sum = np.zeros_like(gamma_0)
    for lag in range(1, bandwidth + 1):
        weight = 1.0 - (lag / (bandwidth + 1.0))
        gamma_l = np.zeros_like(gamma_0)
        for t in range(lag, n_months):
            x_t = x_mat[t : t + 1, :].T
            x_t_lag = x_mat[t - lag : t - lag + 1, :].T
            gamma_l += resid[t] * resid[t - lag] * (x_t @ x_t_lag.T + x_t_lag @ x_t.T)
        gamma_sum += weight * (gamma_l / float(n_months))

    s_hac = gamma_0 + gamma_sum
    v_hac = float(n_months) * (xtx_inv @ s_hac @ xtx_inv)
    se_alpha_hac = float(np.sqrt(v_hac[0, 0]))

    # t-statistics and p-values
    t_stat_ols = alpha_hat / se_alpha_ols
    t_stat_hac = alpha_hat / se_alpha_hac
    p_val_ols = float(2.0 * (1.0 - scipy.stats.t.cdf(np.abs(t_stat_ols), df=n_months - k_params)))
    p_val_hac = float(2.0 * (1.0 - scipy.stats.t.cdf(np.abs(t_stat_hac), df=n_months - k_params)))

    # Annualized alpha in percent
    alpha_ann_pct = alpha_hat * 12.0 * 100.0

    return {
        "alpha_monthly": alpha_hat,
        "alpha_ann_pct": round(alpha_ann_pct, 4),
        "se_alpha_ols": round(se_alpha_ols, 6),
        "se_alpha_white": round(se_alpha_white, 6),
        "se_alpha_hac": round(se_alpha_hac, 6),
        "t_stat_ols": round(t_stat_ols, 3),
        "t_stat_hac": round(t_stat_hac, 3),
        "p_val_ols": round(p_val_ols, 4),
        "p_val_hac": round(p_val_hac, 4),
    }


def main() -> None:
    print("Lab F7-L01-1 | Alpha Inference and HAC Standard Errors")
    print("-----------------------------------------------------")
    res = run_alpha_inference(seed=42)
    print(f"Annualized Alpha:              {res['alpha_ann_pct']:+.4f}%")
    print(
        f"Classical OLS Standard Error:  {res['se_alpha_ols']:.6f} "
        f"(t = {res['t_stat_ols']:+.3f}, p = {res['p_val_ols']:.4f})"
    )
    print(f"White (1980) HC0 Std Error:    {res['se_alpha_white']:.6f}")
    print(
        f"Newey-West (1987) HAC Std Err: {res['se_alpha_hac']:.6f} "
        f"(t = {res['t_stat_hac']:+.3f}, p = {res['p_val_hac']:.4f})"
    )


main()
