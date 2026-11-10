"""Starter template for Module F4 Project: Crash-Risk Overlay.

Students must implement the momentum signal construction, WML dollar-neutral weights,
causal volatility estimation, Daniel & Moskowitz (2016) panic state detection,
dynamic overlay weights, transaction costs, and performance evaluation.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_momentum_signals(
    stock_returns: np.ndarray,
    lookback: int = 12,
    skip_recent: int = 1,
) -> np.ndarray:
    """Compute cross-sectional momentum ranking signals (t-12 to t-2)."""
    raise NotImplementedError("compute_momentum_signals is not implemented")


def construct_wml_weights(
    signals: np.ndarray,
    n_long: int = 10,
    n_short: int = 10,
) -> np.ndarray:
    """Construct dollar-neutral Winner-Minus-Loser (WML) portfolio weights."""
    raise NotImplementedError("construct_wml_weights is not implemented")


def estimate_realized_volatility(
    returns: np.ndarray,
    window: int = 6,
    min_periods: int = 3,
) -> np.ndarray:
    """Compute strictly causal trailing realized annualized volatility."""
    raise NotImplementedError("estimate_realized_volatility is not implemented")


def identify_panic_states(
    market_returns: np.ndarray,
    lookback_months: int = 24,
) -> np.ndarray:
    """Identify Daniel & Moskowitz (2016) panic states."""
    raise NotImplementedError("identify_panic_states is not implemented")


def compute_dynamic_overlay_weights(
    wml_returns: np.ndarray,
    market_returns: np.ndarray,
    panic_states: np.ndarray,
    target_vol: float = 0.15,
    max_leverage: float = 2.0,
) -> dict[str, np.ndarray]:
    """Compute strategy exposure scalars for Static, Vol-Scaled, and Dynamic DM."""
    raise NotImplementedError("compute_dynamic_overlay_weights is not implemented")


def backtest_strategy(
    weights_stock: np.ndarray,
    stock_returns: np.ndarray,
    strategy_scalars: np.ndarray,
    cost_bps: float = 15.0,
) -> dict[str, np.ndarray]:
    """Execute strategy backtest with turnover tracking and transaction costs."""
    raise NotImplementedError("backtest_strategy is not implemented")


def evaluate_performance(
    returns: np.ndarray,
    rf: float = 0.0,
) -> dict[str, float]:
    """Calculate annualized performance, higher-order moments, and drawdown stats."""
    raise NotImplementedError("evaluate_performance is not implemented")


def run_overlay_experiment(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete crash-risk overlay experiment across IS and OOS splits."""
    raise NotImplementedError("run_overlay_experiment is not implemented")
