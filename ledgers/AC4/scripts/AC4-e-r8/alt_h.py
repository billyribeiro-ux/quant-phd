"""Alternative h (round 8): operator.index for whole numbers, Decimal half-up rounding, validation after the arithmetic plan."""
import operator
from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Any


def _w(value: Any, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label}: boolean")
    try:
        n = operator.index(value)
    except TypeError:
        raise ValueError(f"{label}: not a whole number") from None
    if n < 0:
        raise ValueError(f"{label}: negative")
    return int(n)


def _rows(case: Any) -> tuple[int, int, int, list[dict[str, Any]]]:
    if not hasattr(case, "keys"):
        raise ValueError("case must be a mapping")
    for f in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if f not in case:
            raise ValueError(f"missing {f}")
    prods = case["products"]
    if not isinstance(prods, (list, tuple)) or len(prods) == 0:
        raise ValueError("no products")
    names: set[str] = set()
    out = []
    for p in prods:
        for f in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"):
            if f not in p:
                raise ValueError(f"product missing {f}")
        nm = p["name"]
        if not isinstance(nm, str) or nm == "":
            raise ValueError("bad name")
        if nm in names:
            raise ValueError("duplicate name")
        names.add(nm)
        out.append({k: (v if k == "name" else _w(v, k)) for k, v in p.items() if k in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")})
    fixed = _w(case["fixed_overhead_cents"], "fixed")
    price = _w(case["input_price_cents"], "input price")
    ai = _w(case["actual_inputs_used"], "actual inputs")
    if sum(p["budget_units"] for p in out) == 0:
        raise ValueError("no budgeted units")
    return price, fixed, ai, out


def _half(total: Decimal) -> int:
    return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def master_budget(case: Any) -> dict[str, Any]:
    price, fixed, _, ps = _rows(case)
    units = {p["name"]: p["budget_units"] for p in ps}
    rev = {p["name"]: p["budget_units"] * p["budget_price_cents"] for p in ps}
    var = {p["name"]: p["budget_units"] * p["standard_inputs_per_unit"] * price for p in ps}
    tr, tv = sum(rev.values()), sum(var.values())
    return {"units": units, "total_units": sum(units.values()), "revenue_cents": rev, "variable_cost_cents": var,
            "total_revenue_cents": tr, "total_variable_cost_cents": tv, "fixed_cost_cents": fixed,
            "profit_cents": tr - tv - fixed}


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    price, fixed, _, ps = _rows(case)
    n = _w(actual_units, "actual units")
    bu = sum(p["budget_units"] for p in ps)
    with localcontext() as ctx:
        ctx.prec = 60
        br = Decimal(sum(p["budget_units"] * p["budget_price_cents"] for p in ps))
        bv = Decimal(sum(p["budget_units"] * p["standard_inputs_per_unit"] * price for p in ps))
        rev = _half(Decimal(n) * br / Decimal(bu))
        var = _half(Decimal(n) * bv / Decimal(bu))
    return {"units": n, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": fixed,
            "profit_cents": rev - var - fixed}


def variance_decomposition(case: Any) -> dict[str, int]:
    price, fixed, ai, ps = _rows(case)
    master = master_budget(case)["profit_cents"]
    flex = flexible_budget(case, sum(p["actual_units"] for p in ps))["profit_cents"]
    sp = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in ps)
    eff = price * (sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in ps) - ai)
    mix_cm = sum(p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * price) for p in ps) - fixed
    total_actual = sum(p["actual_units"] * p["actual_price_cents"] for p in ps) - price * ai - fixed
    return {"sales_price": sp, "sales_volume": flex - master, "sales_mix": mix_cm - flex, "efficiency": eff,
            "total": total_actual - master}
