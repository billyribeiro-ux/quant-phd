"""Lab CAP2-L05-1: Empirical tests for volatility management after costs and the secular r* decline.

Evaluates Moreira-Muir (2017) volatility-timing portfolio performance net of
turnover costs, and implements a state-space Kalman filter proxy for the natural
real rate of interest r* (Holston, Laubach & Williams 2017).
"""

from __future__ import annotations

import numpy as np


def evaluate_volatility_management(
    base_returns: np.ndarray,
    realized_vols: np.ndarray,
    target_vol: float = 0.12,
    transaction_cost_bps: float = 10.0,
) -> tuple[float, float, float, float]:
    """Compute gross and net Sharpe ratios of Moreira-Muir volatility-managed portfolio."""
    # Sizing: w_t = c / sigma_t^2, normalized so average vol matches target_vol
    raw_weights = 1.0 / (realized_vols**2)
    c_scale = target_vol / float(np.std(raw_weights * base_returns, ddof=1) * np.sqrt(12.0))
    weights = c_scale * raw_weights

    # Gross returns
    r_gross = weights * base_returns

    # Turnover and transaction costs
    turnover = np.abs(np.diff(weights))
    cost_drag = (transaction_cost_bps * 1e-4) * np.concatenate([[0.0], turnover])
    r_net = r_gross - cost_drag

    sr_base = float(np.mean(base_returns) / np.std(base_returns, ddof=1) * np.sqrt(12.0))
    sr_gross = float(np.mean(r_gross) / np.std(r_gross, ddof=1) * np.sqrt(12.0))
    sr_net = float(np.mean(r_net) / np.std(r_net, ddof=1) * np.sqrt(12.0))
    mean_turnover = float(np.mean(turnover) * 12.0)

    return sr_base, sr_gross, sr_net, mean_turnover


def kalman_rstar_estimate(
    real_rate_series: np.ndarray,
    output_gap_series: np.ndarray,
) -> tuple[float, float, np.ndarray]:
    """Estimate natural real rate r* via 1D state-space Kalman filter proxy."""
    # State equation: r*_t = r*_{t-1} + e_{r, t}, e_r ~ N(0, sigma_r^2)
    # Observation equation: r_t = r*_t + theta * y_t + v_t, v ~ N(0, sigma_v^2)
    n = len(real_rate_series)
    sigma_r_sq = 0.0001
    sigma_v_sq = 0.0004
    theta = 0.25

    # Prior state
    x_hat = float(real_rate_series[0])
    p_hat = 0.01

    r_star_path = np.zeros(n)
    for t in range(n):
        # Time update (prediction)
        x_pred = x_hat
        p_pred = p_hat + sigma_r_sq

        # Measurement update
        y_obs = real_rate_series[t] - theta * output_gap_series[t]
        y_resid = y_obs - x_pred
        f_val = p_pred + sigma_v_sq
        k_gain = p_pred / f_val

        x_hat = x_pred + k_gain * y_resid
        p_hat = (1.0 - k_gain) * p_pred
        r_star_path[t] = x_hat

    start_rstar = float(r_star_path[0])
    terminal_rstar = float(r_star_path[-1])

    return start_rstar, terminal_rstar, r_star_path


def main() -> None:
    rng = np.random.default_rng(2017)

    # 1. Resolution 9: Volatility-Managed Portfolios After Frictions
    n_months = 240
    # Regime-switching / heteroskedastic return series
    vol_regimes = rng.choice([0.10, 0.25], size=n_months, p=[0.75, 0.25])
    month_vols = vol_regimes / np.sqrt(12.0)
    market_returns = rng.normal(0.006, month_vols)

    sr_base, sr_gross, sr_net, ann_turnover = evaluate_volatility_management(
        market_returns, month_vols, target_vol=0.12, transaction_cost_bps=12.0
    )

    print("--- Resolution 9: Volatility-Managed Portfolios After Frictions ---")
    print(f"Unmanaged Market Sharpe Ratio:         {sr_base:.3f}")
    print(f"Volatility-Managed Gross Sharpe Ratio: {sr_gross:.3f}")
    print(f"Volatility-Managed Net Sharpe Ratio:   {sr_net:.3f}")
    print(f"Annual Portfolio Turnover:             {ann_turnover:.1f}x")
    print(f"Net Alpha Retention:                   {'POSITIVE EDGE' if sr_net > sr_base else 'EROSION'}")

    # 2. Resolution 10: Secular r* Decline
    # 40 quarters (10 years) of real rates showing secular drop from 2.5% to 0.5%
    trends = np.linspace(0.025, 0.005, 40)
    real_rate = trends + rng.normal(0.0, 0.004, size=40)
    out_gap = rng.normal(0.0, 0.015, size=40)

    start_r, end_r, _ = kalman_rstar_estimate(real_rate, out_gap)

    print("\n--- Resolution 10: Has r* Fallen Permanently? ---")
    print(f"Initial Estimated r* (Annualized):  {start_r * 100.0:.2f}%")
    print(f"Terminal Estimated r* (Annualized): {end_r * 100.0:.2f}%")
    print(f"Estimated Secular r* Shift:        {(end_r - start_r) * 100.0:.2f}%")
    print(f"Structural Break Significance:     {'PERMANENT DECLINE' if end_r < 0.015 else 'STABLE'}")


main()
