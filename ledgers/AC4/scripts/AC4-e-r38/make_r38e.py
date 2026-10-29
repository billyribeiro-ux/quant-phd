"""Writes round-38 student-error mutants of the AC4 project grader into ledgers/AC4/mutants (top level)."""
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
    "r38e_01_volume_variance_reported_as_magnitude.py": (
        "The sales volume variance is reported as its absolute size, so an unfavourable volume variance shows as a positive figure.",
        [("    sales_volume = flexed - master\n", "    sales_volume = abs(flexed - master)\n")],
    ),
    "r38e_02_total_is_sum_of_the_four_parts.py": (
        "The total is taken as the sum of the four variances instead of the actual profit less the master budget profit.",
        [("        \"total\": actual_profit - master,\n", "        \"total\": sales_price + sales_volume + sales_mix + efficiency,\n")],
    ),
    "r38e_03_master_budget_skips_unsold_products.py": (
        "The master budget sums only the products with actual units sold, so a budgeted product that did not sell is left out of the plan.",
        [
            (
                "    input_price, fixed, _, products = _case(case)\n    units = {p[\"name\"]: p[\"budget_units\"] for p in products}\n",
                "    input_price, fixed, _, products = _case(case)\n    products = [p for p in products if p[\"actual_units\"] > 0]\n    units = {p[\"name\"]: p[\"budget_units\"] for p in products}\n",
            )
        ],
    ),
}
for name, (doc, edits) in mutants.items():
    (out / name).write_text(build(doc, edits), encoding="utf-8")
    print("wrote mutant", name)
