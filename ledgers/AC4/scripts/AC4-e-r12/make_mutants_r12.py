"""Generate round-12 student-error mutants from the reference solution by exact one-site substitutions."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1]) / "course/modules/AC/AC4/grader/reference.py"
OUT = pathlib.Path(sys.argv[2])
ref = REF.read_text(encoding="utf-8")

MUTANTS = {
    "m56_sales_price_on_budget_units": (
        "Student error: the sales price variance multiplies each price gap by the budgeted units, not the units sold.",
        '(p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in products)',
        '(p["actual_price_cents"] - p["budget_price_cents"]) * p["budget_units"] for p in products)',
    ),
    "m57_master_variable_on_actual_units": (
        "Student error: the master budget's variable cost per product uses the actual units, not the budgeted units.",
        'variable = {p["name"]: p["budget_units"] * p["standard_inputs_per_unit"] * input_price for p in products}',
        'variable = {p["name"]: p["actual_units"] * p["standard_inputs_per_unit"] * input_price for p in products}',
    ),
    "m58_zero_actual_units_means_budget_total": (
        "Student error: a flexed budget at zero units is treated as the budgeted total, so the zero-unit case is wrong.",
        '    total = _nonnegative(actual_units, "actual_units")\n',
        '    total = _nonnegative(actual_units, "actual_units")\n'
        '    total = total or sum(p["budget_units"] for p in products)\n',
    ),
    "m59_actual_mix_at_actual_price": (
        "Student error: the actual-mix contribution uses the actual selling price instead of the budgeted price.",
        'p["actual_units"] * (p["budget_price_cents"] - p["standard_inputs_per_unit"] * input_price)',
        'p["actual_units"] * (p["actual_price_cents"] - p["standard_inputs_per_unit"] * input_price)',
    ),
    "m60_case_name_pairs_refused": (
        "Student error: product names that differ only in letter case are refused as duplicates.",
        "        if name in seen:\n",
        "        if name.casefold() in {s.casefold() for s in seen}:\n",
    ),
    "m61_actual_profit_at_standard_inputs": (
        "Student error: the actual profit charges the standard input quantity for the output, not the inputs used.",
        "    actual_profit = sum(p[\"actual_units\"] * p[\"actual_price_cents\"] for p in products) - input_price * actual_inputs\n",
        "    actual_profit = sum(p[\"actual_units\"] * p[\"actual_price_cents\"] for p in products) - input_price * standard_inputs\n",
    ),
}

OUT.mkdir(parents=True, exist_ok=True)
for name, (doc, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    # the first line of the docstring names the student error; the reference docstring follows
    head, rest = body.split('"""', 2)[0], body.split('"""', 2)[1:]
    text = f'"""{doc}\n\n' + rest[0].split("\n", 1)[0].lstrip() + "\n" + rest[0].split("\n", 1)[1] + '"""' + rest[1]
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
