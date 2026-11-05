"""Round-7 student-error mutants for LX1-c: each is a copy of a lab twin with one edit. Asserts each edit applies once."""
import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE7-LX1-c")
L1 = (ROOT / "tests/labs/LX1/lab-LX1-project-1.py").read_text(encoding="utf-8")
L2 = (ROOT / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
L3 = (ROOT / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")
M = ROOT / "ledgers/LX1/mutants"

def make(name, src, old, new):
    assert src.count(old) == 1, (name, src.count(old), old)
    (M / name).write_text(src.replace(old, new), encoding="utf-8")
    print("wrote", name)

make("lx1c_r7n01_lab3_window_three_starts_one_month_late.py", L3,
     'WINDOW_THREE_FROM = "2025-10"', 'WINDOW_THREE_FROM = "2025-11"')
make("lx1c_r7n02_lab3_window_three_population_sd.py", L3,
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / n)")
make("lx1c_r7n03_lab3_difference_sign_flipped.py", L3,
     "difference = show(100 * (sd_one - sd_two), 2)", "difference = show(100 * (sd_two - sd_one), 2)")
make("lx1c_r7n04_lab2_burden_missing_parenthesis.py", L2,
     "    return ___" if False else "    return 100 * (start_price / end_price - 1)",
     "    return 100 * (start_price / end_price) - 1")
make("lx1c_r7n05_lab1_real_debt_multiplied_by_price.py", L1,
     "    return Fraction(nominal_cents) / price_level", "    return Fraction(nominal_cents) * price_level")
