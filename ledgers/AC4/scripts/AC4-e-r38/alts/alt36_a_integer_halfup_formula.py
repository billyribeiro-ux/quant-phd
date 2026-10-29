"""Round-36 correct alternative: whole-cent halves-up via (2n + d) // (2d) on integers; numbers.Integral validation; products per-row dict copies."""
import numbers
from fractions import Fraction


def _int(value, name):
    if isinstance(value, bool) or not isinstance(value, numbers.Integral):
        raise ValueError(f"{name} must be a whole number, got {type(value).__name__}")
    return int(value)


def _nonneg(value, name):
    v = _int(value, name)
    if v < 0:
        raise ValueError(f"{name} must not be negative")
    return v


def _half_up(num, den):
    return (2 * num + den) // (2 * den)


def _get(mapping, key):
    try:
        return mapping[key]
    except KeyError:
        raise ValueError(f"missing required field {key}") from None


def _case(case):
    if not hasattr(case, "keys") or not hasattr(case, "__getitem__"):
        raise ValueError("case must be a mapping")
    s = _nonneg(_get(case, "input_price_cents"), "input_price_cents")
    f = _nonneg(_get(case, "fixed_overhead_cents"), "fixed_overhead_cents")
    aq = _nonneg(_get(case, "actual_inputs_used"), "actual_inputs_used")
    raw = _get(case, "products")
    if not isinstance(raw, list) or not raw:
        raise ValueError("products must be a non-empty list of mappings")
    rows, seen = [], set()
    for r in raw:
        if not hasattr(r, "keys"):
            raise ValueError("each product must be a mapping")
        name = _get(r, "name")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("product names must be non-empty, text and unique")
        seen.add(name)
        rows.append({
            "name": name,
            "bu": _nonneg(_get(r, "budget_units"), "budget_units"),
            "bp": _nonneg(_get(r, "budget_price_cents"), "budget_price_cents"),
            "q": _nonneg(_get(r, "standard_inputs_per_unit"), "standard_inputs_per_unit"),
            "au": _nonneg(_get(r, "actual_units"), "actual_units"),
            "ap": _nonneg(_get(r, "actual_price_cents"), "actual_price_cents"),
        })
    if sum(r["bu"] for r in rows) == 0:
        raise ValueError("the budget has no budgeted units")
    return s, f, aq, rows


def master_budget(case):
    s, f, _, rows = _case(case)
    units = {r["name"]: r["bu"] for r in rows}
    revenue = {r["name"]: r["bu"] * r["bp"] for r in rows}
    variable = {r["name"]: r["bu"] * r["q"] * s for r in rows}
    tr, tv = sum(revenue.values()), sum(variable.values())
    return {
        "units": units,
        "revenue_cents": revenue,
        "variable_cost_cents": variable,
        "total_units": sum(units.values()),
        "total_revenue_cents": tr,
        "total_variable_cost_cents": tv,
        "fixed_cost_cents": f,
        "profit_cents": tr - tv - f,
    }


def flexible_budget(case, actual_units):
    s, f, _, rows = _case(case)
    at = _nonneg(actual_units, "actual_units")
    bu = sum(r["bu"] for r in rows)
    brev = sum(r["bu"] * r["bp"] for r in rows)
    bvar = sum(r["bu"] * r["q"] * s for r in rows)
    rev = _half_up(at * brev, bu)
    var = _half_up(at * bvar, bu)
    return {"units": at, "revenue_cents": rev, "variable_cost_cents": var, "fixed_cost_cents": f,
            "profit_cents": rev - var - f}


def variance_decomposition(case):
    s, f, aq, rows = _case(case)
    master = master_budget(case)["profit_cents"]
    flexed = flexible_budget(case, sum(r["au"] for r in rows))["profit_cents"]
    price = sum((r["ap"] - r["bp"]) * r["au"] for r in rows)
    eff = s * (sum(r["q"] * r["au"] for r in rows) - aq)
    contrib = sum(r["au"] * (r["bp"] - r["q"] * s) for r in rows) - f
    mix = contrib - flexed
    volume = flexed - master
    actual = sum(r["au"] * r["ap"] for r in rows) - s * aq - f
    return {"sales_price": price, "sales_volume": volume, "sales_mix": mix, "efficiency": eff,
            "total": actual - master}
