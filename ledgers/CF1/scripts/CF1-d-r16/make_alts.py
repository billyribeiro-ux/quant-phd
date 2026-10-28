"""Write three round-16 alternative correct implementations of the CF1 engine from the reference solution."""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/CF1/scripts/CF1-d-r16/alts"


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:70]
    return text.replace(old, new)


# a: algebraic after-tax flow (EBITDA x (1 - tax) + shield), affine Monte Carlo (a + b * m), exp/log1p Fisher form.
a = swap(ref, "        flows.append(ebitda - tax + working_capital)",
         "        flows.append(ebitda * (1.0 - tax_rate) + depreciation * tax_rate + working_capital)")
a = swap(a, "    return (1.0 + real) * (1.0 + inflation) - 1.0",
         "    return math.expm1(math.log1p(real) + math.log1p(inflation))")
a = swap(a, """    out: list[float] = []
    for _ in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        scaled = dict(project)
        scaled["revenue"] = [m * float(x) for x in project["revenue"]]
        out.append(npv(rate, after_tax_cash_flows(scaled)))
""", """    zero_rev = dict(project)
    zero_rev["revenue"] = [0.0] * len(project["revenue"])
    a0 = npv(rate, after_tax_cash_flows(zero_rev))
    a1 = npv(rate, after_tax_cash_flows(project))
    out: list[float] = []
    for _ in range(n_draws):
        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        out.append(a0 + (a1 - a0) * m)
""")
(out / "alt_r16_a_algebraic_flow_affine_montecarlo.py").write_text(a, encoding="utf-8")

# b: denser IRR search grid over the same window (a different numerical cutoff).
b = swap(ref, "_GRID_POINTS = 4001", "_GRID_POINTS = 8001")
(out / "alt_r16_b_denser_irr_grid.py").write_text(b, encoding="utf-8")

# c: payback recomputes the cumulative sum from the start at each year (a different algorithm, same rule).
c = swap(ref, """    cumulative = discounted[0]
    for t in range(1, len(discounted)):
        if cumulative + discounted[t] >= 0.0:
            return (t - 1) + (-cumulative) / discounted[t]
        cumulative += discounted[t]
""", """    for t in range(1, len(discounted)):
        before = sum(discounted[:t])
        if before + discounted[t] >= 0.0:
            return (t - 1) + (-before) / discounted[t]
""")
(out / "alt_r16_c_payback_cumulative_recomputed.py").write_text(c, encoding="utf-8")
print("wrote 3 alternatives")
