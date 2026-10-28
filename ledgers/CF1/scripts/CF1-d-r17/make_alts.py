"""Write three round-17 alternative correct engines (different algorithms and cutoffs) into a directory (argv[2])."""

import sys
from pathlib import Path

root = Path(sys.argv[1])
dst = Path(sys.argv[2])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:70]
    return text.replace(old, new)


# A: algebraic form of after-tax flows, accumulate-based payback, Horner NPV.
a = swap(
    ref,
    """        ebitda = revenue[t - 1] - costs[t - 1]
        tax = tax_rate * (ebitda - depreciation)
        working_capital = -(nwc[t] - nwc[t - 1])
        flows.append(ebitda - tax + working_capital)
""",
    """        ebitda = revenue[t - 1] - costs[t - 1]
        operating = ebitda * (1.0 - tax_rate) + depreciation * tax_rate
        working_capital = -(nwc[t] - nwc[t - 1])
        flows.append(operating + working_capital)
""",
)
a = swap(
    a,
    """    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    cumulative = discounted[0]
    for t in range(1, len(discounted)):
        if cumulative + discounted[t] >= 0.0:
            return (t - 1) + (-cumulative) / discounted[t]
        cumulative += discounted[t]
    return math.inf
""",
    """    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]
    sums = list(itertools.accumulate(discounted))
    hit = next((t for t in range(1, len(sums)) if sums[t] >= 0.0), None)
    if hit is None:
        return math.inf
    return (hit - 1) + (-sums[hit - 1]) / discounted[hit]
""",
)
a = swap(
    a,
    """    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))
""",
    """    x = 1.0 / (1.0 + rate)
    total = 0.0
    for cf in reversed(flows):
        total = total * x + cf
    return total * 1.0 if False else total
""",
)
# The Horner form is algebraically the same sum; the final expression above is kept as plain total.
a = a.replace("    return total * 1.0 if False else total\n", "    return total\n")
(dst / "alt_r17_a_algebraic_flows_accumulate_payback_horner_npv.py").write_text(a, encoding="utf-8")

# B: bisection with an absolute zero test and a different stopping width; the grid is the same.
b = swap(
    ref,
    """                if f_mid == 0.0:
                    lo = hi = mid
                    break
""",
    """                if abs(f_mid) <= 1e-300:
                    lo = hi = mid
                    break
""",
)
b = swap(b, "                if hi - lo <= 1e-15 * hi:\n", "                if hi - lo <= 4e-14 * hi:\n")
(dst / "alt_r17_b_bisection_absolute_zero_and_wider_stop.py").write_text(b, encoding="utf-8")

# C: Fisher through logarithms; Monte Carlo draws through the normal-cdf-free exp form written as explicit products.
c = swap(
    ref,
    "    return (1.0 + real) * (1.0 + inflation) - 1.0\n",
    "    return math.expm1(math.log1p(real) + math.log1p(inflation))\n",
)
c = swap(
    c,
    "        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n",
    "        scale = m\n        scaled[\"revenue\"] = [scale * float(x) for x in project[\"revenue\"]]\n",
)
(dst / "alt_r17_c_logarithmic_fisher_scaled_revenue.py").write_text(c, encoding="utf-8")
print("wrote 3 alternatives")
