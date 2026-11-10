"""Zeroes the initial period return R_0^true instead of preserving observed initial return.

Defect: Erroneously initializes recovered series at 0.0 instead of R_0^{obs}.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_smoothing_parameter(reported_returns: np.ndarray) -> float:
    if len(reported_returns) < 2:
        return 0.0
    r_t = reported_returns[1:]
    r_lag = reported_returns[:-1]
    cov = np.cov(r_t, r_lag)[0, 1]
    var_lag = np.var(r_lag, ddof=1)
    phi = float(cov / var_lag) if var_lag > 0 else 0.0
    return float(np.clip(phi, 0.0, 0.95))


def unsmooth_returns_ar1(reported_returns: np.ndarray, phi: float) -> np.ndarray:
    recovered = np.zeros_like(reported_returns, dtype=float)
    if len(reported_returns) == 0:
        return recovered
    # MUTANT 5 BUG: sets recovered[0] = 0.0 instead of reported_returns[0]
    recovered[0] = 0.0
    denom = 1.0 - phi
    if denom <= 1e-8:
        denom = 1e-8
    for t in range(1, len(reported_returns)):
        recovered[t] = (reported_returns[t] - phi * reported_returns[t - 1]) / denom
    return recovered


def compute_risk_metrics(returns: np.ndarray, rf_quarterly: float) -> dict[str, float]:
    mean_ann = float(np.mean(returns) * 4.0)
    vol_ann = float(np.std(returns, ddof=1) * 2.0)
    sharpe = float((mean_ann - rf_quarterly * 4.0) / vol_ann) if vol_ann > 0 else 0.0

    wealth = np.cumprod(1.0 + returns)
    peaks = np.maximum.accumulate(wealth)
    drawdowns = (peaks - wealth) / peaks
    max_dd = float(np.max(drawdowns)) if len(drawdowns) > 0 else 0.0

    if len(returns) > 2:
        autocorr = float(np.corrcoef(returns[1:], returns[:-1])[0, 1])
    else:
        autocorr = 0.0

    return {
        "mean_annualized": mean_ann,
        "volatility_annualized": vol_ann,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "first_order_autocorr": autocorr,
    }


def estimate_systematic_risk(asset_returns: np.ndarray, market_returns: np.ndarray) -> dict[str, float]:
    cov_mat = np.cov(asset_returns, market_returns)
    var_m = cov_mat[1, 1]
    cov_am = cov_mat[0, 1]
    beta = float(cov_am / var_m) if var_m > 0 else 0.0

    alpha_q = float(np.mean(asset_returns) - beta * np.mean(market_returns))
    alpha_ann = float(alpha_q * 4.0)

    corr = float(np.corrcoef(asset_returns, market_returns)[0, 1])
    r_squared = float(corr**2)

    diff = asset_returns - market_returns
    tracking_err = float(np.std(diff, ddof=1) * 2.0)

    return {
        "beta": beta,
        "alpha_quarterly": alpha_q,
        "alpha_annualized": alpha_ann,
        "r_squared": r_squared,
        "tracking_error": tracking_err,
    }


def solve_project(instance: dict[str, Any]) -> dict[str, Any]:
    reported = np.asarray(instance["reported_returns"], dtype=float)
    proxy = np.asarray(instance["public_proxy_returns"], dtype=float)
    rf_q = float(instance["rf_quarterly"])

    phi = estimate_smoothing_parameter(reported)
    unsmoothed = unsmooth_returns_ar1(reported, phi)

    rep_metrics = compute_risk_metrics(reported, rf_q)
    unsmooth_metrics = compute_risk_metrics(unsmoothed, rf_q)
    proxy_metrics = compute_risk_metrics(proxy, rf_q)

    rep_sys = estimate_systematic_risk(reported, proxy)
    unsmooth_sys = estimate_systematic_risk(unsmoothed, proxy)

    vol_ratio = unsmooth_metrics["volatility_annualized"] / rep_metrics["volatility_annualized"]
    beta_ratio = unsmooth_sys["beta"] / rep_sys["beta"] if rep_sys["beta"] > 0 else 1.0

    return {
        "phi": phi,
        "reported_metrics": rep_metrics,
        "unsmoothed_metrics": unsmooth_metrics,
        "proxy_metrics": proxy_metrics,
        "reported_systematic": rep_sys,
        "unsmoothed_systematic": unsmooth_sys,
        "volatility_ratio": vol_ratio,
        "beta_ratio": beta_ratio,
    }
