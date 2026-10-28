"""Alternative j (round 8): validation in a different order (products first), total rounding via divmod, namedtuple-free dict returns."""
from typing import Any

_ROW = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")


def _check(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not isinstance(case, dict):
        raise ValueError("the case is not a mapping")
    rows = case.get("products") if "products" in case else None
    if rows is None:
        raise ValueError("the case has no products field")
    if not isinstance(rows, list) or not rows:
        raise ValueError("products must be a non-empty list")
    seen = []
    clean = []
    for r in rows:
        if not isinstance(r, dict):
            raise ValueError("a product is not a mapping")
        for k in _ROW:
            if k not in r:
                raise ValueError(f"no {k}")
        if not isinstance(r["name"], str) or r["name"] == "" or r["name"] in seen:
            raise ValueError("bad or duplicate name")
        seen.append(r["name"])
        vals = {}
        for k in _ROW[1:]:
            v = r[k]
            if isinstance(v, bool) or not isinstance(v, int):
                raise ValueError(f"{k} must be a whole number")
            if v < 0:
                raise ValueError(f"{k} must not be negative")
            vals[k] = v
        vals["name"] = r["name"]
        clean.append(vals)
    if sum(v["budget_units"] for v in clean) == 0:
        raise ValueError("no budgeted units")
    out = []
    for k in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"):
        if k not in case:
            raise ValueError(f"no {k}")
        v = case[k]
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ValueError(f"{k} must be a non-negative whole number")
        out.append(v)
    return out[0], out[1], out[2], clean


def _round(num: int, den: int) -> int:
    q, r = divmod(2 * num + den, 2 * den)
    return q


def master_budget(case: Any) -> dict[str, Any]:
    price, fixed, _, rows = _check(case)
    units = {r["name"]: r["budget_units"] for r in rows}
    rev = {r["name"]: r["budget_units"] * r["budget_price_cents"] for r in rows}
    var = {r["name"]: r["budget_units"] * r["standard_inputs_per_unit"] * price for r in rows}
    total_rev = sum(rev.values())
    total_var = sum(var.values())
    return {"units": units, "total_units": sum(units.values()), "revenue_cents": rev, "variable_cost_cents": var,
            "total_revenue_cents": total_rev, "total_variable_cost_cents": total_var,
            "fixed_cost_cents": fixed, "profit_cents": total_rev - total_var - fixed}


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    price, fixed, _, rows = _check(case)
    if isinstance(actual_units, bool) or not isinstance(actual_units, int) or actual_units < 0:
        raise ValueError("actual_units must be a non-negative whole number")
    bu = sum(r["budget_units"] for r in rows)
    brev = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
    bvar = sum(r["budget_units"] * r["standard_inputs_per_unit"] * price for r in rows)
    rev = _round(actual_units * brev, bu)
    var = _round(actual_units * bvar, bu)
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": fixed, "profit_cents": rev - var - fixed}


def variance_decomposition(case: Any) -> dict[str, int]:
    price, fixed, ai, rows = _check(case)
    master = master_budget(case)["profit_cents"]
    flex = flexible_budget(case, sum(r["actual_units"] for r in rows))["profit_cents"]
    sales_price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    eff = price * sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows) - price * ai
    cm = sum(r["actual_units"] * r["budget_price_cents"] - r["actual_units"] * r["standard_inputs_per_unit"] * price for r in rows) - fixed
    actual = sum(r["actual_units"] * r["actual_price_cents"] for r in rows) - price * ai - fixed
    return {"sales_price": sales_price, "sales_volume": flex - master, "sales_mix": cm - flex,
            "efficiency": eff, "total": actual - master}
