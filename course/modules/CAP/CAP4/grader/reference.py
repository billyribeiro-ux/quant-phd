"""Reference solution for CAP4: Research Thesis & Defense Capstone Grader.

Implements full doctoral-grade solutions for the thesis replication and defense suite:
1. Sample Hygiene & Delisting Adjustment (Shumway corrections and NYSE value-weighting)
2. Econometric Estimation (Fama-MacBeth, Shanken asymptotic correction, GRS efficiency test)
3. Committee Defense Stress Testing (Turnover frictions, look-ahead bias, out-of-sample decay)
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def solve_hygiene_and_delisting(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute sample hygiene and institutional delisting return adjustments.

    Applies Shumway (1997) delisting return replacements (-0.30 for NYSE/AMEX, -0.55 for NASDAQ)
    and evaluates decile spreads under equal-weighting and NYSE-breakpoint capitalization weighting.
    """
    raw_returns = np.array(instance["raw_returns"], dtype=np.float64)  # T x N
    delisting_flags = np.array(instance["delisting_flags"], dtype=bool)  # T x N
    exchange_codes = np.array(instance["exchange_codes"], dtype=np.int64)  # N
    market_caps = np.array(instance["market_caps"], dtype=np.float64)  # N
    anomaly_signals = np.array(instance["anomaly_signals"], dtype=np.float64)  # N
    nyse_p20_cutoff = float(instance["nyse_p20_cutoff"])

    _t_months, n_firms = raw_returns.shape

    # 1. Apply Shumway delisting replacements
    clean_returns = raw_returns.copy()
    for j in range(n_firms):
        delist_mask = delisting_flags[:, j]
        if np.any(delist_mask):
            penalty = -0.30 if exchange_codes[j] == 1 else -0.55
            clean_returns[delist_mask, j] = penalty

    # 2. Portfolio decile assignments
    top_threshold = float(np.percentile(anomaly_signals, 90.0))
    bot_threshold = float(np.percentile(anomaly_signals, 10.0))
    top_decile = anomaly_signals >= top_threshold
    bot_decile = anomaly_signals <= bot_threshold

    # 3. Equal-weighted spreads
    raw_ew_top = np.mean(raw_returns[:, top_decile], axis=1)
    raw_ew_bot = np.mean(raw_returns[:, bot_decile], axis=1)
    raw_ew_spread = float(np.mean(raw_ew_top - raw_ew_bot))

    clean_ew_top = np.mean(clean_returns[:, top_decile], axis=1)
    clean_ew_bot = np.mean(clean_returns[:, bot_decile], axis=1)
    ew_spread = float(np.mean(clean_ew_top - clean_ew_bot))

    delisting_drag = float(raw_ew_spread - ew_spread)

    # 4. Value-weighted spread (all firms)
    w_top = market_caps[top_decile] / np.sum(market_caps[top_decile])
    w_bot = market_caps[bot_decile] / np.sum(market_caps[bot_decile])
    vw_top = clean_returns[:, top_decile] @ w_top
    vw_bot = clean_returns[:, bot_decile] @ w_bot
    vw_spread = float(np.mean(vw_top - vw_bot))

    # 5. Value-weighted spread with NYSE size cutoff (size >= nyse_p20_cutoff)
    valid_top = top_decile & (market_caps >= nyse_p20_cutoff)
    valid_bot = bot_decile & (market_caps >= nyse_p20_cutoff)
    w_nyse_top = market_caps[valid_top] / np.sum(market_caps[valid_top])
    w_nyse_bot = market_caps[valid_bot] / np.sum(market_caps[valid_bot])
    nyse_vw_top = clean_returns[:, valid_top] @ w_nyse_top
    nyse_vw_bot = clean_returns[:, valid_bot] @ w_nyse_bot
    nyse_vw_spread = float(np.mean(nyse_vw_top - nyse_vw_bot))

    return {
        "ew_spread": ew_spread,
        "vw_spread": vw_spread,
        "delisting_drag": delisting_drag,
        "nyse_vw_spread": nyse_vw_spread,
    }


