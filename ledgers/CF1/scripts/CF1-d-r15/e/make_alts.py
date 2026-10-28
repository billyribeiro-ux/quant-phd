"""Derive three alternative correct engines from the reference (round 15 verifier, slice d)."""
import pathlib
REF = pathlib.Path("/tmp/verify15-CF1-d/course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/CF1-v/d15/alts")

def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old[:60]
    return src.replace(old, new)

# A: IRR grid by cumulative multiplication (valid: the grid decides only for close roots); endpoints kept exact.
a = swap(REF,
"""    xs = [
        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))
        for k in range(_GRID_POINTS)
    ]
    xs[0], xs[-1] = _X_LOW, _X_HIGH""",
"""    step = (_X_HIGH / _X_LOW) ** (1.0 / (_GRID_POINTS - 1))
    xs = [_X_LOW]
    for _ in range(_GRID_POINTS - 1):
        xs.append(xs[-1] * step)
    xs[-1] = _X_HIGH""")
OUT.joinpath("alt_r15e_a_irr_grid_cumulative_product.py").write_text(a, encoding="utf-8")

# B: Monte Carlo by the affine identity: NPV(m) = a + b * m, with a and b from two deterministic evaluations.
b = swap(REF,
"""    rng = random.Random(seed)
    out: list[float] = []
    for _ in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        scaled = dict(project)
        scaled["revenue"] = [m * float(x) for x in project["revenue"]]
        out.append(npv(rate, after_tax_cash_flows(scaled)))
    return out""",
"""    def at(multiplier: float) -> float:
        scaled = dict(project)
        scaled["revenue"] = [multiplier * float(x) for x in project["revenue"]]
        return npv(rate, after_tax_cash_flows(scaled))

    at_zero, at_one = at(0.0), at(1.0)
    slope = at_one - at_zero
    rng = random.Random(seed)
    out: list[float] = []
    for _ in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        out.append(at_zero + slope * m)
    return out""")
OUT.joinpath("alt_r15e_b_monte_carlo_affine_in_multiplier.py").write_text(b, encoding="utf-8")

# C: payback by itertools.accumulate and next() instead of an explicit loop.
c = swap(REF,
"""    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    cumulative = discounted[0]
    for t in range(1, len(discounted)):
        if cumulative + discounted[t] >= 0.0:
            return (t - 1) + (-cumulative) / discounted[t]
        cumulative += discounted[t]
    return math.inf""",
"""    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    sums = list(itertools.accumulate(discounted))
    t = next((k for k in range(1, len(discounted)) if sums[k] >= 0.0), None)
    if t is None:
        return math.inf
    return (t - 1) + (-sums[t - 1]) / discounted[t]""")
OUT.joinpath("alt_r15e_c_payback_accumulate_next.py").write_text(c, encoding="utf-8")
print("ok")
