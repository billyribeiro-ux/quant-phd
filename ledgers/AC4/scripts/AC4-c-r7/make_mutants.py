import pathlib, sys
src6 = pathlib.Path("/tmp/verify7-AC4-c/tests/labs/AC4/lab-AC4-L06-1.py").read_text()
src5 = pathlib.Path("/tmp/verify7-AC4-c/tests/labs/AC4/lab-AC4-L05-1.py").read_text()
out = pathlib.Path("/tmp/verify7-AC4-c/ledgers/AC4/mutants/AC4-c-r7")
muts = {
 "n01_L06_mix_uses_budget_total": (src6, "(p.units_actual - Fraction(q_a * p.units_budget, q_b))", "(p.units_actual - Fraction(q_b * p.units_budget, q_b))"),
 "n02_L06_efficiency_allowance_on_budget_units": (src6, "efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_actual for p in products)", "efficiency = -MATERIAL_PRICE * sum(p.kg_actual - p.std_kg * p.units_budget for p in products)"),
 "n03_L06_volume_uses_actual_mix_average": (src6, "volume = Fraction(q_a - q_b) * cm_bar", "volume = Fraction(q_a - q_b) * Fraction(sum(contribution_per_unit(p) * p.units_actual for p in products), q_a)"),
 "n04_L05_fixed_overhead_flexes_with_units": (src5, "return Totals(revenue, material, contribution, FIXED_BUDGET, contribution - FIXED_BUDGET)", "fixed = FIXED_BUDGET * sum(units.values()) // sum(p.units_budget for p in products)\n    return Totals(revenue, material, contribution, fixed, contribution - fixed)"),
 "n05_L05_flexed_uses_actual_kg": (src5, "material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products)", "material = sum(p.std_kg * MATERIAL_PRICE * units[p.name] for p in products) if units == {p.name: p.units_budget for p in products} else sum(p.kg_actual * MATERIAL_PRICE * units[p.name] // p.units_actual for p in products)"),
}
for name, (src, old, new) in muts.items():
    assert src.count(old) == 1, (name, src.count(old))
    (out / f"{name}.py").write_text(src.replace(old, new))
    print("wrote", name)
