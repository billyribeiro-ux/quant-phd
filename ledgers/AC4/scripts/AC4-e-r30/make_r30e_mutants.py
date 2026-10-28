"""Writes the six round-30 student-error mutants of the AC4 project grader as edits of grader/reference.py."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
ref = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/AC4/mutants"

def make(name, doc, edits):
    text = ref
    for old, new in edits:
        n = text.count(old)
        assert n == 1, (name, n, old[:60])
        text = text.replace(old, new)
    # the docstring's first line describes the error; the module docstring is replaced
    end = text.index('"""\n', 3) + 4
    text = '"""' + doc + '\n"""\n' + text[end:]
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)

make("r30e_01_total_is_sum_of_the_four_variances.py",
     "Total variance computed as the sum of the four variances, so the reconciliation holds by construction.",
     [("        \"total\": actual_profit - master,",
       "        \"total\": sales_price + sales_volume + sales_mix + efficiency,")])

make("r30e_02_volume_uses_exact_flexed_profit_rounded_once.py",
     "Sales volume takes the exact flexed profit rounded once, while the mix keeps the whole-cent flexed profit.",
     [("    sales_volume = flexed - master\n",
       "    exact_flexed = Fraction(actual_total * budget_revenue, budget_units) - Fraction(actual_total * budget_variable, budget_units) - fixed\n"
       "    sales_volume = _nearest_cent(exact_flexed) - master\n")])

make("r30e_03_volume_valued_at_actual_mix.py",
     "Sales volume values the change in total units at the actual average contribution per unit, not the budgeted mix.",
     [("    sales_volume = flexed - master\n",
       "    actual_margin_per_unit = Fraction(sum(p[\"actual_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price) for p in products), actual_total)\n"
       "    sales_volume = round((actual_total - sum(p[\"budget_units\"] for p in products)) * actual_margin_per_unit)\n")])

make("r30e_04_zero_units_returns_early_without_fixed_overhead.py",
     "Flexed budget at zero units returns zero profit, dropping the fixed overhead that does not flex.",
     [("    total = _nonnegative(actual_units, \"actual_units\")\n",
       "    total = _nonnegative(actual_units, \"actual_units\")\n"
       "    if total == 0:\n"
       "        _case(case)\n"
       "        return {\"units\": 0, \"revenue_cents\": 0, \"variable_cost_cents\": 0, \"fixed_cost_cents\": 0, \"profit_cents\": 0}\n")])

make("r30e_05_price_variance_skips_products_without_budgeted_units.py",
     "Sales price variance skips any product that has no budgeted units, so an unbudgeted launch's price effect is dropped.",
     [("    sales_price = sum((p[\"actual_price_cents\"] - p[\"budget_price_cents\"]) * p[\"actual_units\"] for p in products)\n",
       "    sales_price = sum(\n"
       "        (p[\"actual_price_cents\"] - p[\"budget_price_cents\"]) * p[\"actual_units\"] for p in products if p[\"budget_units\"] > 0\n"
       "    )\n"
       "")])

make("r30e_06_efficiency_uses_summed_standards_times_total_output.py",
     "Efficiency applies the sum of the per-product standards to the total output, not each product's own actual units.",
     [("    standard_inputs = sum(p[\"standard_inputs_per_unit\"] * p[\"actual_units\"] for p in products)\n    efficiency",
       "    standard_inputs = sum(p[\"standard_inputs_per_unit\"] for p in products) * actual_total\n    efficiency")])
