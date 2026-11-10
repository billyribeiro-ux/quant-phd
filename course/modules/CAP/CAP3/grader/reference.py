"""Reference solution for CAP3: Qualifying Examination Capstone Grader.

Implements full doctoral-grade solutions for the three field prelims:
1. Field Prelim I: Asset Pricing & Continuous-Time Valuation
2. Field Prelim II: Cross-Sectional & Time-Series Econometrics
3. Field Prelim III: Dynamic General Equilibrium & Monetary Macro
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import chi2


def solve_asset_pricing_prelim(instance: dict[str, Any]) -> dict[str, Any]:
    """Solve Field Prelim I: Asset Pricing & Continuous-Time Valuation.

    Calculates:
    - Tangency portfolio Sharpe ratio: sqrt(mu^T Sigma^{-1} mu)
    - Hansen-Jagannathan SDF volatility lower bound: E[m] * sqrt(mu^T Sigma^{-1} mu)
    - Merton continuous-time portfolio fraction: (mu - rf) / (gamma * sigma^2)
    - Merton infinite-horizon consumption propensity:
      [rho + (gamma - 1)(rf + (mu - rf)^2 / (2 * gamma * sigma^2))] / gamma
    """
    ap = instance.get("asset_pricing", instance)
    mu = np.array(ap["mu"], dtype=np.float64)
    sigma = np.array(ap["sigma"], dtype=np.float64)
    rf = float(ap["rf"])
    gamma = float(ap["gamma"])
    mu_stock = float(ap["mu_stock"])
    sigma_stock = float(ap["sigma_stock"])
    rho = float(ap["rho"])

    # 1. Hansen-Jagannathan bound
    sigma_inv = np.linalg.inv(sigma)
    tangency_sharpe = float(np.sqrt(mu @ sigma_inv @ mu))
    mean_sdf = 1.0 / (1.0 + rf)
    hj_volatility_bound = float(mean_sdf * tangency_sharpe)

    # 2. Merton continuous-time portfolio & consumption policy
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
    """Solve Field Prelim II: Cross-Sectional & Time-Series Econometrics.

    Calculates:
    - Fama-MacBeth risk premia with Shanken asymptotic standard errors
    - Gibbons-Ross-Shanken (GRS) test statistic for factor efficiency
    - GMM Hansen J-test statistic and chi-squared p-value
    """
    ec = instance.get("econometrics", instance)
    returns = np.array(ec["returns"], dtype=np.float64)  # T x N
    factors = np.array(ec["factors"], dtype=np.float64)  # T x K
    t_obs, n_assets = returns.shape
    _, n_factors = factors.shape

    # First pass: Time-series regressions R_{i,t} = alpha_i + beta_i' f_t + eps_{i,t}
    f_mean = np.mean(factors, axis=0)  # length K
    x_ts = np.column_stack([np.ones(t_obs), factors])  # T x (K+1)
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

    # Covariance matrices
    sigma_eps = (residuals.T @ residuals) / float(t_obs)
    factors_centered = factors - f_mean
    sigma_f = (factors_centered.T @ factors_centered) / float(t_obs)

    # Second pass: Cross-sectional regression of mean returns on betas (no intercept)
    mean_returns = np.mean(returns, axis=0)  # length N
    beta_cross_inv = np.linalg.inv(betas.T @ betas)
    risk_premia = beta_cross_inv @ (betas.T @ mean_returns)  # length K

    # Shanken (1992) standard error correction
    sigma_f_inv = np.linalg.inv(sigma_f)
    shanken_factor = float(1.0 + risk_premia @ sigma_f_inv @ risk_premia)
    v_shanken = (1.0 / float(t_obs)) * (
        sigma_f + shanken_factor * (beta_cross_inv @ (betas.T @ sigma_eps @ betas) @ beta_cross_inv)
    )
    shanken_se = np.sqrt(np.diag(v_shanken))

    # GRS (1989) test statistic
    sigma_eps_inv = np.linalg.inv(sigma_eps)
    f_factor = float(1.0 + f_mean @ sigma_f_inv @ f_mean)
    alpha_quad = float(alphas @ sigma_eps_inv @ alphas)
    df_numerator = float(n_assets)
    df_denominator = float(t_obs - n_assets - n_factors)
    grs_stat = float((df_denominator / df_numerator) * (alpha_quad / f_factor))

    # GMM Hansen J-test
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
    """Solve Field Prelim III: Dynamic General Equilibrium & Monetary Macro.

    Calculates:
    - Kuttner (2001) high-frequency Fed funds target surprise with month scaling
    - New Keynesian 3-equation Taylor principle determinacy criterion
    - Jordà (2005) local projections impulse responses
    """
    mc = instance.get("macro", instance)
    delta_f = float(mc["futures_price_change"])
    day = int(mc["announcement_day"])
    days_in_month = int(mc["days_in_month"])

    # 1. Kuttner futures scaling
    scale_factor = float(days_in_month) / float(days_in_month - day)
    kuttner_surprise = float(scale_factor * delta_f)

    # 2. New Keynesian determinacy: Taylor principle
    beta_discount = float(mc["beta_discount"])
    kappa_slope = float(mc["kappa_slope"])
    phi_pi = float(mc["phi_pi"])
    phi_y = float(mc["phi_y"])

    taylor_metric = float(phi_pi + ((1.0 - beta_discount) / kappa_slope) * phi_y)
    is_determinate = bool(taylor_metric > 1.0)

    # 3. Local projections impulse responses
    shocks = np.array(mc["shocks"], dtype=np.float64)
    outcomes = np.array(mc["outcomes"], dtype=np.float64)
    max_horizon = int(mc["max_horizon"])
    t_lp = len(shocks)

    lp_irf: list[float] = []

    for h in range(max_horizon + 1):
        # Dependent variable: y_{t+h} - y_{t-1}
        # Regressor: shock_t
        t_valid = t_lp - h
        y_change = outcomes[h:t_lp] - outcomes[:t_valid]  # from t to t+h relative to t-1
        s_reg = shocks[:t_valid]

        # OLS slope = Cov(y_change, s_reg) / Var(s_reg)
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
