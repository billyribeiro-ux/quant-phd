"""Writes round-36 student-error mutants of the AC4 project grader into ledgers/AC4/mutants (top level)."""
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
    "r36e_01_actual_profit_keeps_fixed_overhead.py": (
        "Actual profit is computed without deducting the actual fixed overhead, so the total variance is overstated by the fixed overhead.",
        [("    actual_profit -= fixed\n", "")],
    ),
    "r36e_02_flexed_revenue_truncated_to_dollars.py": (
        "Flexed revenue is truncated to whole dollars (multiples of 100 cents) before the variances are taken.",
        [("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n",
          "    revenue = (total * budget_revenue // budget_units) // 100 * 100\n")],
    ),
    "r36e_03_total_variance_sign_reversed.py": (
        "The total is reported as the master budget profit minus the actual profit, so a favourable total is shown negative.",
        [("        \"total\": actual_profit - master,\n", "        \"total\": master - actual_profit,\n")],
    ),
}
for name, (doc, edits) in mutants.items():
    (out / name).write_text(build(doc, edits), encoding="utf-8")
    print("wrote mutant", name)
