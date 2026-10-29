"""Alternative correct engine for the AC4 suite: Decimal with ROUND_HALF_UP in a 60-digit context; strict int check.

Written from the page's specification alone: whole-cent values halve up; bool, float and text are refused.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal, localcontext
from typing import Any

FIELDS = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _n(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an int (whole cents or units)")
    if value < 0:
        raise ValueError(f"{label} must not be negative")
    return value


def _cents(numerator: int, denominator: int) -> int:
    with localcontext() as ctx:
        ctx.prec = 60
        quotient = (Decimal(numerator) / Decimal(denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(quotient)


def _parse(case: object) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case must be a mapping")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError(f"missing {key}")
    price = _n(case["input_price_cents"], "input_price_cents")
    fixed = _n(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _n(case["actual_inputs_used"], "actual_inputs_used")
    products = case["products"]
    if not isinstance(products, list) or len(products) == 0:
        raise ValueError("products must be a non-empty list")
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for p in products:
        if not isinstance(p, Mapping):
            raise ValueError("product must be a mapping")
        for key in FIELDS:
            if key not in p:
                raise ValueError(f"product missing {key}")
        if not isinstance(p["name"], str) or not p["name"] or p["name"] in seen:
            raise ValueError("product name must be unique non-empty text")
        seen.add(p["name"])
        out.append(
            {
                "name": p["name"],
                "bu": _n(p["budget_units"], "budget_units"),
                "bp": _n(p["budget_price_cents"], "budget_price_cents"),
                "q": _n(p["standard_inputs_per_unit"], "standard_inputs_per_unit"),
                "au": _n(p["actual_units"], "actual_units"),
                "ap": _n(p["actual_price_cents"], "actual_price_cents"),
            }
        )
    if sum(p["bu"] for p in out) == 0:
        raise ValueError("no budgeted units in the master budget")
    return price, fixed, used, out


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    price, fixed, _, ps = _parse(case)
    revenue = {p["name"]: p["bu"] * p["bp"] for p in ps}
    variable = {p["name"]: p["bu"] * p["q"] * price for p in ps}
    tr, tv = sum(revenue.values()), sum(variable.values())
    return {
        "units": {p["name"]: p["bu"] for p in ps},
        "total_units": sum(p["bu"] for p in ps),
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": fixed,
        "profit_cents": tr - tv - fixed,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    price, fixed, _, ps = _parse(case)
    total = _n(actual_units, "actual_units")
    bu = sum(p["bu"] for p in ps)
    rev = _cents(total * sum(p["bu"] * p["bp"] for p in ps), bu)
    var = _cents(total * sum(p["bu"] * p["q"] * price for p in ps), bu)
    return {
        "units": total,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "fixed_cost_cents": fixed,
        "profit_cents": rev - var - fixed,
    }


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    price, fixed, used, ps = _parse(case)
    master = master_budget(case)["profit_cents"]
    flexed = flexible_budget(case, sum(p["au"] for p in ps))["profit_cents"]
    price_var = sum((p["ap"] - p["bp"]) * p["au"] for p in ps)
    eff = price * (sum(p["q"] * p["au"] for p in ps) - used)
    mix = sum(p["au"] * p["bp"] - p["au"] * p["q"] * price for p in ps) - fixed - flexed
    actual = sum(p["au"] * p["ap"] for p in ps) - price * used - fixed
    return {
        "sales_price": price_var,
        "sales_volume": flexed - master,
        "sales_mix": mix,
        "efficiency": eff,
        "total": actual - master,
    }
