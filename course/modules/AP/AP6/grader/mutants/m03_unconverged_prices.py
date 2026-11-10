"""Mutant 03: Omits iterative price adjustment loop, returning initial un-cleared price guess."""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_intermediary_sdf(returns_excess: np.ndarray, capital_ratio: np.ndarray) -> dict[str, Any]:
    eta_lag = capital_ratio[:-1]
    eta_curr = capital_ratio[1:]
    t_len = len(eta_curr)
    x_ar = np.column_stack([np.ones(t_len), eta_lag])
    theta_ar = np.linalg.lstsq(x_ar, eta_curr, rcond=None)[0]
    phi = float(theta_ar[1])
    innovations = eta_curr - x_ar @ theta_ar
    if len(innovations) != returns_excess.shape[0]:
        innovations = innovations[-returns_excess.shape[0] :]
    var_u = float(np.var(innovations, ddof=1))
    n_assets = returns_excess.shape[1]
    betas = np.zeros(n_assets)
    for j in range(n_assets):
        cov_ju = float(np.cov(returns_excess[:, j], innovations)[0, 1])
        betas[j] = cov_ju / var_u
    mean_returns = np.mean(returns_excess, axis=0)
    beta_dot_beta = float(betas @ betas)
    risk_price = float((betas @ mean_returns) / beta_dot_beta)
    alpha = mean_returns - risk_price * betas
    mse = float(np.mean(alpha**2))
    tss = float(np.sum((mean_returns - np.mean(mean_returns)) ** 2))
    r2_cross = float(1.0 - np.sum(alpha**2) / tss) if tss > 1e-12 else 0.0
    b_eta = float(risk_price / var_u)
    return {
        "phi": phi,
        "innovations": innovations,
        "betas": betas,
        "risk_price": risk_price,
        "alpha": alpha,
        "r2_cross": r2_cross,
        "b_eta": b_eta,
        "mse": mse,
    }


def estimate_koijen_yogo_demand(
    holdings_weights: np.ndarray,
    log_prices: np.ndarray,
    characteristics: np.ndarray,
    instruments: np.ndarray,
) -> dict[str, Any]:
    n_institutions, n_stocks = holdings_weights.shape
    k_chars = characteristics.shape[1]
    w_first = np.column_stack([np.ones(n_stocks), instruments, characteristics])
    gamma_first = np.linalg.lstsq(w_first, log_prices, rcond=None)[0]
    hat_log_p = w_first @ gamma_first
    res_unrestricted = log_prices - hat_log_p
    ssr_ur = float(np.sum(res_unrestricted**2))
    w_restricted = np.column_stack([np.ones(n_stocks), characteristics])
    gamma_restr = np.linalg.lstsq(w_restricted, log_prices, rcond=None)[0]
    ssr_r = float(np.sum((log_prices - w_restricted @ gamma_restr) ** 2))
    q_df = instruments.shape[1]
    df_resid = n_stocks - w_first.shape[1]
    f_stat = float(((ssr_r - ssr_ur) / q_df) / (ssr_ur / df_resid)) if ssr_ur > 1e-12 else 999.0

    elasticities = np.zeros(n_institutions)
    alphas = np.zeros(n_institutions)
    gammas = np.zeros((n_institutions, k_chars))
    residuals = np.zeros((n_institutions, n_stocks))
    m_second = np.column_stack([np.ones(n_stocks), -hat_log_p, characteristics])
    m_actual = np.column_stack([np.ones(n_stocks), -log_prices, characteristics])

    for i in range(n_institutions):
        outside_weight = max(1.0 - float(np.sum(holdings_weights[i, :])), 1e-4)
        y_i = np.log(holdings_weights[i, :] / outside_weight)
        theta_i = np.linalg.lstsq(m_second, y_i, rcond=None)[0]
        alphas[i] = float(theta_i[0])
        elasticities[i] = float(theta_i[1])
        gammas[i, :] = theta_i[2:]
        residuals[i, :] = y_i - m_actual @ theta_i

    return {
        "first_stage_f": f_stat,
        "elasticities": elasticities,
        "alphas": alphas,
        "gammas": gammas,
        "residuals": residuals,
    }


def solve_market_clearing_prices(
    aum: np.ndarray,
    shares_out: np.ndarray,
    alpha_i: np.ndarray,
    beta_i: np.ndarray,
    char_effects: np.ndarray,
    tol: float = 1e-7,
    max_iter: int = 500,
) -> np.ndarray:
    # BUG: skips fixed point iteration and returns initial heuristic guess
    n_stocks = len(shares_out)
    total_aum = float(np.sum(aum))
    p_log = np.log(total_aum / (n_stocks * shares_out))
    return np.exp(p_log)


def compute_flow_multiplier(aum_shares: np.ndarray, elasticities: np.ndarray) -> dict[str, float]:
    zeta_m = float(np.sum(aum_shares * elasticities))
    m_multiplier = float(1.0 / zeta_m) if zeta_m > 1e-8 else 999.0
    return {"aggregate_elasticity": zeta_m, "flow_multiplier": m_multiplier}


def estimate_index_event_impact(
    pre_prices: np.ndarray,
    post_prices: np.ndarray,
    flow_fractions: np.ndarray,
) -> dict[str, Any]:
    delta_log_p = np.log(post_prices) - np.log(pre_prices)
    mean_car = float(np.mean(delta_log_p))
    k_len = len(flow_fractions)
    x_mat = np.column_stack([np.ones(k_len), flow_fractions])
    coefs = np.linalg.lstsq(x_mat, delta_log_p, rcond=None)[0]
    intercept = float(coefs[0])
    multiplier = float(coefs[1])
    stock_elasticity = float(1.0 / multiplier) if abs(multiplier) > 1e-8 else 0.0
    residuals = delta_log_p - x_mat @ coefs
    tss = float(np.sum((delta_log_p - mean_car) ** 2))
    r2 = float(1.0 - np.sum(residuals**2) / tss) if tss > 1e-12 else 0.0
    return {
        "multiplier": multiplier,
        "intercept": intercept,
        "stock_elasticity": stock_elasticity,
        "r2": r2,
        "mean_car": mean_car,
    }
