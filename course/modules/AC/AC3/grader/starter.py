"""Starter template for AC3 project: PEAD replication engine.

Implement each function according to the specification on project.html.
All functions must validate inputs and pass the autograder suite.
"""

from __future__ import annotations

from typing import Any


def standardized_unexpected_earnings(
    earnings_history: list[float],
    current_earnings: float,
    forecast_type: str = "seasonal_rw",
) -> float:
    """Compute standardized unexpected earnings (SUE) under seasonal random walk with drift."""
    raise NotImplementedError("Student implementation needed: standardized_unexpected_earnings")


def assign_deciles(sue_scores: dict[str, float]) -> dict[str, int]:
    """Sort firms into 10 deciles (1..10) based on SUE scores."""
    raise NotImplementedError("Student implementation needed: assign_deciles")


def drift_returns(
    announcements: list[dict[str, Any]],
    holding_period: tuple[int, int] = (2, 60),
) -> dict[int, float]:
    """Compute average cumulative abnormal return per SUE decile over holding period."""
    raise NotImplementedError("Student implementation needed: drift_returns")


def hedge_portfolio(
    decile_returns: dict[int, float],
    cost_bps: float = 0.0,
) -> dict[str, float]:
    """Compute long Decile 10, short Decile 1 hedge portfolio performance net of transaction costs."""
    raise NotImplementedError("Student implementation needed: hedge_portfolio")


def subsample_decay_test(
    pre_2000_records: list[dict[str, Any]],
    post_2000_records: list[dict[str, Any]],
    cost_bps: float = 20.0,
) -> dict[str, float]:
    """Test post-2000 decay in post-earnings-announcement drift gross and net of transaction costs."""
    raise NotImplementedError("Student implementation needed: subsample_decay_test")
