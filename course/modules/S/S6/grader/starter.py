"""Starter template for S6: Policy-shock event study engine.

Fill in each function according to the project specification in project.html.
All functions must be pure: validate inputs, raise ValueError on invalid conditions,
and return exact or tolerance-accurate floating point results.
"""

from __future__ import annotations

from collections.abc import Sequence


def fit_normal_model(stock: Sequence[float], market: Sequence[float] | None = None) -> tuple[float, float, float]:
    """Fit normal return model (market model or constant-mean model)."""
    raise NotImplementedError("fit_normal_model not implemented")


def abnormal_returns(stock: Sequence[float], market: Sequence[float] | None, alpha: float, beta: float) -> list[float]:
    """Compute abnormal returns AR_{i,t} = r_{i,t} - (alpha + beta * R_{m,t})."""
    raise NotImplementedError("abnormal_returns not implemented")


def abnormal_return_variance(
    sigma2: float, estimation_market: Sequence[float] | None, event_market: float | None
) -> float:
    """Compute exact variance of abnormal return accounting for estimation error."""
    raise NotImplementedError("abnormal_return_variance not implemented")


def car(abnormal: Sequence[float]) -> float:
    """Compute cumulative abnormal return over the event window."""
    raise NotImplementedError("car not implemented")


def event_t_statistic(cars: Sequence[float]) -> float:
    """Compute cross-sectional t-statistic for mean CAR with ddof=1."""
    raise NotImplementedError("event_t_statistic not implemented")


def clustered_t_statistic(values: Sequence[float], clusters: Sequence[str]) -> float:
    """Compute CR1 cluster-robust t-statistic with small-sample G/(G-1) factor."""
    raise NotImplementedError("clustered_t_statistic not implemented")


def placebo_dates(
    calendar_length: int, event_days: Sequence[int], half_window: int, count: int, seed: int
) -> list[int]:
    """Sample reproducible placebo dates outside event exclusion zones."""
    raise NotImplementedError("placebo_dates not implemented")


def event_window_car(
    stock: Sequence[float],
    market: Sequence[float] | None,
    event_day: int,
    est_len: int,
    window: tuple[int, int],
) -> tuple[float, float]:
    """Compute CAR and its exact variance for one firm event."""
    raise NotImplementedError("event_window_car not implemented")
