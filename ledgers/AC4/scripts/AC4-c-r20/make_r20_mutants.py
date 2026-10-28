"""Write round-20 student-error mutants and alternative correct implementations for AC4 slice c.

Each file is a copy of a twin with one edit; the edit is asserted to match exactly once.
Usage: make_r20_mutants.py <checkout>
"""
from __future__ import annotations

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
L05 = (root / "tests/labs/AC4/lab-AC4-L05-1.py").read_text()
L06 = (root / "tests/labs/AC4/lab-AC4-L06-1.py").read_text()
out = root / "ledgers/AC4/mutants/AC4-c-r20"
(out / "alts").mkdir(parents=True, exist_ok=True)


def edit(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (src.count(old), old[:60])
    return src.replace(old, new)


mutants = {
    # student error: the mix term uses each product's actual-price contribution margin, not the budget margin
    "r20_m01_L06_mix_margin_at_actual_price.py": edit(
        L06,
        "(Fraction(contribution_per_unit(p)) * (p.units_actual",
        "(Fraction(p.price_actual - p.std_kg * MATERIAL_PRICE) * (p.units_actual",
    ),
    # student error: actual material cost priced at standard kilograms instead of actual kilograms
    "r20_m02_L05_actual_material_at_standard_kg.py": edit(
        L05,
        "    material = MATERIAL_PRICE * sum(p.kg_actual for p in products)",
        "    material = MATERIAL_PRICE * sum(p.std_kg * p.units_actual for p in products)",
    ),
    # student error: the total contribution variance takes the budget side from actual units
    "r20_m03_L06_budget_contribution_from_actual_units.py": edit(
        L06,
        "    budget_contribution = sum(contribution_per_unit(p) * p.units_budget for p in products)",
        "    budget_contribution = sum(contribution_per_unit(p) * p.units_actual for p in products)",
    ),
}
for name, text in mutants.items():
    (out / name).write_text(text)

alts = {
    # correct: mix as sum of CM_i q_a,i minus Q_a times the budget average contribution (exact fractions)
    "alts/alt_r20_a_L06_mix_as_sum_minus_total_average.py": edit(
        L06,
        "    mix = sum(\n        (Fraction(contribution_per_unit(p)) * (p.units_actual - Fraction(q_a * p.units_budget, q_b)) for p in products),\n        Fraction(0),\n    )",
        "    mix = sum((Fraction(contribution_per_unit(p) * p.units_actual) for p in products), Fraction(0)) - q_a * cm_bar",
    ),
    # correct: efficiency accumulated one product at a time, with the same standard price
    "alts/alt_r20_b_L06_efficiency_loop.py": edit(
        L06,
        "    efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)",
        "    efficiency = 0\n    for p in products:\n        efficiency -= MATERIAL_PRICE * (p.kg_actual - p.std_kg * p.units_actual)",
    ),
    # correct: flexed budget built from budget_at per product units via a dict comprehension, same numbers
    "alts/alt_r20_c_L05_flexed_units_as_budget_share_check.py": edit(
        L05,
        "    actual_units = {p.name: p.units_actual for p in PRODUCTS}",
        "    actual_units = {p.name: int(p.units_actual) for p in PRODUCTS}",
    ),
}
for name, text in alts.items():
    (out / name).write_text(text)
print("wrote", sorted(mutants), sorted(alts))
