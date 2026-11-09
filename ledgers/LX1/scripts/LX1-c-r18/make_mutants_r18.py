"""Round-18 LX1-c: writes four new student-error mutants of the Lab 3 twin (verifier-written; not builder code).

Each mutant is the Lab 3 twin with one student error. Every replacement is asserted to apply once.
Usage: python -I make_mutants_r18.py <checkout_root>
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
TWIN = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
OUT = ROOT / "ledgers/LX1/mutants"
src = TWIN.read_text(encoding="utf-8")

MUTANTS = {
    "lx1c_r18n01_lab3_change_uses_next_month_rate_lookahead.py": (
        "Student error: labels each log change with its earlier month but uses the next month's rate (a one-month lookahead), so the window counts shift by one month.",
        [("    return [(month, math.log(float(rate / previous))) for (_, previous), (month, rate) in itertools.pairwise(rows)]",
          "    return [(month, math.log(float(nxt / cur))) for (month, cur), (_, nxt) in itertools.pairwise(rows)]")],
    ),
    "lx1c_r18n02_lab3_difference_of_printed_sds.py": (
        "Student error: takes the window one minus window two difference from the two-decimal printed standard deviations, not from the unrounded ones.",
        [("difference = show(100 * (sd_one - sd_two), 2)",
          "difference = str(Decimal(show(100 * sd_one, 2)) - Decimal(show(100 * sd_two, 2)))")],
    ),
    "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py": (
        "Student error: counts a month as an exact zero change when its log change rounds to zero at four decimal places, so tiny nonzero moves are counted as zero.",
        [("zeros = sum(1 for value in values if value == 0.0)",
          "zeros = sum(1 for value in values if round(value, 4) == 0.0)")],
    ),
    "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py": (
        "Student error: centres window two's squared deviations on the window one mean, a reused variable, so window two's dispersion ratio and difference are wrong.",
        [("    sd_two = window_report(window_two)",
          "    mean_one = math.fsum(c for _, c in window_one) / len(window_one)\n"
          "    window_report(window_two)\n"
          "    sd_two = math.sqrt(math.fsum((c - mean_one) ** 2 for _, c in window_two) / (len(window_two) - 1))")],
    ),
    "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py": (
        "Student error: a blank GBP cell is filled with the previous month's rate, so a missing month is taken as a flat rate and no ValueError is raised.",
        [('        for row in reader:\n            month = row["month"]\n            cell = row.get(column) or ""\n',
          '        previous_cell = ""\n        for row in reader:\n            month = row["month"]\n            cell = row.get(column) or previous_cell\n            previous_cell = cell\n')],
    ),
}

for name, (doc, reps) in MUTANTS.items():
    text = src
    for old, new in reps:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    head = '"""' + doc + "\n\n"
    assert text.startswith('"""LX1 project lab 3')
    text = head + text[3:]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
