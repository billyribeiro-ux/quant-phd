"""Write round-17 new student-error mutants and correct alternatives, derived from the reference by exact text edits.

Each edit must match exactly once in reference.py, or the script aborts (no silent no-op).
Usage: python -I make_r17.py <checkout>
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/AC4/mutants"
ALT = ROOT / "ledgers/AC4/scripts/AC4-e-r17/alts"
ALT.mkdir(parents=True, exist_ok=True)


def build(edits, first_line_old, first_line_new):
    text = REF
    assert text.count(first_line_old) == 1, "docstring first line"
    text = text.replace(first_line_old, first_line_new)
    for old, new in edits:
        n = text.count(old)
        assert n == 1, f"edit matches {n} times: {old[:70]!r}"
        text = text.replace(old, new)
    return text


DOC_OLD = '"""Reference solution for the AC4 budget and variance engine (budget_engine.py).'

MUTANTS = {
    "r17e_01_flexed_budget_uses_actual_mix.py": (
        "Student error: the flexed budget uses each product's actual units, not the budgeted mix at the actual total.",
        [
            (
                "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n"
                "    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
                "    revenue = sum(p[\"actual_units\"] * p[\"budget_price_cents\"] for p in products)\n"
                "    variable = sum(p[\"actual_units\"] * p[\"standard_inputs_per_unit\"] * input_price for p in products)\n",
            ),
        ],
    ),
    "r17e_02_flexed_fixed_overhead_scales_with_units.py": (
        "Student error: fixed overhead is scaled with volume in the flexed budget (the error card AC4-c063 refutes).",
        [
            (
                "    return {\n        \"units\": total,",
                "    fixed = _nearest_cent(Fraction(total * fixed, budget_units))\n    return {\n        \"units\": total,",
            ),
        ],
    ),
    "r17e_03_efficiency_on_budget_average_standard.py": (
        "Student error: the efficiency variance uses the budgeted average standard applied to the actual total, "
        "not each product's standard for its actual units.",
        [
            (
                "    standard_inputs = sum(p[\"standard_inputs_per_unit\"] * p[\"actual_units\"] for p in products)\n",
                "    budget_std = sum(p[\"budget_units\"] * p[\"standard_inputs_per_unit\"] for p in products)\n"
                "    budget_total = sum(p[\"budget_units\"] for p in products)\n"
                "    standard_inputs = actual_total * budget_std // budget_total\n",
            ),
        ],
    ),
    "r17e_04_flexible_units_report_budget_units.py": (
        "Student error: the flexible budget reports the budgeted total units in its units key, not the flexed total.",
        [
            (
                "    return {\n        \"units\": total,",
                "    return {\n        \"units\": budget_units,",
            ),
        ],
    ),
}

ALTS = {
    "alt17_a_divmod_nearest_cent.py": (
        "Correct alternative (round 17): nearest whole cent by divmod, halves up; same behaviour on non-negative amounts.",
        [
            (
                "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n",
                "    q, r = divmod(amount.numerator, amount.denominator)\n    return q + (1 if 2 * r >= amount.denominator else 0)\n",
            ),
        ],
    ),
    "alt17_b_efficiency_and_mix_restated.py": (
        "Correct alternative (round 17): efficiency and actual-mix contribution restated as totals over products.",
        [
            (
                "    standard_inputs = sum(p[\"standard_inputs_per_unit\"] * p[\"actual_units\"] for p in products)\n"
                "    efficiency = input_price * (standard_inputs - actual_inputs)\n",
                "    standard_inputs = sum(p[\"standard_inputs_per_unit\"] * p[\"actual_units\"] for p in products)\n"
                "    efficiency = input_price * standard_inputs - input_price * actual_inputs\n",
            ),
            (
                "    actual_mix_contribution = (\n"
                "        sum(\n"
                "            p[\"actual_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price)\n"
                "            for p in products\n"
                "        )\n"
                "        - fixed\n"
                "    )\n",
                "    gross = sum(p[\"actual_units\"] * p[\"budget_price_cents\"] for p in products)\n"
                "    inputs_at_standard = sum(p[\"actual_units\"] * p[\"standard_inputs_per_unit\"] for p in products)\n"
                "    actual_mix_contribution = gross - inputs_at_standard * input_price - fixed\n",
            ),
        ],
    ),
    "alt17_c_truncate_after_half.py": (
        "Correct alternative (round 17): nearest whole cent as int(x + 1/2); exact for the non-negative amounts here.",
        [
            (
                "    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)\n",
                "    return int(amount + Fraction(1, 2))\n",
            ),
        ],
    ),
}

for name, (first, edits) in MUTANTS.items():
    (MUT / name).write_text(build(edits, DOC_OLD, '"""' + first + "\n\nReference of the AC4 engine with one edit."), encoding="utf-8")
    print("wrote", MUT / name)
for name, (first, edits) in ALTS.items():
    (ALT / name).write_text(build(edits, DOC_OLD, '"""' + first + "\n\nReference of the AC4 engine with one edit."), encoding="utf-8")
    print("wrote", ALT / name)
