"""Reference implementation for S6: Policy-shock event study engine.

Full solution implementing the frozen event_study interface.
All data handling is strictly typed and deterministic.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def fit_normal_model(stock: Sequence[float], market: Sequence[float] | None = None) -> tuple[float, float, float]:
    """Fit a normal return model to asset returns over the estimation window.

    If market is None, fits a constant-mean model:
        alpha = mean(stock), beta = 0.0, sigma2 with divisor L - 1.
    If market is provided, fits a market model by OLS:
        r_{i,t} = alpha_i + beta_i * R_{m,t} + eps_{i,t},
        sigma2 with divisor L - 2.

    Returns:
        (alpha, beta, sigma2)
    """
    n = len(stock)
    if market is None:
        if n < 2:
            raise ValueError("constant-mean model requires at least 2 observations")
        alpha = sum(stock) / n
        beta = 0.0
        ss_res = sum((s - alpha) ** 2 for s in stock)
        sigma2 = ss_res / (n - 1)
        return (alpha, beta, sigma2)

    if len(market) != n:
        raise ValueError("unequal lengths of stock and market series")
    if n < 3:
        raise ValueError("market model requires at least 3 observations")

    mean_m = sum(market) / n
    mean_s = sum(stock) / n

    ss_m = sum((m - mean_m) ** 2 for m in market)
    if ss_m <= 0.0:
        raise ValueError("market series has zero sample variance")

    sp_ms = sum((m - mean_m) * (s - mean_s) for m, s in zip(market, stock, strict=True))
    beta = sp_ms / ss_m
    alpha = mean_s - beta * mean_m

    ss_res = sum((s - (alpha + beta * m)) ** 2 for s, m in zip(stock, market, strict=True))
    sigma2 = ss_res / (n - 2)
    return (alpha, beta, sigma2)


def abnormal_returns(stock: Sequence[float], market: Sequence[float] | None, alpha: float, beta: float) -> list[float]:
    """Compute abnormal returns AR_{i,t} = r_{i,t} - (alpha + beta * R_{m,t})."""
    if market is not None:
        if len(stock) != len(market):
            raise ValueError("unequal lengths of stock and market series")
        return [s - (alpha + beta * m) for s, m in zip(stock, market, strict=True)]
    return [s - alpha for s in stock]


def abnormal_return_variance(
    sigma2: float, estimation_market: Sequence[float] | None, event_market: float | None
) -> float:
    """Compute the true variance of an abnormal return including estimation error.

    For constant-mean model (event_market is None):
        Var(AR) = sigma2 * (1 + 1/L).
    For market model:
        Var(AR) = sigma2 * (1 + 1/L + (event_market - mean_m)^2 / SS_m).
    """
    if estimation_market is None:
        raise ValueError("estimation_market cannot be None")
    n = len(estimation_market)
    if n < 1:
        raise ValueError("estimation_market cannot be empty")

    if event_market is None:
        return sigma2 * (1.0 + 1.0 / n)

    if n < 3:
        raise ValueError("market model variance requires at least 3 estimation observations")

    mean_m = sum(estimation_market) / n
    ss_m = sum((m - mean_m) ** 2 for m in estimation_market)
    if ss_m <= 0.0:
        raise ValueError("estimation market series has zero sample variance")

    dev2 = (event_market - mean_m) ** 2
    return sigma2 * (1.0 + 1.0 / n + dev2 / ss_m)


def car(abnormal: Sequence[float]) -> float:
    """Compute cumulative abnormal return (CAR) over the event window."""
    if len(abnormal) == 0:
        raise ValueError("empty abnormal return sequence")
    return float(sum(abnormal))


def event_t_statistic(cars: Sequence[float]) -> float:
    """Compute cross-sectional t-statistic for mean CAR with ddof=1."""
    k = len(cars)
    if k < 2:
        raise ValueError("fewer than 2 CARs provided for event t-statistic")
    mean_car = sum(cars) / k
    sample_var = sum((c - mean_car) ** 2 for c in cars) / (k - 1)
    if sample_var <= 0.0:
        raise ValueError("sample standard deviation is zero")
    s = math.sqrt(sample_var)
    return mean_car / (s / math.sqrt(k))


def clustered_t_statistic(values: Sequence[float], clusters: Sequence[str]) -> float:
    """Compute CR1 cluster-robust t-statistic with small-sample G/(G-1) factor."""
    n = len(values)
    if n == 0:
        raise ValueError("empty values sequence")
    if len(clusters) != n:
        raise ValueError("unequal lengths of values and clusters")

    unique_clusters = sorted(set(clusters))
    g = len(unique_clusters)
    if g < 2:
        raise ValueError("fewer than 2 clusters provided")

    mean_v = sum(values) / n
    cluster_totals: dict[str, float] = {c: 0.0 for c in unique_clusters}
    for v, c in zip(values, clusters, strict=True):
        cluster_totals[c] += v - mean_v

    sum_sq = sum(tot**2 for tot in cluster_totals.values())
    var_cr1 = (g / (g - 1)) * (sum_sq / (n**2))
    if var_cr1 <= 0.0:
        raise ValueError("clustered variance estimate is zero")

    return mean_v / math.sqrt(var_cr1)


def placebo_dates(
    calendar_length: int, event_days: Sequence[int], half_window: int, count: int, seed: int
) -> list[int]:
    """Sample count reproducible placebo dates outside event exclusion zones."""
    if half_window < 0:
        raise ValueError("half_window cannot be negative")

    forbidden: set[int] = set()
    for e in event_days:
        for d in range(e - half_window, e + half_window + 1):
            forbidden.add(d)

    eligible = [d for d in range(calendar_length) if d not in forbidden]
    if count > len(eligible):
        raise ValueError("count greater than number of eligible calendar dates")

    rng = random.Random(seed)
    chosen = rng.sample(eligible, count)
    chosen.sort()
    return chosen


def event_window_car(
    stock: Sequence[float],
    market: Sequence[float] | None,
    event_day: int,
    est_len: int,
    window: tuple[int, int],
) -> tuple[float, float]:
    """Compute CAR and its exact variance for one firm event.

    Estimation window: est_len days ending immediately before the event window starts.
    Event window: event_day + a to event_day + b inclusive.
    """
    a, b = window
    if a > b:
        raise ValueError("window start a cannot exceed window end b")

    start_event = event_day + a
    end_event = event_day + b
    start_est = start_event - est_len
    end_est = start_event - 1

    if start_est < 0:
        raise ValueError("estimation window starts before day 0")
    if end_event >= len(stock):
        raise ValueError("event window exceeds stock series length")
    if market is not None and end_event >= len(market):
        raise ValueError("event window exceeds market series length")

    est_stock = stock[start_est : end_est + 1]
    est_market = market[start_est : end_est + 1] if market is not None else None

    alpha, beta, sigma2 = fit_normal_model(est_stock, est_market)

    ev_stock = stock[start_event : end_event + 1]
    ev_market = market[start_event : end_event + 1] if market is not None else None

    ar_series = abnormal_returns(ev_stock, ev_market, alpha, beta)
    car_val = car(ar_series)

    car_var = 0.0
    if market is not None and ev_market is not None and est_market is not None:
        for em in ev_market:
            car_var += abnormal_return_variance(sigma2, est_market, em)
    else:
        for _ in ev_stock:
            car_var += abnormal_return_variance(sigma2, est_stock, None)

    return (car_val, car_var)
