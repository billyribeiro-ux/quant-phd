"""Reference solution for AC3 project: PEAD replication engine.

Implements standardized unexpected earnings under seasonal random walk with drift,
decile sorting, post-announcement drift CAR measurement, hedge portfolio construction,
and subsample decay evaluation with transaction costs.
"""

from __future__ import annotations

import math
from typing import Any


def standardized_unexpected_earnings(
    earnings_history: list[float],
    current_earnings: float,
    forecast_type: str = "seasonal_rw",
) -> float:
    """Compute standardized unexpected earnings (SUE) under seasonal random walk with drift.

    Raises ValueError for histories shorter than 8 quarters, non-positive forecast error
    volatility, non-finite values, or unsupported forecast models.
    """
    if forecast_type != "seasonal_rw":
        raise ValueError(f"Unsupported forecast_type: {forecast_type}. Expected 'seasonal_rw'")
    if not isinstance(earnings_history, list) or len(earnings_history) < 8:
        raise ValueError("earnings_history must be a list with at least 8 observations")
    if not math.isfinite(current_earnings):
        raise ValueError("current_earnings must be a finite float")
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in earnings_history):
        raise ValueError("All elements of earnings_history must be finite numbers")

    # Seasonal differences d_t = history[t] - history[t-4]
    t_len = len(earnings_history)
    diffs = [float(earnings_history[t] - earnings_history[t - 4]) for t in range(4, t_len)]

    drift = sum(diffs) / len(diffs)
    expected = float(earnings_history[-4]) + drift
    raw_error = float(current_earnings) - expected

    # Historical forecast errors relative to estimated drift
    errors = [d - drift for d in diffs]
    deg_freedom = len(errors) - 1
    if deg_freedom <= 0:
        raise ValueError("Insufficient degrees of freedom for sample variance")

    variance = sum(e**2 for e in errors) / deg_freedom
    if variance <= 0.0 or not math.isfinite(variance):
        raise ValueError("Sample variance of forecast errors must be strictly positive and finite")

    std_dev = math.sqrt(variance)
    return raw_error / std_dev


def assign_deciles(sue_scores: dict[str, float]) -> dict[str, int]:
    """Sort firms into 10 deciles (1..10) based on SUE scores.

    Ties are broken deterministically by firm identifier in ascending lexicographical order.
    Decile 1 corresponds to lowest SUE, Decile 10 to highest SUE.
    Raises ValueError for fewer than 10 firms or non-finite values.
    """
    if not isinstance(sue_scores, dict) or len(sue_scores) < 10:
        raise ValueError("sue_scores must be a dict containing at least 10 firms")

    for k, v in sue_scores.items():
        if not isinstance(k, str) or not k:
            raise ValueError("Firm identifiers must be non-empty strings")
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"SUE score for firm {k} must be a finite number")

    # Stable deterministic sort: score ascending, then firm_id ascending
    sorted_firms = sorted(sue_scores.keys(), key=lambda fid: (sue_scores[fid], fid))
    n = len(sorted_firms)

    deciles: dict[str, int] = {}
    for rank, fid in enumerate(sorted_firms):
        d = min(10, (rank * 10) // n + 1)
        deciles[fid] = d

    return deciles


def drift_returns(
    announcements: list[dict[str, Any]],
    holding_period: tuple[int, int] = (2, 60),
) -> dict[int, float]:
    """Compute average cumulative abnormal return per SUE decile over holding period [t1, t2].

    Holding period [t1, t2] is relative to announcement_day.
    Returns mapping from decile (1..10) to mean CAR.
    Raises ValueError for empty records, invalid holding window, or malformed data.
    """
    if not isinstance(announcements, list) or len(announcements) == 0:
        raise ValueError("announcements must be a non-empty list")
    if not isinstance(holding_period, (tuple, list)) or len(holding_period) != 2:
        raise ValueError("holding_period must be a 2-tuple (t1, t2)")

    t1, t2 = int(holding_period[0]), int(holding_period[1])
    if t1 < 0 or t1 > t2:
        raise ValueError(f"Invalid holding period bounds: [{t1}, {t2}]")

    decile_cars: dict[int, list[float]] = {d: [] for d in range(1, 11)}

    for idx, item in enumerate(announcements):
        if not isinstance(item, dict):
            raise ValueError(f"Announcement record {idx} is not a dictionary")
        if "decile" not in item or "daily_returns" not in item or "announcement_day" not in item:
            raise ValueError(f"Announcement record {idx} missing required fields")

        d = int(item["decile"])
        if d < 1 or d > 10:
            raise ValueError(f"Announcement record {idx} has invalid decile {d}; expected 1..10")

        rets = item["daily_returns"]
        t0 = int(item["announcement_day"])

        if not isinstance(rets, list) or t0 + t2 >= len(rets) or t0 + t1 < 0:
            raise ValueError(f"Announcement record {idx} return series out of bounds for window [{t1}, {t2}]")

        car = sum(float(rets[t0 + k]) for k in range(t1, t2 + 1))
        decile_cars[d].append(car)

    # Compute mean CAR per decile
    out: dict[int, float] = {}
    for d in range(1, 11):
        cars = decile_cars[d]
        out[d] = sum(cars) / len(cars) if cars else 0.0

    return out


def hedge_portfolio(
    decile_returns: dict[int, float],
    cost_bps: float = 0.0,
) -> dict[str, float]:
    """Compute long Decile 10, short Decile 1 hedge portfolio performance net of transaction costs.

    Cost deduction accounts for both long and short legs: 2 * (cost_bps / 10000).
    Raises ValueError for negative costs or missing extreme deciles.
    """
    if not isinstance(decile_returns, dict) or 1 not in decile_returns or 10 not in decile_returns:
        raise ValueError("decile_returns must contain deciles 1 and 10")
    if not isinstance(cost_bps, (int, float)) or cost_bps < 0.0:
        raise ValueError("cost_bps must be a non-negative number")

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
    """Test post-2000 decay in post-earnings-announcement drift gross and net of transaction costs.

    Returns dict with keys: pre_gross, pre_net, post_gross, post_net, gross_decay, net_decay.
    """
    if not isinstance(pre_2000_records, list) or len(pre_2000_records) == 0:
        raise ValueError("pre_2000_records must be non-empty")
    if not isinstance(post_2000_records, list) or len(post_2000_records) == 0:
        raise ValueError("post_2000_records must be non-empty")

    pre_drift = drift_returns(pre_2000_records)
    post_drift = drift_returns(post_2000_records)

    pre_hedge = hedge_portfolio(pre_drift, cost_bps=cost_bps)
    post_hedge = hedge_portfolio(post_drift, cost_bps=cost_bps)

    gross_decay = post_hedge["gross_spread"] - pre_hedge["gross_spread"]
    net_decay = post_hedge["net_spread"] - pre_hedge["net_spread"]

    return {
        "pre_gross": pre_hedge["gross_spread"],
        "pre_net": pre_hedge["net_spread"],
        "post_gross": post_hedge["gross_spread"],
        "post_net": post_hedge["net_spread"],
        "gross_decay": gross_decay,
        "net_decay": net_decay,
    }
