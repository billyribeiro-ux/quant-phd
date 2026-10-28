"""Alternative e: Fraction-based, one generic whole-number validator, class-free."""
from fractions import Fraction
from typing import Any, Mapping

_FIELDS = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")
_ROW = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _whole(value: Any, label: str, *, allow_negative: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label} must be a whole number")
    if value < 0 and not allow_negative:
        raise ValueError(f"{label} must not be negative")
    return value


def _half_up(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _validate(case: Mapping[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(case, Mapping):
        raise ValueError("case must be a mapping")
    for f in _FIELDS:
        if f not in case:
            raise ValueError(f"case has no {f}")
    _whole(case["input_price_cents"], "input price")
    _whole(case["fixed_overhead_cents"], "fixed overhead")
    _whole(case["actual_inputs_used"], "actual inputs")
    rows = case["products"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("products must be a non-empty list")
    names: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("product must be a mapping")
        for f in _ROW:
            if f not in row:
                raise ValueError(f"product has no {f}")
        if not isinstance(row["name"], str) or not row["name"] or row["name"] in names:
            raise ValueError("product names must be non-empty and unique")
        names.add(row["name"])
        for f in _ROW[1:]:
            _whole(row[f], f)
    if sum(r["budget_units"] for r in rows) == 0:
        raise ValueError("no budgeted units")
    return list(rows)


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    rows = _validate(case)
    s = case["input_price_cents"]
    units = {r["name"]: r["budget_units"] for r in rows}
    revenue = {r["name"]: r["budget_units"] * r["budget_price_cents"] for r in rows}
    variable = {r["name"]: r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows}
    tr, tv = sum(revenue.values()), sum(variable.values())
    return {
        "units": units,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_units": sum(units.values()),
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": case["fixed_overhead_cents"],
        "profit_cents": tr - tv - case["fixed_overhead_cents"],
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    rows = _validate(case)
    if isinstance(actual_units, bool) or not isinstance(actual_units, int) or actual_units < 0:
        raise ValueError("actual units must be a non-negative whole number")
    s = case["input_price_cents"]
    bt = sum(r["budget_units"] for r in rows)
    br = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    bv = sum(r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows)
    rev = _half_up(Fraction(actual_units * br, bt))
    var = _half_up(Fraction(actual_units * bv, bt))
    f = case["fixed_overhead_cents"]
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": f, "profit_cents": rev - var - f}


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    rows = _validate(case)
    s = case["input_price_cents"]
    f = case["fixed_overhead_cents"]
    aq = case["actual_inputs_used"]
    bt = sum(r["budget_units"] for r in rows)
    br = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    bv = sum(r["budget_units"] * r["standard_inputs_per_unit"] * s for r in rows)
    master = br - bv - f
    at = sum(r["actual_units"] for r in rows)
    flexed = _half_up(Fraction(at * br, bt)) - _half_up(Fraction(at * bv, bt)) - f
    price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    mix_margin = sum(r["actual_units"] * (r["budget_price_cents"] - r["standard_inputs_per_unit"] * s) for r in rows)
    std = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows)
    actual_profit = sum(r["actual_price_cents"] * r["actual_units"] for r in rows) - s * aq - f
    out = {
        "sales_price": price,
        "sales_volume": flexed - master,
        "sales_mix": mix_margin - f - flexed,
        "efficiency": s * (std - aq),
    }
    out["total"] = actual_profit - master
    return out
