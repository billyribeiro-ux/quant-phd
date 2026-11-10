"""Mutant 3: includes announcement day 0 and 1 in drift holding period, conflating jump with drift."""

from __future__ import annotations

import math
from typing import Any


def standardized_unexpected_earnings(
    earnings_history: list[float],
    current_earnings: float,
    forecast_type: str = "seasonal_rw",
) -> float:
    if forecast_type != "seasonal_rw":
        raise ValueError(f"Unsupported forecast_type: {forecast_type}")
    if len(earnings_history) < 8:
        raise ValueError("Need at least 8 quarters")
    diffs = [float(earnings_history[t] - earnings_history[t - 4]) for t in range(4, len(earnings_history))]
    drift = sum(diffs) / len(diffs)
    expected = float(earnings_history[-4]) + drift
    raw_error = float(current_earnings) - expected
    errors = [d - drift for d in diffs]
    variance = sum(e**2 for e in errors) / (len(errors) - 1)
    if variance <= 0.0 or not math.isfinite(variance):
        raise ValueError("Sample variance must be positive")
    return raw_error / math.sqrt(variance)


def assign_deciles(sue_scores: dict[str, float]) -> dict[str, int]:
    sorted_firms = sorted(sue_scores.keys(), key=lambda fid: (sue_scores[fid], fid))
    n = len(sorted_firms)
    return {fid: min(10, (rank * 10) // n + 1) for rank, fid in enumerate(sorted_firms)}


def drift_returns(
    announcements: list[dict[str, Any]],
    holding_period: tuple[int, int] = (2, 60),
) -> dict[int, float]:
    """Mutant error: includes day 0 and day 1 in the sum."""
    _t1, t2 = holding_period
    decile_cars: dict[int, list[float]] = {d: [] for d in range(1, 11)}
    for item in announcements:
        d = int(item["decile"])
        rets = item["daily_returns"]
        t0 = int(item["announcement_day"])
        # Bug: starts at 0 instead of t1 (includes day 0 and day 1)
        car = sum(float(rets[t0 + k]) for k in range(0, t2 + 1))
        decile_cars[d].append(car)
    return {d: (sum(cars) / len(cars) if cars else 0.0) for d, cars in decile_cars.items()}


def hedge_portfolio(
    decile_returns: dict[int, float],
    cost_bps: float = 0.0,
) -> dict[str, float]:
    gross = float(decile_returns[10]) - float(decile_returns[1])
    cost_deduction = 2.0 * (float(cost_bps) / 10000.0)
    net = gross - cost_deduction
    return {
        "gross_spread": gross,
        "cost_deduction": cost_deduction,
        "net_spread": net,
    }


def subsample_decay_test(
    pre_2000_records: list[dict[str, Any]],
    post_2000_records: list[dict[str, Any]],
    cost_bps: float = 20.0,
) -> dict[str, float]:
    pre_drift = drift_returns(pre_2000_records)
    post_drift = drift_returns(post_2000_records)
    pre_hedge = hedge_portfolio(pre_drift, cost_bps=cost_bps)
    post_hedge = hedge_portfolio(post_drift, cost_bps=cost_bps)
    return {
        "pre_gross": pre_hedge["gross_spread"],
        "pre_net": pre_hedge["net_spread"],
        "post_gross": post_hedge["gross_spread"],
        "post_net": post_hedge["net_spread"],
        "gross_decay": post_hedge["gross_spread"] - pre_hedge["gross_spread"],
        "net_decay": post_hedge["net_spread"] - pre_hedge["net_spread"],
    }
