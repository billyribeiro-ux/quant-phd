"""Mutant 2: omits the Shanken factor risk premium correction term, returning uncorrected Fama-MacBeth OLS variance."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def solve_hygiene_and_delisting(instance: dict[str, Any]) -> dict[str, Any]:
    raw_returns = np.array(instance["raw_returns"], dtype=np.float64)
    delisting_flags = np.array(instance["delisting_flags"], dtype=bool)
    exchange_codes = np.array(instance["exchange_codes"], dtype=np.int64)
    market_caps = np.array(instance["market_caps"], dtype=np.float64)
    anomaly_signals = np.array(instance["anomaly_signals"], dtype=np.float64)
    nyse_p20_cutoff = float(instance["nyse_p20_cutoff"])

    _t_months, n_firms = raw_returns.shape

    clean_returns = raw_returns.copy()
    for j in range(n_firms):
        delist_mask = delisting_flags[:, j]
        if np.any(delist_mask):
            penalty = -0.30 if exchange_codes[j] == 1 else -0.55
            clean_returns[delist_mask, j] = penalty

    top_threshold = float(np.percentile(anomaly_signals, 90.0))
    bot_threshold = float(np.percentile(anomaly_signals, 10.0))
    top_decile = anomaly_signals >= top_threshold
    bot_decile = anomaly_signals <= bot_threshold

    raw_ew_top = np.mean(raw_returns[:, top_decile], axis=1)
    raw_ew_bot = np.mean(raw_returns[:, bot_decile], axis=1)
    raw_ew_spread = float(np.mean(raw_ew_top - raw_ew_bot))

    clean_ew_top = np.mean(clean_returns[:, top_decile], axis=1)
    clean_ew_bot = np.mean(clean_returns[:, bot_decile], axis=1)
    ew_spread = float(np.mean(clean_ew_top - clean_ew_bot))

    delisting_drag = float(raw_ew_spread - ew_spread)

    w_top = market_caps[top_decile] / np.sum(market_caps[top_decile])
    w_bot = market_caps[bot_decile] / np.sum(market_caps[bot_decile])
    vw_spread = float(np.mean(clean_returns[:, top_decile] @ w_top - clean_returns[:, bot_decile] @ w_bot))

    valid_top = top_decile & (market_caps >= nyse_p20_cutoff)
    valid_bot = bot_decile & (market_caps >= nyse_p20_cutoff)
    w_nyse_top = market_caps[valid_top] / np.sum(market_caps[valid_top])
    w_nyse_bot = market_caps[valid_bot] / np.sum(market_caps[valid_bot])
    nyse_vw_spread = float(np.mean(clean_returns[:, valid_top] @ w_nyse_top - clean_returns[:, valid_bot] @ w_nyse_bot))

    return {
        "ew_spread": ew_spread,
        "vw_spread": vw_spread,
        "delisting_drag": delisting_drag,
        "nyse_vw_spread": nyse_vw_spread,
    }


def solve_econometric_estimation(instance: dict[str, Any]) -> dict[str, Any]:
    panel_returns = np.array(instance["panel_returns"], dtype=np.float64)
    factor_series = np.array(instance["factor_series"], dtype=np.float64)
    t_panel, n_assets = panel_returns.shape
    _, n_factors = factor_series.shape

    x_ts = np.column_stack([np.ones(t_panel), factor_series])
    x_ts_inv = np.linalg.inv(x_ts.T @ x_ts)
    b_ts = x_ts_inv @ (x_ts.T @ panel_returns)

    alpha_hat = b_ts[0]
    beta_hat = b_ts[1:].T
    resids = panel_returns - x_ts @ b_ts
    sigma_eps = (resids.T @ resids) / float(t_panel - n_factors - 1)
    inv_sigma_eps = np.linalg.inv(sigma_eps)

    r_bar = np.mean(panel_returns, axis=0)
    var_beta = np.linalg.inv(beta_hat.T @ beta_hat)
    lambda_hat = var_beta @ (beta_hat.T @ r_bar)

    sigma_f = np.cov(factor_series, rowvar=False)

    # DEFECT: Omits Shanken factor risk premium correction, setting shanken_factor = 1.0 exactly
    shanken_factor = 1.0

    v_pricing = var_beta @ (beta_hat.T @ sigma_eps @ beta_hat) @ var_beta
    cov_lambda = (1.0 / t_panel) * (sigma_f + shanken_factor * v_pricing)
    shanken_se = [float(np.sqrt(cov_lambda[k, k])) for k in range(n_factors)]

    inv_sigma_f = np.linalg.inv(sigma_f)
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
    gross_alpha = float(instance["gross_alpha"])
    turnover = float(instance["turnover"])
    decay_rate = float(instance["decay_rate"])
    look_ahead_penalty = float(instance["look_ahead_penalty"])
    microcap_penalty = float(instance["microcap_penalty"])
    trading_cost_bps = float(instance["trading_cost_bps"])
    reported_t_stat = float(instance["reported_t_stat"])

    cost_per_turn = trading_cost_bps / 10000.0
    turnover_drag = turnover * cost_per_turn
    unhedged_margin = gross_alpha - look_ahead_penalty - microcap_penalty - turnover_drag
    net_alpha = float(unhedged_margin * (1.0 - decay_rate))

    margin_before_turnover = gross_alpha - look_ahead_penalty - microcap_penalty
    breakeven_cost_bps = float((margin_before_turnover / turnover) * 10000.0)

    t_stat_stressed = float(reported_t_stat * (net_alpha / gross_alpha))
    resilience_score = float(np.clip(100.0 * (net_alpha / 0.0200) * (t_stat_stressed / 2.0), 0.0, 100.0))
    defense_verdict = bool(resilience_score >= 50.0 and net_alpha > 0.015)

    return {
        "net_alpha": net_alpha,
        "breakeven_cost_bps": breakeven_cost_bps,
        "resilience_score": resilience_score,
        "defense_verdict": defense_verdict,
    }
