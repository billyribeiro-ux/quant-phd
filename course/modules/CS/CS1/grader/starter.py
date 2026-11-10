"""Starter implementation of Atlas A1 returns module.

Raises NotImplementedError for all functions.
"""

from __future__ import annotations

from collections.abc import Sequence


def simple_return(prices: Sequence[float]) -> list[float]:
    """Compute simple (arithmetic) returns: r_t = P_t / P_{t-1} - 1."""
    raise NotImplementedError("simple_return is not yet implemented")


def log_return(prices: Sequence[float]) -> list[float]:
    """Compute continuously compounded (log) returns: ell_t = ln(P_t / P_{t-1})."""
    raise NotImplementedError("log_return is not yet implemented")
