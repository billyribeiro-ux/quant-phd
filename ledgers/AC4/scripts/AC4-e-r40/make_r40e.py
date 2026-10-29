import pathlib
REF = pathlib.Path("/tmp/verify40-AC4-e/course/modules/AC/AC4/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/verify40-AC4-e/ledgers/AC4/mutants")
MUTANTS = {
    "r40e_01_flexed_variable_cost_truncated_revenue_rounded.py": (
        "Student error: the flexed variable cost is truncated toward zero, while the flexed revenue is rounded to the nearest cent.",
        '    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))',
        '    variable = (total * budget_variable) // budget_units',
    ),
    "r40e_02_efficiency_standard_on_budgeted_units.py": (
        "Student error: the efficiency variance takes the standard inputs of the budgeted units, not of the units sold.",
        '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)',
        '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["budget_units"] for p in products)',
    ),
    "r40e_03_master_profit_forgets_fixed_overhead.py": (
        "Student error: the master budget profit is revenue less variable cost, and the fixed overhead is left out of it.",
        '        "profit_cents": total_revenue - total_variable - fixed,',
        '        "profit_cents": total_revenue - total_variable,',
    ),
    "r40e_04_no_budgeted_units_check_missing.py": (
        "Student error: a case with no budgeted units is not refused, so the flexed budget divides by zero.",
        '    if sum(p["budget_units"] for p in products) == 0:\n        raise ValueError("the master budget has no budgeted units, so no budgeted mix exists")\n',
        '',
    ),
}
for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    first_end = REF.index('"""', 3) + 3
    body = REF[first_end:]
    text = '"""' + doc + '\n\nA full module like reference.py, with one student error.\n"""' + body
    text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
