"""Correct alternative: rounding as floor(x) plus one when the fractional part is at least one half, via Fraction; masks read through a dict copy."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Mapping


def _fields(case: Any) -> dict[str, Any]:
    if not isinstance(case, Mapping):
        raise ValueError("a case is a mapping")
    data = dict(case)
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in data:
            raise ValueError("the case lacks " + key)
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"):
        v = data[key]
        if type(v) is not int or v < 0:
            raise ValueError(key + " must be a non-negative whole number")
    prods = data["products"]
    if not isinstance(prods, list) or len(prods) == 0:
        raise ValueError("products must be a non-empty list")
    cleaned = []
    names: set[str] = set()
    for item in prods:
        if not isinstance(item, Mapping):
            raise ValueError("each product is a mapping")
        keys = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")
        for key in keys:
            if key not in item:
                raise ValueError("a product lacks " + key)
        nm = item["name"]
        if type(nm) is not str or not nm:
            raise ValueError("a name is non-empty text")
        if nm in names:
            raise ValueError("a name repeats")
        names.add(nm)
        entry = {"name": nm}
        for key in keys[1:]:
            v = item[key]
            if type(v) is not int or v < 0:
                raise ValueError(key + " must be a non-negative whole number")
            entry[key] = v
        cleaned.append(entry)
    if sum(e["budget_units"] for e in cleaned) <= 0:
        raise ValueError("the budget has no units")
    data["products"] = cleaned
    return data


def _round(x: Fraction) -> int:
    base = math.floor(x)
    return base + 1 if x - base >= Fraction(1, 2) else base


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    d = _fields(case)
    s = d["input_price_cents"]
    f = d["fixed_overhead_cents"]
    rows = d["products"]
    units = {r["name"]: r["budget_units"] for r in rows}
    revenue = {r["name"]: r["budget_units"] * r["budget_price_cents"] for r in rows}
    variable = {r["name"]: r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows}
    total_revenue = sum(revenue.values())
    total_variable = sum(variable.values())
    return {
        "units": units,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_units": sum(units.values()),
        "total_revenue_cents": total_revenue,
        "total_variable_cost_cents": total_variable,
        "fixed_cost_cents": f,
        "profit_cents": total_revenue - total_variable - f,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    d = _fields(case)
    if type(actual_units) is not int or actual_units < 0:
        raise ValueError("actual_units must be a non-negative whole number")
    s = d["input_price_cents"]
    f = d["fixed_overhead_cents"]
    rows = d["products"]
    bu = sum(r["budget_units"] for r in rows)
    brev = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    bvar = sum(r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows)
    rev = _round(Fraction(actual_units * brev, bu))
    var = _round(Fraction(actual_units * bvar, bu))
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": f, "profit_cents": rev - var - f}


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    d = _fields(case)
    s = d["input_price_cents"]
    f = d["fixed_overhead_cents"]
    aq = d["actual_inputs_used"]
    rows = d["products"]
    at = sum(r["actual_units"] for r in rows)
    fp = flexible_budget(case, at)["profit_cents"]
    mp = master_budget(case)["profit_cents"]
    price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    eff = s * (sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows) - aq)
    mix_contrib = sum(r["actual_units"] * r["budget_price_cents"] - r["actual_units"] * r["standard_inputs_per_unit"] * s for r in rows) - f
    actual_total = sum(r["actual_units"] * r["actual_price_cents"] for r in rows) - s * aq - f
    return {
        "sales_price": price,
        "sales_volume": fp - mp,
        "sales_mix": mix_contrib - fp,
        "efficiency": eff,
        "total": actual_total - mp,
    }
