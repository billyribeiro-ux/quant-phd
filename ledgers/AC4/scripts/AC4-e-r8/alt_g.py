"""Alternative g: class-based engine; validation by a single pass over a schema table; mix as actual-mix contribution less flexed profit, computed through the flexed-revenue helper."""
from fractions import Fraction
from typing import Any

SCHEMA = {
    "budget_units": int, "budget_price_cents": int, "standard_inputs_per_unit": int,
    "actual_units": int, "actual_price_cents": int,
}


class _Engine:
    def __init__(self, case: Any) -> None:
        for field in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
            if field not in case:
                raise ValueError(f"no {field}")
        for field in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used"):
            v = case[field]
            if type(v) is not int or v < 0:
                raise ValueError(f"{field} must be a non-negative whole number")
        rows = case["products"]
        if not rows:
            raise ValueError("no products")
        names = [r.get("name") for r in rows]
        if any(not isinstance(n, str) or not n for n in names) or len(set(names)) != len(names):
            raise ValueError("bad names")
        for r in rows:
            for k, t in SCHEMA.items():
                if k not in r:
                    raise ValueError(f"missing {k}")
                if type(r[k]) is not t or r[k] < 0:
                    raise ValueError(f"{k} invalid")
        if sum(r["budget_units"] for r in rows) == 0:
            raise ValueError("no budgeted units")
        self.case = case
        self.rows = rows
        self.s = case["input_price_cents"]
        self.f = case["fixed_overhead_cents"]
        self.bt = sum(r["budget_units"] for r in rows)
        self.br = sum(r["budget_units"] * r["budget_price_cents"] for r in rows)
        self.bv = sum(r["budget_units"] * r["standard_inputs_per_unit"] * self.s for r in rows)

    def flex_parts(self, units: int) -> tuple[int, int]:
        # budgeted mix flexed to units; halves up, through exact fractions
        rev = Fraction(units * self.br, self.bt)
        var = Fraction(units * self.bv, self.bt)
        return (int(rev + Fraction(1, 2)), int(var + Fraction(1, 2)))


def master_budget(case: Any) -> dict[str, Any]:
    e = _Engine(case)
    units = {r["name"]: r["budget_units"] for r in e.rows}
    rev = {r["name"]: r["budget_units"] * r["budget_price_cents"] for r in e.rows}
    var = {r["name"]: r["budget_units"] * r["standard_inputs_per_unit"] * e.s for r in e.rows}
    return {
        "units": units, "revenue_cents": rev, "variable_cost_cents": var,
        "total_units": e.bt, "total_revenue_cents": e.br, "total_variable_cost_cents": e.bv,
        "fixed_cost_cents": e.f, "profit_cents": e.br - e.bv - e.f,
    }


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    e = _Engine(case)
    if type(actual_units) is not int or actual_units < 0:
        raise ValueError("actual units")
    rev, var = e.flex_parts(actual_units)
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": e.f, "profit_cents": rev - var - e.f}


def variance_decomposition(case: Any) -> dict[str, int]:
    e = _Engine(case)
    rows = e.rows
    at = sum(r["actual_units"] for r in rows)
    rev, var = e.flex_parts(at)
    flexed = rev - var - e.f
    master = e.br - e.bv - e.f
    price = sum((r["actual_price_cents"] - r["budget_price_cents"]) * r["actual_units"] for r in rows)
    actual_margin = sum(r["actual_units"] * r["budget_price_cents"] for r in rows) - sum(
        r["actual_units"] * r["standard_inputs_per_unit"] * e.s for r in rows)
    std = sum(r["standard_inputs_per_unit"] * r["actual_units"] for r in rows)
    aq = e.case["actual_inputs_used"]
    actual_profit = sum(r["actual_units"] * r["actual_price_cents"] for r in rows) - e.s * aq - e.f
    return {
        "sales_price": price,
        "sales_volume": flexed - master,
        "sales_mix": (actual_margin - e.f) - flexed,
        "efficiency": e.s * (std - aq),
        "total": actual_profit - master,
    }
