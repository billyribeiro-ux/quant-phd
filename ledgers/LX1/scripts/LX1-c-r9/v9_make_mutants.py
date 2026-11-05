"""Round-9 verifier: writes four new student-error mutants of the LX1 project labs into ledgers/LX1/mutants/.
Each is derived from the committed twin by one exact replacement (asserted to match exactly once). The module
docstring is replaced by one line whose first sentence names the error (mutant convention, as in r8n04)."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
twins = root / "tests/labs/LX1"
out = root / "ledgers/LX1/mutants"

SPECS = [
    ("lx1c_r9n01_lab2_real_value_without_division.py", "lab-LX1-project-2",
     "Student omits the division, so every real value equals the nominal debt. LX1 project lab 2 (rung 2 completion).",
     "    return Fraction(nominal_cents) / price_level\n",
     "    return Fraction(nominal_cents)\n"),
    ("lx1c_r9n02_lab3_largest_change_by_min_magnitude.py", "lab-LX1-project-3",
     "Student picks the smallest-magnitude change as the largest. LX1 project lab 3 (rung 3 check).",
     "biggest_month, biggest = max(window, key=lambda item: abs(item[1]))",
     "biggest_month, biggest = min(window, key=lambda item: abs(item[1]))"),
    ("lx1c_r9n03_lab3_gap_allows_one_missing_month.py", "lab-LX1-project-3",
     "Student's continuity test allows one missing month between rows. LX1 project lab 3 (rung 3 check).",
     "        if month_index(current) != month_index(previous) + 1:\n",
     "        if month_index(current) > month_index(previous) + 2:\n"),
    ("lx1c_r9n04_lab3_two_pass_divides_by_n.py", "lab-LX1-project-3",
     "Student's two-pass formula divides by n, so it disagrees with statistics.stdev and the lab must raise. LX1 project lab 3 (rung 3 check).",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))",
     "    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / n)"),
]

for name, lab, first_line, old, new in SPECS:
    text = (twins / f"{lab}.py").read_text(encoding="utf-8")
    start = text.index('"""')
    end = text.index('"""', start + 3) + 3
    body = text[end:]
    assert body.count(old) == 1, (name, body.count(old))
    body = body.replace(old, new)
    mutant = f'"""{first_line}"""' + body
    (out / name).write_text(mutant, encoding="utf-8")
    print("wrote", name)
