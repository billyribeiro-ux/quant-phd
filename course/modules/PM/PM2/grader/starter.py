"""Starter template for PM2: Venture Capital (Term-Sheet Economics).

Implement the required functions to model cap table evolution, anti-dilution
adjustments, and exit waterfalls with liquidation preferences.
"""

from __future__ import annotations

from typing import Any


def compute_anti_dilution_price(
    old_conv_price: float,
    new_issue_price: float,
    investment: float,
    fully_diluted_pre: float,
    common_preferred_pre: float,
    method: str,
) -> float:
    """Compute adjusted conversion price under anti-dilution protection in down-rounds."""
    raise NotImplementedError("Student implementation required.")


def build_cap_table(instance: dict[str, Any]) -> dict[str, Any]:
    """Model cap table evolution across Series A, B, and C rounds."""
    raise NotImplementedError("Student implementation required.")


def calculate_exit_waterfall(
    exit_value: float,
    cap_table: dict[str, Any],
    seniority: str = "standard",
) -> dict[str, float]:
    """Calculate the equilibrium exit waterfall payoff across all stakeholder classes."""
    raise NotImplementedError("Student implementation required.")


def evaluate_term_sheet(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete term-sheet evaluation: cap table and waterfall across test exit values."""
    raise NotImplementedError("Student implementation required.")
