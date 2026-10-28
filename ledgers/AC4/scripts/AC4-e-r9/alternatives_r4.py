"""Three independent correct implementations of budget_engine.py (over-constraint probes).

Written from the page's specification only, not from grader/reference.py. Each is a valid engine that
differs in validation style, rounding method and code structure. Writes alt_a.py, alt_b.py, alt_c.py to argv[1].
"""
import pathlib, sys

OUT = pathlib.Path(sys.argv[1])

ALT_A = '''
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
'''

ALT_B = '''
"""Alt B: exact integer half-up via divmod, validation with isinstance and a bool guard, flat loops."""
from fractions import Fraction

def _int(v, name):
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(f"{name}: expected a whole number")
    if v < 0:
        raise ValueError(f"{name}: negative")
    return v

def _unpack(case):
    if not isinstance(case, dict):
        raise ValueError("case must be a mapping")
    need = ("input_price_cents", "fixed_overhead_cents", "actual_inputs_used", "products")
    if any(k not in case for k in need):
        raise ValueError("case is missing a field")
    s = _int(case["input_price_cents"], "input price")
    f = _int(case["fixed_overhead_cents"], "fixed overhead")
    aq = _int(case["actual_inputs_used"], "actual inputs")
    plist = case["products"]
    if not isinstance(plist, list) or len(plist) == 0:
        raise ValueError("no products")
    seen = set()
    out = []
    for p in plist:
        if not isinstance(p, dict) or any(k not in p for k in ("name", "budget_units", "budget_price_cents",
                "standard_inputs_per_unit", "actual_units", "actual_price_cents")):
            raise ValueError("product fields")
        n = p["name"]
        if not isinstance(n, str) or not n.strip() or n in seen:
            raise ValueError("product name")
        seen.add(n)
        out.append((n, _int(p["budget_units"], "bu"), _int(p["budget_price_cents"], "bp"),
                    _int(p["standard_inputs_per_unit"], "q"), _int(p["actual_units"], "au"),
                    _int(p["actual_price_cents"], "ap")))
    if sum(t[1] for t in out) == 0:
        raise ValueError("zero budgeted units")
    return s, f, aq, out

def _round_half_up(fr):
    num, den = fr.numerator, fr.denominator
    q, r = divmod(2 * num + den, 2 * den)
    return q

def master_budget(case):
    s, f, _, rows = _unpack(case)
    units = {n: bu for n, bu, _, _, _, _ in rows}
    rev = {n: bu * bp for n, bu, bp, _, _, _ in rows}
    var = {n: bu * q * s for n, bu, _, q, _, _ in rows}
    tu = sum(units.values())
    trev = sum(rev.values())
    tvar = sum(var.values())
    return {"units": units, "revenue_cents": rev, "variable_cost_cents": var, "total_units": tu,
            "total_revenue_cents": trev, "total_variable_cost_cents": tvar, "fixed_cost_cents": f,
            "profit_cents": trev - tvar - f}

def flexible_budget(case, actual_units):
    s, f, _, rows = _unpack(case)
    t = _int(actual_units, "actual units")
    bu = sum(r[1] for r in rows)
    brev = sum(r[1] * r[2] for r in rows)
    bvar = sum(r[1] * r[3] * s for r in rows)
    rv = _round_half_up(Fraction(t * brev, bu))
    vc = _round_half_up(Fraction(t * bvar, bu))
    return {"units": t, "revenue_cents": rv, "variable_cost_cents": vc, "fixed_cost_cents": f,
            "profit_cents": rv - vc - f}

def variance_decomposition(case):
    s, f, aq, rows = _unpack(case)
    m = master_budget(case)["profit_cents"]
    total_au = sum(r[4] for r in rows)
    fl = flexible_budget(case, total_au)["profit_cents"]
    price = sum((r[5] - r[2]) * r[4] for r in rows)
    std_in = sum(r[3] * r[4] for r in rows)
    eff = s * (std_in - aq)
    mix = sum(r[4] * (r[2] - r[3] * s) for r in rows) - f - fl
    profit = sum(r[4] * r[5] for r in rows) - s * aq - f
    return {"sales_price": price, "sales_volume": fl - m, "sales_mix": mix, "efficiency": eff,
            "total": profit - m}
'''

ALT_C = '''
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
'''

for name, text in (("alt_a.py", ALT_A), ("alt_b.py", ALT_B), ("alt_c.py", ALT_C)):
    (OUT / name).write_text(text.lstrip("\n"))
    print("wrote", name)
