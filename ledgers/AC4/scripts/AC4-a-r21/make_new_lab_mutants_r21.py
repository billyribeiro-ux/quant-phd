"""Round 21: writes 6 new student-error mutants of the AC4-a lab twins into ledgers/AC4/mutants/AC4-a-r21/.
Each replacement must match exactly once in its twin, or the script fails loud."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
out = root / "ledgers/AC4/mutants/AC4-a-r21"
out.mkdir(parents=True, exist_ok=True)
SPECS = [
    ("L01", "L01_p01_high_chosen_by_cost",
     "high = max(range(len(rows)), key=lambda i: (rows[i][0], -i))",
     "high = max(range(len(rows)), key=lambda i: (rows[i][1], -i))"),
    ("L01", "L01_p02_residual_against_generator_line",
     "residual = Fraction(cost) - (fixed + variable * hours)",
     "residual = Fraction(cost) - (GEN_FIXED_CENTS + GEN_VARIABLE_CENTS * hours)"),
    ("L02", "L02_p01_margin_of_safety_from_first_break_even",
     "upper = break_even(FIXED_CENTS + STEP_CENTS, margin)",
     "upper = break_even(FIXED_CENTS, margin)"),
    ("L02", "L02_p02_planned_income_ignores_step",
     "planned = operating_income(PLANNED_UNITS)",
     "planned = (PRICE_CENTS - VARIABLE_CENTS) * PLANNED_UNITS - FIXED_CENTS"),
    ("L02", "L02_p03_first_whole_unit_by_round",
     "first_whole = -(-first.numerator // first.denominator)",
     "first_whole = round(float(first))"),
    ("L02", "L02_p04_zero_counted_as_loss",
     "loss = operating_income(units) < 0",
     "loss = operating_income(units) <= 0"),
]
for lab, name, old, new in SPECS:
    src = (root / f"tests/labs/AC4/lab-AC4-{lab}-1.py").read_text(encoding="utf-8")
    assert src.count(old) == 1, (name, src.count(old))
    (out / f"{name}.py").write_text(src.replace(old, new), encoding="utf-8")
    print("wrote", name)
