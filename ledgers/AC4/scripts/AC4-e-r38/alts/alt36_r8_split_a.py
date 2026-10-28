"""Alt A: Decimal rounding, dict-based products, type-exact integer checks."""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

def _whole(value, name):
    if type(value) is not int:
        raise ValueError(name + " must be a whole number")
    return value

def _count(value, name):
    value = _whole(value, name)
    if value < 0:
        raise ValueError(name + " must not be negative")
    return value

def _read(case):
    if not isinstance(case, dict):
        raise ValueError("case must be a dict")
    for key in ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products"):
        if key not in case:
            raise ValueError("missing " + key)
    price = _count(case["input_price_cents"], "input_price_cents")
    fixed = _count(case["fixed_overhead_cents"], "fixed_overhead_cents")
    used = _count(case["actual_inputs_used"], "actual_inputs_used")
    products = case["products"]
    if not isinstance(products, list) or not products:
        raise ValueError("products must be a non-empty list")
    names = []
    rows = []
    for item in products:
        if not isinstance(item, dict):
            raise ValueError("product must be a dict")
        for key in ("name", "budget_units", "budget_price_cents", "standard_inputs_per_unit",
                    "actual_units", "actual_price_cents"):
            if key not in item:
                raise ValueError("product missing " + key)
        if not isinstance(item["name"], str) or item["name"] == "":
            raise ValueError("name must be non-empty")
        if item["name"] in names:
            raise ValueError("duplicate name")
        names.append(item["name"])
        rows.append({
            "name": item["name"],
            "bu": _count(item["budget_units"], "budget_units"),
            "bp": _count(item["budget_price_cents"], "budget_price_cents"),
            "q": _count(item["standard_inputs_per_unit"], "standard_inputs_per_unit"),
            "au": _count(item["actual_units"], "actual_units"),
            "ap": _count(item["actual_price_cents"], "actual_price_cents"),
        })
    if sum(r["bu"] for r in rows) == 0:
        raise ValueError("no budgeted units")
    return price, fixed, used, rows

def _half_up(fraction):
    d = Decimal(fraction.numerator) / Decimal(fraction.denominator)
    return int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))

def master_budget(case):
    price, fixed, _, rows = _read(case)
    units = {r["name"]: r["bu"] for r in rows}
    revenue = {r["name"]: r["bu"] * r["bp"] for r in rows}
    variable = {r["name"]: r["bu"] * r["q"] * price for r in rows}
    tr = sum(revenue.values())
    tv = sum(variable.values())
    return {
        "units": dict(units), "revenue_cents": dict(revenue), "variable_cost_cents": dict(variable),
        "total_units": sum(units.values()), "total_revenue_cents": tr, "total_variable_cost_cents": tv,
        "fixed_cost_cents": fixed, "profit_cents": tr - tv - fixed,
    }

def flexible_budget(case, actual_units):
    price, fixed, _, rows = _read(case)
    total = _count(actual_units, "actual_units")
    bu = sum(r["bu"] for r in rows)
    br = sum(r["bu"] * r["bp"] for r in rows)
    bv = sum(r["bu"] * r["q"] * price for r in rows)
    rev = _half_up(Fraction(total * br, bu))
    var = _half_up(Fraction(total * bv, bu))
    return {"units": total, "revenue_cents": rev, "variable_cost_cents": var,
            "fixed_cost_cents": fixed, "profit_cents": rev - var - fixed}

def variance_decomposition(case):
    price, fixed, used, rows = _read(case)
    master = master_budget(case)["profit_cents"]
    at = sum(r["au"] for r in rows)
    flexed = flexible_budget(case, at)["profit_cents"]
    price_var = sum((r["ap"] - r["bp"]) * r["au"] for r in rows)
    eff = price * (sum(r["q"] * r["au"] for r in rows) - used)
    mix_contrib = sum(r["au"] * (r["bp"] - r["q"] * price) for r in rows) - fixed
    actual_profit = sum(r["au"] * r["ap"] for r in rows) - price * used - fixed
    volume = flexed - master
    mix = mix_contrib - flexed
    return {"sales_price": price_var, "sales_volume": volume, "sales_mix": mix,
            "efficiency": eff, "total": actual_profit - master}