def solve_econometric_estimation(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute cross-sectional factor estimation, Shanken correction, and GRS test.

    Calculates:
    - First-pass time-series regressions: alphas, betas, residual covariance
    - Second-pass cross-sectional regression: factor risk premia lambda
    - Shanken (1992) asymptotic standard error correction factor: c = 1 + lambda' Sigma_f^{-1} lambda
    - Gibbons-Ross-Shanken (GRS) statistic and F-distribution p-value
    """
    panel_returns = np.array(instance["panel_returns"], dtype=np.float64)  # T x N
    factor_series = np.array(instance["factor_series"], dtype=np.float64)  # T x K
    t_panel, n_assets = panel_returns.shape
    _, n_factors = factor_series.shape

    # 1. First-pass time-series regressions: R_{i,t} = alpha_i + beta_i' f_t + eps_{i,t}
    x_ts = np.column_stack([np.ones(t_panel), factor_series])  # T x (K+1)
    x_ts_inv = np.linalg.inv(x_ts.T @ x_ts)
    b_ts = x_ts_inv @ (x_ts.T @ panel_returns)  # (K+1) x N

    alpha_hat = b_ts[0]  # length N
    beta_hat = b_ts[1:].T  # N x K
    resids = panel_returns - x_ts @ b_ts
    sigma_eps = (resids.T @ resids) / float(t_panel - n_factors - 1)
    inv_sigma_eps = np.linalg.inv(sigma_eps)

    # 2. Second-pass cross-sectional regression: E[R] = beta @ lambda
    r_bar = np.mean(panel_returns, axis=0)  # length N
    var_beta = np.linalg.inv(beta_hat.T @ beta_hat)  # K x K
    lambda_hat = var_beta @ (beta_hat.T @ r_bar)  # length K

    # 3. Shanken (1992) correction factor
    sigma_f = np.cov(factor_series, rowvar=False)  # K x K
    inv_sigma_f = np.linalg.inv(sigma_f)
    shanken_quad = float(lambda_hat @ inv_sigma_f @ lambda_hat)
    shanken_factor = float(1.0 + shanken_quad)

    # Shanken asymptotic variance: (1/T) * [Sigma_f + c * (beta' beta)^{-1} beta' Sigma_eps beta (beta' beta)^{-1}]
    v_pricing = var_beta @ (beta_hat.T @ sigma_eps @ beta_hat) @ var_beta
    cov_lambda = (1.0 / t_panel) * (sigma_f + shanken_factor * v_pricing)
    shanken_se = [float(np.sqrt(cov_lambda[k, k])) for k in range(n_factors)]

    # 4. Gibbons-Ross-Shanken (GRS) statistic
    f_bar = np.mean(factor_series, axis=0)
    grs_df_num = n_assets
    grs_df_denom = t_panel - n_assets - n_factors
    grs_scale = float(grs_df_denom / grs_df_num)

    quad_alpha = float(alpha_hat @ inv_sigma_eps @ alpha_hat)
    quad_f = float(f_bar @ inv_sigma_f @ f_bar)
    grs_statistic = float(grs_scale * (quad_alpha / (1.0 + quad_f)))
    grs_p_value = float(1.0 - stats.f.cdf(grs_statistic, dfn=grs_df_num, dfd=grs_df_denom))

    return {
        "lambda_premia": [float(x) for x in lambda_hat],
        "shanken_factor": shanken_factor,
        "shanken_se": shanken_se,
        "grs_statistic": grs_statistic,
        "grs_p_value": grs_p_value,
    }


def solve_defense_stress_test(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute committee defense stress testing across adversarial attack vectors.

    Calculates:
    - Net economic alpha under look-ahead, microcap, and turnover frictions
    - Break-even execution cost (bps/turn)
    - Defense committee resilience score and passing verdict
    """
    gross_alpha = float(instance["gross_alpha"])
    turnover = float(instance["turnover"])
    decay_rate = float(instance["decay_rate"])
    look_ahead_penalty = float(instance["look_ahead_penalty"])
    microcap_penalty = float(instance["microcap_penalty"])
    trading_cost_bps = float(instance["trading_cost_bps"])
    reported_t_stat = float(instance["reported_t_stat"])

    # 1. Turnover execution friction
    cost_per_turn = trading_cost_bps / 10000.0
    turnover_drag = turnover * cost_per_turn

    # 2. Pre-decay net margin
    unhedged_margin = gross_alpha - look_ahead_penalty - microcap_penalty - turnover_drag

    # 3. Out-of-sample structural decay scaling
    net_alpha = float(unhedged_margin * (1.0 - decay_rate))

    # 4. Break-even trading cost where net alpha reaches zero
    margin_before_turnover = gross_alpha - look_ahead_penalty - microcap_penalty
    breakeven_cost_bps = float((margin_before_turnover / turnover) * 10000.0)

    # 5. Stressed defense t-statistic and resilience score
    t_stat_stressed = float(reported_t_stat * (net_alpha / gross_alpha))
    resilience_score = float(np.clip(100.0 * (net_alpha / 0.0200) * (t_stat_stressed / 2.0), 0.0, 100.0))
    defense_verdict = bool(resilience_score >= 50.0 and net_alpha > 0.015)

    return {
        "net_alpha": net_alpha,
        "breakeven_cost_bps": breakeven_cost_bps,
        "resilience_score": resilience_score,
        "defense_verdict": defense_verdict,
    }
