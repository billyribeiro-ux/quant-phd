"""Alternative i (round 8): class-based; per-product margins; flexed budget via shares as Fractions; validation via a helper class."""
from fractions import Fraction
from typing import Any


class _Case:
    def __init__(self, case: Any) -> None:
        if not isinstance(case, dict):
            raise ValueError("case must be a dict")
        for k in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
            if k not in case:
                raise ValueError(f"no {k}")
        self.s = self._int(case["input_price_cents"], "input_price_cents")
        self.f = self._int(case["fixed_overhead_cents"], "fixed_overhead_cents")
        self.aq = self._int(case["actual_inputs_used"], "actual_inputs_used")
        self.rows = [self._row(r) for r in case["products"]] if isinstance(case["products"], list) else self._bad()
        if not self.rows:
            raise ValueError("empty product list")
        names = [r["name"] for r in self.rows]
        if len(set(names)) != len(names):
            raise ValueError("duplicate product name")
        if sum(r["bu"] for r in self.rows) == 0:
            raise ValueError("no budgeted units")

    @staticmethod
    def _bad() -> list[dict[str, Any]]:
        raise ValueError("products must be a list")

    @staticmethod
    def _int(v: Any, label: str) -> int:
        if type(v) is not int:
            raise ValueError(f"{label} must be a whole number (not bool or float)")
        if v < 0:
            raise ValueError(f"{label} is negative")
        return v

    def _row(self, r: Any) -> dict[str, Any]:
        keys = {"name": "name", "bu": "budget_units", "bp": "budget_price_cents", "q": "standard_inputs_per_unit",
                "au": "actual_units", "ap": "actual_price_cents"}
        for short, long in keys.items():
            if not isinstance(r, dict) or long not in r:
                raise ValueError(f"product lacks {long}")
        name = r["name"]
        if not isinstance(name, str) or not name:
            raise ValueError("empty name")
        out: dict[str, Any] = {"name": name}
        for short, long in keys.items():
            if short != "name":
                out[short] = self._int(r[long], f"{name}.{long}")
        return out


def _half_up(x: Fraction) -> int:
    n, d = x.numerator, x.denominator
    return (2 * n + d) // (2 * d)


def master_budget(case: Any) -> dict[str, Any]:
    c = _Case(case)
    revenue = {r["name"]: r["bu"] * r["bp"] for r in c.rows}
    variable = {r["name"]: r["bu"] * r["q"] * c.s for r in c.rows}
    units = {r["name"]: r["bu"] for r in c.rows}
    tr = sum(revenue.values())
    tv = sum(variable.values())
    return {"units": units, "total_units": sum(units.values()), "revenue_cents": revenue,
            "variable_cost_cents": variable, "total_revenue_cents": tr, "total_variable_cost_cents": tv,
            "fixed_cost_cents": c.f, "profit_cents": tr - tv - c.f}


def flexible_budget(case: Any, actual_units: Any) -> dict[str, Any]:
    c = _Case(case)
    if type(actual_units) is not int or actual_units < 0:
        raise ValueError("actual_units must be a non-negative whole number")
    bu = sum(r["bu"] for r in c.rows)
    share = [Fraction(r["bu"], bu) for r in c.rows]
    rev_per = sum((sh * r["bp"] for sh, r in zip(share, c.rows)), Fraction(0))
    var_per = sum((sh * r["q"] * c.s for sh, r in zip(share, c.rows)), Fraction(0))
    rev = _half_up(actual_units * rev_per)
    var = _half_up(actual_units * var_per)
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": c.f, "profit_cents": rev - var - c.f}


def variance_decomposition(case: Any) -> dict[str, int]:
    c = _Case(case)
    master = master_budget(case)["profit_cents"]
    flex = flexible_budget(case, sum(r["au"] for r in c.rows))["profit_cents"]
    price = sum((r["ap"] - r["bp"]) * r["au"] for r in c.rows)
    eff = c.s * sum(r["q"] * r["au"] for r in c.rows) - c.s * c.aq
    margin_actual = sum(r["au"] * (r["bp"] - r["q"] * c.s) for r in c.rows) - c.f
    total = sum(r["au"] * r["ap"] for r in c.rows) - c.s * c.aq - c.f - master
    return {"sales_price": price, "sales_volume": flex - master, "sales_mix": margin_actual - flex,
            "efficiency": eff, "total": total}
