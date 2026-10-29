"""Correct alternative: rounding by divmod remainder comparison; validation with a single pass and a helper for products."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _whole(value: Any, what: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{what}: whole number required")
    if value < minimum:
        raise ValueError(f"{what}: below {minimum}")
    return value


def _unpack(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, Mapping):
        raise ValueError("case: mapping required")
    needed = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")
    absent = [k for k in needed if k not in case]
    if absent:
        raise ValueError("case: missing " + absent[0])
    s = _whole(case["input_price_cents"], "input price")
    f = _whole(case["fixed_overhead_cents"], "fixed overhead")
    aq = _whole(case["actual_inputs_used"], "actual inputs")
    prods = case["products"]
    if not isinstance(prods, list) or not prods:
        raise ValueError("products: non-empty list required")
    out: list[dict[str, Any]] = []
    seen: list[str] = []
    for p in prods:
        if not isinstance(p, Mapping):
            raise ValueError("product: mapping required")
        for k in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"):
            if k not in p:
                raise ValueError("product: missing " + k)
        name = p["name"]
        if not isinstance(name, str) or not name.strip(" ") and name == "":
            raise ValueError("product name: text required")
        if isinstance(name, bool) or not isinstance(name, str) or name == "":
            raise ValueError("product name: non-empty text required")
        if name in seen:
            raise ValueError("product name: duplicate")
        seen.append(name)
        out.append({
            "name": name,
            "bu": _whole(p["budget_units"], "budget units"),
            "bp": _whole(p["budget_price_cents"], "budget price"),
            "q": _whole(p["standard_inputs_per_unit"], "standard inputs"),
            "au": _whole(p["actual_units"], "actual units"),
            "ap": _whole(p["actual_price_cents"], "actual price"),
        })
    if sum(p["bu"] for p in out) == 0:
        raise ValueError("no budgeted units")
    return s, f, aq, out


def _round_half_up(n: int, d: int) -> int:
    q, r = divmod(n, d)
    return q + 1 if 2 * r >= d else q


def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:
    s, f, _, ps = _unpack(case)
    units = {p["name"]: p["bu"] for p in ps}
    revenue = {p["name"]: p["bu"] * p["bp"] for p in ps}
    variable = {p["name"]: p["bu"] * p["q"] * s for p in ps}
    tu = sum(units.values())
    tr = sum(revenue.values())
    tv = sum(variable.values())
    return {
        "units": dict(units),
        "revenue_cents": dict(revenue),
        "variable_cost_cents": dict(variable),
        "total_units": tu,
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": f,
        "profit_cents": tr - tv - f,
    }


def flexible_budget(case: Mapping[str, Any], actual_units: int) -> dict[str, Any]:
    s, f, _, ps = _unpack(case)
    t = _whole(actual_units, "actual units argument")
    bu = sum(p["bu"] for p in ps)
    brev = sum(p["bu"] * p["bp"] for p in ps)
    bvar = sum(p["bu"] * p["q"] * s for p in ps)
    rev = _round_half_up(t * brev, bu)
    var = _round_half_up(t * bvar, bu)
    return {"units": t, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": f, "profit_cents": rev - var - f}


def variance_decomposition(case: Mapping[str, Any]) -> dict[str, int]:
    s, f, aq, ps = _unpack(case)
    mp = master_budget(case)["profit_cents"]
    total_out = sum(p["au"] for p in ps)
    fp = flexible_budget(case, total_out)["profit_cents"]
    sp = 0
    for p in ps:
        sp += (p["ap"] - p["bp"]) * p["au"]
    std = sum(p["q"] * p["au"] for p in ps)
    eff = s * (std - aq)
    margin_on_actual = 0
    for p in ps:
        margin_on_actual += p["au"] * (p["bp"] - p["q"] * s)
    mix = margin_on_actual - f - fp
    revenue_actual = sum(p["au"] * p["ap"] for p in ps)
    total = revenue_actual - s * aq - f - mp
    return {"sales_price": sp, "sales_volume": fp - mp, "sales_mix": mix, "efficiency": eff, "total": total}
