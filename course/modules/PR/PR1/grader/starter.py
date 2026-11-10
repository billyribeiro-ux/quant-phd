"""Starter template for the PR1 Allocator Shoot-Out project.

Implement each allocator function and the rolling backtest engine.
"""

from __future__ import annotations

from typing import Any


def equal_weight(n: int) -> list[float]:
    """Compute 1/N portfolio weights for n assets."""
    raise NotImplementedError


def sample_mv(window: list[list[float]], gamma: float) -> list[float]:
    """Compute long-only sample mean-variance weights."""
    raise NotImplementedError


def shrinkage_mv(window: list[list[float]], gamma: float, delta: float) -> list[float]:
    """Compute long-only shrinkage mean-variance weights."""
    raise NotImplementedError


def black_litterman(
    window: list[list[float]],
    w_mkt: list[float],
    tau: float,
    p: list[list[float]],
    q: list[float],
    omega: list[float],
    gamma: float,
) -> list[float]:
    """Compute long-only Black-Litterman weights."""
    raise NotImplementedError


def min_variance(window: list[list[float]]) -> list[float]:
    """Compute long-only minimum-variance weights."""
    raise NotImplementedError


def run_backtest(instance: dict[str, Any], method: str) -> dict[str, Any]:
    """Execute out-of-sample rolling backtest for the specified method."""
    raise NotImplementedError
