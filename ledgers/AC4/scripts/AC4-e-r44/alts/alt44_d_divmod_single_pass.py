"""Alternative correct engine for the AC4 suite: half-up by divmod, validation by operator.index, one pass over products.

Written from the page's specification alone: whole-cent values halve up; bool, float and text are refused.
"""

from __future__ import annotations

import operator
from collections.abc import Mapping
from typing import Any


def _int(value: object, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a whole number, not a boolean")
    try:
        return operator.index(value)  # type: ignore[arg-type]
    except TypeError:
        raise ValueError(f"{label} must be a whole number") from None


def _unit(value: object, label: str) -> int:
    number = _int(value, label)
    if number < 0:
        raise ValueError(f"{label} must not be negative")
    return number


def _half_up(numerator: int, denominator: int) -> int:
    q, r = divmod(numerator, denominator)
    return q + (1 if 2 * r >= denominator else 0)


def _read(case: object) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("the case must be a mapping")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError(f"the case needs {key}")
    price = _unit(case["input_price_cents"], "input_price_cents")
    fixed = _unit(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _unit(case["actual_inputs_used"], "actual_inputs_used")
    raw = case["products"]
    if not isinstance(raw, list) or not raw:
        raise ValueError("products must be a non-empty list")
    names: set[str] = set()
    rows: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("a product must be a mapping")
        for key in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"):
            if key not in item:
                raise ValueError(f"a product needs {key}")
        name = item["name"]
        if not isinstance(name, str) or name == "" or name in names:
            raise ValueError("a product name must be a unique non-empty string")
        names.add(name)
        rows.append(
            {
                "name": name,
                "bu": _unit(item["budget_units"], f"{name} budget_units"),
                "bp": _unit(item["budget_price_cents"], f"{name} budget_price_cents"),
                "q": _unit(item["standard_inputs_per_unit"], f"{name} standard_inputs_per_unit"),
                "au": _unit(item["actual_units"], f"{name} actual_units"),
                "ap": _unit(item["actual_price_cents"], f"{name} actual_price_cents"),
            }
        )
    if sum(r["bu"] for r in rows) == 0:
        raise ValueError("no budgeted units")
    return price, fixed, used, rows


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    price, fixed, _, rows = _read(case)
    units = {r["name"]: r["bu"] for r in rows}
    revenue = {r["name"]: r["bu"] * r["bp"] for r in rows}
    variable = {r["name"]: r["bu"] * r["q"] * price for r in rows}
    total_revenue = sum(revenue.values())
    total_variable = sum(variable.values())
    return {
        "units": units,
        "total_units": sum(units.values()),
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_revenue_cents": total_revenue,
        "total_variable_cost_cents": total_variable,
        "fixed_cost_cents": fixed,
        "profit_cents": total_revenue - total_variable - fixed,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    price, fixed, _, rows = _read(case)
    total = _unit(actual_units, "actual_units")
    bu = sum(r["bu"] for r in rows)
    rev = _half_up(total * sum(r["bu"] * r["bp"] for r in rows), bu)
    var = _half_up(total * sum(r["bu"] * r["q"] * price for r in rows), bu)
    return {
        "units": total,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "fixed_cost_cents": fixed,
        "profit_cents": rev - var - fixed,
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    price, fixed, used, rows = _read(case)
    bu = sum(r["bu"] for r in rows)
    budget_rev = sum(r["bu"] * r["bp"] for r in rows)
    budget_var = sum(r["bu"] * r["q"] * price for r in rows)
    master = budget_rev - budget_var - fixed
    total_units = sum(r["au"] for r in rows)
    flexed = _half_up(total_units * budget_rev, bu) - _half_up(total_units * budget_var, bu) - fixed
    sales_price = sum((r["ap"] - r["bp"]) * r["au"] for r in rows)
    efficiency = price * (sum(r["q"] * r["au"] for r in rows) - used)
    mix = sum(r["au"] * (r["bp"] - r["q"] * price) for r in rows) - fixed - flexed
    actual = sum(r["au"] * r["ap"] for r in rows) - price * used - fixed
    return {
        "sales_price": sales_price,
        "sales_volume": flexed - master,
        "sales_mix": mix,
        "efficiency": efficiency,
        "total": actual - master,
    }
