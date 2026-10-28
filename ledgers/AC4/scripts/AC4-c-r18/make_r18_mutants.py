"""Write the round 18 student-error mutants of the AC4 L05 and L06 twins into ledgers/AC4/mutants/AC4-c-r18/.

Usage: python3 -I make_r18_mutants.py <checkout>. Each mutant is a one-line change; the script asserts the
target text occurs exactly once, so a silent no-op cannot pass as a mutant.
"""
import os
import sys

checkout = sys.argv[1]
out_dir = os.path.join(checkout, "ledgers/AC4/mutants/AC4-c-r18")
os.makedirs(out_dir, exist_ok=True)
L06 = open(os.path.join(checkout, "tests/labs/AC4/lab-AC4-L06-1.py"), encoding="utf-8").read()
L05 = open(os.path.join(checkout, "tests/labs/AC4/lab-AC4-L05-1.py"), encoding="utf-8").read()

mutants = {
    # Mix contributions valued at actual prices (CM_act = p_a,i - s_i*pi) instead of budget prices.
    "r18_m01_L06_mix_contribution_at_actual_price.py": (L06, "(Fraction(contribution_per_unit(p)) * (p.units_actual",
        "(Fraction(p.price_actual - p.std_kg * MATERIAL_PRICE) * (p.units_actual"),
    # Volume variance uses the actual average contribution per unit (actual contribution / actual units).
    "r18_m02_L06_volume_at_actual_average_contribution.py": (L06, "volume = Fraction(q_a - q_b) * cm_bar",
        "volume = Fraction(q_a - q_b) * Fraction(sum(p.price_actual * p.units_actual - MATERIAL_PRICE * p.kg_actual for p in products), q_a)"),
    # Sales price variance sign reversed (budget minus actual price).
    "r18_m03_L06_sales_price_sign_reversed.py": (L06, "sales_price = sum((p.price_actual - p.price_budget) * p.units_actual for p in products)",
        "sales_price = sum((p.price_budget - p.price_actual) * p.units_actual for p in products)"),
    # Operating-profit variance printed without the fixed-cost variance (contribution variance only).
    "r18_m04_L06_operating_variance_omits_fixed.py": (L06, "print(f\"operating_profit_variance {result['total'] + (FIXED_BUDGET - FIXED_ACTUAL)}\")",
        "print(f\"operating_profit_variance {result['total']}\")"),
    # Master budget fixed overhead taken from the actual amount (510,000) rather than the budget (500,000).
    "r18_m05_L05_master_fixed_at_actual.py": (L05, "    return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)",
        "    return Totals(revenue, material, contribution, FIXED_ACTUAL, contribution - FIXED_ACTUAL)"),
    # Equivalent on Lab 1: integer floor of the mix-share allowance (1150*600//1000 and 1150*400//1000 are exact).
    "r18_m06_L06_allowance_floor_equivalent.py": (L06, "Fraction(q_a * p.units_budget, q_b)",
        "Fraction((q_a * p.units_budget) // q_b)"),
}
for name, (base, old, new) in mutants.items():
    assert base.count(old) == 1, (name, base.count(old))
    open(os.path.join(out_dir, name), "w", encoding="utf-8").write(base.replace(old, new))
    print("wrote", name)
