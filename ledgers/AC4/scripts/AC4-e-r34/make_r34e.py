"""Writes round-34 student-error mutants (top-level ledgers/AC4/mutants) and correct alternatives (alts/) of the AC4 project grader."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
ref = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/AC4/mutants"
alts = ROOT / "ledgers/AC4/scripts/AC4-e-r34/alts"


def build(doc, edits):
    text = ref
    for old, new in edits:
        n = text.count(old)
        assert n == 1, (n, old[:70])
        text = text.replace(old, new)
    end = text.index('"""\n', 3) + 4
    return '"""' + doc + '\n"""\n' + text[end:]


mutants = {
    "r34e_01_mix_measured_against_master_profit.py": (
        "Sales mix variance is the actual mix contribution less the master budget profit, so the volume effect is counted again inside the mix.",
        [("    sales_mix = actual_mix_contribution - flexed\n", "    sales_mix = actual_mix_contribution - master\n")],
    ),
    "r34e_02_flexed_variable_cost_truncated_revenue_rounded.py": (
        "Flexed variable cost is truncated toward zero while flexed revenue is rounded half up to the whole cent.",
        [("    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
          "    variable = (total * budget_variable) // budget_units\n")],
    ),
    "r34e_03_efficiency_divided_by_actual_units.py": (
        "Efficiency variance is divided by the actual total units, giving a per-unit figure in place of cents.",
        [("    efficiency = input_price * (standard_inputs - actual_inputs)\n",
          "    efficiency = input_price * (standard_inputs - actual_inputs) // max(sum(p[\"actual_units\"] for p in products), 1)\n")],
    ),
}
for name, (doc, edits) in mutants.items():
    (out / name).write_text(build(doc, edits), encoding="utf-8")
    print("wrote mutant", name)

alts.mkdir(parents=True, exist_ok=True)
half_up = (
    "def _half_up(num: int, den: int) -> int:\n"
    "    return (2 * num + den) // (2 * den)\n\n\n"
)
alt_a = build("Alternative A (correct): flexed revenue and variable cost rounded half up with integer divmod.", [
    ("def master_budget(", half_up + "def master_budget("),
    ("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n",
     "    revenue = _half_up(total * budget_revenue, budget_units)\n"),
    ("    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
     "    variable = _half_up(total * budget_variable, budget_units)\n"),
])
alt_b = build("Alternative B (correct): sales mix derived as the total less the other three variances.", [
    ("    sales_mix = actual_mix_contribution - flexed\n",
     "    sales_mix = (actual_profit - master) - sales_volume - sales_price - efficiency\n"),
])
alt_c = build("Alternative C (correct): half-up rounding by exact Fraction floor(x + 1/2).", [
    ("def master_budget(", "import math\n\n\ndef _half_up_frac(x: Fraction) -> int:\n    return math.floor(x + Fraction(1, 2))\n\n\ndef master_budget("),
    ("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n",
     "    revenue = _half_up_frac(Fraction(total * budget_revenue, budget_units))\n"),
    ("    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
     "    variable = _half_up_frac(Fraction(total * budget_variable, budget_units))\n"),
])
(alts / "alt34_a_divmod_half_up.py").write_text(alt_a, encoding="utf-8")
(alts / "alt34_b_mix_derived_from_total.py").write_text(alt_b, encoding="utf-8")
(alts / "alt34_c_floor_half_fraction.py").write_text(alt_c, encoding="utf-8")
print("wrote alternatives")
