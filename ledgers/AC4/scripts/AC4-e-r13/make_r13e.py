import pathlib, sys
R = pathlib.Path(sys.argv[1]).read_text()
M = pathlib.Path(sys.argv[2])
def mk(name, doc, pairs):
    src = R
    for old, new in pairs:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    (M / f"{name}.py").write_text(f'"""{doc}"""\n' + src.split('"""', 2)[2].lstrip("\n"))
mk("r13e_01_flexed_variable_cost_rounds_up_always",
   "Student error: the flexed variable cost is rounded up to the next cent whatever its fraction, not to the nearest cent.",
   [("    variable = _nearest_cent(Fraction(total * budget_variable, budget_units))",
     "    variable = -(-(total * budget_variable) // budget_units)")])
mk("r13e_02_products_not_a_list_is_a_type_error",
   "Student error: a products field that is not a list (None, a number, a mapping) raises TypeError, not ValueError.",
   [('    if not isinstance(raw, list) or not raw:\n        raise ValueError("the case needs at least one product")',
     '    if not isinstance(raw, list):\n        raise TypeError("products must be a list")\n    if not raw:\n        raise ValueError("the case needs at least one product")')])
mk("r13e_03_mix_rounds_each_product_term",
   "Student error: each product's actual-mix margin term is rounded to a whole cent before the terms are summed.",
   [("    actual_mix_contribution = (\n        sum(\n            p[\"actual_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price)\n            for p in products\n        )\n        - fixed\n    )",
     "    actual_mix_contribution = (\n        sum(\n            _nearest_cent(Fraction(p[\"actual_units\"] * (p[\"budget_price_cents\"] - p[\"standard_inputs_per_unit\"] * input_price) * 2, 2))\n            for p in products\n        )\n        - fixed\n    )")])
mk("r13e_04_flexible_budget_skips_name_checks",
   "Student error: flexible_budget does not check product names, so an empty or duplicate name is accepted there.",
   [("    input_price, fixed, _, products = _case(case)\n    total = _nonnegative(actual_units, \"actual_units\")",
     "    input_price, fixed, _, products = _case(case)\n    total = _nonnegative(actual_units, \"actual_units\")\n    if any(not p[\"name\"] for p in products):\n        products = [dict(p) for p in products]")])
print("ok")
