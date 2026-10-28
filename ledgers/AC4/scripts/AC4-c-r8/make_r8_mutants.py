"""Generate round-8 student-error mutants (s01-s05) and alternative correct implementations (alt02-alt05).

Run with: python -I <checkout>/ledgers/AC4/scripts/AC4-c-r8/make_r8_mutants.py <checkout>
Each file is a full copy of the twin with one line replaced; every replacement must match exactly once.
"""

import sys
from pathlib import Path

co = Path(sys.argv[1])
src6 = (co / "tests/labs/AC4/lab-AC4-L06-1.py").read_text(encoding="utf-8")
src5 = (co / "tests/labs/AC4/lab-AC4-L05-1.py").read_text(encoding="utf-8")
out = co / "ledgers/AC4/mutants/AC4-c-r8"
out.mkdir(parents=True, exist_ok=True)

MIX = "Fraction(q_a * p.units_budget, q_b)"
VOL = "    volume = Fraction(q_a - q_b) * cm_bar"
EFF = "    efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)"
ACT = "    actual_contribution = sum(p.price_actual * p.units_actual - MATERIAL_PRICE * p.kg_actual for p in products)"
MIXSUM = (
    "    mix = sum(\n"
    "        (Fraction(contribution_per_unit(p)) * (p.units_actual - Fraction(q_a * p.units_budget, q_b)) for p in products),\n"
    "        Fraction(0),\n"
    "    )"
)
CONS = "    sales_price = sum((p.price_actual - p.price_budget) * p.units_actual for p in products)"
FLX = "    flexed = budget_at(PRODUCTS, actual_units)"

L6 = {
    # student-error mutants (new in round 8)
    "s01_L06_mix_share_from_actual_total.py": [(MIX, "Fraction(q_a * p.units_actual, q_a)")],
    "s02_L06_volume_at_actual_mix_margin.py": [
        (VOL, "    volume = Fraction(q_a - q_b) * Fraction(sum(contribution_per_unit(p) * p.units_actual for p in products), q_a)")
    ],
    "s03_L06_efficiency_allowance_on_budget_units.py": [
        (EFF, "    efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_budget for p in products)")
    ],
    "s04_L06_actual_revenue_at_budget_price.py": [
        (ACT, "    actual_contribution = sum(p.price_budget * p.units_actual - MATERIAL_PRICE * p.kg_actual for p in products)")
    ],
    # alternative correct implementations (must survive: same printed output, exit 0)
    "alt02_mix_as_sum_CM_qa_minus_Qa_cmbar.py": [
        (MIXSUM, "    mix = sum((Fraction(contribution_per_unit(p)) * p.units_actual for p in products), Fraction(0)) - Fraction(q_a) * cm_bar")
    ],
    "alt03_mix_float_then_round.py": [
        (
            MIXSUM,
            "    mix = sum((float(contribution_per_unit(p)) * (p.units_actual - q_a * p.units_budget / q_b) for p in products), 0.0)",
        ),
        ('        "sales_mix": whole_cents(mix, "sales mix variance"),', '        "sales_mix": round(mix),'),
    ],
    "alt04_budget_mix_average_per_product_weights.py": [
        (
            "    cm_bar = Fraction(sum(contribution_per_unit(p) * p.units_budget for p in products), q_b)",
            "    cm_bar = sum((Fraction(p.units_budget, q_b) * contribution_per_unit(p) for p in products), Fraction(0))",
        )
    ],
    "alt05_efficiency_per_product_loop.py": [
        (
            EFF,
            "    efficiency = sum(-MATERIAL_PRICE * (p.kg_actual - p.std_kg * p.units_actual) for p in products)",
        )
    ],
}
L5 = {
    "s05_L05_flexed_budget_at_budget_units.py": [
        (FLX, "    flexed = budget_at(PRODUCTS, master_units)")
    ],
}
for name, reps in L6.items():
    text = src6
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(text, encoding="utf-8")
for name, reps in L5.items():
    text = src5
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(text, encoding="utf-8")
print("written", sorted(p.name for p in out.glob("*.py")))
