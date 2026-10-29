"""Writes three round-32 student-error mutants of the AC4 project grader (edits of grader/reference.py)."""
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
    end = text.index('"""\n', 3) + 4
    text = '"""' + doc + '\n"""\n' + text[end:]
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)


make("r32e_01_volume_at_budget_contribution_per_unit.py",
     "Sales volume valued as the change in total units times the budget contribution per unit, rounded once.",
     [("    sales_volume = flexed - master\n",
       "    budget_total = sum(p[\"budget_units\"] for p in products)\n"
       "    budget_contribution = Fraction(\n"
       "        sum(p[\"budget_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price) for p in products),\n"
       "        budget_total,\n"
       "    )\n"
       "    sales_volume = round((actual_total - budget_total) * budget_contribution)\n")])

make("r32e_02_flexed_revenue_at_average_price_truncated.py",
     "Flexed revenue uses the budget average price per unit truncated to whole cents, then multiplied by the actual total.",
     [("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n",
       "    revenue = total * (budget_revenue // budget_units)\n")])

make("r32e_03_mix_uses_actual_selling_price.py",
     "Sales mix variance takes each product's contribution at its actual selling price, so the price effect is counted twice.",
     [("            p[\"actual_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price)\n",
       "            p[\"actual_units\"] * (p[\"actual_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price)\n")])
