"""Dynamic DM fails to scale down exposure during panic states (ignores panic overlay)."""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_momentum_signals(stock_returns: np.ndarray, lookback: int = 12, skip_recent: int = 1) -> np.ndarray:
    n_months, n_stocks = stock_returns.shape
    signals = np.zeros((n_months, n_stocks), dtype=np.float64)
    for t in range(lookback, n_months):
        signals[t] = np.sum(stock_returns[t - lookback : t - skip_recent], axis=0)
    return signals


def construct_wml_weights(signals: np.ndarray, n_long: int = 10, n_short: int = 10) -> np.ndarray:
    n_months, n_stocks = signals.shape
    weights = np.zeros((n_months, n_stocks), dtype=np.float64)
    for t in range(n_months):
        sig = signals[t]
        if np.all(sig == 0.0):
            continue
        ranks = np.argsort(np.argsort(sig))
        weights[t, ranks >= (n_stocks - n_long)] = 1.0 / float(n_long)
        weights[t, ranks < n_short] = -1.0 / float(n_short)
    return weights


def estimate_realized_volatility(returns: np.ndarray, window: int = 6, min_periods: int = 3) -> np.ndarray:
    t_len = len(returns)
    vol = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len):
        history = returns[max(0, t - window) : t]
        if len(history) < min_periods:
            vol[t] = 0.16
        else:
            vol[t] = max(0.04, float(np.std(history, ddof=1)) * np.sqrt(12.0))
    return vol


def identify_panic_states(market_returns: np.ndarray, lookback_months: int = 24) -> np.ndarray:
    t_len = len(market_returns)
    panic = np.zeros(t_len, dtype=bool)
    for t in range(lookback_months, t_len):
        if float(np.sum(market_returns[t - lookback_months : t])) < 0.0:
            panic[t] = True
    return panic


def compute_dynamic_overlay_weights(
    wml_returns: np.ndarray,
    market_returns: np.ndarray,
    panic_states: np.ndarray,
    target_vol: float = 0.15,
    max_leverage: float = 2.0,
) -> dict[str, np.ndarray]:
    t_len = len(wml_returns)
    wml_vol = estimate_realized_volatility(wml_returns, window=6)
    static_w = np.ones(t_len, dtype=np.float64)
    vol_scaled_w = np.zeros(t_len, dtype=np.float64)
    dynamic_dm_w = np.zeros(t_len, dtype=np.float64)
    for t in range(t_len):
        v = max(wml_vol[t], 0.04)
        scaled = min(max_leverage, target_vol / v)
        vol_scaled_w[t] = scaled
        # MUTATION: ignores panic overlay, keeping exposure fully unhedged
        dynamic_dm_w[t] = scaled
    return {"static": static_w, "vol_scaled": vol_scaled_w, "dynamic_dm": dynamic_dm_w}


def backtest_strategy(
    weights_stock: np.ndarray, stock_returns: np.ndarray, strategy_scalars: np.ndarray, cost_bps: float = 15.0
) -> dict[str, np.ndarray]:
    n_months, n_stocks = stock_returns.shape
    gross = np.zeros(n_months, dtype=np.float64)
    turnover = np.zeros(n_months, dtype=np.float64)
    costs = np.zeros(n_months, dtype=np.float64)
    net = np.zeros(n_months, dtype=np.float64)
    pos = np.zeros((n_months, n_stocks), dtype=np.float64)
    for t in range(n_months):
        pos[t] = strategy_scalars[t] * weights_stock[t]
    for t in range(n_months):
        gross[t] = float(np.sum(pos[t] * stock_returns[t]))
        turnover[t] = float(0.5 * np.sum(np.abs(pos[t] if t == 0 else pos[t] - pos[t - 1])))
        costs[t] = turnover[t] * (cost_bps * 1e-4)
        net[t] = gross[t] - costs[t]
    return {"gross_returns": gross, "turnover": turnover, "costs": costs, "net_returns": net}


def evaluate_performance(returns: np.ndarray, rf: float = 0.0) -> dict[str, float]:
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
    ann_return = float(np.mean(excess)) * 12.0
    ann_vol = max(1e-8, float(np.std(excess, ddof=1)) * np.sqrt(12.0))
    sharpe = ann_return / ann_vol
    c = returns - np.mean(returns)
    m2 = float(np.mean(c**2))
    skewness = float(np.mean(c**3)) / max(1e-8, m2**1.5)
    kurtosis = (float(np.mean(c**4)) / max(1e-8, m2**2.0)) - 3.0
    cum = np.cumprod(1.0 + returns)
    dd = (np.maximum.accumulate(cum) - cum) / np.maximum.accumulate(cum)
    max_dd = float(np.max(dd))
    return {
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "max_drawdown": max_dd,
        "calmar": ann_return / max(1e-6, max_dd),
    }


def run_overlay_experiment(instance: dict[str, Any]) -> dict[str, Any]:
    stk: np.ndarray = instance["stock_returns"]
    mkt: np.ndarray = instance["market_returns"]
    is_split: int = instance["in_sample_split"]
    rf: float = instance["risk_free_rate"]
    sig = compute_momentum_signals(stk)
    w = construct_wml_weights(sig)
    raw = np.sum(w * stk, axis=1)
    pan = identify_panic_states(mkt)
    sc = compute_dynamic_overlay_weights(raw, mkt, pan)
    bts = {
        s: backtest_strategy(w, stk, sc[s], cost_bps=instance["cost_bps"])
        for s in ["static", "vol_scaled", "dynamic_dm"]
    }
    is_m = {s: evaluate_performance(bts[s]["net_returns"][12:is_split], rf=rf) for s in bts}
    oos_m = {s: evaluate_performance(bts[s]["net_returns"][is_split:], rf=rf) for s in bts}
    return {
        "signals": sig,
        "base_weights": w,
        "panic_states": pan,
        "scalars": sc,
        "backtests": bts,
        "is_metrics": is_m,
        "oos_metrics": oos_m,
    }
