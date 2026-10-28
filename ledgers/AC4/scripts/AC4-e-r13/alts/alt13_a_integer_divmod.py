"""Alternative 13a: integer-only nearest-cent rounding with divmod; validation by explicit type tests."""
from collections.abc import Mapping
from typing import Any

FIELDS = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _int(v: Any, what: str) -> int:
    if type(v) is not int:
        raise ValueError(f"{what} must be a whole number")
    if v < 0:
        raise ValueError(f"{what} must not be negative")
    return v


def _half_up(num: int, den: int) -> int:
    q, r = divmod(2 * num + den, 2 * den)
    return q


def _load(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case must be a mapping")
    for f in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if f not in case:
            raise ValueError("missing field " + f)
    s = _int(case["input_price_cents"], "input price")
    fixed = _int(case["fixed_overhead_cents"], "fixed overhead")
    aq = _int(case["actual_inputs_used"], "actual inputs")
    rows = case["products"]
    if type(rows) is not list or len(rows) == 0:
        raise ValueError("products must be a non-empty list")
    out: list[dict[str, Any]] = []
    names: set[str] = set()
    for r in rows:
        if not isinstance(r, Mapping):
            raise ValueError("each product must be a mapping")
        for f in FIELDS:
            if f not in r:
                raise ValueError("product missing " + f)
        n = r["name"]
        if type(n) is not str or n == "":
            raise ValueError("bad product name")
        if n in names:
            raise ValueError("duplicate product name")
        names.add(n)
        out.append({"name": n, **{f: _int(r[f], f) for f in FIELDS[1:]}})
    if sum(p["budget_units"] for p in out) == 0:
        raise ValueError("no budgeted units")
    return s, fixed, aq, out


def master_budget(case: Any) -> dict[str, Any]:
    s, fixed, _, rows = _load(case)
    units = {p["name"]: p["budget_units"] for p in rows}
    rev = {p["name"]: p["budget_units"] * p["budget_price_cents"] for p in rows}
    var = {p["name"]: p["budget_units"] * p["standard_inputs_per_unit"] * s for p in rows}
    tr, tv = sum(rev.values()), sum(var.values())
    return {"units": units, "revenue_cents": rev, "variable_cost_cents": var, "total_units": sum(units.values()),
            "total_revenue_cents": tr, "total_variable_cost_cents": tv, "fixed_cost_cents": fixed,
            "profit_cents": tr - tv - fixed}


def _flex_parts(rows: list[dict[str, Any]], s: int, total: int) -> tuple[int, int]:
    bu = sum(p["budget_units"] for p in rows)
    br = sum(p["budget_units"] * p["budget_price_cents"] for p in rows)
    bv = sum(p["budget_units"] * p["standard_inputs_per_unit"] * s for p in rows)
    return _half_up(total * br, bu), _half_up(total * bv, bu)


def flexible_budget(case: Any, actual_units: int) -> dict[str, Any]:
    s, fixed, _, rows = _load(case)
    total = _int(actual_units, "actual units")
    rev, var = _flex_parts(rows, s, total)
    return {"units": total, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": fixed,
            "profit_cents": rev - var - fixed}


def variance_decomposition(case: Any) -> dict[str, int]:
    s, fixed, aq, rows = _load(case)
    m = master_budget(case)["profit_cents"]
    at = sum(p["actual_units"] for p in rows)
    flex = flexible_budget(case, at)["profit_cents"]
    price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in rows)
    eff = s * (sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in rows) - aq)
    mix_c = sum(p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * s) for p in rows) - fixed
    act = sum(p["actual_units"] * p["actual_price_cents"] for p in rows) - s * aq - fixed
    return {"sales_price": price, "sales_volume": flex - m, "sales_mix": mix_c - flex, "efficiency": eff,
            "total": act - m}
