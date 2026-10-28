"""Writes two more round-38 student-error mutants (top level of ledgers/AC4/mutants) from the grader reference."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
ref = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/AC4/mutants"


def build(doc, edits):
    text = ref
    for old, new in edits:
        n = text.count(old)
        assert n == 1, (n, old[:70])
        text = text.replace(old, new)
    end = text.index('"""\n', 3) + 4
    return '"""' + doc + '\n"""\n' + text[end:]


mutants = {
    "r38e_04_efficiency_skips_unbudgeted_products.py": (
        "The efficiency variance counts standard inputs only for products that have budgeted units, so a product that was sold without a budget adds no efficiency variance.",
        [(
            '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)\n',
            '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products if p["budget_units"] > 0)\n',
        )],
    ),
    "r38e_05_price_variance_against_standard_cost.py": (
        "The sales price variance is measured against the standard input cost per unit instead of the budgeted selling price.",
        [(
            '    sales_price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in products)\n',
            '    sales_price = sum((p["actual_price_cents"] - p["standard_inputs_per_unit"] * input_price) * p["actual_units"] for p in products)\n',
        )],
    ),
}
for name, (doc, edits) in mutants.items():
    (out / name).write_text(build(doc, edits), encoding="utf-8")
    print("wrote mutant", name)
