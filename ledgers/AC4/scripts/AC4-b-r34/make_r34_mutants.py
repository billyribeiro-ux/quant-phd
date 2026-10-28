"""Write new student-error mutants of the two AC4 lab twins into ledgers/AC4/mutants/AC4-b-r34/.

Each mutant is the committed twin with exactly one student-style edit; the edit is asserted to match once.
"""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
out = root / "ledgers/AC4/mutants/AC4-b-r34"
out.mkdir(parents=True, exist_ok=True)
l03 = (root / "tests/labs/AC4/lab-AC4-L03-1.py").read_text(encoding="utf-8")
l04 = (root / "tests/labs/AC4/lab-AC4-L04-1.py").read_text(encoding="utf-8")

edits = {
    "m_L03_r34_breakeven_adds_scrap.py": (
        l03,
        "breakeven_price = (avoidable_make_cost(base) + base.scrap_value) // base.units",
        "breakeven_price = (avoidable_make_cost(base) - base.scrap_value) // base.units",
    ),
    "m_L03_r34_full_cost_omits_dedicated_fixed.py": (
        l03,
        "        + c.dedicated_fixed // c.units\n    )",
        "    )",
    ),
    "m_L03_r34_sunk_book_value_in_make_cost.py": (
        l03,
        "    return c.units * per_unit + c.dedicated_fixed\n",
        "    return c.units * per_unit + c.dedicated_fixed + c.equipment_book_value\n",
    ),
    "m_L04_r34_sensitivity_keeps_sixty_setups.py": (
        l04,
        'ActivityPool("setups", 4_000_000, (20, 20)),',
        'ActivityPool("setups", 4_000_000, (20, 60)),',
    ),
    "m_L04_r34_cross_subsidy_sign_flipped.py": (
        l04,
        "shift = act[p.name] - vol[p.name]",
        "shift = vol[p.name] - act[p.name]",
    ),
    "m_L04_r34_pool_rate_by_units.py": (
        l04,
        "    rate = exact_rate(pool.cost, sum(pool.driver_counts), pool.name)\n        for product",
        "    rate = exact_rate(pool.cost, sum(p.units for p in products), pool.name)\n        for product",
    ),
}
for name, (src, old, new) in edits.items():
    assert src.count(old) == 1, (name, src.count(old))
    (out / name).write_text(src.replace(old, new), encoding="utf-8")
    print("wrote", name)
