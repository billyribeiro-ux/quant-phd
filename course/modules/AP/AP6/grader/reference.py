"""Reference implementation for AP6 Flow-Impact Estimation & Inelastic Markets Engine.

Implements:
1. Intermediary Asset Pricing SDF (He, Kelly & Manela 2017; He & Krishnamurthy 2013)
2. Characteristics-Based Institutional Demand System (Koijen & Yogo 2019)
3. Contraction Fixed-Point Asset Market Clearing System
4. Aggregate Inelastic Markets Flow Multiplier (Gabaix & Koijen 2021)
5. Index Inclusion Flow Impact Event Estimator
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_intermediary_sdf(returns_excess: np.ndarray, capital_ratio: np.ndarray) -> dict[str, Any]:
    """Estimate primary dealer equity capital ratio SDF and cross-sectional factor pricing.

    Parameters
    ----------
    returns_excess : np.ndarray, shape (T, N)
        Excess returns of N test assets across T time periods.
    capital_ratio : np.ndarray, shape (T+1,)
        Intermediary aggregate equity capital ratio eta_t.

    Returns
    -------
    dict[str, Any]
        Dictionary containing AR(1) persistence, capital shocks, factor betas,
        cross-sectional risk price, pricing errors, cross-sectional R2, and SDF loading.
    """
    eta_lag = capital_ratio[:-1]
    eta_curr = capital_ratio[1:]
    t_len = len(eta_curr)

    # Estimate AR(1) process on intermediary capital ratio: eta_t = mu + phi * eta_{t-1} + u_t
    x_ar = np.column_stack([np.ones(t_len), eta_lag])
    theta_ar = np.linalg.lstsq(x_ar, eta_curr, rcond=None)[0]
    phi = float(theta_ar[1])
    innovations = eta_curr - x_ar @ theta_ar

    # Ensure length alignment with returns_excess
    if len(innovations) != returns_excess.shape[0]:
        innovations = innovations[-returns_excess.shape[0] :]

    var_u = float(np.var(innovations, ddof=1))
    n_assets = returns_excess.shape[1]

    # Compute time-series factor betas beta_i = Cov(R_i^e, u) / Var(u)
    betas = np.zeros(n_assets)
    for j in range(n_assets):
        cov_ju = float(np.cov(returns_excess[:, j], innovations)[0, 1])
        betas[j] = cov_ju / var_u

    mean_returns = np.mean(returns_excess, axis=0)

    # Cross-sectional pricing regression without intercept: E[R^e] = lambda_eta * beta
    # lambda_eta = (beta' beta)^(-1) beta' E[R^e]
    beta_dot_beta = float(betas @ betas)
    risk_price = float((betas @ mean_returns) / beta_dot_beta)

    # Pricing errors and cross-sectional R^2
    alpha = mean_returns - risk_price * betas
    mse = float(np.mean(alpha**2))
    tss = float(np.sum((mean_returns - np.mean(mean_returns)) ** 2))
    r2_cross = float(1.0 - np.sum(alpha**2) / tss) if tss > 1e-12 else 0.0

    # SDF loading b_eta = lambda_eta / Var(u)
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
    """Estimate characteristics-based demand system parameters via 2SLS IV regression.

    Parameters
    ----------
    holdings_weights : np.ndarray, shape (I, N)
        Portfolio weights for I institutional types across N assets.
    log_prices : np.ndarray, shape (N,)
        Log prices of N assets.
    characteristics : np.ndarray, shape (N, K)
        Asset characteristics (e.g. log market equity, book-to-market).
    instruments : np.ndarray, shape (N, L)
        Exogenous instruments correlated with prices but orthogonal to latent demand.

    Returns
    -------
    dict[str, Any]
        First-stage F-statistic, price elasticities, alphas, characteristic loadings,
        and regression residuals.
    """
    n_institutions, n_stocks = holdings_weights.shape
    k_chars = characteristics.shape[1]

    # First stage regression: log_p = c_1 + instruments * gamma_z + characteristics * gamma_x + v
    w_first = np.column_stack([np.ones(n_stocks), instruments, characteristics])
    gamma_first = np.linalg.lstsq(w_first, log_prices, rcond=None)[0]
    hat_log_p = w_first @ gamma_first

    # First stage F-statistic on instruments
    res_unrestricted = log_prices - hat_log_p
    ssr_ur = float(np.sum(res_unrestricted**2))

    w_restricted = np.column_stack([np.ones(n_stocks), characteristics])
    gamma_restr = np.linalg.lstsq(w_restricted, log_prices, rcond=None)[0]
    ssr_r = float(np.sum((log_prices - w_restricted @ gamma_restr) ** 2))

    q_df = instruments.shape[1]
    df_resid = n_stocks - w_first.shape[1]
    f_stat = float(((ssr_r - ssr_ur) / q_df) / (ssr_ur / df_resid)) if ssr_ur > 1e-12 else 999.0

    # Second stage regression for each institution
    # y_{i,n} = ln(w_{i,n} / w_{i,0}) = alpha_i - beta_i * hat_log_p + characteristics * gamma_i + e_i
    elasticities = np.zeros(n_institutions)
    alphas = np.zeros(n_institutions)
    gammas = np.zeros((n_institutions, k_chars))
    residuals = np.zeros((n_institutions, n_stocks))

    # Regressors with predicted price: [1, -hat_log_p, characteristics]
    m_second = np.column_stack([np.ones(n_stocks), -hat_log_p, characteristics])
    # Regressors with actual price for true 2SLS residuals: [1, -log_prices, characteristics]
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
    """Solve the non-linear market clearing system for equilibrium asset prices.

    Market clearing condition:
    sum_{i=1}^I A_i * w_{i,n}(p^*) = P_n^* * Q_n,  for each asset n = 1, ..., N.

    Parameters
    ----------
    aum : np.ndarray, shape (I,)
        Total AUM across institutional investor types.
    shares_out : np.ndarray, shape (N,)
        Shares outstanding Q_n for each asset.
    alpha_i : np.ndarray, shape (I,)
        Base demand intercepts.
    beta_i : np.ndarray, shape (I,)
        Price elasticity coefficients (beta_i > 0).
    char_effects : np.ndarray, shape (I, N)
        Pre-computed characteristic loadings X_n * gamma_i.
    tol : float, optional
        Convergence tolerance on sup-norm of price change.
    max_iter : int, optional
        Maximum contraction iterations.

    Returns
    -------
    np.ndarray, shape (N,)
        Equilibrium price vector P^* = exp(p^*).
    """
    n_stocks = len(shares_out)
    n_institutions = len(aum)
    log_q = np.log(shares_out)

    # Initial log price guess based on equal share of aggregate AUM
    total_aum = float(np.sum(aum))
    p_log = np.log(total_aum / (n_stocks * shares_out))
    omega = 0.5  # relaxation damping factor

    for _ in range(max_iter):
        # Compute portfolio weights for all institutions
        # delta_{i,n} = alpha_i - beta_i * p_n + char_{i,n}
        # w_{i,n} = exp(delta_{i,n}) / (1 + sum_k exp(delta_{i,k}))
        dollar_demand = np.zeros(n_stocks)
        for i in range(n_institutions):
            delta_i = alpha_i[i] - beta_i[i] * p_log + char_effects[i, :]
            # Subtract max for numerical stability
            max_delta = np.max(delta_i)
            exp_delta = np.exp(delta_i - max_delta)
            denom = np.exp(-max_delta) + np.sum(exp_delta)
            weights_i = exp_delta / denom
            dollar_demand += aum[i] * weights_i

        # Target log price satisfying P_n * Q_n = D_n => ln(P_n) = ln(D_n) - ln(Q_n)
        target_log_p = np.log(np.maximum(dollar_demand, 1e-10)) - log_q
        diff = np.max(np.abs(target_log_p - p_log))

        p_log = (1.0 - omega) * p_log + omega * target_log_p
        if diff < tol:
            break

    return np.exp(p_log)


def compute_flow_multiplier(aum_shares: np.ndarray, elasticities: np.ndarray) -> dict[str, float]:
    """Compute aggregate market elasticity and macro flow multiplier (Gabaix-Koijen 2021).

    zeta_m = sum_i s_i * zeta_i
    M = 1 / zeta_m

    Parameters
    ----------
    aum_shares : np.ndarray, shape (I,)
        Market share of total equity assets held by each institutional type.
    elasticities : np.ndarray, shape (I,)
        Price elasticity of demand for each institutional type.

    Returns
    -------
    dict[str, float]
        Dictionary with aggregate_elasticity and flow_multiplier.
    """
    zeta_m = float(np.sum(aum_shares * elasticities))
    m_multiplier = float(1.0 / zeta_m) if zeta_m > 1e-8 else 999.0
    return {
        "aggregate_elasticity": zeta_m,
        "flow_multiplier": m_multiplier,
    }


def estimate_index_event_impact(
    pre_prices: np.ndarray,
    post_prices: np.ndarray,
    flow_fractions: np.ndarray,
) -> dict[str, Any]:
    """Estimate empirical flow multiplier from index inclusion event study.

    Regresses cumulative abnormal return Delta ln(P_k) on flow shock Delta Q_k / Q_k.

    Parameters
    ----------
    pre_prices : np.ndarray, shape (K,)
        Stock prices prior to index inclusion announcement.
    post_prices : np.ndarray, shape (K,)
        Stock prices following inclusion effective date.
    flow_fractions : np.ndarray, shape (K,)
        Exogenous passive tracking flow as a fraction of shares outstanding.

    Returns
    -------
    dict[str, Any]
        Estimated price impact multiplier mu, intercept, stock elasticity, R^2, and mean CAR.
    """
    delta_log_p = np.log(post_prices) - np.log(pre_prices)
    mean_car = float(np.mean(delta_log_p))

    # OLS regression: Delta ln(P_k) = c + mu * flow_k + e_k
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
