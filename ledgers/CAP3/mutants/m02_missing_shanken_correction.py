"""Mutant 2: omits Shanken factor risk premium correction term, returning uncorrected Fama-MacBeth OLS variance."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import chi2


def solve_asset_pricing_prelim(instance: dict[str, Any]) -> dict[str, Any]:
    ap = instance.get("asset_pricing", instance)
    mu = np.array(ap["mu"], dtype=np.float64)
    sigma = np.array(ap["sigma"], dtype=np.float64)
    rf = float(ap["rf"])
    gamma = float(ap["gamma"])
    mu_stock = float(ap["mu_stock"])
    sigma_stock = float(ap["sigma_stock"])
    rho = float(ap["rho"])

    sigma_inv = np.linalg.inv(sigma)
    tangency_sharpe = float(np.sqrt(mu @ sigma_inv @ mu))
    mean_sdf = 1.0 / (1.0 + rf)
    hj_volatility_bound = float(mean_sdf * tangency_sharpe)

    excess_return = mu_stock - rf
    stock_var = sigma_stock**2
    merton_fraction = float(excess_return / (gamma * stock_var))

    growth_component = rf + (excess_return**2) / (2.0 * gamma * stock_var)
    optimal_consumption_ratio = float((rho + (gamma - 1.0) * growth_component) / gamma)

    return {
        "tangency_sharpe": tangency_sharpe,
        "hj_volatility_bound": hj_volatility_bound,
        "merton_fraction": merton_fraction,
        "optimal_consumption_ratio": optimal_consumption_ratio,
    }


def solve_econometrics_prelim(instance: dict[str, Any]) -> dict[str, Any]:
    ec = instance.get("econometrics", instance)
    returns = np.array(ec["returns"], dtype=np.float64)
    factors = np.array(ec["factors"], dtype=np.float64)
    t_obs, n_assets = returns.shape
    _, n_factors = factors.shape

    f_mean = np.mean(factors, axis=0)
    x_ts = np.column_stack([np.ones(t_obs), factors])
    x_ts_inv = np.linalg.inv(x_ts.T @ x_ts)

    alphas = np.zeros(n_assets)
    betas = np.zeros((n_assets, n_factors))
    residuals = np.zeros((t_obs, n_assets))

    for i in range(n_assets):
        y = returns[:, i]
        coeff = x_ts_inv @ (x_ts.T @ y)
        alphas[i] = coeff[0]
        betas[i, :] = coeff[1:]
        residuals[:, i] = y - x_ts @ coeff

    sigma_eps = (residuals.T @ residuals) / float(t_obs)
    factors_centered = factors - f_mean
    sigma_f = (factors_centered.T @ factors_centered) / float(t_obs)

    mean_returns = np.mean(returns, axis=0)
    beta_cross_inv = np.linalg.inv(betas.T @ betas)
    risk_premia = beta_cross_inv @ (betas.T @ mean_returns)

    # DEFECT: Omits Shanken correction and beta estimation variance entirely,
    # returning uncorrected pure factor variance
    v_shanken = (1.0 / float(t_obs)) * sigma_f
    shanken_se = np.sqrt(np.diag(v_shanken))

    sigma_f_inv = np.linalg.inv(sigma_f)
    sigma_eps_inv = np.linalg.inv(sigma_eps)
    f_factor = float(1.0 + f_mean @ sigma_f_inv @ f_mean)
    alpha_quad = float(alphas @ sigma_eps_inv @ alphas)
    df_numerator = float(n_assets)
    df_denominator = float(t_obs - n_assets - n_factors)
    grs_stat = float((df_denominator / df_numerator) * (alpha_quad / f_factor))

    gmm_n_obs = int(ec["gmm_n_obs"])
    gmm_moments = int(ec["gmm_moments"])
    gmm_params = int(ec["gmm_params"])
    sample_g = np.array(ec["sample_g"], dtype=np.float64)
    w_mat = np.array(ec["weighting_matrix"], dtype=np.float64)

    hansen_j_stat = float(gmm_n_obs * (sample_g @ w_mat @ sample_g))
    df_j = gmm_moments - gmm_params
    j_pvalue = float(chi2.sf(hansen_j_stat, df_j))

    return {
        "risk_premia": [float(x) for x in risk_premia],
        "shanken_se": [float(x) for x in shanken_se],
        "grs_stat": grs_stat,
        "hansen_j_stat": hansen_j_stat,
        "j_pvalue": j_pvalue,
    }


def solve_macro_prelim(instance: dict[str, Any]) -> dict[str, Any]:
    mc = instance.get("macro", instance)
    delta_f = float(mc["futures_price_change"])
    day = int(mc["announcement_day"])
    days_in_month = int(mc["days_in_month"])

    scale_factor = float(days_in_month) / float(days_in_month - day)
    kuttner_surprise = float(scale_factor * delta_f)

    beta_discount = float(mc["beta_discount"])
    kappa_slope = float(mc["kappa_slope"])
    phi_pi = float(mc["phi_pi"])
    phi_y = float(mc["phi_y"])

    taylor_metric = float(phi_pi + ((1.0 - beta_discount) / kappa_slope) * phi_y)
    is_determinate = bool(taylor_metric > 1.0)

    shocks = np.array(mc["shocks"], dtype=np.float64)
    outcomes = np.array(mc["outcomes"], dtype=np.float64)
    max_horizon = int(mc["max_horizon"])
    t_lp = len(shocks)

    lp_irf: list[float] = []
    for h in range(max_horizon + 1):
        t_valid = t_lp - h
        y_change = outcomes[h:t_lp] - outcomes[:t_valid]
        s_reg = shocks[:t_valid]
        cov_val = float(np.mean((y_change - np.mean(y_change)) * (s_reg - np.mean(s_reg))))
        s_var = float(np.var(s_reg))
        slope = cov_val / s_var if s_var > 1e-12 else 0.0
        lp_irf.append(float(slope))

    return {
        "kuttner_surprise": kuttner_surprise,
        "taylor_metric": taylor_metric,
        "is_determinate": is_determinate,
        "lp_impulse_responses": lp_irf,
    }
