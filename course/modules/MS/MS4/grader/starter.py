"""Starter implementation for MS4 Factor Strategy Capacity Study.

Complete each function below following the specification in project.html.
"""

from __future__ import annotations

from typing import Any


def compute_trade_lists(
    w_initial: list[float],
    w_target: list[float],
    aum: float,
    prices: list[float],
) -> dict[str, Any]:
    """Compute signed dollar and share trades, and portfolio turnover."""
    raise NotImplementedError("compute_trade_lists not implemented")


def estimate_impact_costs(
    dollar_trades: list[float],
    adv: list[float],
    sigma: list[float],
    prefactor_y: float = 0.5,
) -> dict[str, float]:
    """Estimate execution drag under the square-root market impact law."""
    raise NotImplementedError("estimate_impact_costs not implemented")


def simulate_capacity_curve(
    aum_grid: list[float],
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    gross_alpha: float,
    prefactor_y: float = 0.5,
) -> dict[str, list[float]]:
    """Simulate cost and net alpha degradation across an AUM grid."""
    raise NotImplementedError("simulate_capacity_curve not implemented")


def find_capacity_limits(
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    gross_alpha: float,
    prefactor_y: float = 0.5,
) -> dict[str, float]:
    """Calculate exact break-even and profit-maximizing strategy capacity limits."""
    raise NotImplementedError("find_capacity_limits not implemented")


def mitigate_costs(
    ranks: list[float],
    current_weights: list[float],
    target_n_assets: int,
    buffer_ratio: float = 1.5,
) -> list[float]:
    """Mitigate trading costs using buy-hold buffer zones (hysteresis)."""
    raise NotImplementedError("mitigate_costs not implemented")
