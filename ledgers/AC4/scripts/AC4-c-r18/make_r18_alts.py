"""Write three round 18 alternative correct implementations of the AC4 L05 and L06 twins into
ledgers/AC4/mutants/AC4-c-r18/alts/. Each must print the page's expected block (the runner reports SAME).

Usage: python3 -I make_r18_alts.py <checkout>
"""
import os
import re
import sys

checkout = sys.argv[1]
out_dir = os.path.join(checkout, "ledgers/AC4/mutants/AC4-c-r18/alts")
os.makedirs(out_dir, exist_ok=True)
L06 = open(os.path.join(checkout, "tests/labs/AC4/lab-AC4-L06-1.py"), encoding="utf-8").read()
L05 = open(os.path.join(checkout, "tests/labs/AC4/lab-AC4-L05-1.py"), encoding="utf-8").read()

# A: mix as one scaled-integer sum over Q_b (no per-product fraction), then one division.
mix_old = re.search(r"    mix = sum\(\n.*?\n    \)\n", L06, re.S).group(0)
mix_new = ("    mix = Fraction(\n"
           "        sum(contribution_per_unit(p) * (p.units_actual * q_b - q_a * p.units_budget) for p in products), q_b\n"
           "    )\n")
alt_a = L06.replace(mix_old, mix_new)
assert alt_a != L06
open(os.path.join(out_dir, "alt_r18_a_L06_mix_scaled_integers.py"), "w", encoding="utf-8").write(alt_a)

# B: sales price as revenue difference at budget and actual prices; efficiency from totals of kilograms.
sp_old = "    sales_price = sum((p.price_actual - p.price_budget) * p.units_actual for p in products)\n"
sp_new = ("    sales_price = sum(p.price_actual * p.units_actual for p in products) - "
          "sum(p.price_budget * p.units_actual for p in products)\n")
eff_old = "    efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)\n"
eff_new = ("    efficiency = -MATERIAL_PRICE * (sum(p.kg_actual for p in products) - "
           "sum(p.std_kg * p.units_actual for p in products))\n")
alt_b = L06.replace(sp_old, sp_new).replace(eff_old, eff_new)
assert alt_b.count(sp_new) == 1 and alt_b.count(eff_new) == 1
open(os.path.join(out_dir, "alt_r18_b_L06_price_and_efficiency_totals.py"), "w", encoding="utf-8").write(alt_b)

# C: L05 budget_at computes material from total standard kilograms, then subtracts it from revenue.
c_old = "    material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)\n"
c_new = "    material = MATERIAL_PRICE * sum(p.std_kg * units[p.name] for p in products)\n"
alt_c = L05.replace(c_old, c_new)
assert alt_c.count(c_new) == 1
open(os.path.join(out_dir, "alt_r18_c_L05_material_from_total_kg.py"), "w", encoding="utf-8").write(alt_c)
print("wrote three alternatives")
