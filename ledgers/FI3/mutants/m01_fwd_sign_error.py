"""Mutant 1: Inverts sign in discrete forward rate calculation."""

from __future__ import annotations

from typing import Any

import numpy as np


def fama_bliss_forward_rates(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    yields = np.asarray(yields, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    if maturities.ndim != 1 or len(maturities) < 2:
        raise ValueError("maturities must be a 1D array of at least 2 maturities")
    if np.any(maturities <= 0) or np.any(np.diff(maturities) <= 0):
        raise ValueError("maturities must be strictly increasing positive")
    if yields.shape[-1] != len(maturities):
        raise ValueError("dimension mismatch")
    if not np.all(np.isfinite(yields)):
        raise ValueError("yields must be finite")

    fwd = np.empty_like(yields, dtype=np.float64)
    if yields.ndim == 1:
        fwd[0] = yields[0]
        for k in range(1, len(maturities)):
            d_tau = maturities[k] - maturities[k - 1]
            # BUG: inverted numerator
            fwd[k] = (maturities[k - 1] * yields[k - 1] - maturities[k] * yields[k]) / d_tau
    elif yields.ndim == 2:
        fwd[:, 0] = yields[:, 0]
        for k in range(1, len(maturities)):
            d_tau = maturities[k] - maturities[k - 1]
            # BUG: inverted numerator
            fwd[:, k] = (maturities[k - 1] * yields[:, k - 1] - maturities[k] * yields[:, k]) / d_tau
    else:
        raise ValueError("yields must be 1D or 2D array")
    return fwd


def excess_bond_returns(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    yields = np.asarray(yields, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    if yields.ndim != 2:
        raise ValueError("yields must be 2D")
    t_obs, k_mat = yields.shape
    if t_obs < 2 or k_mat < 2:
        raise ValueError("dimensions too small")
    if len(maturities) != k_mat or not np.allclose(maturities, np.arange(1, k_mat + 1)):
        raise ValueError("maturities must be integer annual grid")
    rx = np.empty((t_obs - 1, k_mat - 1), dtype=np.float64)
    for n_idx in range(1, k_mat):
        n_val = maturities[n_idx]
        rx[:, n_idx - 1] = -(n_val - 1.0) * yields[1:, n_idx - 1] + n_val * yields[:-1, n_idx] - yields[:-1, 0]
    return rx


def cochrane_piazzesi_factor(yields: np.ndarray, maturities: np.ndarray) -> dict[str, Any]:
    yields = np.asarray(yields, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    t_obs, _ = yields.shape
    fwd_5 = fama_bliss_forward_rates(yields[:, :5], maturities[:5])
    f_t = fwd_5[:-1, :]
    rx_all = excess_bond_returns(yields[:, :5], maturities[:5])
    rx_bar = np.mean(rx_all, axis=1)
    design_f = np.column_stack([np.ones(t_obs - 1), f_t])
    gamma, _, _, _ = np.linalg.lstsq(design_f, rx_bar, rcond=None)
    cp_factor = design_f @ gamma
    ss_tot = np.sum((rx_bar - np.mean(rx_bar)) ** 2)
    ss_res = np.sum((rx_bar - cp_factor) ** 2)
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0
    loadings = np.empty(4, dtype=np.float64)
    var_cp = np.var(cp_factor)
    for i in range(4):
        loadings[i] = float(np.cov(rx_all[:, i], cp_factor)[0, 1] / var_cp) if var_cp > 1e-14 else 1.0
    return {"gamma": gamma, "cp_factor": cp_factor, "r2": r2, "loadings": loadings}


def acm_term_premium(yields: np.ndarray, maturities: np.ndarray, num_factors: int = 3) -> dict[str, Any]:
    yields = np.asarray(yields, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    t_obs, k_mat = yields.shape
    y_centered = yields - np.mean(yields, axis=0)
    _, _, vt = np.linalg.svd(y_centered, full_matrices=False)
    factors = y_centered @ vt[:num_factors, :].T
    x_lag = np.column_stack([np.ones(t_obs - 1), factors[:-1]])
    x_lead = factors[1:]
    b_var, _, _, _ = np.linalg.lstsq(x_lag, x_lead, rcond=None)
    mu = b_var[0, :]
    phi = b_var[1:, :].T
    v_res = x_lead - x_lag @ b_var
    sigma_v = (v_res.T @ v_res) / float(len(v_res))
    rx_mat = excess_bond_returns(yields, maturities)
    z_reg = np.column_stack([np.ones(t_obs - 1), v_res, factors[:-1]])
    coeffs, _, _, _ = np.linalg.lstsq(z_reg, rx_mat, rcond=None)
    alpha = coeffs[0, :]
    beta = coeffs[1 : 1 + num_factors, :].T
    c_mat = coeffs[1 + num_factors :, :].T
    res_e = rx_mat - z_reg @ coeffs
    sigma_e_sq = np.var(res_e, axis=0)
    lambda1, _, _, _ = np.linalg.lstsq(beta, c_mat, rcond=None)
    alpha_adj = alpha + 0.5 * (np.sum((beta @ sigma_v) * beta, axis=1) + sigma_e_sq)
    lambda0, _, _, _ = np.linalg.lstsq(beta, alpha_adj, rcond=None)
    short_rate = yields[:, 0]
    w_sr = np.column_stack([np.ones(t_obs), factors])
    b_sr, _, _, _ = np.linalg.lstsq(w_sr, short_rate, rcond=None)
    delta0 = b_sr[0]
    delta1 = b_sr[1:]
    expected_short_rate = np.empty((t_obs, k_mat), dtype=np.float64)
    term_premium = np.empty((t_obs, k_mat), dtype=np.float64)
    for k_idx in range(k_mat):
        n_steps = max(1, round(maturities[k_idx]))
        e_factors = factors.copy()
        sum_expected_r = delta0 + e_factors @ delta1
        for _ in range(1, n_steps):
            e_factors = mu + e_factors @ phi.T
            sum_expected_r += delta0 + e_factors @ delta1
        avg_expected_r = sum_expected_r / float(n_steps)
        expected_short_rate[:, k_idx] = avg_expected_r
        term_premium[:, k_idx] = yields[:, k_idx] - avg_expected_r
    return {
        "term_premium": term_premium,
        "expected_short_rate": expected_short_rate,
        "fitted_yields": yields.copy(),
        "phi": phi,
        "lambda1": lambda1,
        "lambda0": lambda0,
    }


def carry_and_roll_down(yield_curve: np.ndarray, maturities: np.ndarray, horizon: float = 1.0) -> dict[str, np.ndarray]:
    yield_curve = np.asarray(yield_curve, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    k_mat = len(maturities)
    carry = horizon * yield_curve
    roll_down = np.zeros(k_mat, dtype=np.float64)
    for i in range(k_mat):
        tau = maturities[i]
        if tau > horizon:
            tau_rem = tau - horizon
            y_rem = float(np.interp(tau_rem, maturities, yield_curve))
            roll_down[i] = tau_rem * (yield_curve[i] - y_rem)
    total_carry_roll = carry + roll_down
    return {
        "carry": carry,
        "roll_down": roll_down,
        "total_carry_roll": total_carry_roll,
        "annualized_carry_roll": total_carry_roll / horizon,
    }


def curve_trade_pnl_attribution(
    weights: np.ndarray,
    maturities: np.ndarray,
    yields_t0: np.ndarray,
    yields_t1: np.ndarray,
    dt: float,
    financing_rate: float,
) -> dict[str, float]:
    weights = np.asarray(weights, dtype=np.float64)
    maturities = np.asarray(maturities, dtype=np.float64)
    yields_t0 = np.asarray(yields_t0, dtype=np.float64)
    yields_t1 = np.asarray(yields_t1, dtype=np.float64)
    m_legs = len(weights)
    delta_y = yields_t1 - yields_t0
    delta_level = float(np.mean(delta_y))
    carry_pnl = float(np.sum(weights * (yields_t0 - financing_rate) * dt))
    roll_vals = np.zeros(m_legs, dtype=np.float64)
    for i in range(m_legs):
        tau = maturities[i]
        if tau > dt:
            tau_rem = tau - dt
            y_rem = float(np.interp(tau_rem, maturities, yields_t0))
            roll_vals[i] = tau_rem * (yields_t0[i] - y_rem)
    rolldown_pnl = float(np.sum(weights * roll_vals))
    level_pnl = float(-np.sum(weights * maturities * delta_level))
    slope_pnl = float(-np.sum(weights * maturities * (delta_y - delta_level)))
    curvature_pnl = 0.0
    convexity_pnl = float(0.5 * np.sum(weights * (maturities**2) * (delta_y**2)))
    p0 = np.exp(-maturities * yields_t0)
    p1 = np.exp(-(maturities - dt) * yields_t1)
    ret_bonds = (p1 - p0) / p0 - financing_rate * dt
    total_pnl = float(np.sum(weights * ret_bonds))
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
