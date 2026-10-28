"""Alternative correct engine for the AC4 suite: rounding by floor of value plus one half; validation by operator.index.

Written from the page's specification alone (not from the reference): whole-cent values halve up; bool, float and text are refused.
"""

from __future__ import annotations

import math
import operator
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

_CASE = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")
_PRODUCT = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _int(value: object, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label} is a boolean")
    try:
        return int(operator.index(value))
    except TypeError:
        raise ValueError(f"{label} is not a whole number") from None


def _pos(value: object, label: str) -> int:
    n = _int(value, label)
    if n < 0:
        raise ValueError(f"{label} is negative")
    return n


def _half_up(q: Fraction) -> int:
    return math.floor(q + Fraction(1, 2))


def _load(case: object) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case is not a mapping")
    for key in _CASE:
        if key not in case:
            raise ValueError(f"missing {key}")
    price = _pos(case["input_price_cents"], "input_price_cents")
    fixed = _pos(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _pos(case["actual_inputs_used"], "actual_inputs_used")
    rows = case["products"]
    if type(rows) is not list or len(rows) == 0:
        raise ValueError("products must be a non-empty list")
    names: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("a product is not a mapping")
        for key in _PRODUCT:
            if key not in row:
                raise ValueError(f"a product has no {key}")
        name = row["name"]
        if not isinstance(name, str) or name == "" or name in names:
            raise ValueError("bad product name")
        names.add(name)
        out.append(
            {
                "name": name,
                "bu": _pos(row["budget_units"], f"{name} budget_units"),
                "bp": _pos(row["budget_price_cents"], f"{name} budget_price_cents"),
                "q": _pos(row["standard_inputs_per_unit"], f"{name} standard_inputs_per_unit"),
                "au": _pos(row["actual_units"], f"{name} actual_units"),
                "ap": _pos(row["actual_price_cents"], f"{name} actual_price_cents"),
            }
        )
    if sum(p["bu"] for p in out) == 0:
        raise ValueError("no budgeted units")
    return price, fixed, used, out


def _flex_parts(products: list[dict[str, Any]], price: int, total: int) -> tuple[int, int, int]:
    bu = sum(p["bu"] for p in products)
    rev = sum(p["bu"] * p["bp"] for p in products)
    var = sum(p["bu"] * p["q"] * price for p in products)
    return _half_up(Fraction(total * rev, bu)), _half_up(Fraction(total * var, bu)), bu


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    price, fixed, _, products = _load(case)
    units = {p["name"]: p["bu"] for p in products}
    revenue = {p["name"]: p["bu"] * p["bp"] for p in products}
    variable = {p["name"]: p["bu"] * p["q"] * price for p in products}
    tr = sum(revenue.values())
    tv = sum(variable.values())
    return {
        "units": dict(units),
        "revenue_cents": dict(revenue),
        "variable_cost_cents": dict(variable),
        "total_units": sum(units.values()),
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": fixed,
        "profit_cents": tr - tv - fixed,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    price, fixed, _, products = _load(case)
    total = _pos(actual_units, "actual_units")
    rev, var, _ = _flex_parts(products, price, total)
    return {
        "units": total,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "fixed_cost_cents": fixed,
        "profit_cents": rev - var - fixed,
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    price, fixed, used, products = _load(case)
    master = master_budget(case)["profit_cents"]
    total_au = sum(p["au"] for p in products)
    rev, var, _ = _flex_parts(products, price, total_au)
    flexed = rev - var - fixed
    sales_price = sum((p["ap"] - p["bp"]) * p["au"] for p in products)
    efficiency = price * (sum(p["q"] * p["au"] for p in products) - used)
    mix = sum(p["au"] * (p["bp"] - p["q"] * price) for p in products) - fixed - flexed
    actual = sum(p["au"] * p["ap"] for p in products) - price * used - fixed
    return {
        "sales_price": sales_price,
        "sales_volume": flexed - master,
        "sales_mix": mix,
        "efficiency": efficiency,
        "total": actual - master,
    }
