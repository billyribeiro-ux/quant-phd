"""Starter for the CF8 project: treasury_forecast.py.

Implement every function so that it matches the specification on the project page, then run the autograder, or
locally, with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Every function validates the named conditions and raises ValueError with a message that names the rule that failed.
None may print or warn, and none may change its argument. Money is whole cents; every money output is an int.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def forecast(case: Mapping[str, Any]) -> list[dict[str, int]]:
    """Thirteen weekly rows: receipts, disbursements, draw, repayment, cash, drawn balance, liquidity and headroom."""
    raise NotImplementedError("forecast")


def revolver_plan(case: Mapping[str, Any]) -> dict[str, int]:
    """Peak drawn balance, required commitment (the largest drawn balance on the uncapped path, opening balance
    included) and the largest shortfall below minimum cash."""
    raise NotImplementedError("revolver_plan")


def covenant_pinch(case: Mapping[str, Any]) -> dict[str, int]:
    """The week, 1 to 13, of smallest covenant headroom (earliest on a tie), and that headroom in cents."""
    raise NotImplementedError("covenant_pinch")


def action_cash_impact(case: Mapping[str, Any], action: str, days: int) -> int:
    """Change in cumulative cash by the end of week 13, in cents, from shortening DSO or lengthening DPO by days."""
    raise NotImplementedError("action_cash_impact")
