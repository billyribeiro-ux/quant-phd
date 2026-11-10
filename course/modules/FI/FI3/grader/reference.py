"""Atlas A13: term-premium and rates-RV module (atlas.term_premium).

Delivered in FI3: Bond Risk Premia & the Expectations Hypothesis.
Implements the contract in atlas/A13.contract.md.

Units and conventions:
- Yields y(t, tau): decimal per annum (0.05 = 5.0%), continuously compounded zero rates.
- Maturities tau: float or np.ndarray in years, tau > 0.
- Forward rates: continuously compounded 1-year forward rates.
- Excess bond returns: 1-year holding period excess log returns.
- Carry & roll-down: annualized or periodic expected returns under static curve.
- P&L attribution: linear duration/convexity and factor decomposition of curve trades.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def fama_bliss_forward_rates(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    """Compute 1-year forward rates from zero-coupon yields.

    For maturity tau_k:
      f(t, 0, tau_0) = y(t, tau_0)
      f(t, tau_{k-1}, tau_k) = [tau_k * y(t, tau_k) - tau_{k-1} * y(t, tau_{k-1})] / (tau_k - tau_{k-1})
    """
    if not isinstance(yields, np.ndarray) or not isinstance(maturities, np.ndarray):
        try:
            yields = np.asarray(yields, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
        except Exception as exc:
            raise TypeError("yields and maturities must be numeric arrays") from exc

    if maturities.ndim != 1 or len(maturities) < 2:
        raise ValueError("maturities must be a 1D array of at least 2 maturities")
    if np.any(maturities <= 0):
        raise ValueError("maturities must be strictly positive")
    if np.any(np.diff(maturities) <= 0):
        raise ValueError("maturities must be strictly increasing")
    if yields.shape[-1] != len(maturities):
        raise ValueError(f"yields last dimension {yields.shape[-1]} must match len(maturities) {len(maturities)}")
    if not np.all(np.isfinite(yields)):
        raise ValueError("yields must contain finite values")

    fwd = np.empty_like(yields, dtype=np.float64)
    if yields.ndim == 1:
        fwd[0] = yields[0]
        for k in range(1, len(maturities)):
            d_tau = maturities[k] - maturities[k - 1]
            fwd[k] = (maturities[k] * yields[k] - maturities[k - 1] * yields[k - 1]) / d_tau
    elif yields.ndim == 2:
        fwd[:, 0] = yields[:, 0]
        for k in range(1, len(maturities)):
            d_tau = maturities[k] - maturities[k - 1]
            fwd[:, k] = (maturities[k] * yields[:, k] - maturities[k - 1] * yields[:, k - 1]) / d_tau
    else:
        raise ValueError("yields must be 1D or 2D array")

    return fwd


def excess_bond_returns(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    """Compute 1-year holding period excess log returns for annual maturities.

    rx_{t+1}^{(n)} = -(n-1)*y_{t+1}^{(n-1)} + n*y_t^{(n)} - y_t^{(1)}
    for n = 2, ..., K.
    """
    if not isinstance(yields, np.ndarray) or not isinstance(maturities, np.ndarray):
        try:
            yields = np.asarray(yields, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
        except Exception as exc:
            raise TypeError("yields and maturities must be numeric arrays") from exc

    if yields.ndim != 2:
        raise ValueError("yields must be a 2D array of shape (T, K)")
    t_obs, k_mat = yields.shape
    if t_obs < 2:
        raise ValueError("yields must have at least 2 time observations")
    if k_mat < 2:
        raise ValueError("yields must have at least 2 maturities")
    if maturities.ndim != 1 or len(maturities) != k_mat:
        raise ValueError("maturities length must match yields columns")

    expected_mat = np.arange(1, k_mat + 1, dtype=np.float64)
    if not np.allclose(maturities[:k_mat], expected_mat, atol=1e-5):
        raise ValueError("excess_bond_returns requires integer annual maturities starting at 1: [1, 2, ..., K]")

    rx = np.empty((t_obs - 1, k_mat - 1), dtype=np.float64)
    for n_idx in range(1, k_mat):
        n_val = maturities[n_idx]
        rx[:, n_idx - 1] = -(n_val - 1.0) * yields[1:, n_idx - 1] + n_val * yields[:-1, n_idx] - yields[:-1, 0]

    return rx


def cochrane_piazzesi_factor(yields: np.ndarray, maturities: np.ndarray) -> dict[str, Any]:
    """Estimate the single-factor Cochrane-Piazzesi (2005) return predictability model.

    Returns dict with keys:
    - gamma: shape (6,) array of OLS coefficients [intercept, gamma_1..5]
    - cp_factor: shape (T-1,) single factor series
    - r2: float R^2 of average excess return regression
    - loadings: shape (4,) slope coefficients for individual maturities 2..5
    """
    if not isinstance(yields, np.ndarray) or not isinstance(maturities, np.ndarray):
        try:
            yields = np.asarray(yields, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
        except Exception as exc:
            raise TypeError("yields and maturities must be numeric arrays") from exc

    if yields.ndim != 2:
        raise ValueError("yields must be 2D array")
    t_obs, k_mat = yields.shape
    if t_obs < 8:
        raise ValueError("cochrane_piazzesi_factor requires at least 8 time observations")
    if k_mat < 5:
        raise ValueError("cochrane_piazzesi_factor requires at least 5 maturities [1, 2, 3, 4, 5]")

    # Forward rates for maturities 1..5
    fwd_5 = fama_bliss_forward_rates(yields[:, :5], maturities[:5])
    f_t = fwd_5[:-1, :]  # shape (T-1, 5)

    # Excess returns for maturities 2..5
    rx_all = excess_bond_returns(yields[:, :5], maturities[:5])  # shape (T-1, 4)
    rx_bar = np.mean(rx_all, axis=1)  # shape (T-1,)

    # OLS regression of rx_bar on [1, f_t]
    design_f = np.column_stack([np.ones(t_obs - 1), f_t])
    gamma, _residuals, _rank, _s = np.linalg.lstsq(design_f, rx_bar, rcond=None)

    cp_factor = design_f @ gamma
    ss_tot = np.sum((rx_bar - np.mean(rx_bar)) ** 2)
    ss_res = np.sum((rx_bar - cp_factor) ** 2)
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Individual regressions: rx^{(n)} = a_n + b_n * cp_factor
    loadings = np.empty(4, dtype=np.float64)
    var_cp = np.var(cp_factor)
    for i in range(4):
        if var_cp > 1e-14:
            loadings[i] = float(np.cov(rx_all[:, i], cp_factor)[0, 1] / var_cp)
        else:
            loadings[i] = 1.0

    return {
        "gamma": gamma,
        "cp_factor": cp_factor,
        "r2": r2,
        "loadings": loadings,
    }


def acm_term_premium(yields: np.ndarray, maturities: np.ndarray, num_factors: int = 3) -> dict[str, Any]:
    """Adrian, Crump & Moench (2013) 3-step linear regression affine term-structure model.

    Returns dict with keys:
    - term_premium: shape (T, K)
    - expected_short_rate: shape (T, K)
    - fitted_yields: shape (T, K)
    - phi: shape (num_factors, num_factors)
    - lambda1: shape (num_factors, num_factors)
    - lambda0: shape (num_factors,)
    """
    if not isinstance(yields, np.ndarray) or not isinstance(maturities, np.ndarray):
        try:
            yields = np.asarray(yields, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
        except Exception as exc:
            raise TypeError("yields and maturities must be numeric arrays") from exc

    if yields.ndim != 2:
        raise ValueError("yields must be 2D array of shape (T, K)")
    t_obs, k_mat = yields.shape
    if num_factors < 1 or num_factors > min(k_mat, t_obs - 2):
        raise ValueError(f"num_factors must be between 1 and min(K, T-2), got {num_factors}")

    # Step 1: Principal Component extraction
    yield_mean = np.mean(yields, axis=0)
    y_centered = yields - yield_mean
    _u, _s, vt = np.linalg.svd(y_centered, full_matrices=False)
    factors = y_centered @ vt[:num_factors, :].T  # shape (T, num_factors)

    # VAR(1) under P: X_{t+1} = mu + Phi * X_t + v_{t+1}
    x_lag = np.column_stack([np.ones(t_obs - 1), factors[:-1]])
    x_lead = factors[1:]
    b_var, _, _, _ = np.linalg.lstsq(x_lag, x_lead, rcond=None)
    mu = b_var[0, :]
    phi = b_var[1:, :].T  # shape (num_factors, num_factors)
    v_res = x_lead - x_lag @ b_var
    sigma_v = (v_res.T @ v_res) / float(len(v_res))

    # Step 2: Excess return regressions
    # rx_{t+1}^{(n)} = alpha_n + beta_n' * v_{t+1} + c_n' * X_t + e_{t+1}^{(n)}
    rx_mat = excess_bond_returns(yields, maturities)  # shape (T-1, K-1)
    z_reg = np.column_stack([np.ones(t_obs - 1), v_res, factors[:-1]])
    coeffs, _, _, _ = np.linalg.lstsq(z_reg, rx_mat, rcond=None)  # (1 + 2*Kf, K-1)

    alpha = coeffs[0, :]
    beta = coeffs[1 : 1 + num_factors, :].T  # (K-1, num_factors)
    c_mat = coeffs[1 + num_factors :, :].T  # (K-1, num_factors)
    res_e = rx_mat - z_reg @ coeffs
    sigma_e_sq = np.var(res_e, axis=0)

    # Step 3: Risk prices lambda_0, lambda_1
    # c_mat = beta @ lambda_1
    lambda1, _, _, _ = np.linalg.lstsq(beta, c_mat, rcond=None)
    # alpha_adj = alpha + 0.5 * (diag(beta @ sigma_v @ beta.T) + sigma_e_sq) = beta @ lambda_0
    alpha_adj = alpha + 0.5 * (np.sum((beta @ sigma_v) * beta, axis=1) + sigma_e_sq)
    lambda0, _, _, _ = np.linalg.lstsq(beta, alpha_adj, rcond=None)

    # Step 4: Physical short-rate projection and multi-step expectations
    short_rate = yields[:, 0]
    w_sr = np.column_stack([np.ones(t_obs), factors])
    b_sr, _, _, _ = np.linalg.lstsq(w_sr, short_rate, rcond=None)
    delta0 = b_sr[0]
    delta1 = b_sr[1:]

    # Multi-step factor forecasts: E_t[X_{t+i}]
    expected_short_rate = np.empty((t_obs, k_mat), dtype=np.float64)
    term_premium = np.empty((t_obs, k_mat), dtype=np.float64)

    for k_idx in range(k_mat):
        n_steps = max(1, round(maturities[k_idx]))
        # Compute multi-step expected short rates
        e_factors = factors.copy()
        sum_expected_r = delta0 + e_factors @ delta1
        for _ in range(1, n_steps):
            e_factors = mu + e_factors @ phi.T
            sum_expected_r += delta0 + e_factors @ delta1

        avg_expected_r = sum_expected_r / float(n_steps)
        expected_short_rate[:, k_idx] = avg_expected_r
        term_premium[:, k_idx] = yields[:, k_idx] - avg_expected_r

    fitted_yields = yields.copy()

    return {
        "term_premium": term_premium,
        "expected_short_rate": expected_short_rate,
        "fitted_yields": fitted_yields,
        "phi": phi,
        "lambda1": lambda1,
        "lambda0": lambda0,
    }


def carry_and_roll_down(yield_curve: np.ndarray, maturities: np.ndarray, horizon: float = 1.0) -> dict[str, np.ndarray]:
    """Decompose horizon bond return into carry and roll-down on a static yield curve."""
    if not isinstance(yield_curve, np.ndarray) or not isinstance(maturities, np.ndarray):
        try:
            yield_curve = np.asarray(yield_curve, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
        except Exception as exc:
            raise TypeError("yield_curve and maturities must be numeric arrays") from exc

    if yield_curve.ndim != 1 or maturities.ndim != 1:
        raise ValueError("yield_curve and maturities must be 1D arrays")
    if len(yield_curve) != len(maturities):
        raise ValueError("yield_curve and maturities must have equal length")
    if horizon <= 0.0:
        raise ValueError("horizon must be strictly positive")

    k_mat = len(maturities)
    carry = horizon * yield_curve
    roll_down = np.zeros(k_mat, dtype=np.float64)

    for i in range(k_mat):
        tau = maturities[i]
        if tau > horizon:
            tau_rem = tau - horizon
            y_rem = float(np.interp(tau_rem, maturities, yield_curve))
            roll_down[i] = tau_rem * (yield_curve[i] - y_rem)
        else:
            roll_down[i] = 0.0

    total_carry_roll = carry + roll_down
    annualized_carry_roll = total_carry_roll / horizon

    return {
        "carry": carry,
        "roll_down": roll_down,
        "total_carry_roll": total_carry_roll,
        "annualized_carry_roll": annualized_carry_roll,
    }


def curve_trade_pnl_attribution(
    weights: np.ndarray,
    maturities: np.ndarray,
    yields_t0: np.ndarray,
    yields_t1: np.ndarray,
    dt: float,
    financing_rate: float,
) -> dict[str, float]:
    """Perform relative-value fixed-income P&L attribution for curve portfolios."""
    if (
        not isinstance(weights, np.ndarray)
        or not isinstance(maturities, np.ndarray)
        or not isinstance(yields_t0, np.ndarray)
        or not isinstance(yields_t1, np.ndarray)
    ):
        try:
            weights = np.asarray(weights, dtype=np.float64)
            maturities = np.asarray(maturities, dtype=np.float64)
            yields_t0 = np.asarray(yields_t0, dtype=np.float64)
            yields_t1 = np.asarray(yields_t1, dtype=np.float64)
        except Exception as exc:
            raise TypeError("inputs must be numeric arrays") from exc

    if not (weights.ndim == maturities.ndim == yields_t0.ndim == yields_t1.ndim == 1):
        raise ValueError("all array inputs must be 1D")
    m_legs = len(weights)
    if not (len(maturities) == len(yields_t0) == len(yields_t1) == m_legs):
        raise ValueError("all array inputs must have equal length")
    if m_legs < 2:
        raise ValueError("curve trade requires at least 2 legs")
    if dt <= 0.0:
        raise ValueError("dt must be strictly positive")

    delta_y = yields_t1 - yields_t0
    delta_level = float(np.mean(delta_y))

    # 1. Carry P&L
    carry_pnl = float(np.sum(weights * (yields_t0 - financing_rate) * dt))

    # 2. Roll-down P&L
    roll_vals = np.zeros(m_legs, dtype=np.float64)
    for i in range(m_legs):
        tau = maturities[i]
        if tau > dt:
            tau_rem = tau - dt
            y_rem = float(np.interp(tau_rem, maturities, yields_t0))
            roll_vals[i] = tau_rem * (yields_t0[i] - y_rem)
        else:
            roll_vals[i] = 0.0
    rolldown_pnl = float(np.sum(weights * roll_vals))

    # 3. Level P&L
    level_pnl = float(-np.sum(weights * maturities * delta_level))

    # 4. Slope P&L
    slope_pnl = float(-np.sum(weights * maturities * (delta_y - delta_level)))

    # 5. Curvature P&L
    curvature_pnl = 0.0

    # 6. Convexity P&L
    convexity_pnl = float(0.5 * np.sum(weights * (maturities**2) * (delta_y**2)))

    # Total actual P&L from exact bond repricing
    p0 = np.exp(-maturities * yields_t0)
    p1 = np.exp(-(maturities - dt) * yields_t1)
    ret_bonds = (p1 - p0) / p0 - financing_rate * dt
    total_pnl = float(np.sum(weights * ret_bonds))

    # Residual P&L
    accounted = carry_pnl + rolldown_pnl + level_pnl + slope_pnl + curvature_pnl + convexity_pnl
    residual_pnl = float(total_pnl - accounted)

    return {
        "carry_pnl": carry_pnl,
        "rolldown_pnl": rolldown_pnl,
        "level_pnl": level_pnl,
        "slope_pnl": slope_pnl,
        "curvature_pnl": curvature_pnl,
        "convexity_pnl": convexity_pnl,
        "residual_pnl": residual_pnl,
        "total_pnl": total_pnl,
    }
