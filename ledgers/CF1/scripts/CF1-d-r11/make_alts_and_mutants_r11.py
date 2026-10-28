"""Round 11 (verifier CF1-d): write five alternative correct engines and three new student-error mutants.

Usage: python make_alts_and_mutants_r11.py <checkout> <alt_dir> <mutant_dir>
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
    # Horner-style accumulation from the last flow: same NPV, different rounding path.
    "alt_r11_1_npv_horner_from_last_flow.py": [
        (
            "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
            "    acc = 0.0\n    for cf in reversed(list(flows)):\n        acc = acc / (1.0 + rate) + cf\n    return acc",
        ),
    ],
    # Payback with a cutoff 1e-9 below zero, and prefix sums through math.fsum.
    "alt_r11_2_payback_fsum_prefix_cutoff.py": [
        (
            "        if cumulative + discounted[t] >= 0.0:",
            "        if math.fsum([cumulative, discounted[t]]) >= -1e-9:",
        ),
    ],
    # Monte Carlo NPV as the affine identity a + b * m, with a = NPV at m = 0 and b = NPV at m = 1 minus a.
    "alt_r11_3_monte_carlo_affine_identity.py": [
        (
            "        scaled = dict(project)\n        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n        out.append(npv(rate, after_tax_cash_flows(scaled)))",
            "        zero_rev = dict(project)\n        zero_rev[\"revenue\"] = [0.0 * float(x) for x in project[\"revenue\"]]\n"
            "        one_rev = dict(project)\n        one_rev[\"revenue\"] = [1.0 * float(x) for x in project[\"revenue\"]]\n"
            "        a = npv(rate, after_tax_cash_flows(zero_rev))\n"
            "        b = npv(rate, after_tax_cash_flows(one_rev)) - a\n"
            "        out.append(a + b * m)",
        ),
    ],
    # Fisher identity written as the expanded sum; the same identity, not a rule of thumb.
    "alt_r11_4_fisher_expanded_sum.py": [
        ("    return (1.0 + real) * (1.0 + inflation) - 1.0", "    return real + inflation + real * inflation"),
    ],
    # Operating flow written in the convention's algebraic form EBITDA * (1 - tax) + depreciation * tax.
    "alt_r11_5_operating_flow_algebraic_form.py": [
        (
            "        tax = tax_rate * (ebitda - depreciation)\n        working_capital = -(nwc[t] - nwc[t - 1])\n        flows.append(ebitda - tax + working_capital)",
            "        working_capital = -(nwc[t] - nwc[t - 1])\n        flows.append(ebitda * (1.0 - tax_rate) + depreciation * tax_rate + working_capital)",
        ),
    ],
}

MUTS = {
    "m58_npv_drops_zero_flows_from_the_time_index.py": (
        "npv drops the zero flows before discounting, so a zero flow in a later year loses its place in the time index and "
        "later flows are discounted one period too little.",
        [
            (
                "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
                "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(c for c in flows if c != 0.0))",
            ),
        ],
    ),
    "m59_monte_carlo_reseeds_at_seed_plus_draw_index.py": (
        "The student seeds each draw with seed plus the draw index, so the draws do not follow the single seeded stream "
        "from random.Random(seed) that the specification names.",
        [
            (
                "        z = rng.gauss(0.0, 1.0)",
                "        z = random.Random(seed + len(out)).gauss(0.0, 1.0)",
            ),
        ],
    ),
    "m60_fisher_nominal_clamped_at_zero.py": (
        "The student clamps the nominal rate at zero, reading a negative nominal rate as impossible, so the Fisher "
        "identity is not exact when the nominal rate is negative.",
        [
            (
                "    return (1.0 + real) * (1.0 + inflation) - 1.0",
                "    return max(0.0, (1.0 + real) * (1.0 + inflation) - 1.0)",
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
