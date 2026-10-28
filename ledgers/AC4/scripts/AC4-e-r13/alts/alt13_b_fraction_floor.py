"""Alternative 13b: Fraction arithmetic, nearest cent by floor(x + 1/2); validation with numbers.Integral and bool test."""
import math
import numbers
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

PF = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _n(v: Any, what: str) -> int:
    if isinstance(v, bool) or not isinstance(v, numbers.Integral):
        raise ValueError(what + " must be a whole number")
    if v < 0:
        raise ValueError(what + " must not be negative")
    return int(v)


def _cent(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _rows(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("the case must be a mapping")
    try:
        s, fixed, aq, raw = case["input_price_cents"], case["fixed_overhead_cents"], case["actual_inputs_used"], case["products"]
    except KeyError as exc:
        raise ValueError("the case lacks a field") from exc
    s, fixed, aq = _n(s, "input price"), _n(fixed, "fixed overhead"), _n(aq, "actual inputs")
    if not isinstance(raw, list) or not raw:
        raise ValueError("the products must be a non-empty list")
    prods = []
    seen = set()
    for r in raw:
        if not isinstance(r, Mapping) or any(f not in r for f in PF):
            raise ValueError("a product must be a mapping with every field")
        nm = r["name"]
        if not isinstance(nm, str) or nm == "" or nm in seen:
            raise ValueError("a product name must be unique non-empty text")
        seen.add(nm)
        prods.append({"name": nm, **{f: _n(r[f], f) for f in PF[1:]}})
    if sum(p["budget_units"] for p in prods) <= 0:
        raise ValueError("no budgeted units")
    return s, fixed, aq, prods


def master_budget(case: Any) -> dict[str, Any]:
    s, fixed, _, prods = _rows(case)
    units = {p["name"]: p["budget_units"] for p in prods}
    rev = {p["name"]: p["budget_units"] * p["budget_price_cents"] for p in prods}
    var = {p["name"]: p["budget_units"] * p["standard_inputs_per_unit"] * s for p in prods}
    tr, tv = sum(rev.values()), sum(var.values())
    return {"units": units, "revenue_cents": rev, "variable_cost_cents": var, "total_units": sum(units.values()),
            "total_revenue_cents": tr, "total_variable_cost_cents": tv, "fixed_cost_cents": fixed,
            "profit_cents": tr - tv - fixed}


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    s, fixed, _, prods = _rows(case)
    total = _n(actual_units, "actual units")
    bu = sum(p["budget_units"] for p in prods)
    br = sum(p["budget_units"] * p["budget_price_cents"] for p in prods)
    bv = sum(p["budget_units"] * p["standard_inputs_per_unit"] * s for p in prods)
    rev = _cent(Fraction(total * br, bu))
    var = _cent(Fraction(total * bv, bu))
    return {"units": total, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": fixed,
            "profit_cents": rev - var - fixed}


def variance_decomposition(case: Any) -> dict[str, int]:
    s, fixed, aq, prods = _rows(case)
    m = master_budget(case)["profit_cents"]
    flex = flexible_budget(case, sum(p["actual_units"] for p in prods))["profit_cents"]
    price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in prods)
    eff = s * (sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in prods) - aq)
    mix_c = sum(p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * s) for p in prods) - fixed
    act = sum(p["actual_units"] * p["actual_price_cents"] for p in prods) - s * aq - fixed
    return {"sales_price": price, "sales_volume": flex - m, "sales_mix": mix_c - flex, "efficiency": eff,
            "total": act - m}
