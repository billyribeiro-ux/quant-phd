"""Write round-8 student-error mutants m38-m40 from the reference solution by exact string replacement."""
import pathlib
ref = pathlib.Path("/tmp/verify8-AC4-e/course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("/tmp/verify8-AC4-e/ledgers/AC4/mutants")

def make(name, doc, edits):
    text = ref
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    body = text.split('"""', 2)[2].lstrip("\n")  # drop the reference module docstring; keep the code
    (out / name).write_text(f'"""{doc}"""\n' + body, encoding="utf-8")

# m38: the flexed budget rounds the budgeted revenue and cost PER UNIT to the cent before scaling to the actual total.
make(
    "m38_flexed_per_unit_rounded_first.py",
    "flexible_budget rounds the budgeted revenue and variable cost per unit to the nearest cent before it scales them to the actual units.",
    [
        ("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n"
         "    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
         "    revenue = total * _nearest_cent(Fraction(budget_revenue, budget_units))\n"
         "    variable = total * _nearest_cent(Fraction(budget_variable, budget_units))\n"),
    ],
)

# m39: the whole-number check for actual_inputs_used is applied only by master_budget; the other two functions skip the boolean refusal.
make(
    "m39_bool_actual_inputs_refused_only_by_master.py",
    "The boolean refusal for actual_inputs_used is applied only in master_budget; flexible_budget and variance_decomposition accept True as one input unit.",
    [
        ('    actual_inputs = _nonnegative(case["actual_inputs_used"], "actual_inputs_used")\n',
         '    _raw_ai = case["actual_inputs_used"]\n'
         '    actual_inputs = int(_raw_ai) if isinstance(_raw_ai, bool) else _nonnegative(_raw_ai, "actual_inputs_used")\n'),
        ("def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:\n"
         '    """The master budget: budgeted units, revenue and cost by product, and the budgeted profit, in cents."""\n'
         "    input_price, fixed, _, products = _case(case)\n",
         "def master_budget(case: Mapping[str, Any]) -> dict[str, Any]:\n"
         '    """The master budget: budgeted units, revenue and cost by product, and the budgeted profit, in cents."""\n'
         "    input_price, fixed, _ai, products = _case(case)\n"
         "    _nonnegative(case[\"actual_inputs_used\"], \"actual_inputs_used\")\n"),
    ],
)

# m40: zero budgeted units is refused by master_budget only; flexible_budget and variance_decomposition return zeros instead.
make(
    "m40_zero_budget_units_refused_only_by_master.py",
    "Only master_budget refuses a budget with no budgeted units; flexible_budget returns zero revenue and cost instead of raising ValueError.",
    [
        ("    input_price, fixed, _, products = _case(case)\n    units = {p[\"name\"]: p[\"budget_units\"] for p in products}\n",
         "    input_price, fixed, _, products = _case(case)\n    if sum(p[\"budget_units\"] for p in products) == 0:\n        raise ValueError(\"no budgeted units\")\n    units = {p[\"name\"]: p[\"budget_units\"] for p in products}\n"),
        ('    if sum(p["budget_units"] for p in products) == 0:\n'
         '        raise ValueError("the master budget has no budgeted units, so no budgeted mix exists")\n'
         "    return input_price, fixed, actual_inputs, products\n",
         "    return input_price, fixed, actual_inputs, products\n"),
        ("    budget_units = sum(p[\"budget_units\"] for p in products)\n"
         "    budget_revenue = sum(p[\"budget_units\"] * p[\"budget_price_cents\"] for p in products)\n"
         "    budget_variable = sum(p[\"budget_units\"] * p[\"standard_inputs_per_unit\"] * input_price for p in products)\n"
         "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n"
         "    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n",
         "    budget_units = sum(p[\"budget_units\"] for p in products)\n"
         "    budget_revenue = sum(p[\"budget_units\"] * p[\"budget_price_cents\"] for p in products)\n"
         "    budget_variable = sum(p[\"budget_units\"] * p[\"standard_inputs_per_unit\"] * input_price for p in products)\n"
         "    if budget_units == 0:\n"
         "        return {\"units\": total, \"revenue_cents\": 0, \"variable_cost_cents\": 0, \"fixed_cost_cents\": fixed,\n"
         "                \"profit_cents\": -fixed}\n"
         "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))\n"
         "    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))\n"),
    ],
)
print("written")
