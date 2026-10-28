"""Write five alternative correct budget_engine.py implementations (scratch) that differ from the reference in
algorithm and in numerical method. Each must pass the whole suite on every seed; the runner checks that."""
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# A: Decimal rounding with ROUND_HALF_UP, dict()/list() copies of the inputs, total as the sum of the four variances.
A = '''from __future__ import annotations
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
'''

# B: whole-cent flexed via Fraction and math.floor(x + 1/2); validation with a helper returning a new tuple;
# name check strips whitespace for the emptiness test only (names are kept as given).
B = A.replace(
    "def _half_up(x: Fraction) -> int:\n    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(\"1\"), rounding=ROUND_HALF_UP)\n    return int(d)",
    "def _half_up(x: Fraction) -> int:\n    import math\n    return math.floor(x + Fraction(1, 2))",
).replace('if not isinstance(nm, str) or nm == "" or nm in names:', 'if not isinstance(nm, str) or nm.strip() == "" or nm in names:')
assert B != A

# C: cutoffs written as a different but equivalent algorithm: the mix from the 'margin per unit' form with the
# total as actual minus budget, computed directly (not as the sum of the four).
C = A.replace(
    "    total = price + vol + mix + eff\n",
    "    actual = sum(p['au'] * p['ap'] for p in prods) - s * AQ - F\n    total = actual - mp\n",
).replace("def _pos(v: Any, what: str) -> int:\n    n = _int(v, what)", "def _pos(v: Any, what: str) -> int:\n    n = _int(v, what)")
assert C != A

# D: mapping-of-products accepted only as a list: products are read with a loop and a running total, no sum().
D = A.replace(
    "    tr = sum(rev.values())\n    tv = sum(var.values())\n",
    "    tr = 0\n    tv = 0\n    for p in prods:\n        tr += rev[p['name']]\n        tv += var[p['name']]\n",
)
assert D != A

# E: flexed budget rounding by the exact-fraction method with a rounding offset written as a comparison, not a floor.
E = A.replace(
    "def _half_up(x: Fraction) -> int:\n    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(\"1\"), rounding=ROUND_HALF_UP)\n    return int(d)",
    "def _half_up(x: Fraction) -> int:\n    n = int(x)\n    return n + 1 if x - n >= Fraction(1, 2) else n",
)
assert E != A

for name, src in {"alt_r12_a_decimal_half_up": A, "alt_r12_b_fraction_floor_strip": B,
                  "alt_r12_c_total_from_actual": C, "alt_r12_d_loop_totals": D,
                  "alt_r12_e_compare_rounding": E}.items():
    (OUT / f"{name}.py").write_text(src, encoding="utf-8")
    print("wrote", name)
