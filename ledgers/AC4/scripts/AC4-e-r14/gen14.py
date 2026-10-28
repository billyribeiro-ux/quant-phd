import pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
R = (ROOT / "course/modules/AC/AC4/grader/reference.py").read_text()
M = ROOT / "ledgers/AC4/mutants"
ALT = ROOT / "ledgers/AC4/scripts/AC4-e-r14/alts"
ALT.mkdir(parents=True, exist_ok=True)
def build(src, doc, pairs):
    for old, new in pairs:
        assert src.count(old) == 1, (doc[:40], old[:70], src.count(old))
        src = src.replace(old, new)
    body = src.split('"""', 2)[2].lstrip("\n")
    return f'"""{doc}"""\n' + body
muts = {
 "r14e_01_fixed_overhead_scales_with_volume": (
   "Student error: the flexed budget scales the fixed overhead with the actual volume, so the flexed profit subtracts a volume-proportional share of the fixed overhead.",
   [('    return {\n        "units": total,\n        "revenue_cents": revenue,\n        "variable_cost_cents": variable,\n        "fixed_cost_cents": fixed,\n        "profit_cents": revenue - variable - fixed,\n    }',
     '    flexed_fixed = _nearest_cent(Fraction(total * fixed, budget_units))\n    return {\n        "units": total,\n        "revenue_cents": revenue,\n        "variable_cost_cents": variable,\n        "fixed_cost_cents": flexed_fixed,\n        "profit_cents": revenue - variable - flexed_fixed,\n    }')]),
 "r14e_02_efficiency_standard_on_budget_units": (
   "Student error: the efficiency variance takes the standard input allowance on the budgeted units instead of the actual units.",
   [('    standard_inputs = sum(p["standard_inputs_per_unit"] * p["actual_units"] for p in products)',
     '    standard_inputs = sum(p["standard_inputs_per_unit"] * p["budget_units"] for p in products)')]),
 "r14e_03_price_variance_on_budget_units": (
   "Student error: the sales price variance multiplies each price difference by the budgeted units instead of the actual units.",
   [('    sales_price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["actual_units"] for p in products)',
     '    sales_price = sum((p["actual_price_cents"] - p["budget_price_cents"]) * p["budget_units"] for p in products)')]),
 "r14e_04_flexed_revenue_halves_down": (
   "Student error: the flexed revenue rounds exact half cents down, not up, so a flexed amount that ends in one half is taken to the lower cent.",
   [("    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units))",
     "    revenue = _nearest_cent(Fraction(total * budget_revenue, budget_units) - Fraction(1, 2**40))")]),
}
for name, (doc, pairs) in muts.items():
    (M / f"{name}.py").write_text(build(R, doc, pairs))
# Correct alternatives: the sales mix as the residual of the total (an exact identity), and the
# same engine with the exact-half rule written as floor(x + 1/2) through a separate Fraction helper.
alt_a = build(R, "Alternative 14a (correct): the sales mix is taken as the residual of the total after the other three variances, which equals the page's definition exactly.",
  [("    sales_mix = actual_mix_contribution - flexed\n", "    sales_mix = None\n"),
   ('        "total": actual_profit - master,\n    }',
    '        "total": actual_profit - master,\n    }'.replace('"total"', '"total"'))])
alt_a = alt_a.replace('    return {\n        "sales_price": sales_price,',
  '    total_variance = actual_profit - master\n    residual = total_variance - sales_price - sales_volume - efficiency\n    return {\n        "sales_price": sales_price,', 1)
alt_a = alt_a.replace('        "sales_mix": sales_mix,', '        "sales_mix": residual,', 1)
(ALT / "alt14_a_mix_as_residual.py").write_text(alt_a)
alt_b = build(R, "Alternative 14b (correct): the nearest cent is floor(x + 1/2) computed by integer division with the remainder, halves up.",
  [("    return (2 * amount.numerator + amount.denominator) // (2 * amount.denominator)",
    "    q, r = divmod(amount.numerator, amount.denominator)\n    return q + (1 if 2 * r >= amount.denominator else 0)")])
(ALT / "alt14_b_divmod_nearest.py").write_text(alt_b)
print("ok")
