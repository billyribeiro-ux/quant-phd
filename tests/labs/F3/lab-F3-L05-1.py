"""Lab F3-L05-1: TSMOM Pooled Regression vs Within-Asset Econometric Decomposition.

Implements the Moskowitz, Ooi & Pedersen (2012) pooled regression and the Huang,
Li, Wang & Zhou (2020) critique. Simulates i.i.d. asset returns with cross-sectional
dispersion in unconditional means, demonstrating that pooled OLS produces a
spurious positive t-statistic, while the fixed-effects within estimator recovers zero.
"""

from __future__ import annotations

import numpy as np


def evaluate_tsmom_pooled_critique(seed: int = 42) -> dict[str, float]:
    """Demonstrate the between-asset bias in pooled TSMOM regressions."""
    rng = np.random.default_rng(seed)
    n_assets = 50
    n_months = 360  # 30 years
    lookback = 12

    # 1. Simulate assets with heterogeneous unconditional means but STRICTLY ZERO serial correlation (iid)
    # Means vary across assets: N(0.04/12, 0.05/12)
    asset_means = rng.normal(0.04 / 12.0, 0.05 / 12.0, size=n_assets)
    asset_vols = rng.uniform(0.10 / np.sqrt(12.0), 0.25 / np.sqrt(12.0), size=n_assets)

    returns = np.zeros((n_months, n_assets))
    for i in range(n_assets):
        returns[:, i] = rng.normal(asset_means[i], asset_vols[i], size=n_months)

    # 2. Build pooled panel: dependent y = r_{t+1}^i / sigma_t^i, regressor x = sign(past 12m)
    y_list: list[float] = []
    x_list: list[float] = []
    asset_id_list: list[int] = []

    for t in range(lookback, n_months - 1):
        for i in range(n_assets):
            past_ret = np.sum(returns[t - lookback : t, i])
            # Historical volatility
            hist_vol = float(np.std(returns[max(0, t - 24) : t, i], ddof=1))
            if hist_vol <= 0:
                hist_vol = 0.01

            y = float(returns[t + 1, i] / hist_vol)
            x = float(np.sign(past_ret))

            y_list.append(y)
            x_list.append(x)
            asset_id_list.append(i)

    y_arr = np.array(y_list)
    x_arr = np.array(x_list)
    asset_ids = np.array(asset_id_list)
    n_obs = len(y_arr)

    # Model A: Naive Pooled OLS (Moskowitz et al. 2012 specification)
    x_pooled = np.column_stack([np.ones(n_obs), x_arr])
    beta_pooled, _, _, _ = np.linalg.lstsq(x_pooled, y_arr, rcond=None)
    residuals_pooled = y_arr - x_pooled @ beta_pooled
    se_pooled = np.sqrt(np.sum(residuals_pooled**2) / (n_obs - 2) * np.linalg.inv(x_pooled.T @ x_pooled)[1, 1])
    t_pooled = float(beta_pooled[1] / se_pooled)

    # Model B: Asset-demeaned Fixed Effects / Within Estimator (Huang et al. 2020)
    # Demean y and x within each asset
    y_within = np.zeros_like(y_arr)
    x_within = np.zeros_like(x_arr)
    for i in range(n_assets):
        mask = asset_ids == i
        y_within[mask] = y_arr[mask] - np.mean(y_arr[mask])
        x_within[mask] = x_arr[mask] - np.mean(x_arr[mask])

    # OLS on demeaned data without intercept
    beta_within = float(np.sum(x_within * y_within) / np.sum(x_within**2))
    resid_within = y_within - beta_within * x_within
    se_within = float(np.sqrt(np.sum(resid_within**2) / (n_obs - n_assets - 1) / np.sum(x_within**2)))
    t_within = float(beta_within / se_within)

    # Model C: Asset-by-asset individual regressions (% with positive and significant t-stat)
    sig_count = 0
    for i in range(n_assets):
        mask = asset_ids == i
        y_sub = y_arr[mask]
        x_sub = x_arr[mask]
        x_mat = np.column_stack([np.ones_like(x_sub), x_sub])
        b_sub = np.linalg.lstsq(x_mat, y_sub, rcond=None)[0]
        res_sub = y_sub - x_mat @ b_sub
        se_sub = np.sqrt(np.sum(res_sub**2) / (len(y_sub) - 2) * np.linalg.inv(x_mat.T @ x_mat)[1, 1])
        t_sub = b_sub[1] / se_sub
        if t_sub > 1.96:
            sig_count += 1
    pct_sig_individual = float(sig_count / n_assets * 100.0)

    return {
        "beta_pooled": round(float(beta_pooled[1]), 4),
        "t_pooled": round(t_pooled, 2),
        "beta_within": round(beta_within, 4),
        "t_within": round(t_within, 2),
        "pct_sig_individual": round(pct_sig_individual, 1),
    }


def main() -> None:
    print("Lab F3-L05-1 | TSMOM Pooled Regression vs Huang et al. (2020) Critique")
    print("---------------------------------------------------------------------")
    res = evaluate_tsmom_pooled_critique(seed=42)
    print(f"Pooled OLS Slope (beta):       {res['beta_pooled']:+.4f} (t = {res['t_pooled']:.2f})")
    print(f"Within-Asset FE Slope (beta):  {res['beta_within']:+.4f} (t = {res['t_within']:.2f})")
    print(f"Assets with Sig Individual t:  {res['pct_sig_individual']:.1f}% (nominal 5% test)")
    print("-" * 69)
    tp, tw = res["t_pooled"], res["t_within"]
    print(
        f"Under true i.i.d. returns, pooled OLS is biased (t = {tp:.2f}), "
        f"while within FE is insignificant (t = {tw:.2f})."
    )


main()
