"""Starter implementation for CF6: Raising Capital & Investment Banking (ipo_pricing.py).

Implement each function according to the project specification.
"""

from __future__ import annotations

from typing import Any


def rock_equilibrium_price(
    v_low: float,
    v_high: float,
    prob_high: float,
    s_shares: int,
    informed_demand: int,
    uninformed_budget: float,
) -> tuple[float, float, float]:
    """Compute Rock (1986) winner's curse equilibrium offer price, allocation, and underpricing."""
    raise NotImplementedError("Implement rock_equilibrium_price")


def bookbuilding_allocation(
    bids: list[dict[str, Any]],
    total_shares: int,
    clearing_price: float,
    rule: str = "discretionary",
) -> dict[str, Any]:
    """Allocate shares to bookbuilding bids under pro-rata or discretionary rules."""
    raise NotImplementedError("Implement bookbuilding_allocation")


def seo_announcement_impact(
    v_assets_good: float,
    v_assets_bad: float,
    prob_good: float,
    project_cost: float,
    project_npv: float,
    slack_cash: float = 0.0,
) -> dict[str, Any]:
    """Myers-Majluf (1984) adverse selection equity issuance decision and price impact."""
    raise NotImplementedError("Implement seo_announcement_impact")


def long_run_bhar(firm_returns: list[float], benchmark_returns: list[float]) -> dict[str, Any]:
    """Compute buy-and-hold abnormal return (BHAR) and wealth relative over T periods."""
    raise NotImplementedError("Implement long_run_bhar")


def syndicate_economics(
    gross_proceeds_cents: int,
    spread_bps: int = 700,
    lead_manager_share: float = 0.60,
    co_manager_share: float = 0.30,
    selling_group_share: float = 0.10,
) -> dict[str, int]:
    """Decompose underwriting gross spread and allocate syndicate fees in integer cents."""
    raise NotImplementedError("Implement syndicate_economics")
