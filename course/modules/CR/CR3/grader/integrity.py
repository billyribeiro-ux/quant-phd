"""Integrity and input validation helpers for the CR3 credit cycle engine.

Validates input types, dimensions, bounded domains, and mathematical consistency.
Raises ValueError on invalid numerical domains or lengths, and TypeError on bad types.
"""

from __future__ import annotations

import math


def validate_bond_data(bond_data: dict[str, list[float]]) -> None:
    """Validate cross-sectional bond panel data."""
    required = ["spread_bps", "duration", "coupon", "amount_outstanding", "merton_edf", "industry_id"]
    for k in required:
        if k not in bond_data:
            raise ValueError(f"Missing required key in bond_data: {k}")
        if not isinstance(bond_data[k], list):
            raise TypeError(f"bond_data['{k}'] must be a list")

    n = len(bond_data["spread_bps"])
    if n < 10:
        raise ValueError(f"bond_data requires at least 10 bonds for regression, got {n}")

    for k in required:
        if len(bond_data[k]) != n:
            raise ValueError(f"Length mismatch: {k} has length {len(bond_data[k])}, expected {n}")

    for i in range(n):
        if bond_data["spread_bps"][i] <= 0:
            raise ValueError(f"spread_bps[{i}] must be strictly positive, got {bond_data['spread_bps'][i]}")
        if bond_data["duration"][i] <= 0:
            raise ValueError(f"duration[{i}] must be strictly positive, got {bond_data['duration'][i]}")
        if bond_data["coupon"][i] < 0:
            raise ValueError(f"coupon[{i}] must be non-negative, got {bond_data['coupon'][i]}")
        if bond_data["amount_outstanding"][i] <= 0:
            raise ValueError(f"amount_outstanding[{i}] must be strictly positive")
        edf = bond_data["merton_edf"][i]
        if not (0.0 < edf < 1.0):
            raise ValueError(f"merton_edf[{i}] must be in (0, 1), got {edf}")


def validate_sentiment_inputs(
    hy: list[float],
    spreads: list[float],
    ebp: list[float],
    weights: list[float] | None,
) -> None:
    """Validate credit market sentiment inputs."""
    if not (isinstance(hy, list) and isinstance(spreads, list) and isinstance(ebp, list)):
        raise TypeError("hy, spreads, and ebp must be lists of floats")
    n = len(hy)
    if n < 8:
        raise ValueError(f"Sentiment time series requires at least 8 periods, got {n}")
    if len(spreads) != n or len(ebp) != n:
        raise ValueError(f"Length mismatch among sentiment series: {n}, {len(spreads)}, {len(ebp)}")

    for i in range(n):
        if not math.isfinite(hy[i]) or not math.isfinite(spreads[i]) or not math.isfinite(ebp[i]):
            raise ValueError(f"Non-finite value at index {i}")
        if not (0.0 <= hy[i] <= 1.0):
            raise ValueError(f"High-yield issuance share at index {i} must be in [0, 1], got {hy[i]}")
        if spreads[i] <= 0:
            raise ValueError(f"Credit spread at index {i} must be positive, got {spreads[i]}")

    if weights is not None:
        if len(weights) != 3:
            raise ValueError(f"weights must have length 3, got {len(weights)}")
        if any(w < 0 for w in weights) or sum(weights) <= 0:
            raise ValueError("weights must be non-negative and sum to positive value")


def validate_recession_inputs(
    indicator: list[float],
    term_spread: list[float],
    recessions: list[int],
) -> None:
    """Validate recession probit regression inputs."""
    n = len(indicator)
    if n < 15:
        raise ValueError(f"Recession regression requires at least 15 observations, got {n}")
    if len(term_spread) != n or len(recessions) != n:
        raise ValueError(f"Length mismatch in recession series: {n}, {len(term_spread)}, {len(recessions)}")

    n_rec = sum(recessions)
    if n_rec == 0 or n_rec == n:
        raise ValueError("recessions series must contain both 0 and 1 outcomes")

    for i in range(n):
        if recessions[i] not in (0, 1):
            raise ValueError(f"recession_flags[{i}] must be 0 or 1, got {recessions[i]}")
        if not math.isfinite(indicator[i]) or not math.isfinite(term_spread[i]):
            raise ValueError(f"Non-finite predictor at index {i}")


def validate_evaluation_inputs(y_true: list[int], y_prob: list[float], threshold: float) -> None:
    """Validate forecast evaluation inputs."""
    n = len(y_true)
    if n < 2:
        raise ValueError(f"Evaluation requires at least 2 observations, got {n}")
    if len(y_prob) != n:
        raise ValueError(f"Length mismatch: y_true has {n}, y_prob has {len(y_prob)}")
    if not (0.0 < threshold < 1.0):
        raise ValueError(f"threshold must be in (0, 1), got {threshold}")

    for i in range(n):
        if y_true[i] not in (0, 1):
            raise ValueError(f"y_true[{i}] must be 0 or 1, got {y_true[i]}")
        if not (0.0 <= y_prob[i] <= 1.0):
            raise ValueError(f"y_prob[{i}] must be in [0, 1], got {y_prob[i]}")


def validate_loan_params(
    debt: float,
    ebitda: float,
    addback: float,
    senior_share: float,
    distress: float,
) -> None:
    """Validate leveraged loan waterfall parameters."""
    if debt <= 0:
        raise ValueError(f"initial_debt must be strictly positive, got {debt}")
    if ebitda <= 0:
        raise ValueError(f"ebitda must be strictly positive, got {ebitda}")
    if addback < 0:
        raise ValueError(f"addback_fraction must be non-negative, got {addback}")
    if not (0.0 < senior_share <= 1.0):
        raise ValueError(f"senior_share must be in (0, 1], got {senior_share}")
    if not (0.0 <= distress <= 1.0):
        raise ValueError(f"distress_factor must be in [0, 1], got {distress}")
