"""Starter stub for the FC3 project: Fund-skill test.

Students implement alpha_and_t, chance_count, and bootstrap_skilled_set.
"""

from __future__ import annotations


def alpha_and_t(returns: list[float], factor: list[float]) -> tuple[float, float]:
    """Compute OLS alpha (monthly intercept) and its t-statistic."""
    raise NotImplementedError


def chance_count(t_stats: list[float], critical: float) -> int:
    """Count the number of funds with t-statistic strictly greater than the critical value."""
    raise NotImplementedError


def bootstrap_skilled_set(
    returns: list[list[float]],
    factor: list[float],
    level: float,
    n_boot: int,
    seed: int,
) -> list[int]:
    """Identify skilled funds via bootstrap maximum-t threshold."""
    raise NotImplementedError
