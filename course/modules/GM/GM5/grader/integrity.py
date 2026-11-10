"""Integrity and input validation module for GM5 Grader.

Ensures strict typing, bounds checking, shape consistency, and mathematical invariants
for crisis mechanism mapping, balance sheet deleveraging, and liquidity spirals.
"""

from __future__ import annotations

import numpy as np


def validate_balance_sheet(
    position: float,
    price: float,
    cash: float,
    debt: float,
    haircut: float,
) -> None:
    """Validate balance sheet scalar inputs."""
    if not all(isinstance(x, (int, float)) for x in (position, price, cash, debt, haircut)):
        raise TypeError("Balance sheet variables must be real numeric types")
    if position < 0.0:
        raise ValueError(f"Position must be non-negative (got {position})")
    if price <= 0.0:
        raise ValueError(f"Price must be strictly positive (got {price})")
    if cash < 0.0:
        raise ValueError(f"Cash must be non-negative (got {cash})")
    if debt < 0.0:
        raise ValueError(f"Debt must be non-negative (got {debt})")
    if not (0.0 < haircut <= 1.0):
        raise ValueError(f"Haircut must lie in (0, 1] (got {haircut})")


def validate_simulation_inputs(
    p0: float,
    q0: float,
    cash0: float,
    debt0: float,
    haircut0: float,
    exogenous_shocks: list[float] | np.ndarray,
    lambda_impact: float,
) -> None:
    """Validate full liquidity spiral simulation inputs."""
    validate_balance_sheet(q0, p0, cash0, debt0, haircut0)
    if lambda_impact < 0.0:
        raise ValueError(f"Market depth parameter lambda must be non-negative (got {lambda_impact})")
    if len(exogenous_shocks) == 0:
        raise ValueError("Exogenous shocks array must not be empty")
    for s in exogenous_shocks:
        if not isinstance(s, (int, float)):
            raise TypeError("Shock elements must be numeric")
        if abs(s) > 1.0:
            raise ValueError(f"Percentage return shock {s} exceeds 100%")
