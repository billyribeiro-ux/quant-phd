"""Lab F2-L06-1: Factor Model Horse Race, GRS Test, and Max-Sharpe Metric.

Compares CAPM, Fama-French 3, Carhart 4, Fama-French 5, and the Hou-Xue-Zhang
q-factor model on 25 test assets using the Gibbons-Ross-Shanken (1989) test
and the Barillas-Shanken (2017) maximum squared Sharpe ratio metric Sh^2(f).
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def run_factor_model_comparison(seed: int = 42) -> dict[str, float]:
    """Execute GRS tests and compute max squared Sharpe ratios across 5 models."""
    rng = np.random.default_rng(seed)
    n_months = 360  # 30 years
    n_assets = 25  # 25 test portfolios (e.g. 5x5 Size-BM)

    # Underlying factors
    mkt = rng.normal(0.065 / 12, 0.155 / np.sqrt(12), size=n_months)
    smb = rng.normal(0.025 / 12, 0.100 / np.sqrt(12), size=n_months)
    hml = rng.normal(0.035 / 12, 0.110 / np.sqrt(12), size=n_months)
    wml = 0.075 / 12 + rng.normal(0.0, 0.130 / np.sqrt(12), size=n_months)
    rmw = rng.normal(0.038 / 12, 0.080 / np.sqrt(12), size=n_months)
    cma = rng.normal(0.032 / 12, 0.070 / np.sqrt(12), size=n_months)

    # q-factor components: MKT, ME (size), IA (investment), ROE (profitability)
    # q-factor IA and ROE track CMA and RMW with slight noise / quarterly timing
    q_me = smb + rng.normal(0, 0.02 / np.sqrt(12), size=n_months)
    q_ia = cma + rng.normal(0, 0.02 / np.sqrt(12), size=n_months)
    q_roe = rmw + rng.normal(0, 0.02 / np.sqrt(12), size=n_months)

    # Model dictionaries
    models = {
        "CAPM": np.column_stack([mkt]),
        "FF3": np.column_stack([mkt, smb, hml]),
        "Carhart": np.column_stack([mkt, smb, hml, wml]),
        "FF5": np.column_stack([mkt, smb, hml, rmw, cma]),
        "q-factor": np.column_stack([mkt, q_me, q_ia, q_roe]),
    }

    # Simulate 25 test assets with realistic factor structure + slight mispricing
    b_mkt = rng.uniform(0.7, 1.3, size=n_assets)
    b_smb = rng.uniform(-0.4, 0.8, size=n_assets)
    b_hml = rng.uniform(-0.5, 0.7, size=n_assets)
    # True pricing errors (CAPM has largest alphas, FF5 / q-factor smallest)
    true_alpha = rng.normal(0.0, 0.015 / 12, size=n_assets)

    test_returns = np.zeros((n_months, n_assets))
    for t in range(n_months):
        idio = rng.normal(0, 0.18 / np.sqrt(12), size=n_assets)
        test_returns[t, :] = true_alpha + b_mkt * mkt[t] + b_smb * smb[t] + b_hml * hml[t] + idio

    # Helper: GRS test and Max-Sharpe computation
    def evaluate_model(f_mat: np.ndarray) -> tuple[float, float, float]:
        t_obs = len(test_returns)
        k_factors = f_mat.shape[1]

        # 1. Barillas-Shanken Max Squared Sharpe ratio (annualized)
        mu_f = np.mean(f_mat, axis=0)
        sigma_f = np.cov(f_mat, rowvar=False, ddof=1)
        if k_factors == 1:
            sigma_f_inv = 1.0 / sigma_f
            sh2_ann = float((mu_f[0] ** 2) * sigma_f_inv * 12.0)
            sh2_monthly = float((mu_f[0] ** 2) * sigma_f_inv)
        else:
            sigma_f_inv = np.linalg.inv(sigma_f)
            sh2_ann = float((mu_f @ sigma_f_inv @ mu_f) * 12.0)
            sh2_monthly = float(mu_f @ sigma_f_inv @ mu_f)

        # 2. Time-series regressions of 25 assets on factors
        x_des = np.column_stack([np.ones(t_obs), f_mat])
        betas = np.linalg.lstsq(x_des, test_returns, rcond=None)[0]
        alphas = betas[0, :]
        resids = test_returns - x_des @ betas

        # Residual covariance matrix (unbiased: T - K - 1)
        sigma_eps = (resids.T @ resids) / (t_obs - k_factors - 1)
        sigma_eps_inv = np.linalg.inv(sigma_eps)

        # GRS F-statistic
        # F = (T - N - K)/N * (1 + f_bar' * Sigma_f^-1 * f_bar)^-1 * alpha' * Sigma_eps^-1 * alpha
        grs_scale = (t_obs - n_assets - k_factors) / n_assets
        alpha_quad = alphas @ sigma_eps_inv @ alphas
        grs_stat = float(grs_scale * (1.0 / (1.0 + sh2_monthly)) * alpha_quad)
        p_val = float(1.0 - scipy.stats.f.cdf(grs_stat, n_assets, t_obs - n_assets - k_factors))

        return sh2_ann, grs_stat, p_val

    results = {}
    for name, f_mat in models.items():
        sh2, grs, p = evaluate_model(f_mat)
        results[f"sh2_{name}"] = round(sh2, 4)
        results[f"grs_{name}"] = round(grs, 2)
        results[f"p_{name}"] = round(p, 4)

    return results


def main() -> None:
    print("Lab F2-L06-1 | Factor Model Horse Race (GRS & Barillas-Shanken)")
    print("----------------------------------------------------------------")
    res = run_factor_model_comparison(seed=42)
    models = ["CAPM", "FF3", "Carhart", "FF5", "q-factor"]
    print(f"{'Model':<10} | {'Sh^2(f) (Ann)':<14} | {'GRS Stat':<10} | {'p-value':<8}")
    print("-" * 50)
    for m in models:
        print(f"{m:<10} | {res[f'sh2_{m}']:<14.4f} | {res[f'grs_{m}']:<10.2f} | {res[f'p_{m}']:<8.4f}")
    print("-" * 50)
    print("Model ranking by max squared Sharpe ratio expands monotonically with unspanned factors.")


main()
