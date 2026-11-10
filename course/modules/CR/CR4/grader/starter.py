"""Starter template for CR4 Capital Structure Recovery Waterfall & Fulcrum Engine.

Implement the four core functions and the top-level runner.
Raise NotImplementedError in each stub.
"""

from __future__ import annotations

from typing import Any


def calculate_waterfall_strict(
    tranches: list[dict[str, Any]],
    ev: float,
) -> list[dict[str, Any]]:
    """Allocate enterprise value down the capital structure according to strict Absolute Priority Rule.

    Identifies the unique fulcrum security tranche.
    """
    raise NotImplementedError("calculate_waterfall_strict not yet implemented")


def calculate_waterfall_with_carveout(
    tranches: list[dict[str, Any]],
    ev: float,
    carveout: dict[str, Any],
) -> list[dict[str, Any]]:
    """Apply consensual plan carve-out / APR violation adjustments to strict waterfall."""
    raise NotImplementedError("calculate_waterfall_with_carveout not yet implemented")


def reorganization_equity_distribution(
    tranches: list[dict[str, Any]],
    ev: float,
    new_debt_issued: float,
    cash_dist: float,
) -> dict[str, Any]:
    """Distribute Plan of Reorganization (POR) consideration: cash, take-back debt, and reorganized equity."""
    raise NotImplementedError("reorganization_equity_distribution not yet implemented")


def evaluate_expected_returns(
    tranches: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    purchase_prices: dict[str, float],
    holding_period_years: float,
) -> dict[str, Any]:
    """Evaluate scenario-weighted expected recovery, MOIC, and annualized IRR across tranches."""
    raise NotImplementedError("evaluate_expected_returns not yet implemented")


def run_waterfall_engine(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute end-to-end recovery waterfall analysis on instance."""
    raise NotImplementedError("run_waterfall_engine not yet implemented")
