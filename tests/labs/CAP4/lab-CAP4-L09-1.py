"""Lab CAP4-L09-1: Referee Response Matrix & Robustness Sensitivity Diagnostic.

Evaluates the peer review revision protocol by executing referee-demanded robustness checks:
sample window trimming, alternative clustering, and outlier winsorization thresholds (0.5% vs 1% vs 2.5%),
computing parameter sensitivity metrics across the response matrix.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)
    n_obs = 360

    # 1. Baseline empirical specification: Y = alpha + beta * X + eps
    # True beta = 0.35
    x = np.random.normal(0.0, 1.0, size=n_obs)
    # Add fat-tailed shocks to simulate real financial outliers
    eps = np.random.standard_t(df=4, size=n_obs) * 0.5
    y = 0.05 + 0.35 * x + eps

    # Baseline OLS (1% winsorization)
    def run_ols(x_arr: np.ndarray, y_arr: np.ndarray) -> tuple[float, float]:
        n = len(x_arr)
        x_mat = np.column_stack([np.ones(n), x_arr])
        b = np.linalg.inv(x_mat.T @ x_mat) @ (x_mat.T @ y_arr)
        res = y_arr - x_mat @ b
        s2 = float(np.sum(res**2) / (n - 2))
        var_b = s2 * np.linalg.inv(x_mat.T @ x_mat)[1, 1]
        return float(b[1]), float(np.sqrt(var_b))

    def winsorize_pct(arr: np.ndarray, pct: float) -> np.ndarray:
        low = float(np.percentile(arr, pct))
        high = float(np.percentile(arr, 100.0 - pct))
        clipped = np.clip(arr, low, high)
        return np.asarray(clipped, dtype=np.float64)

    # 2. Referee Demands:
    # Demand A: Winsorization sensitivity (0.5%, 1.0%, 2.5%)
    beta_base, se_base = run_ols(winsorize_pct(x, 1.0), winsorize_pct(y, 1.0))
    beta_w05, _se_w05 = run_ols(winsorize_pct(x, 0.5), winsorize_pct(y, 0.5))
    beta_w25, _se_w25 = run_ols(winsorize_pct(x, 2.5), winsorize_pct(y, 2.5))

    # Demand B: Subsample trimming (excluding Great Financial Crisis 2008-2009, e.g. 24 middle months)
    mask_trimmed = np.ones(n_obs, dtype=bool)
    mask_trimmed[160:184] = False
    beta_trimmed, _se_trimmed = run_ols(winsorize_pct(x[mask_trimmed], 1.0), winsorize_pct(y[mask_trimmed], 1.0))

    # Demand C: Cluster-robust standard error inflation (simulated double clustering)
    cluster_inflation = 1.28
    se_double_cluster = se_base * cluster_inflation

    # 3. Sensitivity Bounds & Response Matrix Metrics
    all_betas = [beta_base, beta_w05, beta_w25, beta_trimmed]
    max_beta_dev = float(np.max(np.abs(np.array(all_betas) - beta_base)))
    pct_max_dev = (max_beta_dev / beta_base) * 100.0
    min_t_stat = float(np.min([b / se_double_cluster for b in all_betas]))

    print(f"Baseline Coefficient (1.0% Winsor): {beta_base:.4f} (se={se_base:.4f})")
    print(f"0.5% Winsor Coefficient: {beta_w05:.4f}")
    print(f"2.5% Winsor Coefficient: {beta_w25:.4f}")
    print(f"Subsample Trimmed Coefficient: {beta_trimmed:.4f}")
    print(f"Double-Clustered Standard Error: {se_double_cluster:.4f}")
    print(f"Maximum Coefficient Deviation: {pct_max_dev:.2f}%")
    print(f"Worst-Case Referee t-Statistic: {min_t_stat:.2f}")


main()
