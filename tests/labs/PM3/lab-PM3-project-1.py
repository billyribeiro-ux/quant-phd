"""Lab PM3-project-1: Unsmoothing Private Credit Returns & Systematic Risk Assessment.

Rung 2 completed solution: Estimates first-order appraisal smoothing parameter phi,
inverts the AR(1) smoothing filter to recover unobserved quarterly returns, and compares
reported vs. de-smoothed volatility, Sharpe ratio, and public loan proxy beta.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_smoothing_parameter(reported_returns: np.ndarray) -> float:
    """Estimate the first-order appraisal smoothing parameter phi via sample autocorrelation.

    Parameters
    ----------
    reported_returns : np.ndarray
        Quarterly reported private credit returns.

    Returns
    -------
    float
        Estimated AR(1) smoothing parameter phi clamped to [0.0, 0.95].
    """
    r_t = reported_returns[1:]
    r_lag = reported_returns[:-1]
    cov = np.cov(r_t, r_lag)[0, 1]
    var_lag = np.var(r_lag, ddof=1)
    phi = float(cov / var_lag) if var_lag > 0 else 0.0
    return float(np.clip(phi, 0.0, 0.95))


def unsmooth_returns_ar1(reported_returns: np.ndarray, phi: float) -> np.ndarray:
    """Invert the AR(1) smoothing filter to recover the unobserved true return series.

    Parameters
    ----------
    reported_returns : np.ndarray
        Quarterly reported private credit returns.
    phi : float
        Smoothing parameter in [0.0, 0.95].

    Returns
    -------
    np.ndarray
        Recovered quarterly true returns.
    """
    recovered = np.zeros_like(reported_returns)
    recovered[0] = reported_returns[0]
    denom = 1.0 - phi
    for t in range(1, len(reported_returns)):
        recovered[t] = (reported_returns[t] - phi * reported_returns[t - 1]) / denom
    return recovered


def compute_risk_metrics(returns: np.ndarray, rf_quarterly: float) -> dict[str, float]:
    """Calculate annualized mean, volatility, Sharpe ratio, max drawdown, and autocorrelation.

    Parameters
    ----------
    returns : np.ndarray
        Quarterly return series.
    rf_quarterly : float
        Quarterly risk-free rate.

    Returns
    -------
    dict[str, float]
        Dictionary containing risk and performance metrics.
    """
    mean_ann = float(np.mean(returns) * 4.0)
    vol_ann = float(np.std(returns, ddof=1) * 2.0)
    sharpe = float((mean_ann - rf_quarterly * 4.0) / vol_ann) if vol_ann > 0 else 0.0

    # Max drawdown from cumulative wealth
    wealth = np.cumprod(1.0 + returns)
    peaks = np.maximum.accumulate(wealth)
    drawdowns = (peaks - wealth) / peaks
    max_dd = float(np.max(drawdowns)) if len(drawdowns) > 0 else 0.0

    autocorr = float(np.corrcoef(returns[1:], returns[:-1])[0, 1]) if len(returns) > 2 else 0.0

    return {
        "mean_annualized": mean_ann,
        "volatility_annualized": vol_ann,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "first_order_autocorr": autocorr,
    }


def estimate_systematic_risk(asset_returns: np.ndarray, market_returns: np.ndarray) -> dict[str, float]:
    """Compute market beta, alpha, R-squared, and tracking error against a benchmark.

    Parameters
    ----------
    asset_returns : np.ndarray
        Asset quarterly returns.
    market_returns : np.ndarray
        Benchmark (public leveraged loan proxy) quarterly returns.

    Returns
    -------
    dict[str, float]
        Dictionary with beta, quarterly/annual alpha, R2, and tracking error.
    """
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
    """Execute the complete private credit de-smoothing and risk evaluation pipeline."""
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


def main() -> None:
    # 20 quarters of sample illustrative data
    rep_sample = np.array(
        [
            0.021,
            0.023,
            0.019,
            0.022,
            0.020,
            0.018,
            0.021,
            0.024,
            0.022,
            0.015,
            0.012,
            0.014,
            0.018,
            0.021,
            0.023,
            0.020,
            0.022,
            0.025,
            0.024,
            0.021,
        ]
    )
    proxy_sample = np.array(
        [
            0.025,
            0.030,
            0.010,
            0.028,
            0.018,
            0.005,
            0.022,
            0.035,
            0.020,
            -0.015,
            -0.025,
            0.010,
            0.025,
            0.032,
            0.028,
            0.015,
            0.026,
            0.038,
            0.025,
            0.018,
        ]
    )
    rf_q = 0.0075

    inst = {
        "reported_returns": rep_sample,
        "public_proxy_returns": proxy_sample,
        "rf_quarterly": rf_q,
    }

    result = solve_project(inst)

    print("Project Rung 2 Completed Solution Output:")
    print(f"Estimated Smoothing Parameter (phi):     {result['phi']:10.4f}")
    vol_rep_pct = result["reported_metrics"]["volatility_annualized"] * 100
    print(f"Reported Annualized Volatility:          {vol_rep_pct:10.4f}%")
    print(
        f"De-Smoothed Annualized Volatility:       {result['unsmoothed_metrics']['volatility_annualized'] * 100:10.4f}%"
    )
    print(f"Volatility Expansion Ratio:              {result['volatility_ratio']:10.4f}x")
    print(f"Reported Loan Market Beta:               {result['reported_systematic']['beta']:10.4f}")
    print(f"De-Smoothed Loan Market Beta:            {result['unsmoothed_systematic']['beta']:10.4f}")
    print(f"Beta Adjustment Ratio:                   {result['beta_ratio']:10.4f}x")
    print(f"Reported Sharpe Ratio:                   {result['reported_metrics']['sharpe_ratio']:10.4f}")
    print(f"De-Smoothed Sharpe Ratio:                {result['unsmoothed_metrics']['sharpe_ratio']:10.4f}")
    print(f"Reported Max Drawdown:                   {result['reported_metrics']['max_drawdown'] * 100:10.4f}%")
    print(f"De-Smoothed Max Drawdown:                {result['unsmoothed_metrics']['max_drawdown'] * 100:10.4f}%")

    assert result["phi"] > 0.0
    assert result["volatility_ratio"] > 1.0
    assert result["beta_ratio"] > 1.0
    assert result["unsmoothed_metrics"]["max_drawdown"] >= result["reported_metrics"]["max_drawdown"]


main()
