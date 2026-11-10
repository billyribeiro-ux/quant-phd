"""Starter template for MS2 project: Batch-auction counterfactual.

Implement simulate_continuous_book, simulate_batch_auction, and run_counterfactual.
"""

from __future__ import annotations

from typing import Any


def simulate_continuous_book(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    """Simulate order flow execution in a continuous limit order book (CLOB)."""
    raise NotImplementedError("Student implementation required.")


def simulate_batch_auction(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    batch_interval: float,
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    """Simulate order flow execution in frequent batch auctions (FBA)."""
    raise NotImplementedError("Student implementation required.")


def run_counterfactual(
    events: list[dict[str, Any]],
    initial_price: float,
    half_spread: float,
    batch_intervals: list[float],
    mm_latency: float,
    sniper_latencies: list[float],
) -> dict[str, Any]:
    """Run full counterfactual comparing continuous trading against frequent batch auctions."""
    raise NotImplementedError("Student implementation required.")
