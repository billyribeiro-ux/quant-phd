"""Alt C: class-based engine; validation by a single helper; rounding by floor(x + 1/2) on Fractions."""
import math
from fractions import Fraction

class _Case:
    def __init__(self, case):
        if not hasattr(case, "get"):
            raise ValueError("case must be a mapping")
        self.s = self._w(case, "input_price_cents")
        self.f = self._w(case, "fixed_overhead_cents")
        self.aq = self._w(case, "actual_inputs_used")
        products = case.get("products")
        if not isinstance(products, (list, tuple)) or not products:
            raise ValueError("products")
        self.rows = []
        names = set()
        for p in products:
            if not hasattr(p, "get"):
                raise ValueError("product")
            vals = {}
            for k in ("budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units",
                      "actual_price_cents"):
                vals[k] = self._w(p, k)
            name = p.get("name")
            if not isinstance(name, str) or name == "" or name in names:
                raise ValueError("name")
            names.add(name)
            self.rows.append((name, vals))
        if sum(v["budget_units"] for _, v in self.rows) == 0:
            raise ValueError("no budgeted units")

    @staticmethod
    def _w(mapping, key):
        if key not in mapping:
            raise ValueError("missing " + key)
        v = mapping[key]
        if type(v) is bool or type(v) is not int:
            raise ValueError(key + " must be int")
        if v < 0:
            raise ValueError(key + " must be >= 0")
        return v

def _rhu(x):
    return math.floor(x + Fraction(1, 2))

def master_budget(case):
    c = _Case(case)
    units = {n: v["budget_units"] for n, v in c.rows}
    revenue = {n: v["budget_units"] * v["budget_price_cents"] for n, v in c.rows}
    variable = {n: v["budget_units"] * v["standard_inputs_per_unit"] * c.s for n, v in c.rows}
    tr, tv = sum(revenue.values()), sum(variable.values())
    return {"units": units, "revenue_cents": revenue, "variable_cost_cents": variable,
            "total_units": sum(units.values()), "total_revenue_cents": tr, "total_variable_cost_cents": tv,
            "fixed_cost_cents": c.f, "profit_cents": tr - tv - c.f}

def flexible_budget(case, actual_units):
    c = _Case(case)
    if type(actual_units) is not int or actual_units < 0:
        raise ValueError("actual units must be a non-negative int")
    bu = sum(v["budget_units"] for _, v in c.rows)
    br = sum(v["budget_units"] * v["budget_price_cents"] for _, v in c.rows)
    bv = sum(v["budget_units"] * v["standard_inputs_per_unit"] * c.s for _, v in c.rows)
    rev = _rhu(Fraction(actual_units * br, bu))
    var = _rhu(Fraction(actual_units * bv, bu))
    return {"units": actual_units, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": c.f, "profit_cents": rev - var - c.f}

def variance_decomposition(case):
    c = _Case(case)
    master = master_budget(case)["profit_cents"]
    at = sum(v["actual_units"] for _, v in c.rows)
    flexed = flexible_budget(case, at)["profit_cents"]
    price = sum((v["actual_price_cents"] - v["budget_price_cents"]) * v["actual_units"] for _, v in c.rows)
    eff = c.s * (sum(v["standard_inputs_per_unit"] * v["actual_units"] for _, v in c.rows) - c.aq)
    contrib = sum(v["actual_units"] * (v["budget_price_cents"] - v["standard_inputs_per_unit"] * c.s)
                  for _, v in c.rows) - c.f
    total = (sum(v["actual_units"] * v["actual_price_cents"] for _, v in c.rows) - c.s * c.aq - c.f) - master
    return {"sales_price": price, "sales_volume": flexed - master, "sales_mix": contrib - flexed,
            "efficiency": eff, "total": total}
