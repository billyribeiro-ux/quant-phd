"""Round 23 new student-error mutants and correct alternatives for AC4 slice c (L05 and L06 lab twins).

Usage: make_r23_mutants.py <checkout>. Each replacement must match exactly once, else the script fails.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
out_dir = root / "ledgers/AC4/mutants/AC4-c-r23"
alt_dir = out_dir / "alts"
alt_dir.mkdir(parents=True, exist_ok=True)
L05 = (root / "tests/labs/AC4/lab-AC4-L05-1.py").read_text(encoding="utf-8")
L06 = (root / "tests/labs/AC4/lab-AC4-L06-1.py").read_text(encoding="utf-8")


def mutate(src: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        n = src.count(old)
        assert n == 1, (old, n)
        src = src.replace(old, new)
    return src


mutants = {
    # student adds the fixed-cost variance into the contribution total
    "r23_m01_L06_total_contribution_takes_fixed_gap.py": mutate(
        L06,
        [("    total = actual_contribution - budget_contribution\n",
          "    total = actual_contribution - budget_contribution - (FIXED_BUDGET - FIXED_ACTUAL)\n")],
    ),
    # student weights the sales price variance by budget units instead of actual units
    "r23_m02_L06_sales_price_at_budget_units.py": mutate(
        L06,
        [("(p.price_actual - p.price_budget) * p.units_actual for p in products}",
          "(p.price_actual - p.price_budget) * p.units_budget for p in products}")],
    ),
    # student uses the budget units of each product as the mix base, not Q_a times the budget share
    "r23_m03_L06_mix_base_is_budget_units.py": mutate(
        L06,
        [("Fraction(q_a * p.units_budget, q_b)", "Fraction(p.units_budget, 1)")],
    ),
    # student flexes fixed overhead with volume in the L05 flexed budget
    "r23_m04_L05_fixed_overhead_flexes_with_units.py": mutate(
        L05,
        [("    return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)",
          "    fixed = FIXED_BUDGET * sum(units.values()) // sum(p.units_budget for p in products)\n"
          "    return Totals(revenue, material, contribution, fixed, contribution - fixed)")],
    ),
    # student reverses the sign of the sales mix variance
    "r23_m05_L06_mix_sign_reversed_in_sum.py": mutate(
        L06,
        [("    out = {\n        \"sales_price\": sales_price,\n        \"sales_volume\": whole_cents(volume, \"sales volume variance\"),\n        \"sales_mix\": whole_cents(mix, \"sales mix variance\"),",
          "    out = {\n        \"sales_price\": sales_price,\n        \"sales_volume\": whole_cents(volume, \"sales volume variance\"),\n        \"sales_mix\": -whole_cents(mix, \"sales mix variance\"),")],
    ),
    # student computes the L05 actual revenue at standard price
    "r23_m06_L05_actual_revenue_at_budget_price.py": mutate(
        L05,
        [("    revenue = sum(p.price_actual * p.units_actual for p in products)",
          "    revenue = sum(p.price_budget * p.units_actual for p in products)")],
    ),
}

# correct alternatives: must print exactly the baseline output
alts = {
    # mix written as sum of CM_i q_a,i minus Q_a times CMbar_b (valid algebra)
    "alt_r23_a_L06_mix_as_cm_sum_minus_average.py": mutate(
        L06,
        [("    mix = sum(\n        (Fraction(contribution_per_unit(p)) * (p.units_actual - Fraction(q_a * p.units_budget, q_b)) for p in products),\n        Fraction(0),\n    )",
          "    mix = sum(Fraction(contribution_per_unit(p) * p.units_actual) for p in products) - q_a * cm_bar")],
    ),
    # L05 budget total computed per product and then summed (same numbers)
    "alt_r23_b_L05_budget_totals_per_product.py": mutate(
        L05,
        [("    revenue = sum(p.price_budget * units[p.name] for p in products)\n    material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)\n    contribution = revenue - material\n    return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)",
          "    rows = [(p.price_budget * units[p.name], p.std_kg * MATERIAL_PRICE * units[p.name]) for p in products]\n    revenue = sum(r for r, _ in rows)\n    material = sum(m for _, m in rows)\n    contribution = revenue - material\n    return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)")],
    ),
}

for name, src in mutants.items():
    (out_dir / name).write_text(src, encoding="utf-8")
for name, src in alts.items():
    (alt_dir / name).write_text(src, encoding="utf-8")
print("wrote", len(mutants), "mutants and", len(alts), "alternatives")
