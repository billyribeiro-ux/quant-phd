"""Starter template for GM5 Project: Crisis Mechanism Dossier & Simulator.

Implement the functions below. Do not modify signatures or type annotations.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def compute_margin_call(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
) -> dict[str, float]:
    """Compute balance sheet equity, margin requirement, deficit, and leverage."""
    raise NotImplementedError("compute_margin_call not implemented")


def calculate_forced_sales(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
    target_leverage: float | None = None,
) -> dict[str, float]:
    """Calculate the required forced liquidation quantity to resolve a margin deficit."""
    raise NotImplementedError("calculate_forced_sales not implemented")


def estimate_fire_sale_discount(
    forced_volume: float,
    market_depth: float,
    permanent_impact_coef: float = 0.0,
) -> dict[str, float]:
    """Estimate temporary and permanent price impact from forced asset liquidation."""
    raise NotImplementedError("estimate_fire_sale_discount not implemented")


def simulate_liquidity_spiral(
    p0: float,
    q0: float,
    cash0: float,
    debt0: float,
    haircut0: float,
    exogenous_shocks: list[float] | np.ndarray,
    lambda_impact: float,
    target_leverage: float | None = None,
    haircut_sensitivity: float = 0.0,
    max_haircut: float = 0.50,
    policy_backstop: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Simulate a multi-period liquidity spiral coupling loss and margin spirals."""
    raise NotImplementedError("simulate_liquidity_spiral not implemented")


def evaluate_policy_intervention(
    baseline_run: dict[str, Any],
    backstopped_run: dict[str, Any],
) -> dict[str, float]:
    """Evaluate quantitative benefits of a policy backstop relative to baseline crash."""
    raise NotImplementedError("evaluate_policy_intervention not implemented")


def classify_crisis_regime(
    initial_leverage: float,
    haircut_increase: float,
    spiral_multiplier: float,
    defaulted: bool,
) -> str:
    """Classify systemic crisis regime based on amplification and balance sheet state."""
    raise NotImplementedError("classify_crisis_regime not implemented")
