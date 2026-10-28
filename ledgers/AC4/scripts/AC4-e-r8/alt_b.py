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
