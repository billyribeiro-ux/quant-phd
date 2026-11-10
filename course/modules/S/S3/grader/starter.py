"""Starter implementation for S3 project: Pairs-trading audit.

Implement every function to the contract in project.html, then run the autograder locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations


def alpha_beta(y: list[float], x: list[float]) -> tuple[float, float]:
    """Estimate y = alpha + beta * x + e by ordinary least squares with intercept."""
    raise NotImplementedError("alpha_beta is not implemented")


def adf_t(series: list[float], lags: int) -> float:
    """Compute the Augmented Dickey-Fuller t-statistic with an intercept:

    Delta y_t = alpha + gamma * y_{t-1} + sum_{j=1}^{lags} delta_j * Delta y_{t-j} + e_t.
    """
    raise NotImplementedError("adf_t is not implemented")


def trading_spread(y: list[float], x: list[float], split: int) -> list[float]:
    """Calculate the out-of-sample spread on the trading window [split, len(y))."""
    raise NotImplementedError("trading_spread is not implemented")


def eg_t(y: list[float], x: list[float], split: int, lags: int) -> float:
    """Compute the Engle-Granger cointegration test statistic."""
    raise NotImplementedError("eg_t is not implemented")


def half_life(spread: list[float]) -> float:
    """Calculate the half-life of mean reversion from an AR(1) spread fit."""
    raise NotImplementedError("half_life is not implemented")


def survives(eg_stat: float, eg_critical: float, half_life_value: float) -> bool:
    """Determine whether a pairs-trading candidate survives the econometric audit."""
    raise NotImplementedError("survives is not implemented")
