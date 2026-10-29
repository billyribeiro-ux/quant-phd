"""Correct alternative: flexed amounts rounded with Decimal ROUND_HALF_UP on exact quotients; type checks via type() is int."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from typing import Any

_PRODUCT_KEYS = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _int(value: Any, label: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} must be a whole number")
    return value


def _count(value: Any, label: str) -> int:
    v = _int(value, label)
    if v < 0:
        raise ValueError(f"{label} must not be negative")
    return v


def _validated(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case must be a mapping")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError(f"missing {key}")
    rows_in = case["products"]
    if type(rows_in) is not list or len(rows_in) == 0:
        raise ValueError("products must be a non-empty list")
    s = _count(case["input_price_cents"], "input_price_cents")
    f = _count(case["fixed_overhead_cents"], "fixed_overhead_cents")
    aq = _count(case["actual_inputs_used"], "actual_inputs_used")
    rows: list[dict[str, Any]] = []
    names: set[str] = set()
    for item in rows_in:
        if not isinstance(item, Mapping):
            raise ValueError("a product must be a mapping")
        for key in _PRODUCT_KEYS:
            if key not in item:
                raise ValueError(f"product missing {key}")
        nm = item["name"]
        if type(nm) is not str or nm == "":
            raise ValueError("bad product name")
        if nm in names:
            raise ValueError("duplicate product name")
        names.add(nm)
        rows.append({
            "name": nm,
            "budget_units": _count(item["budget_units"], "budget_units"),
            "budget_price_cents": _count(item["budget_price_cents"], "budget_price_cents"),
            "standard_inputs_per_unit": _count(item["standard_inputs_per_unit"], "standard_inputs_per_unit"),
            "actual_units": _count(item["actual_units"], "actual_units"),
            "actual_price_cents": _count(item["actual_price_cents"], "actual_price_cents"),
        })
    if sum(r["budget_units"] for r in rows) == 0:
        raise ValueError("no budgeted units")
    return s, f, aq, rows


def _half_up(q: Fraction) -> int:
    with localcontext() as ctx:
        ctx.prec = 80
        d = (Decimal(q.numerator) / Decimal(q.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(d)


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    s, f, _, rows = _validated(case)
    units = {r["name"]: r["budget_units"] for r in rows}
    rev = {r["name"]: r["budget_units"] * r["budget_price_cents"] for r in rows}
    var = {r["name"]: r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows}
    tr = sum(rev.values())
    tv = sum(var.values())
    return {
        "units": units,
        "revenue_cents": rev,
        "variable_cost_cents": var,
        "total_units": sum(units.values()),
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": f,
        "profit_cents": tr - tv - f,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    s, f, _, rows = _validated(case)
    n = _count(actual_units, "actual_units")
    bu = sum(r["budget_units"] for r in rows)
    brev = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    bvar = sum(r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows)
    rev = _half_up(Fraction(n * brev, bu))
    var = _half_up(Fraction(n * bvar, bu))
    return {"units": n, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": f, "profit_cents": rev - var - f}


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    s, f, aq, rows = _validated(case)
    master = master_budget(case)["profit_cents"]
    at = sum(r["actual_units"] for r in rows)
    flexed = flexible_budget(case, at)["profit_cents"]
    price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    std_for_output = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows)
    eff = s * (std_for_output - aq)
    mix = sum(r["actual_units"] * (r["budget_price_cents"] - r["standard_inputs_per_unit"] * s) for r in rows) - f - flexed
    actual_profit = sum(r["actual_units"] * r["actual_price_cents"] for r in rows) - s * aq - f
    return {"sales_price": price, "sales_volume": flexed - master, "sales_mix": mix, "efficiency": eff, "total": actual_profit - master}
