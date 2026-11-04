"""LX2-c round 4: writes four new student-error mutants of the rung-2 completion lab (ledgers/LX2/mutants/).

Each mutant is the completed solution (tests/labs/LX2/lab-LX2-project-2.py) with one student error introduced.
Every replacement is asserted to apply exactly once, so no mutant is silently identical to the twin.
Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/make_r4_mutants.py
"""

from pathlib import Path

ROOT = Path.cwd()
TWIN = (ROOT / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/LX2/mutants"

MUTANTS = {
    "r4_lab2_hit_rate_horizon_minus_one.py": (
        '"""Hit rate divides the hit count by H - 1 = 5, an off-by-one horizon, instead of H = 6.\n\n',
        [("    hit_rate = Fraction(hits, horizon)", "    hit_rate = Fraction(hits, horizon - 1)")],
    ),
    "r4_lab2_bias_drops_first_month.py": (
        '"""Bias sums the errors of months 14 to 18 only, dropping month 13, then divides by H = 6.\n\n',
        [("    bias = Fraction(sum(errors), horizon)", "    bias = Fraction(sum(errors[1:]), horizon)")],
    ),
    "r4_lab2_forecast_lagged_one_month.py": (
        '"""Forecast uses the previous month index, forecast(t - 1), so each error is one month stale.\n\n',
        [("    return 100 + 2 * t\n", "    return 100 + 2 * (t - 1)\n")],
    ),
    "r4_lab2_hit_rate_three_decimals.py": (
        '"""Hit rate is printed to three decimals (0.667), while the page prints four decimals.\n\n',
        [("decimal_text(hit_rate, 4)", "decimal_text(hit_rate, 3)")],
    ),
}

for name, (doc_first, reps) in MUTANTS.items():
    text = TWIN
    for old, new in reps:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    # the docstring's first line describes the error; the twin's own docstring follows
    text = text.replace('"""LX2 project lab 2', doc_first + "LX2 project lab 2", 1)
    assert text != TWIN
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
