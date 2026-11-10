"""Reference implementation for Module F4 Project: Crash-Risk Overlay.

Implements cross-sectional momentum, causal realized volatility estimation,
Daniel & Moskowitz (2016) panic-state identification, dynamic overlay scaling,
turnover/transaction cost modeling, and higher-order tail risk diagnostics.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_momentum_signals(
    stock_returns: np.ndarray,
    lookback: int = 12,
    skip_recent: int = 1,
) -> np.ndarray:
    """Compute cross-sectional momentum ranking signals (t-12 to t-2).

    Parameters
    ----------
    stock_returns : np.ndarray
        Array of shape (T, N) of monthly stock returns.
    lookback : int
        Lookback window in months (default 12).
    skip_recent : int
        Recent months to skip to avoid bid-ask bounce / short-term reversal (default 1).

    Returns
    -------
    np.ndarray
        Array of shape (T, N) with momentum signals. Rows before lookback are 0.
    """
    n_months, n_stocks = stock_returns.shape
    signals = np.zeros((n_months, n_stocks), dtype=np.float64)

    for t in range(lookback, n_months):
        start_idx = t - lookback
        end_idx = t - skip_recent
        signals[t] = np.sum(stock_returns[start_idx:end_idx], axis=0)

    return signals


def construct_wml_weights(
    signals: np.ndarray,
    n_long: int = 10,
    n_short: int = 10,
) -> np.ndarray:
    """Construct dollar-neutral Winner-Minus-Loser (WML) portfolio weights.

    Parameters
    ----------
    signals : np.ndarray
        Array of shape (T, N) of cross-sectional momentum signals.
    n_long : int
        Number of long positions (winners).
    n_short : int
        Number of short positions (losers).

    Returns
    -------
    np.ndarray
        Array of shape (T, N) where long stocks sum to +1.0, short stocks sum to -1.0,
        and net exposure is 0.0. If signals are all zeros, returns zeros.
    """
    n_months, n_stocks = signals.shape
    weights = np.zeros((n_months, n_stocks), dtype=np.float64)

    for t in range(n_months):
        sig = signals[t]
        if np.all(sig == 0.0):
            continue

        ranks = np.argsort(np.argsort(sig))  # 0 to n_stocks - 1
        loser_mask = ranks < n_short
        winner_mask = ranks >= (n_stocks - n_long)

        weights[t, winner_mask] = 1.0 / float(n_long)
        weights[t, loser_mask] = -1.0 / float(n_short)

    return weights


def estimate_realized_volatility(
    returns: np.ndarray,
    window: int = 6,
    min_periods: int = 3,
) -> np.ndarray:
    """Compute strictly causal trailing realized annualized volatility.

    Parameters
    ----------
    returns : np.ndarray
        1D array of monthly returns (T,).
    window : int
        Trailing rolling window in months (default 6).
    min_periods : int
        Minimum historical months required (default 3).

    Returns
    -------
    np.ndarray
        1D array of shape (T,) with annualized realized volatility.
        For t, standard deviation is computed over returns[max(0, t-window) : t].
        Strictly causal: month t return is never included in month t volatility forecast.
    """
    t_len = len(returns)
    vol = np.zeros(t_len, dtype=np.float64)
    default_prior = 0.16

    for t in range(t_len):
        start_idx = max(0, t - window)
        history = returns[start_idx:t]
        if len(history) < min_periods:
            vol[t] = default_prior
        else:
            s = float(np.std(history, ddof=1))
            vol[t] = max(0.04, s * np.sqrt(12.0))

    return vol


def identify_panic_states(
    market_returns: np.ndarray,
    lookback_months: int = 24,
) -> np.ndarray:
    """Identify Daniel & Moskowitz (2016) panic / bear market states.

    A panic state (I_panic = 1) occurs when the cumulative trailing market
    return over past lookback_months is strictly negative.

    Parameters
    ----------
    market_returns : np.ndarray
        1D array of monthly market returns.
    lookback_months : int
        Lookback for cumulative market return (default 24).

    Returns
    -------
    np.ndarray
        Boolean array of shape (T,) indicating active panic states.
    """
    t_len = len(market_returns)
    panic = np.zeros(t_len, dtype=bool)

    for t in range(lookback_months, t_len):
        cum_mkt = float(np.sum(market_returns[t - lookback_months : t]))
        if cum_mkt < 0.0:
            panic[t] = True

    return panic


def compute_dynamic_overlay_weights(
    wml_returns: np.ndarray,
    market_returns: np.ndarray,
    panic_states: np.ndarray,
    target_vol: float = 0.15,
    max_leverage: float = 2.0,
) -> dict[str, np.ndarray]:
    """Compute strategy exposure scalars for Static, Vol-Scaled, and Dynamic DM.

    Parameters
    ----------
    wml_returns : np.ndarray
        Unscaled 1D monthly returns of WML strategy.
    market_returns : np.ndarray
        1D monthly market returns.
    panic_states : np.ndarray
        Boolean 1D array of panic states.
    target_vol : float
        Annualized target volatility (default 0.15).
    max_leverage : float
        Maximum allowable gross exposure scalar (default 2.0).

    Returns
    -------
    dict[str, np.ndarray]
        Contains exposure scalars (T,) for 'static', 'vol_scaled', and 'dynamic_dm'.
    """
    t_len = len(wml_returns)
    wml_vol = estimate_realized_volatility(wml_returns, window=6)

    static_w = np.ones(t_len, dtype=np.float64)
    vol_scaled_w = np.zeros(t_len, dtype=np.float64)
    dynamic_dm_w = np.zeros(t_len, dtype=np.float64)

    for t in range(t_len):
        v = max(wml_vol[t], 0.04)
        scaled = min(max_leverage, target_vol / v)
        vol_scaled_w[t] = scaled

        # Daniel & Moskowitz crash-risk overlay:
        # In panic states, optionality surges on loser leg. Scale down exposure to 20%
        # to avoid short-squeeze crash during bear market rebounds.
        if panic_states[t]:
            dynamic_dm_w[t] = scaled * 0.20
        else:
            dynamic_dm_w[t] = scaled

    return {
        "static": static_w,
        "vol_scaled": vol_scaled_w,
        "dynamic_dm": dynamic_dm_w,
    }


def backtest_strategy(
    weights_stock: np.ndarray,
    stock_returns: np.ndarray,
    strategy_scalars: np.ndarray,
    cost_bps: float = 15.0,
) -> dict[str, np.ndarray]:
    """Execute strategy backtest with turnover tracking and transaction costs.

    Parameters
    ----------
    weights_stock : np.ndarray
        Base unscaled weights (T, N).
    stock_returns : np.ndarray
        Stock returns (T, N).
    strategy_scalars : np.ndarray
        1D exposure scalars (T,).
    cost_bps : float
        Transaction costs in basis points per unit turned over (default 15.0 bps).

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary with 'gross_returns', 'turnover', 'costs', and 'net_returns'.
    """
    n_months, n_stocks = stock_returns.shape
    gross_returns = np.zeros(n_months, dtype=np.float64)
    turnover = np.zeros(n_months, dtype=np.float64)
    costs = np.zeros(n_months, dtype=np.float64)
    net_returns = np.zeros(n_months, dtype=np.float64)

    scaled_positions = np.zeros((n_months, n_stocks), dtype=np.float64)
    for t in range(n_months):
        scaled_positions[t] = strategy_scalars[t] * weights_stock[t]

    cost_multiplier = cost_bps * 1e-4

    for t in range(n_months):
        gross_returns[t] = float(np.sum(scaled_positions[t] * stock_returns[t]))

        if t == 0:
            turnover[t] = float(0.5 * np.sum(np.abs(scaled_positions[t])))
        else:
            turnover[t] = float(0.5 * np.sum(np.abs(scaled_positions[t] - scaled_positions[t - 1])))

        costs[t] = turnover[t] * cost_multiplier
        net_returns[t] = gross_returns[t] - costs[t]

    return {
        "gross_returns": gross_returns,
        "turnover": turnover,
        "costs": costs,
        "net_returns": net_returns,
    }


def evaluate_performance(
    returns: np.ndarray,
    rf: float = 0.0,
) -> dict[str, float]:
    """Calculate annualized performance, higher-order moments, and drawdown stats.

    Parameters
    ----------
    returns : np.ndarray
        1D array of monthly returns.
    rf : float
        Monthly risk-free rate (default 0.0).

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - ann_return: float
        - ann_vol: float
        - sharpe: float
        - skewness: float
        - kurtosis: float
        - max_drawdown: float (positive number)
        - calmar: float
    """
    if len(returns) == 0:
        return {
            "ann_return": 0.0,
            "ann_vol": 0.0,
            "sharpe": 0.0,
            "skewness": 0.0,
            "kurtosis": 0.0,
            "max_drawdown": 0.0,
            "calmar": 0.0,
        }

    excess = returns - rf
    mean_excess = float(np.mean(excess))
    std_dev = float(np.std(excess, ddof=1))

    ann_return = mean_excess * 12.0
    ann_vol = max(1e-8, std_dev * np.sqrt(12.0))
    sharpe = ann_return / ann_vol

    centered = returns - np.mean(returns)
    m2 = float(np.mean(centered**2))
    m3 = float(np.mean(centered**3))
    m4 = float(np.mean(centered**4))

    skewness = m3 / max(1e-8, m2**1.5)
    kurtosis = (m4 / max(1e-8, m2**2.0)) - 3.0

    cum_wealth = np.cumprod(1.0 + returns)
    running_max = np.maximum.accumulate(cum_wealth)
    drawdowns = (running_max - cum_wealth) / running_max
    max_dd = float(np.max(drawdowns))
    calmar = ann_return / max(1e-6, max_dd)

    return {
        "ann_return": float(ann_return),
        "ann_vol": float(ann_vol),
        "sharpe": float(sharpe),
        "skewness": float(skewness),
        "kurtosis": float(kurtosis),
        "max_drawdown": float(max_dd),
        "calmar": float(calmar),
    }


def run_overlay_experiment(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete crash-risk overlay experiment across IS and OOS splits.

    Parameters
    ----------
    instance : dict[str, Any]
        Instance dictionary from make_instance.

    Returns
    -------
    dict[str, Any]
        Dictionary with in-sample and out-of-sample backtest results and metrics.
    """
    stock_returns: np.ndarray = instance["stock_returns"]
    market_returns: np.ndarray = instance["market_returns"]
    in_sample_split: int = instance["in_sample_split"]
    rf: float = instance["risk_free_rate"]
    cost_bps: float = instance["cost_bps"]

    signals = compute_momentum_signals(stock_returns, lookback=12, skip_recent=1)
    base_weights = construct_wml_weights(signals, n_long=10, n_short=10)

    raw_wml = np.zeros(len(stock_returns))
    for t in range(len(stock_returns)):
        raw_wml[t] = float(np.sum(base_weights[t] * stock_returns[t]))

    panic_states = identify_panic_states(market_returns, lookback_months=24)
    scalars = compute_dynamic_overlay_weights(raw_wml, market_returns, panic_states)

    strategies = ["static", "vol_scaled", "dynamic_dm"]
    backtests: dict[str, dict[str, np.ndarray]] = {}
    is_metrics: dict[str, dict[str, float]] = {}
    oos_metrics: dict[str, dict[str, float]] = {}

    for strat in strategies:
        bt = backtest_strategy(base_weights, stock_returns, scalars[strat], cost_bps=cost_bps)
        backtests[strat] = bt

        net_is = bt["net_returns"][12:in_sample_split]
        is_metrics[strat] = evaluate_performance(net_is, rf=rf)

        net_oos = bt["net_returns"][in_sample_split:]
        oos_metrics[strat] = evaluate_performance(net_oos, rf=rf)

    return {
        "signals": signals,
        "base_weights": base_weights,
        "panic_states": panic_states,
        "scalars": scalars,
        "backtests": backtests,
        "is_metrics": is_metrics,
        "oos_metrics": oos_metrics,
    }
