"""Round 23 (LX1-c): writes four new student-error mutants of the project lab 3 twin, each a single-line edit,
to ledgers/LX1/mutants/. Usage: python -I make_mutants_r23.py <repo_root>"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "ledgers/LX1/mutants"
lab3 = (root / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")
edits = {
    "lx1c_r23n01_lab3_window_three_one_month_early.py": (
        "# Student error: window three starts at 2025-09 (13 changes), one month before the brief's 2025-10 to 2026-09.\n",
        'WINDOW_THREE_FROM = "2025-10"', 'WINDOW_THREE_FROM = "2025-09"'),
    "lx1c_r23n02_lab3_population_sd_denominator_n.py": (
        "# Student error: the dispersion divides by n (the population formula), not n - 1 (the sample formula).\n",
        "/ (n - 1))", "/ n)"),
    "lx1c_r23n03_lab3_largest_change_as_simple_percent.py": (
        "# Student error: the largest change is printed as a simple percentage change exp(l) - 1, not as the log change.\n",
        "show(100 * biggest, 2)", "show(100 * (math.exp(biggest) - 1), 2)"),
    "lx1c_r23n04_lab3_window_two_excludes_first_change.py": (
        "# Student error: window two keeps only the changes strictly after 2000-01 (the first change, 2000-01, is dropped).\n",
        "item[0] >= WINDOW_TWO_FROM", "item[0] > WINDOW_TWO_FROM"),
}
for name, (header, old, new) in edits.items():
    assert lab3.count(old) == 1, (name, lab3.count(old))
    (out / name).write_text(header + lab3.replace(old, new), encoding="utf-8")
    print("wrote", name)
