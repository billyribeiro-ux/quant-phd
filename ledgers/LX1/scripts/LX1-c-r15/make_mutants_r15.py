"""Round-15 verifier: writes three new student-error lab mutants from the twins (ledgers/LX1/mutants/r15n*.py).
Argument 1 is the checkout root. Each replacement asserts it matches exactly once in the twin."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
M = root / "ledgers/LX1/mutants"


def make(src_lab, out_name, first_line, old, new):
    text = (root / f"tests/labs/LX1/{src_lab}.py").read_text(encoding="utf-8")
    assert text.count(old) == 1, (out_name, text.count(old))
    text = text.replace(old, new)
    lines = text.split("\n", 1)
    assert lines[0].startswith('"""')
    text = f'"""{first_line}\n' + lines[0][3:] + ("\n" + lines[1] if len(lines) > 1 else "")
    (M / out_name).write_text(text, encoding="utf-8")
    print("wrote", out_name)


make("lab-LX1-project-1", "r15n01_lab1_burden_percent_of_end_real_value.py",
     "LX1 project lab 1 (rung 1). Student error: the burden change is taken as a percent of the period-5 real value, not of the period-0 real value.",
     "    change = burden_change_percent(path[0], path[-1])",
     "    change = 100 * (real_debt_cents(NOMINAL_DEBT_CENTS, path[0]) - real_debt_cents(NOMINAL_DEBT_CENTS, path[-1])) / real_debt_cents(NOMINAL_DEBT_CENTS, path[-1])")

make("lab-LX1-project-3", "r15n02_lab3_window_three_year_on_year_changes.py",
     "LX1 project lab 3 (rung 3). Student error: the window-three changes are twelve-month (year-on-year) log changes, not monthly ones.",
     "    window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]",
     "    window_three = [(rows[i][0], math.log(float(rows[i][1] / rows[i - 12][1]))) for i in range(len(rows) - 12, len(rows))]")

make("lab-LX1-project-3", "r15n03_lab3_two_pass_sd_scaled_by_sqrt_n_minus_one_over_n.py",
     "LX1 project lab 3 (rung 3). Student error: the two-pass standard deviation is scaled by sqrt((n - 1) / n), the factor for the wrong direction.",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1)) * math.sqrt((n - 1) / n)")
