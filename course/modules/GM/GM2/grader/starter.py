"""Starter code for GM2 Project: Real-Time Regime Classification & Asset Allocation.

Implement the four functions below following the exact specifications in project.html.
Do not modify the function signatures or return types.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def classify_regimes_realtime(
    growth: np.ndarray,
    inflation: np.ndarray,
    lookback: int = 36,
    burn_in: int = 24,
) -> tuple[np.ndarray, np.ndarray]:
    """Perform causal, online regime classification into 4 macroeconomic quadrants.

    Parameters
    ----------
    growth : np.ndarray
        1D array of monthly growth indicators of length T.
    inflation : np.ndarray
        1D array of monthly inflation indicators of length T.
    lookback : int
        Window length for trailing z-score estimation.
    burn_in : int
        Initial burn-in period before classifications begin.

    Returns
    -------
    regimes : np.ndarray
        1D integer array of shape (T,) with values in {-1, 0, 1, 2, 3}.
    probs : np.ndarray
        2D float array of shape (T, 4) with normalized probability weights.
    """
    raise NotImplementedError("classify_regimes_realtime not implemented")


def estimate_regime_moments(
    returns: np.ndarray,
    regimes: np.ndarray,
    min_obs: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate annualized return moments and covariance matrices conditional on macro regimes.

    Parameters
    ----------
    returns : np.ndarray
        2D array of shape (T, N) of monthly asset returns.
    regimes : np.ndarray
        1D integer array of shape (T,) of regime classifications in {-1, 0, 1, 2, 3}.
    min_obs : int
        Minimum number of historical observations in a regime to calculate separate moments.

    Returns
    -------
    expected_returns : np.ndarray
        2D array of shape (4, N) of annualized expected returns.
    cov_matrices : np.ndarray
        3D array of shape (4, N, N) of annualized positive-definite covariance matrices.
    se_returns : np.ndarray
        2D array of shape (4, N) of standard errors of annualized mean returns.
    """
    raise NotImplementedError("estimate_regime_moments not implemented")


def optimize_regime_allocation(
    regime_probs: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrices: np.ndarray,
    risk_aversion: float = 3.0,
    max_leverage: float = 1.0,
) -> np.ndarray:
    """Compute optimal regime-conditional asset allocation weights.

    Parameters
    ----------
    regime_probs : np.ndarray
        Array of shape (4,) or (T, 4) with regime probabilities.
    expected_returns : np.ndarray
        Array of shape (4, N) with annualized return vectors per regime.
    cov_matrices : np.ndarray
        Array of shape (4, N, N) with annualized covariance matrices per regime.
    risk_aversion : float
        Mean-variance risk aversion coefficient gamma > 0.
    max_leverage : float
        Maximum gross leverage bound.

    Returns
    -------
    weights : np.ndarray
        Array of shape (N,) or (T, N) of optimal portfolio allocations.
    """
    raise NotImplementedError("optimize_regime_allocation not implemented")


def backtest_regime_strategy(
    asset_returns: np.ndarray,
    weights: np.ndarray,
    transaction_cost_bps: float = 10.0,
    burn_in: int = 24,
) -> dict[str, Any]:
    """Execute causal backtest of dynamic regime-conditional portfolio.

    Parameters
    ----------
    asset_returns : np.ndarray
        2D array of shape (T, N) of realized monthly asset returns.
    weights : np.ndarray
        2D array of shape (T, N) of portfolio weights.
    transaction_cost_bps : float
        One-way transaction cost in basis points (10 bps = 0.0010).
    burn_in : int
        Number of burn-in periods before strategy execution begins.

    Returns
    -------
    dict[str, Any]
        Dictionary with net_returns, equity_curve, annualized_return,
        annualized_volatility, sharpe_ratio, max_drawdown, annualized_turnover.
    """
    raise NotImplementedError("backtest_regime_strategy not implemented")
