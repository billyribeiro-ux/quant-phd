"""Alternative B (correct): sales mix derived as the total less the other three variances.
"""

from __future__ import annotations

import numbers
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

PRODUCT_FIELDS = (
    "name",
    "budget_units",
    "budget_price_cents",
    "standard_inputs_per_unit",
    "actual_units",
    "actual_price_cents",
)
CASE_FIELDS = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")


def _whole(value: object, name: str) -> int:
    """An integer that is not a bool, or a ValueError naming the field."""
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number of cents or units, not {value!r}")
    return int(value)


def _nonnegative(value: object, name: str) -> int:
    number = _whole(value, name)
    if number < 0:
        raise ValueError(f"{name} must not be negative, got {number}")
    return number


def _nearest_cent(amount: Fraction) -> int:
    """The nearest whole cent, halves up. The amounts here are never negative."""
    if amount < 0:
        raise ValueError("a flexed amount cannot be negative")
    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)


def _case(case: object) -> tuple[int, int, int, list[dict[str, Any]]]:
    """Validate a case; return (input price, fixed overhead, actual inputs used, products)."""
    if not isinstance(case, Mapping):
        raise ValueError("the case must be a mapping of the case fields")
    for field in CASE_FIELDS:
        if field not in case:
            raise ValueError(f"the case has no {field!r} field")
    input_price = _nonnegative(case["input_price_cents"], "input_price_cents")
    fixed = _nonnegative(case["fixed_overhead_cents"], "fixed_overhead_cents")
    actual_inputs = _nonnegative(case["actual_inputs_used"], "actual_inputs_used")
    raw = case["products"]
    if not isinstance(raw, list) or not raw:
        raise ValueError("the case needs at least one product")
    products: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("each product must be a mapping")
        for field in PRODUCT_FIELDS:
            if field not in item:
                raise ValueError(f"a product has no {field!r} field")
        name = item["name"]
        if not isinstance(name, str) or not name:
            raise ValueError("a product name must be a non-empty string")
        if name in seen:
            raise ValueError(f"the product name {name!r} appears twice")
        seen.add(name)
        products.append(
            {
                "name": name,
                "budget_units": _nonnegative(item["budget_units"], f"{name} budget_units"),
                "budget_price_cents": _nonnegative(item["budget_price_cents"], f"{name} budget_price_cents"),
                "standard_inputs_per_unit": _nonnegative(
                    item["standard_inputs_per_unit"], f"{name} standard_inputs_per_unit"
                ),
                "actual_units": _nonnegative(item["actual_units"], f"{name} actual_units"),
                "actual_price_cents": _nonnegative(item["actual_price_cents"], f"{name} actual_price_cents"),
            }
        )
    if sum(p["budget_units"] for p in products) == 0:
        raise ValueError("the master budget has no budgeted units, so no budgeted mix exists")
    return input_price, fixed, actual_inputs, products


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    """The master budget: budgeted units, revenue and cost by product, and the budgeted profit, in cents."""
    input_price, fixed, _, products = _case(case)
    units = {p["name"]: p["budget_units"] for p in products}
    revenue = {p["name"]: p["budget_units"] * p["budget_price_cents"] for p in products}
    variable = {p["name"]: p["budget_units"] * p["standard_inputs_per_unit"] * input_price for p in products}
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
    """The budget flexed to a total of ``actual_units`` units at the budgeted mix, in cents."""
    input_price, fixed, _, products = _case(case)
    total = _nonnegative(actual_units, "actual_units")
    budget_units = sum(p["budget_units"] for p in products)
    budget_revenue = sum(p["budget_units"] * p["budget_price_cents"] for p in products)
    budget_variable = sum(p["budget_units"] * p["standard_inputs_per_unit"] * input_price for p in products)
    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))
    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))
    return {
        "units": total,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "fixed_cost_cents": fixed,
        "profit_cents": revenue - variable - fixed,
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    """The four profit variances and their total, in cents; favourable is positive."""
    input_price, fixed, actual_inputs, products = _case(case)
    master = master_budget(case)["profit_cents"]
    actual_total = sum(p["actual_units"] for p in products)
    flexed = flexible_budget(case, actual_total)["profit_cents"]
    sales_price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in products)
    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)
    efficiency = input_price * (standard_inputs - actual_inputs)
    actual_mix_contribution = (
        sum(
            p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * input_price)
            for p in products
        )
        - fixed
    )
    actual_profit = sum(p["actual_units"] * p["actual_price_cents"] for p in products) - input_price * actual_inputs
    actual_profit -= fixed
    sales_volume = flexed - master
    sales_mix = (actual_profit - master) - sales_volume - sales_price - efficiency
    return {
        "sales_price": sales_price,
        "sales_volume": sales_volume,
        "sales_mix": sales_mix,
        "efficiency": efficiency,
        "total": actual_profit - master,
    }
