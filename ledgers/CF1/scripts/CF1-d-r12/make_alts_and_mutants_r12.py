"""Round 12 (verifier CF1-d): five alternative correct engines and five new student-error mutants.

Usage: python make_alts_and_mutants_r12.py <checkout> <alt_dir> <mutant_dir>
Every edit must match the reference exactly once (apply asserts this).
"""

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
ALT = pathlib.Path(sys.argv[2])
MUT = pathlib.Path(sys.argv[3])
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")


def apply(src: str, edits: list[tuple[str, str]]) -> str:
    for old, new in edits:
        n = src.count(old)
        assert n == 1, (old[:70], n)
        src = src.replace(old, new, 1)
    return src


ALTS = {
    # NPV by a running discount factor instead of a power per flow: same sum, different rounding path.
    "alt_r12_1_npv_running_discount_factor.py": [
        (
            "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
            "    total, factor = 0.0, 1.0\n    for cf in flows:\n        total += cf * factor\n        factor /= 1.0 + rate\n    return total",
        ),
    ],
    # IRR scan on a coarser grid of 2001 samples: the page says the grid decides only roots closer than one step.
    "alt_r12_2_irr_grid_2001_points.py": [
        ("_GRID_POINTS = 4001", "_GRID_POINTS = 2001"),
    ],
    # Payback treats a cumulative value within 1e-12 of zero as recovered (a rounding cutoff, not a rule change).
    "alt_r12_3_payback_rounding_cutoff.py": [
        (
            "        if cumulative + discounted[t] >= 0.0:",
            "        if cumulative + discounted[t] >= -1e-12:",
        ),
    ],
    # Monte Carlo multiplier written as exp(volatility * z) * exp(-volatility ** 2 / 2): the same value, a different rounding path.
    "alt_r12_4_monte_carlo_split_exponentials.py": [
        (
            "        m = math.exp(volatility * z - volatility * volatility / 2.0)",
            "        m = math.exp(volatility * z) * math.exp(-volatility * volatility / 2.0)",
        ),
    ],
    # Fisher written as real + inflation + real * inflation rearranged as (1 + real) * (1 + inflation) - 1 with
    # the nominal rate computed by exp(log1p) form: the same identity.
    "alt_r12_5_fisher_log1p_form.py": [
        (
            "    return (1.0 + real) * (1.0 + inflation) - 1.0",
            "    return math.expm1(math.log1p(real) + math.log1p(inflation))",
        ),
    ],
}

MUTS = {
    "r12d_01_shield_dropped_in_final_year.py": (
        "The student drops the depreciation tax shield in the last year of life, so the operating flow of that year "
        "is taxed on EBITDA alone while the earlier years receive the shield.",
        [
            (
                "        tax = tax_rate * (ebitda - depreciation)",
                "        tax = tax_rate * (ebitda - (depreciation if t < life else 0.0))",
            ),
        ],
    ),
    "r12d_02_payback_accepts_zero_outlay.py": (
        "payback_period accepts a zero outlay: the guard is written as a refusal only of a positive first flow, so a "
        "zero flows[0] is not refused as the specification's negative-outlay rule requires.",
        [
            (
                '    if not flows[0] < 0:',
                '    if flows[0] > 0:',
            ),
        ],
    ),
    "r12d_03_monte_carlo_correction_sign_flipped.py": (
        "The lognormal correction is added rather than subtracted, so the draw multiplier has mean exp(volatility "
        "squared) and not one, and the mean of the draws misses the deterministic NPV.",
        [
            (
                "        m = math.exp(volatility * z - volatility * volatility / 2.0)",
                "        m = math.exp(volatility * z + volatility * volatility / 2.0)",
            ),
        ],
    ),
    "r12d_04_npv_discounts_from_the_last_flow.py": (
        "NPV indexes the flows from the last one, so each flow is discounted by the number of flows after it rather "
        "than by its year t.",
        [
            (
                "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
                "    n = len(flows) - 1\n    return sum(cf / (1.0 + rate) ** (n - t) for t, cf in enumerate(flows))",
            ),
        ],
    ),
    "r12d_05_real_deflation_skips_working_capital.py": (
        "With real=True the student deflates the operating flows but leaves the working-capital flows nominal, so the "
        "real flows mix bases within one year.",
        [
            (
                "    if real:\n        flows = [cf / (1.0 + inflation) ** t for t, cf in enumerate(flows)]",
                "    if real:\n        flows = [\n            (cf if t == 0 else (ebitda_t - tax_t) / (1.0 + inflation) ** t + wc_t)\n"
                "            for t, cf, ebitda_t, tax_t, wc_t in zip(range(len(flows)), flows, ops, taxes, wcs)\n        ]",
            ),
            (
                "    flows = [-float(capex)]\n    for t in range(1, life + 1):\n        ebitda = revenue[t - 1] - costs[t - 1]\n"
                "        tax = tax_rate * (ebitda - depreciation)\n        working_capital = -(nwc[t] - nwc[t - 1])\n"
                "        flows.append(ebitda - tax + working_capital)",
                "    flows = [-float(capex)]\n    ops, taxes, wcs = [0.0], [0.0], [0.0]\n    for t in range(1, life + 1):\n"
                "        ebitda = revenue[t - 1] - costs[t - 1]\n        tax = tax_rate * (ebitda - depreciation)\n"
                "        working_capital = -(nwc[t] - nwc[t - 1])\n        ops.append(ebitda)\n        taxes.append(tax)\n"
                "        wcs.append(working_capital)\n        flows.append(ebitda - tax + working_capital)",
            ),
        ],
    ),
}

for name, edits in ALTS.items():
    (ALT / name).write_text(apply(REF, edits), encoding="utf-8")
    print("wrote alt", name)
for name, (desc, edits) in MUTS.items():
    text = REF.replace(
        '"""Reference solution for the CF1 capital-budgeting engine (capbudget.py).',
        '"""' + desc + "\n\nReference solution for the CF1 capital-budgeting engine (capbudget.py).",
        1,
    )
    (MUT / name).write_text(apply(text, edits), encoding="utf-8")
    print("wrote mutant", name)
