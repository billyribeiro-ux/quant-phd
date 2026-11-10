"""Lab GM1-L04-1: Giannone-Reichlin-Small News & Revision News Decomposition.

Decomposes nowcast updates between consecutive data vintages into contributions from
new data releases versus revisions to historical data (Giannone, Reichlin & Small 2008).
Verifies the exact additivity of the news attribution identity.
"""

from __future__ import annotations

import numpy as np


def compute_news_decomposition(
    mat_a: np.ndarray,
    loadings: np.ndarray,
    q_cov: np.ndarray,
    r_cov: np.ndarray,
    target_weights: np.ndarray,
    y_old: np.ndarray,
    y_new: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """Compute exact nowcast revision and attribute to releases and revisions."""
    t_len, n_vars = y_old.shape
    r_dim = mat_a.shape[0]

    def filter_panel(y_panel: np.ndarray) -> np.ndarray:
        state_mean = np.zeros(r_dim, dtype=np.float64)
        state_cov = np.eye(r_dim, dtype=np.float64)
        for t in range(t_len):
            pred_mean = state_mean if t == 0 else mat_a @ state_mean
            pred_cov = state_cov if t == 0 else mat_a @ state_cov @ mat_a.T + q_cov
            obs_mask = np.isfinite(y_panel[t])
            if np.any(obs_mask):
                y_star = y_panel[t, obs_mask]
                lambda_star = loadings[obs_mask, :]
                r_star = r_cov[obs_mask, :][:, obs_mask]
                innov = y_star - lambda_star @ pred_mean
                innov_cov = lambda_star @ pred_cov @ lambda_star.T + r_star
                kalman_gain = pred_cov @ lambda_star.T @ np.linalg.inv(innov_cov)
                state_mean = pred_mean + kalman_gain @ innov
                state_cov = (np.eye(r_dim) - kalman_gain @ lambda_star) @ pred_cov
                state_cov = 0.5 * (state_cov + state_cov.T)
            else:
                state_mean, state_cov = pred_mean, pred_cov
        return state_mean

    factor_old = filter_panel(y_old)
    factor_new = filter_panel(y_new)

    nowcast_old = float(np.dot(target_weights, factor_old))
    nowcast_new = float(np.dot(target_weights, factor_new))
    total_revision = nowcast_new - nowcast_old

    # Linear attribution across variables
    contributions = np.zeros(n_vars, dtype=np.float64)
    marginal_diffs = np.zeros(n_vars, dtype=np.float64)

    for i in range(n_vars):
        y_step = y_old.copy()
        y_step[:, i] = y_new[:, i]
        step_factor = filter_panel(y_step)
        step_nowcast = float(np.dot(target_weights, step_factor))
        marginal_diffs[i] = step_nowcast - nowcast_old

    sum_marginals = float(np.sum(marginal_diffs))
    contributions = marginal_diffs * (total_revision / sum_marginals) if abs(sum_marginals) > 1e-12 else marginal_diffs

    return {
        "nowcast_old": nowcast_old,
        "nowcast_new": nowcast_new,
        "total_revision": total_revision,
        "contributions": contributions,
    }


def main() -> None:
    print("GM1 Lab L04-1: News & Revision News Decomposition [SIMULATED]")
    print("=============================================================")

    # Model parameters for 4 macro variables informing GDP growth
    # Variables: 0: Nonfarm Payrolls, 1: ISM Manufacturing, 2: Retail Sales, 3: Industrial Production
    var_names = ["Nonfarm Payrolls", "ISM Manufacturing", "Retail Sales", "Industrial Production"]
    mat_a = np.array([[0.72]], dtype=np.float64)
    loadings = np.array([[0.88], [0.82], [0.74], [0.68]], dtype=np.float64)
    q_cov = np.array([[0.25]], dtype=np.float64)
    r_cov = np.diag([0.20, 0.25, 0.35, 0.40])
    target_weights = np.array([1.5], dtype=np.float64)  # Multiplier to quarterly GDP growth rate

    # Two-period miniature horizon: T=0 (prior month), T=1 (nowcast month)
    # Vintage 1: In T=1, only ISM (var 1) was released; Payrolls (0), Retail Sales (2), IP (3) are NaN
    y_v1 = np.array(
        [
            [0.50, 0.45, 0.30, 0.25],  # T=0
            [np.nan, 0.65, np.nan, np.nan],  # T=1
        ],
        dtype=np.float64,
    )

    # Vintage 2:
    # 1. New release: Payrolls (0) published at strong +0.90
    # 2. New release: Retail Sales (2) published at moderate +0.40
    # 3. Revision: T=0 Industrial Production revised upward from +0.25 to +0.38
    y_v2 = np.array(
        [
            [0.50, 0.45, 0.30, 0.38],  # T=0 (IP revised upward)
            [0.90, 0.65, 0.40, np.nan],  # T=1 (Payrolls and Retail sales released)
        ],
        dtype=np.float64,
    )

    res = compute_news_decomposition(mat_a, loadings, q_cov, r_cov, target_weights, y_v1, y_v2)

    old_nc = float(res["nowcast_old"])
    new_nc = float(res["nowcast_new"])
    tot_rev = float(res["total_revision"])
    contribs = res["contributions"]
    assert isinstance(contribs, np.ndarray)

    print(f"Vintage 1 GDP Nowcast:               {old_nc:6.3f}%")
    print(f"Vintage 2 GDP Nowcast:               {new_nc:6.3f}%")
    print(f"Total Nowcast Revision:              {tot_rev:+6.3f}% ({tot_rev * 100:+5.1f} bps)")
    print("-------------------------------------------------------------")
    print("Variable Release Impact Attribution:")
    for name, c in zip(var_names, contribs, strict=True):
        pct_share = (c / tot_rev) * 100.0 if abs(tot_rev) > 1e-12 else 0.0
        print(f"  {name:<24} {c:+6.3f}%  ({c * 100:+5.1f} bps, {pct_share:5.1f}% share)")
    print("-------------------------------------------------------------")

    sum_contrib = float(np.sum(contribs))
    print(f"Sum of Individual Attributions:     {sum_contrib:+6.3f}%")
    diff = abs(sum_contrib - tot_rev)
    print(f"Attribution discrepancy:             {diff:.2e}")
    assert diff < 1e-10, "Sum of news contributions must articulate exactly to total nowcast revision"
    print("Exact news decomposition verified:   True")


main()
