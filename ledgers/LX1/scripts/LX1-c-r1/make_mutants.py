"""Writes student-error mutants of the rung-2 completion solution and the lab-3 check (LX1-c round 1).

Usage (from the checkout root): python3 -I ledgers/LX1/scripts/LX1-c-r1/make_mutants.py
Each mutant is a complete module; its first docstring line names the student error.
"""
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "ledgers" / "LX1" / "mutants"
OUT.mkdir(parents=True, exist_ok=True)
twin = (ROOT / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
lab3 = (ROOT / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")

def mut2(name, description, old, new):
    src = twin.replace(old, new, 1)
    assert src != twin, name
    lines = src.split("\n")
    # first docstring line describes the error
    head = lines[0]
    assert head.startswith('"""'), head
    lines[0] = f'"""{description}. ' + head[3:]
    (OUT / f"{name}.py").write_text("\n".join(lines), encoding="utf-8")

mut2("lx1c_m01_rung2_real_value_without_division",
     "Student leaves the division out of the real value, so the nominal debt is printed as the real debt",
     "return Fraction(nominal_cents) / price_level" if "return Fraction(nominal_cents) / price_level" in twin else "return ___",
     "return Fraction(nominal_cents)")
mut2("lx1c_m02_rung2_burden_ratio_inverted",
     "Student inverts the burden ratio, using end price over start price",
     "return 100 * (start_price / end_price - 1)", "return 100 * (end_price / start_price - 1)")
mut2("lx1c_m03_rung2_real_value_multiplied",
     "Student multiplies the nominal debt by the price level instead of dividing",
     "return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) * price_level")
mut2("lx1c_m04_rung2_burden_as_ratio_no_percent",
     "Student returns the ratio minus one without the factor 100 of percent",
     "return 100 * (start_price / end_price - 1)", "return start_price / end_price - 1")
mut2("lx1c_m05_rung2_real_value_rounded_before_burden",
     "Student rounds the real value to the cent before computing the burden change from it",
     "return 100 * (start_price / end_price - 1)",
     "return 100 * (Fraction(round_half_up(Fraction(4000000) / start_price)) / Fraction(round_half_up(Fraction(4000000) / end_price)) - 1)")
mut2("lx1c_m06_rung2_start_and_end_swapped_in_real_value",
     "Student uses the first path value for every period's real value",
     "return Fraction(nominal_cents) / price_level", "return Fraction(nominal_cents) / PATH[0]")

# lab-3 student errors (applied to the twin source)
def mut3(name, description, old, new):
    src = lab3.replace(old, new, 1)
    assert src != lab3, name
    lines = src.split("\n")
    assert lines[0].startswith('"""'), lines[0]
    lines[0] = f'"""{description}. ' + lines[0][3:]
    (OUT / f"{name}.py").write_text("\n".join(lines), encoding="utf-8")

mut3("lx1c_m07_lab3_population_sd_denominator_n",
     "Student divides by n rather than n - 1 in the standard deviation",
     "return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / n)")
mut3("lx1c_m08_lab3_window_two_starts_one_month_late",
     "Student starts window two at 2000-02, dropping the 2000-01 change",
     'WINDOW_TWO_FROM = "2000-01"', 'WINDOW_TWO_FROM = "2000-02"')
mut3("lx1c_m09_lab3_simple_return_not_log",
     "Student uses the simple return x_m / x_(m-1) - 1 in place of the log change",
     "return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]",
     "return [(month, float(rate / previous - 1)) for (_, previous), (month, rate) in itertools.pairwise(rows)]")
mut3("lx1c_m10_lab3_blank_cell_skipped",
     "Student skips a blank cell silently instead of failing loud",
     '            if DECIMAL_PATTERN.fullmatch(cell) is None:\n                raise ValueError',
     '            if DECIMAL_PATTERN.fullmatch(cell) is None:\n                continue\n            if False:\n                raise ValueError')
print("wrote", len(list(OUT.glob("lx1c_m*.py"))), "mutants")
