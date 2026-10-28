from __future__ import annotations
from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from typing import Any
import numbers

FIELDS = ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit", "actual_units", "actual_price_cents")

def _int(v: Any, what: str) -> int:
    if isinstance(v, bool) or not isinstance(v, numbers.Integral):
        raise ValueError(f"{what} must be a whole number, not {v!r}")
    return int(v)

def _pos(v: Any, what: str) -> int:
    n = _int(v, what)
    if n < 0:
        raise ValueError(f"{what} must not be negative")
    return n

def _case(case: Any):
    if not isinstance(case, Mapping):
        raise ValueError("the case must be a mapping")
    c = dict(case)
    for k in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if k not in c:
            raise ValueError(f"no {k}")
    raw = c["products"]
    if not isinstance(raw, list) or not raw:
        raise ValueError("products must be a non-empty list of mappings")
    prods = []
    names: set[str] = set()
    for item in raw:
        if not isinstance(item, Mapping):
            raise ValueError("a product must be a mapping")
        d = dict(item)
        for f in FIELDS:
            if f not in d:
                raise ValueError(f"a product has no {f}")
        nm = d["name"]
        if not isinstance(nm, str) or nm == "" or nm in names:
            raise ValueError("a product name must be non-empty text, unique")
        names.add(nm)
        prods.append({
            "name": nm,
            "bu": _pos(d["budget_units"], "budget_units"),
            "bp": _pos(d["budget_price_cents"], "budget_price_cents"),
            "q": _pos(d["standard_inputs_per_unit"], "standard_inputs_per_unit"),
            "au": _pos(d["actual_units"], "actual_units"),
            "ap": _pos(d["actual_price_cents"], "actual_price_cents"),
        })
    if sum(p["bu"] for p in prods) == 0:
        raise ValueError("no budgeted units")
    return _pos(c["input_price_cents"], "input_price_cents"), _pos(c["fixed_overhead_cents"], "fixed_overhead_cents"), _pos(c["actual_inputs_used"], "actual_inputs_used"), prods

def _half_up(x: Fraction) -> int:
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(d)

def master_budget(case):
    s, F, _, prods = _case(case)
    units = {p["name"]: p["bu"] for p in prods}
    rev = {p["name"]: p["bu"] * p["bp"] for p in prods}
    var = {p["name"]: p["bu"] * p["q"] * s for p in prods}
    tr = sum(rev.values())
    tv = sum(var.values())
    return {"units": units, "total_units": sum(units.values()), "revenue_cents": rev, "variable_cost_cents": var,
            "total_revenue_cents": tr, "total_variable_cost_cents": tv, "fixed_cost_cents": F, "profit_cents": tr - tv - F}

def flexible_budget(case, actual_units):
    s, F, _, prods = _case(case)
    t = _pos(actual_units, "actual_units")
    bu = sum(p["bu"] for p in prods)
    brev = sum(p["bu"] * p["bp"] for p in prods)
    bvar = sum(p["bu"] * p["q"] * s for p in prods)
    r = _half_up(Fraction(t * brev, bu))
    v = _half_up(Fraction(t * bvar, bu))
    return {"units": t, "revenue_cents": r, "variable_cost_cents": v, "fixed_cost_cents": F, "profit_cents": r - v - F}

def variance_decomposition(case):
    s, F, AQ, prods = _case(case)
    mp = master_budget(case)["profit_cents"]
    AT = sum(p["au"] for p in prods)
    fl = flexible_budget(case, AT)["profit_cents"]
    price = sum((p["ap"] - p["bp"]) * p["au"] for p in prods)
    eff = s * (sum(p["q"] * p["au"] for p in prods) - AQ)
    mix = (sum(p["au"] * (p["bp"] - p["q"] * s) for p in prods) - F) - fl
    vol = fl - mp
    total = price + vol + mix + eff
    return {"sales_price": price, "sales_volume": vol, "sales_mix": mix, "efficiency": eff, "total": total}
