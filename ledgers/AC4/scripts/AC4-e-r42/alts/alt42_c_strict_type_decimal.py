"""Alternative correct engine for the AC4 suite: strict int type checks; quotients rounded with Decimal ROUND_HALF_UP.

Written from the page's specification alone: whole-cent values halve up; bool, float and text are refused.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def _n(value: object, label: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} is not an int")
    if value < 0:
        raise ValueError(f"{label} is negative")
    return value


def _cents(numer: int, denom: int) -> int:
    value = (Decimal(numer) / Decimal(denom)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(value)


def _read(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case must be a mapping")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError(f"missing {key}")
    price = _n(case["input_price_cents"], "input_price_cents")
    fixed = _n(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _n(case["actual_inputs_used"], "actual_inputs_used")
    rows = case["products"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("products must be a non-empty list")
    names: list[str] = []
    out = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("product must be a mapping")
        for key in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"):
            if key not in row:
                raise ValueError(f"product missing {key}")
        name = row["name"]
        if not isinstance(name, str) or name == "" or name in names:
            raise ValueError("bad name")
        names.append(name)
        out.append(
            {
                "name": name,
                "bu": _n(row["budget_units"], "budget_units"),
                "bp": _n(row["budget_price_cents"], "budget_price_cents"),
                "q": _n(row["standard_inputs_per_unit"], "standard_inputs_per_unit"),
                "au": _n(row["actual_units"], "actual_units"),
                "ap": _n(row["actual_price_cents"], "actual_price_cents"),
            }
        )
    if sum(p["bu"] for p in out) == 0:
        raise ValueError("no budgeted units")
    return price, fixed, used, out


def _flexed(price: int, fixed: int, products: list[dict[str, Any]], total: int) -> tuple[int, int, int]:
    bu = sum(p["bu"] for p in products)
    rev_per = sum(p["bu"] * p["bp"] for p in products)
    var_per = sum(p["bu"] * p["q"] * price for p in products)
    rev = _cents(total * rev_per, bu)
    var = _cents(total * var_per, bu)
    return rev, var, rev - var - fixed


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    price, fixed, _, products = _read(case)
    units = {p["name"]: p["bu"] for p in products}
    revenue = {p["name"]: p["bu"] * p["bp"] for p in products}
    variable = {p["name"]: p["bu"] * p["q"] * price for p in products}
    total_rev = sum(revenue.values())
    total_var = sum(variable.values())
    return {
        "units": units,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_units": sum(units.values()),
        "total_revenue_cents": total_rev,
        "total_variable_cost_cents": total_var,
        "fixed_cost_cents": fixed,
        "profit_cents": total_rev - total_var - fixed,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    price, fixed, _, products = _read(case)
    total = _n(actual_units, "actual_units")
    rev, var, profit = _flexed(price, fixed, products, total)
    return {
        "units": total,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "fixed_cost_cents": fixed,
        "profit_cents": profit,
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    price, fixed, used, products = _read(case)
    budget = master_budget(case)["profit_cents"]
    total_au = sum(p["au"] for p in products)
    _, _, flexed = _flexed(price, fixed, products, total_au)
    price_var = sum((p["ap"] - p["bp"]) * p["au"] for p in products)
    std_inputs = sum(p["q"] * p["au"] for p in products)
    eff = price * (std_inputs - used)
    mix = sum(p["au"] * (p["bp"] - p["q"] * price) for p in products) - fixed - flexed
    actual = sum(p["au"] * p["ap"] for p in products) - price * used - fixed
    return {
        "sales_price": price_var,
        "sales_volume": flexed - budget,
        "sales_mix": mix,
        "efficiency": eff,
        "total": actual - budget,
    }
