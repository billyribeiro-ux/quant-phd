import pathlib
REF = pathlib.Path("/tmp/verify42-AC4-e/course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/verify42-AC4-e/ledgers/AC4/mutants")
MUTANTS = {
    "r42e_01_total_is_sum_of_the_four_variances.py": (
        "Student error: the total variance is set to the sum of the four variances, so the reconciliation holds by construction.",
        '        "total": actual_profit - master,',
        '        "total": sales_price + sales_volume + sales_mix + efficiency,',
    ),
    "r42e_02_master_budget_key_named_without_cents.py": (
        "Student error: the master budget returns the total revenue under the key total_revenue, without the _cents suffix the page names.",
        '        "total_revenue_cents": total_revenue,',
        '        "total_revenue": total_revenue,',
    ),
    "r42e_03_flexed_variable_cost_is_actual_input_cost.py": (
        "Student error: the flexed variable cost is the input price times the input units actually used, not the budgeted variable cost per unit at the flexed volume.",
        '    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))',
        '    variable = input_price * _nonnegative(case["actual_inputs_used"], "actual_inputs_used")',
    ),
}
for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    first_end = REF.index('"""', 3) + 3
    body = REF[first_end:]
    text = '"""' + doc + '\n\nA full module like reference.py, with one student error.\n"""' + body
    text = text.replace(old, new)
    assert text != REF
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)

MUTANTS2 = {
    "r42e_04_standard_inputs_summed_over_products_times_total.py": (
        "Student error: the standard input count is the sum of each product's standard inputs per unit, times the total units sold, instead of each product's own standard times its own units.",
        '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)',
        '    standard_inputs = sum(p["standard_inputs_per_unit"] for p in products) * actual_total',
    ),
    "r42e_05_favourable_efficiency_refused.py": (
        "Student error: a case whose actual input use is below the standard for the output is refused, so the efficiency variance is only ever unfavourable.",
        '    actual_profit = sum(p["actual_units"] * p["actual_price_cents"] for p in products) - input_price * actual_inputs',
        '    if actual_inputs < sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products):\n        raise ValueError("the input use is below the standard")\n    actual_profit = sum(p["actual_units"] * p["actual_price_cents"] for p in products) - input_price * actual_inputs',
    ),
}
for name, (doc, old, new) in MUTANTS2.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    first_end = REF.index('"""', 3) + 3
    body = REF[first_end:]
    text = '"""' + doc + '\n\nA full module like reference.py, with one student error.\n"""' + body
    text = text.replace(old, new)
    assert text != REF
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
