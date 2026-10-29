"""Alternative correct engine for the AC4 suite: validation with numbers.Integral; a single pipeline of named steps.

Written from the page's specification alone: whole-cent values halve up; bool, float and text are refused.
"""

from __future__ import annotations

import numbers
from collections.abc import Mapping
from fractions import Fraction
from typing import Any


def _whole(value: object, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{label} must be a whole number")
    number = int(value)
    if number < minimum:
        raise ValueError(f"{label} must be at least {minimum}")
    return number


def _steps(case: object) -> dict[str, Any]:
    if not isinstance(case, Mapping):
        raise ValueError("the case must be a mapping")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError(f"no {key}")
    price = _whole(case["input_price_cents"], "input_price_cents")
    fixed = _whole(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _whole(case["actual_inputs_used"], "actual_inputs_used")
    rows = case["products"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("products must be a non-empty list of mappings")
    products = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("a product must be a mapping")
        for key in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"):
            if key not in row:
                raise ValueError(f"a product has no {key}")
        name = row["name"]
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("a product name must be non-empty text and unique")
        seen.add(name)
        products.append(
            {
                "name": name,
                "bu": _whole(row["budget_units"], f"{name} budget_units"),
                "bp": _whole(row["budget_price_cents"], f"{name} budget_price_cents"),
                "q": _whole(row["standard_inputs_per_unit"], f"{name} standard_inputs_per_unit"),
                "au": _whole(row["actual_units"], f"{name} actual_units"),
                "ap": _whole(row["actual_price_cents"], f"{name} actual_price_cents"),
            }
        )
    if sum(p["bu"] for p in products) == 0:
        raise ValueError("the master budget has no budgeted units")
    return {"price": price, "fixed": fixed, "used": used, "products": products}


def _nearest(q: Fraction) -> int:
    return int((q + Fraction(1, 2)) // 1)


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    s = _steps(case)
    ps = s["products"]
    units = {p["name"]: p["bu"] for p in ps}
    revenue = {p["name"]: p["bu"] * p["bp"] for p in ps}
    variable = {p["name"]: p["bu"] * p["q"] * s["price"] for p in ps}
    total_rev = sum(revenue.values())
    total_var = sum(variable.values())
    return {
        "units": units,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_units": sum(units.values()),
        "total_revenue_cents": total_rev,
        "total_variable_cost_cents": total_var,
        "fixed_cost_cents": s["fixed"],
        "profit_cents": total_rev - total_var - s["fixed"],
    }


def _flex(s: dict[str, Any], total: int) -> tuple[int, int]:
    ps = s["products"]
    bu = sum(p["bu"] for p in ps)
    rev = sum(p["bu"] * p["bp"] for p in ps)
    var = sum(p["bu"] * p["q"] * s["price"] for p in ps)
    return _nearest(Fraction(total * rev, bu)), _nearest(Fraction(total * var, bu))


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    s = _steps(case)
    total = _whole(actual_units, "actual_units")
    rev, var = _flex(s, total)
    return {
        "units": total,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "fixed_cost_cents": s["fixed"],
        "profit_cents": rev - var - s["fixed"],
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    s = _steps(case)
    ps = s["products"]
    price, fixed = s["price"], s["fixed"]
    budget_profit = master_budget(case)["profit_cents"]
    total_au = sum(p["au"] for p in ps)
    rev, var = _flex(s, total_au)
    flexed = rev - var - fixed
    price_var = sum((p["ap"] - p["bp"]) * p["au"] for p in ps)
    eff = price * (sum(p["q"] * p["au"] for p in ps) - s["used"])
    actual_mix_contrib = sum(p["au"] * p["bp"] - p["au"] * p["q"] * price for p in ps) - fixed
    mix = actual_mix_contrib - flexed
    actual_profit = sum(p["au"] * p["ap"] for p in ps) - price * s["used"] - fixed
    return {
        "sales_price": price_var,
        "sales_volume": flexed - budget_profit,
        "sales_mix": mix,
        "efficiency": eff,
        "total": actual_profit - budget_profit,
    }
