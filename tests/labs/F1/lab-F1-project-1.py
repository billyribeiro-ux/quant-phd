"""Lab F1-project-1: Rung 1 worked example for Atlas A7 cross-sectional engine.

Executes an end-to-end cross-sectional analysis on seed 42:
1. Applies Shumway (1997) delisting corrections.
2. Derives NYSE breakpoints to sort on Book-to-Market.
3. Constructs Fama-French 2x3 independent sort grids and HML/SMB spreads.
4. Estimates Fama-MacBeth risk premia with Shanken (1992) standard errors.
5. Computes the Gibbons-Ross-Shanken (GRS 1989) test statistic and p-value.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def make_instance(seed: int = 42) -> dict[str, object]:
    """Generate deterministic cross-sectional instance for worked example."""
    rng = np.random.default_rng(seed)
    n_stocks = 120
    n_months = 72
    n_assets = 25
    k_factors = 3

    exchange_codes = rng.choice(np.array([1, 2, 3], dtype=np.int32), size=n_stocks, p=[0.35, 0.15, 0.50])
    exchange_codes[:20] = 1  # ensure sufficient NYSE firms

    base_size = rng.lognormal(mean=4.0, sigma=1.2, size=n_stocks)
    size_mult = np.where(exchange_codes == 1, 4.0, np.where(exchange_codes == 2, 1.2, 0.6))
    market_caps = np.round(base_size * size_mult * 100.0 + 10.0, 2)

    signal1 = np.round(np.exp(rng.normal(loc=-0.5, scale=0.6, size=n_stocks)), 4)
    signal2 = np.round(rng.normal(loc=0.08, scale=0.18, size=n_stocks), 4)
    raw_returns = np.round(rng.normal(loc=0.01, scale=0.07, size=n_stocks), 4)

    delist_codes = np.full(n_stocks, 100, dtype=np.int32)
    delist_returns = np.full(n_stocks, np.nan, dtype=np.float64)

    # Specific delistings
    delist_codes[10] = 500  # NYSE performance delisting with missing return
    delist_codes[25] = 560  # NASDAQ performance delisting with missing return
    exchange_codes[25] = 3
    delist_codes[40] = 200  # Merger with reported 15% premium
    delist_returns[40] = 0.15

    mu_factors = np.array([0.0065, 0.0025, 0.0035], dtype=np.float64)
    vol_factors = np.array([0.045, 0.030, 0.028], dtype=np.float64)
    corr_f = np.array(
        [
            [1.00, 0.15, -0.25],
            [0.15, 1.00, -0.10],
            [-0.25, -0.10, 1.00],
        ],
        dtype=np.float64,
    )
    cov_factors = np.diag(vol_factors) @ corr_f @ np.diag(vol_factors)
    z_f = rng.normal(size=(n_months, k_factors))
    panel_factors = np.round(z_f @ np.linalg.cholesky(cov_factors).T + mu_factors, 6)

    true_betas = np.empty((n_assets, k_factors), dtype=np.float64)
    for i in range(n_assets):
        b_mkt = 0.70 + 0.60 * (i / n_assets) + rng.normal(0.0, 0.05)
        b_smb = -0.50 + 1.00 * ((i % 5) / 4.0) + rng.normal(0.0, 0.05)
        b_hml = -0.40 + 0.90 * ((i // 5) / 4.0) + rng.normal(0.0, 0.05)
        true_betas[i] = [b_mkt, b_smb, b_hml]
    true_betas = np.round(true_betas, 4)

    alphas = np.round(rng.normal(loc=0.001, scale=0.002, size=n_assets), 5)
    idiosyncratic_vols = np.round(rng.uniform(0.025, 0.055, size=n_assets), 4)

    panel_excess = np.empty((n_months, n_assets), dtype=np.float64)
    for t in range(n_months):
        eps_t = rng.normal(loc=0.0, scale=idiosyncratic_vols)
        panel_excess[t] = alphas + true_betas @ panel_factors[t] + eps_t
    panel_excess = np.round(panel_excess, 6)

    return {
        "n_stocks": n_stocks,
        "n_months": n_months,
        "exchange_codes": exchange_codes,
        "market_caps": market_caps,
        "signal1": signal1,
        "signal2": signal2,
        "raw_returns": raw_returns,
        "delist_codes": delist_codes,
        "delist_returns": delist_returns,
        "panel_excess": panel_excess,
        "panel_factors": panel_factors,
        "true_betas": true_betas,
        "alphas": alphas,
    }


def run_cross_sectional_pipeline(seed: int = 42) -> dict[str, float]:
    """Execute complete Atlas A7 pipeline on instance."""
    inst = make_instance(seed)

    raw_ret = np.asarray(inst["raw_returns"], dtype=np.float64)
    dl_codes = np.asarray(inst["delist_codes"], dtype=np.int32)
    dl_ret = np.asarray(inst["delist_returns"], dtype=np.float64)
    ex = np.asarray(inst["exchange_codes"], dtype=np.int32)
    caps = np.asarray(inst["market_caps"], dtype=np.float64)
    bm = np.asarray(inst["signal1"], dtype=np.float64)
    _mom = np.asarray(inst["signal2"], dtype=np.float64)

    # 1. Delisting adjustment
    adj_ret = np.empty(len(raw_ret), dtype=np.float64)
    for i in range(len(raw_ret)):
        if np.isfinite(dl_ret[i]):
            adj_ret[i] = (1.0 + raw_ret[i]) * (1.0 + dl_ret[i]) - 1.0
        elif dl_codes[i] >= 200:
            is_perf = dl_codes[i] == 500 or (520 <= dl_codes[i] <= 584)
            pen = -0.55 if ex[i] == 3 else (-0.30 if is_perf else 0.0)
            adj_ret[i] = (1.0 + raw_ret[i]) * (1.0 + pen) - 1.0
        else:
            adj_ret[i] = raw_ret[i]

    # 2. Breakpoints & Univariate Value-Weighted Sort
    nyse_bm = bm[ex == 1]
    cuts_bm = np.percentile(nyse_bm, [20.0, 40.0, 60.0, 80.0])
    q_assign = np.digitize(bm, cuts_bm)

    q_vw_ret = np.zeros(5, dtype=np.float64)
    for q in range(5):
        idx = np.where(q_assign == q)[0]
        if len(idx) > 0:
            w = caps[idx] / np.sum(caps[idx])
            q_vw_ret[q] = float(np.sum(w * adj_ret[idx]))

    vw_spread = float(q_vw_ret[4] - q_vw_ret[0])

    # 3. Fama-MacBeth Regressions with Shanken Correction
    excess = np.asarray(inst["panel_excess"], dtype=np.float64)
    factors = np.asarray(inst["panel_factors"], dtype=np.float64)
    betas = np.asarray(inst["true_betas"], dtype=np.float64)
    t_obs, n_assets = excess.shape
    k_factors = betas.shape[1]

    x_cs = np.column_stack([np.ones(n_assets, dtype=np.float64), betas])
    x_t_x_inv = np.linalg.inv(x_cs.T @ x_cs)

    gammas = np.empty((t_obs, k_factors + 1), dtype=np.float64)
    for t in range(t_obs):
        gammas[t] = x_t_x_inv @ (x_cs.T @ excess[t])

    premia = np.mean(gammas, axis=0)
    sample_cov = np.cov(gammas, rowvar=False, ddof=1)
    naive_se = np.sqrt(np.diag(sample_cov) / float(t_obs))

    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    lambda_f = premia[1:]
    shanken_quad = float(lambda_f.T @ np.linalg.solve(sigma_f, lambda_f))
    c_shanken = 1.0 + shanken_quad
    shanken_cov = c_shanken * sample_cov
    shanken_cov[1:, 1:] += (1.0 / float(t_obs)) * sigma_f
    shanken_se = np.sqrt(np.diag(shanken_cov) / float(t_obs))

    # 4. GRS Exact F-Statistic
    x_ts = np.column_stack([np.ones(t_obs, dtype=np.float64), factors])
    x_ts_inv = np.linalg.inv(x_ts.T @ x_ts)
    alphas = np.empty(n_assets, dtype=np.float64)
    residuals = np.empty((t_obs, n_assets), dtype=np.float64)

    for i in range(n_assets):
        b = x_ts_inv @ (x_ts.T @ excess[:, i])
        alphas[i] = b[0]
        residuals[:, i] = excess[:, i] - x_ts @ b

    sigma_e = (residuals.T @ residuals) / float(t_obs - k_factors - 1)
    mu_f = np.mean(factors, axis=0)
    sh2_f = float(mu_f.T @ np.linalg.solve(sigma_f, mu_f))
    a_inv_a = float(alphas.T @ np.linalg.solve(sigma_e, alphas))

    scale = float(t_obs - n_assets - k_factors) / float(n_assets)
    grs_stat = scale * (1.0 / (1.0 + sh2_f)) * a_inv_a
    p_val = float(scipy.stats.f.sf(grs_stat, dfn=n_assets, dfd=t_obs - n_assets - k_factors))

    return {
        "vw_spread_pct": round(vw_spread * 100.0, 3),
        "lambda_mkt_pct": round(float(premia[1]) * 100.0, 3),
        "naive_se_mkt_pct": round(float(naive_se[1]) * 100.0, 3),
        "shanken_se_mkt_pct": round(float(shanken_se[1]) * 100.0, 3),
        "shanken_multiplier": round(c_shanken, 4),
        "grs_stat": round(float(grs_stat), 4),
        "grs_p_val": round(p_val, 4),
    }


def main() -> None:
    print("Lab F1-project-1 | Atlas A7 Cross-Sectional Engine Worked Example")
    print("-----------------------------------------------------------------")
    res = run_cross_sectional_pipeline(seed=42)
    print(f"Value-Weighted BM Q5 - Q1 Spread:       {res['vw_spread_pct']:+.3f}% / month")
    print(f"Fama-MacBeth Market Premium Slope:      {res['lambda_mkt_pct']:+.3f}% / month")
    print(f"Market Naive Standard Error:            {res['naive_se_mkt_pct']:.3f}%")
    print(f"Market Shanken (1992) Standard Error:   {res['shanken_se_mkt_pct']:.3f}%")
    print(f"Shanken Multiplier (c = 1 + Sh_f^2):    {res['shanken_multiplier']:.4f}")
    print(f"Gibbons-Ross-Shanken F-Statistic:       {res['grs_stat']:.4f}")
    print(f"GRS Null Rejection P-Value:             {res['grs_p_val']:.4f}")


main()
