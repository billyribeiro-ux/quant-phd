"""Starter for the AC4 project: budget_engine.py.

Implement every function to the specification on the project page (section "Rung 3"), then run the autograder
there, or locally with the browser's flags:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions: a case is a mapping with the fields the page lists; money is whole cents (int) and quantities are
whole units (int). Every function validates its input and raises ValueError for a case it cannot use. None may
print, warn or change its argument. Use the standard library only.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    """Budgeted units, revenue and variable cost by product, the totals and the budgeted profit, in cents."""
    raise NotImplementedError("master_budget")


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    """The budget flexed to ``actual_units`` total units at the budgeted mix; each amount to the nearest cent."""
    raise NotImplementedError("flexible_budget")


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    """Sales price, sales volume, sales mix and efficiency variances, and their total, in cents."""
    raise NotImplementedError("variance_decomposition")
