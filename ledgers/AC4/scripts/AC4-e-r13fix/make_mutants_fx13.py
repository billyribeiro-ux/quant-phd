# ruff: noqa: E501
"""Write ten student-error mutants of the AC4 reference into ledgers/AC4/mutants/ (fx13_ prefix).

Each mutant is the reference with one replacement; every anchor must occur exactly once, or the script stops.
The first docstring line of each mutant names the student error.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
REF = ROOT / "course/modules/AC/AC4/grader/reference.py"
OUT = ROOT / "ledgers/AC4/mutants"
REF_DOC = '"""Reference solution for the AC4 budget and variance engine (budget_engine.py).'

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "fx13_price_variance_favourable_only": (
        "Student error: the sales price variance keeps only the favourable price changes, so a price fall is dropped.",
        [
            (
                '    sales_price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in products)',
                '    sales_price = sum(max(0, (p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"]) for p in products)',
            )
        ],
    ),
    "fx13_mix_reported_as_size": (
        "Student error: the sales mix variance is reported as its size, so an unfavourable mix shows as positive.",
        [("    sales_mix = actual_mix_contribution - flexed", "    sales_mix = abs(actual_mix_contribution - flexed)")],
    ),
    "fx13_negative_product_units_clamped": (
        "Student error: a negative actual unit count on a product is clamped to zero instead of refused.",
        [
            (
                '"actual_units": _nonnegative(item["actual_units"], f"{name} actual_units"),',
                '"actual_units": max(0, _whole(item["actual_units"], f"{name} actual_units")),',
            )
        ],
    ),
    "fx13_zero_budget_product_divides": (
        "Student error: the budgeted margin per unit is computed for every product, so a product with no budgeted units divides by zero.",
        [
            (
                '    master = master_budget(case)["profit_cents"]',
                '    master = master_budget(case)["profit_cents"]\n    _margin = [p["budget_price_cents"] / p["budget_units"] for p in products]',
            )
        ],
    ),
    "fx13_flexed_rounded_per_product": (
        "Student error: the flexed revenue is rounded product by product and the rounded parts are added.",
        [
            (
                "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))",
                '    revenue = sum(_nearest_cent(Fraction(total * p["budget_units"] * p["budget_price_cents"], budget_units)) for p in products)',
            )
        ],
    ),
    "fx13_mix_truncated_from_exact": (
        "Student error: the sales mix is computed from the exact flexed profit and truncated to a whole cent.",
        [
            (
                "    sales_mix = actual_mix_contribution - flexed",
                '    _bu = sum(p["budget_units"] for p in products)\n'
                '    _br = sum(p["budget_units"] * p["budget_price_cents"] for p in products)\n'
                '    _bv = sum(p["budget_units"] * p["standard_inputs_per_unit"] * input_price for p in products)\n'
                '    _exact = Fraction(sum(p["actual_units"] for p in products) * _br, _bu) - Fraction(\n'
                '        sum(p["actual_units"] for p in products) * _bv, _bu\n'
                "    ) - fixed\n"
                "    sales_mix = int(Fraction(actual_mix_contribution) - _exact)",
            )
        ],
    ),
    "fx13_zero_actual_inputs_refused": (
        "Student error: a case in which no input unit was used is refused, although zero is a valid count.",
        [
            (
                '    actual_inputs = _nonnegative(case["actual_inputs_used"], "actual_inputs_used")',
                '    actual_inputs = _nonnegative(case["actual_inputs_used"], "actual_inputs_used")\n'
                "    if actual_inputs == 0:\n"
                '        raise ValueError("no input units were used")',
            )
        ],
    ),
    "fx13_bool_unit_argument_as_one": (
        "Student error: flexible_budget reads True as one unit, because a bool is an int, instead of refusing it.",
        [
            (
                '    total = _nonnegative(actual_units, "actual_units")',
                '    total = 1 if actual_units is True else _nonnegative(actual_units, "actual_units")',
            )
        ],
    ),
    "fx13_negative_fixed_overhead_accepted": (
        "Student error: a negative fixed overhead is accepted, because only the sign of the other fields is checked.",
        [
            (
                '    fixed = _nonnegative(case["fixed_overhead_cents"], "fixed_overhead_cents")',
                '    fixed = _whole(case["fixed_overhead_cents"], "fixed_overhead_cents")',
            )
        ],
    ),
    "fx13_zero_standard_inputs_refused": (
        "Student error: a product whose standard input count is zero is refused, although a product may use no input.",
        [
            (
                '        products.append(\n            {\n                "name": name,',
                '        if item["standard_inputs_per_unit"] == 0:\n'
                '            raise ValueError("a product needs at least one standard input")\n'
                '        products.append(\n            {\n                "name": name,',
            )
        ],
    ),
}


def main() -> None:
    reference = REF.read_text(encoding="utf-8")
    assert reference.count(REF_DOC) == 1, "reference docstring anchor"
    for name, (description, edits) in MUTANTS.items():
        text = reference.replace(REF_DOC, f'"""{description}', 1)
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: anchor found {count} times: {old[:70]!r}")
            text = text.replace(old, new, 1)
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
