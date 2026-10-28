"""Generate round-17 AC4-c mutants and alternatives from the committed twins.

Usage: python3 -I make_mutants.py <checkout>
Each entry: (file name, page twin, [(old, new), ...]). Every old string must occur exactly once.
"""
import os
import sys

checkout = sys.argv[1]
out_dir = os.path.join(checkout, "ledgers/AC4/mutants/AC4-c-r17")
os.makedirs(out_dir, exist_ok=True)
T5 = os.path.join(checkout, "tests/labs/AC4/lab-AC4-L05-1.py")
T6 = os.path.join(checkout, "tests/labs/AC4/lab-AC4-L06-1.py")

MUT = [
    ("ne01_L06_efficiency_only_product_B.py", T6, [
        ("efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)",
         "efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products[1:])"),
    ]),
    ("ne02_L06_unweighted_average_contribution.py", T6, [
        ("cm_bar = Fraction(sum(contribution_per_unit(p) * p.units_budget for p in products), q_b)",
         "cm_bar = Fraction(sum(contribution_per_unit(p) for p in products), len(products))"),
    ]),
    ("ne03_L06_operating_variance_fixed_sign.py", T6, [
        ("print(f\"operating_profit_variance {result['total'] + (FIXED_BUDGET - FIXED_ACTUAL)}\")",
         "print(f\"operating_profit_variance {result['total'] - (FIXED_BUDGET - FIXED_ACTUAL)}\")"),
    ]),
    ("ne04_L05_flexed_fixed_at_actual.py", T5, [
        ("return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)",
         "return Totals(revenue, material, contribution, FIXED_ACTUAL, contribution - FIXED_ACTUAL)"),
    ]),
    ("ne05_L05_flexed_revenue_at_actual_price.py", T5, [
        ("    revenue = sum(p.price_budget * units[p.name] for p in products)",
         "    revenue = sum(p.price_actual * units[p.name] for p in products)"),
    ]),
    ("ne06_L06_efficiency_at_actual_price_equivalent.py", T6, [
        ("efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)",
         "efficiency = -sum(p.price_actual * 0 + MATERIAL_PRICE for p in products[:1]) * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)"),
    ]),
    ("ne07_L06_budget_shares_rounded_to_two_places.py", T6, [
        ("    volume = Fraction(q_a - q_b) * cm_bar",
         "    volume = Fraction(q_a - q_b) * cm_bar\n    _shares = [round(Fraction(p.units_budget, q_b), 2) for p in products]"),
        ("        (Fraction(contribution_per_unit(p)) * (p.units_actual - Fraction(q_a * p.units_budget, q_b)) for p in products),",
         "        (Fraction(contribution_per_unit(p)) * (p.units_actual - q_a * s) for p, s in zip(products, _shares)),"),
    ]),
    ("alt06_L06_mix_by_cross_multiplication.py", T6, [
        ("        (Fraction(contribution_per_unit(p)) * (p.units_actual - Fraction(q_a * p.units_budget, q_b)) for p in products),",
         "        (Fraction(contribution_per_unit(p)) * Fraction(p.units_actual * q_b - q_a * p.units_budget, q_b) for p in products),"),
    ]),
    ("alt07_L05_flexed_via_per_product_contribution.py", T5, [
        ("    revenue = sum(p.price_budget * units[p.name] for p in products)\n    material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)\n    contribution = revenue - material",
         "    revenue = sum(p.price_budget * units[p.name] for p in products)\n    material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)\n    contribution = sum((p.price_budget - p.std_kg * MATERIAL_PRICE) * units[p.name] for p in products)"),
    ]),
    ("alt08_L06_volume_as_sum_of_budget_share_margins.py", T6, [
        ("    volume = Fraction(q_a - q_b) * cm_bar",
         "    volume = sum((Fraction(contribution_per_unit(p)) * (Fraction(q_a * p.units_budget, q_b) - p.units_budget) for p in products), Fraction(0))"),
    ]),
]

for name, twin, subs in MUT:
    src = open(twin, encoding="utf-8").read()
    for old, new in subs:
        n = src.count(old)
        assert n == 1, (name, n, old[:60])
        src = src.replace(old, new)
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
        fh.write(src)
    print("wrote", name)
