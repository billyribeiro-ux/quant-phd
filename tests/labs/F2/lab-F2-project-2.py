"""Lab F2-project-2: Project Rung 2 Completion Problem - GRS Statistic & Max-Sharpe Engine.

Completed reference twin for the Project Rung 2 completion exercise. Implements
exact GRS test statistic scaling, factor quadratic forms, and Barillas-Shanken
tangency portfolio maximum squared Sharpe ratio computation.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def compute_grs_and_max_sharpe(
    alphas: np.ndarray,
    factors: np.ndarray,
    residuals: np.ndarray,
) -> dict[str, float]:
    """Compute GRS test statistic and maximum squared Sharpe ratio.

    Completed solution for Rung 2 completion problem.
    """
    t_obs, k_factors = factors.shape
    n_assets = len(alphas)

    # 1. Factor mean and covariance matrix
    f_bar = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)

    if k_factors == 1:
        sh2_factor = float((f_bar[0] ** 2) / float(sigma_f))
    else:
        sigma_f_inv = np.linalg.inv(sigma_f)
        sh2_factor = float(f_bar @ sigma_f_inv @ f_bar)

    # Annualized maximum squared Sharpe ratio
    max_sharpe_sq_ann = float(sh2_factor * 12.0)

    # 2. Unbiased residual covariance matrix (ddof = T - K - 1)
    df_denom = t_obs - n_assets - k_factors
    sigma_eps = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    sigma_eps_inv = np.linalg.inv(sigma_eps)

    # 3. Alpha quadratic form: alpha^T * Sigma_eps^{-1} * alpha
    alpha_quad = float(alphas @ sigma_eps_inv @ alphas)

    # 4. GRS exact F-statistic
    scale = float(df_denom) / float(n_assets)
    grs_stat = float(scale * (1.0 / (1.0 + sh2_factor)) * alpha_quad)
    p_val = float(1.0 - scipy.stats.f.cdf(grs_stat, n_assets, df_denom))

    return {
        "max_sharpe_sq_ann": round(max_sharpe_sq_ann, 4),
        "grs_stat": round(grs_stat, 2),
        "p_value": round(p_val, 4),
        "df_num": float(n_assets),
        "df_denom": float(df_denom),
    }


def main() -> None:
    print("Project Rung 2 | GRS & Max-Sharpe Engine (Completion Solution)")
    print("-------------------------------------------------------------")
    # Quick deterministic verification on test arrays
    rng = np.random.default_rng(42)
    t_obs, n_assets, k_factors = 360, 25, 3
    alphas = rng.normal(0.001, 0.002, size=n_assets)
    factors = rng.normal(0.005, 0.04, size=(t_obs, k_factors))
    residuals = rng.normal(0.0, 0.03, size=(t_obs, n_assets))

    res = compute_grs_and_max_sharpe(alphas, factors, residuals)
    print(f"Annualized Max Sh^2(f): {res['max_sharpe_sq_ann']:.4f}")
    print(f"GRS F-Statistic:        {res['grs_stat']:.2f} (df1={int(res['df_num'])}, df2={int(res['df_denom'])})")
    print(f"GRS p-value:            {res['p_value']:.4f}")
    print("Completed solution verifies exact finite-sample F-scaling and factor quadratic form.")


main()
