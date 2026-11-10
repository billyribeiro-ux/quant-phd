"""Lab 5: Clustered standard errors, degrees of freedom corrections, and GRS test."""

from __future__ import annotations

import numpy as np


def compute_panel_se(
    y: np.ndarray,
    x_mat: np.ndarray,
    entities: np.ndarray,
    time_periods: np.ndarray,
) -> dict[str, float]:
    n, k = x_mat.shape
    xtx_inv = np.linalg.pinv(x_mat.T @ x_mat)
    params = xtx_inv @ (x_mat.T @ y)
    resid = y - x_mat @ params

    # 1. Homoskedastic OLS
    s2_ols = float(np.sum(resid**2) / (n - k))
    se_ols = float(np.sqrt(s2_ols * xtx_inv[1, 1]))

    # 2. White HC0
    meat_white = (x_mat.T * (resid**2)) @ x_mat
    cov_white = xtx_inv @ meat_white @ xtx_inv
    se_white = float(np.sqrt(cov_white[1, 1]))

    # 3. Clustered by entity
    def _cluster_cov(groups: np.ndarray) -> np.ndarray:
        ug = np.unique(groups)
        g_len = len(ug)
        meat = np.zeros((k, k))
        for g in ug:
            g_mask = groups == g
            score = x_mat[g_mask].T @ resid[g_mask]
            meat += np.outer(score, score)
        df_corr = (g_len / max(1, g_len - 1)) * ((n - 1) / max(1, n - k))
        res_cov: np.ndarray = np.asarray(df_corr * (xtx_inv @ meat @ xtx_inv))
        return res_cov

    cov_ent = _cluster_cov(entities)
    cov_time = _cluster_cov(time_periods)

    combined = [f"{e}_{t}" for e, t in zip(entities, time_periods, strict=False)]
    _, gid = np.unique(combined, return_inverse=True)
    cov_both = cov_ent + cov_time - _cluster_cov(gid)

    return {
        "OLS": se_ols,
        "White HC0": se_white,
        "Firm Clustered": float(np.sqrt(max(0.0, cov_ent[1, 1]))),
        "Time Clustered": float(np.sqrt(max(0.0, cov_time[1, 1]))),
        "Two-Way Clustered": float(np.sqrt(max(0.0, cov_both[1, 1]))),
    }


def compute_grs_stat(
    alphas: np.ndarray,
    resid_cov: np.ndarray,
    factor_means: np.ndarray,
    factor_cov: np.ndarray,
    t_len: int,
    n_assets: int,
    k_factors: int,
) -> tuple[float, float]:
    """Compute Gibbons, Ross & Shanken (1989) exact F-statistic and asymptotic Chi-square."""
    inv_sigma = np.linalg.pinv(resid_cov)
    inv_factor_cov = np.linalg.pinv(factor_cov)

    quad_f = float(factor_means.T @ inv_factor_cov @ factor_means)
    shanken_denom = 1.0 + quad_f
    alpha_quad = float(alphas.T @ inv_sigma @ alphas)

    # Finite sample F-statistic
    df1 = n_assets
    df2 = t_len - n_assets - k_factors
    grs_f = (float(df2) / float(df1)) * (alpha_quad / shanken_denom)

    # Asymptotic Chi-square statistic
    asymp_chi2 = float(t_len) * (alpha_quad / shanken_denom)
    return grs_f, asymp_chi2


def main() -> None:
    rng = np.random.default_rng(42)
    n_firms, n_months = 50, 48
    n_obs = n_firms * n_months

    firms = np.repeat(np.arange(n_firms), n_months)
    months = np.tile(np.arange(n_months), n_firms)

    # Correlated errors within firm across time (firm effect)
    firm_effect = rng.normal(0, 0.05, size=n_firms)
    time_shock = rng.normal(0, 0.04, size=n_months)
    eps = firm_effect[firms] + time_shock[months] + rng.normal(0, 0.06, size=n_obs)

    x_sig = rng.normal(0, 1, size=n_obs)
    y_ret = 0.005 + 0.015 * x_sig + eps
    x_mat = np.column_stack([np.ones(n_obs), x_sig])

    se_results = compute_panel_se(y_ret, x_mat, firms, months)

    print("Panel Standard Error Sensitivity (Petersen 2009 Comparison):")
    print(f"  Sample: N = {n_firms} firms, T = {n_months} months ({n_obs} obs)")
    for name, val in se_results.items():
        t_stat = 0.015 / val
        print(f"  {name:<18}: SE = {val:.6f} | t-statistic = {t_stat:.2f}")

    # GRS finite sample vs asymptotic test
    n_assets, k_factors = 10, 3
    alphas = np.array([0.002] * n_assets)
    sigma_eps = np.eye(n_assets) * 0.001
    f_mean = np.array([0.006, 0.002, 0.003])
    f_cov = np.eye(k_factors) * 0.002

    f_stat, chi2_stat = compute_grs_stat(alphas, sigma_eps, f_mean, f_cov, n_months, n_assets, k_factors)
    print("\nGRS (1989) Model Evaluation Test:")
    print(f"  Exact Finite-Sample GRS F({n_assets}, {n_months - n_assets - k_factors}): {f_stat:.3f}")
    print(f"  Asymptotic Chi-Square({n_assets}): {chi2_stat:.3f} (scaled F: {chi2_stat / n_assets:.3f})")


main()
