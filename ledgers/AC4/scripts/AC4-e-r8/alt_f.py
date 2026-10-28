"""Alternative f: integer-only half-up rounding, per-product loops, KeyError translated to ValueError."""
from typing import Any

PRODUCT_KEYS = ["name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents"]


def _get(mapping: Any, key: str) -> Any:
    try:
        return mapping[key]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"missing {key}") from exc


def _int(value: Any) -> int:
    if type(value) is not int:
        raise ValueError("expected a whole number")
    if value < 0:
        raise ValueError("expected a non-negative whole number")
    return value


def _check(case: Any) -> list[Any]:
    if not isinstance(case, dict):
        raise ValueError("case must be a dict")
    _int(_get(case, "input_price_cents"))
    _int(_get(case, "fixed_overhead_cents"))
    _int(_get(case, "actual_inputs_used"))
    products = _get(case, "products")
    if not isinstance(products, (list, tuple)) or len(products) == 0:
        raise ValueError("no products")
    seen = []
    for p in products:
        for k in PRODUCT_KEYS:
            _get(p, k)
        if not isinstance(p["name"], str) or p["name"] == "" or p["name"] in seen:
            raise ValueError("bad name")
        seen.append(p["name"])
        for k in PRODUCT_KEYS[1:]:
            _int(p[k])
    if sum(p["budget_units"] for p in products) == 0:
        raise ValueError("zero budgeted units")
    return list(products)


def _round(numer: int, denom: int) -> int:
    # nearest integer to numer/denom, halves up, numer >= 0, denom > 0
    return (2 * numer + denom) // (2 * denom)


def master_budget(case: Any) -> dict[str, Any]:
    prods = _check(case)
    s = case["input_price_cents"]
    out: dict[str, Any] = {"units": {}, "revenue_cents": {}, "variable_cost_cents": {}}
    for p in prods:
        out["units"][p["name"]] = p["budget_units"]
        out["revenue_cents"][p["name"]] = p["budget_units"] * p["budget_price_cents"]
        out["variable_cost_cents"][p["name"]] = p["budget_units"] * p["standard_inputs_per_unit"] * s
    out["total_units"] = sum(out["units"].values())
    out["total_revenue_cents"] = sum(out["revenue_cents"].values())
    out["total_variable_cost_cents"] = sum(out["variable_cost_cents"].values())
    out["fixed_cost_cents"] = case["fixed_overhead_cents"]
    out["profit_cents"] = out["total_revenue_cents"] - out["total_variable_cost_cents"] - out["fixed_cost_cents"]
    return out


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    prods = _check(case)
    if type(actual_units) is not int or actual_units < 0:
        raise ValueError("actual units must be a non-negative int")
    s = case["input_price_cents"]
    bt = sum(p["budget_units"] for p in prods)
    br = sum(p["budget_units"] * p["budget_price_cents"] for p in prods)
    bv = sum(p["budget_units"] * p["standard_inputs_per_unit"] * s for p in prods)
    rev = _round(actual_units * br, bt)
    var = _round(actual_units * bv, bt)
    fixed = case["fixed_overhead_cents"]
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": fixed, "profit_cents": rev - var - fixed}


def variance_decomposition(case: Any) -> dict[str, int]:
    prods = _check(case)
    s = case["input_price_cents"]
    fixed = case["fixed_overhead_cents"]
    bt = sum(p["budget_units"] for p in prods)
    br = sum(p["budget_units"] * p["budget_price_cents"] for p in prods)
    bv = sum(p["budget_units"] * p["standard_inputs_per_unit"] * s for p in prods)
    budget_profit = br - bv - fixed
    at = sum(p["actual_units"] for p in prods)
    flexed = _round(at * br, bt) - _round(at * bv, bt) - fixed
    sales_price = 0
    mix_margin = 0
    std_inputs = 0
    actual_revenue = 0
    for p in prods:
        sales_price += (p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"]
        mix_margin += p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * s)
        std_inputs += p["standard_inputs_per_unit"] * p["actual_units"]
        actual_revenue += p["actual_price_cents"] * p["actual_units"]
    aq = case["actual_inputs_used"]
    actual_profit = actual_revenue - s * aq - fixed
    return {
        "sales_price": sales_price,
        "sales_volume": flexed - budget_profit,
        "sales_mix": (mix_margin - fixed) - flexed,
        "efficiency": s * (std_inputs - aq),
        "total": actual_profit - budget_profit,
    }
