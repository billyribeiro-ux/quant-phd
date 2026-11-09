"""Round 21 (LX1-c): writes four new student-error mutants, each a single-line edit of the twin
tests/labs/LX1/lab-LX1-project-{1,3}.py, to ledgers/LX1/mutants/. Usage: python -I make_mutants_r21.py <repo_root>"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "ledgers/LX1/mutants"
lab3 = (root / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")
lab1 = (root / "tests/labs/LX1/lab-LX1-project-1.py").read_text(encoding="utf-8")

edits = {
    "lx1c_r21n01_lab3_ratio_from_printed_sds.py": (
        lab3,
        "# Student error: the window ratio is computed from the two printed dispersions (2.47 / 2.79), not the unrounded values.\n",
        'show(sd_two / sd_one, 2)',
        'show(float(show(100 * sd_two, 2)) / float(show(100 * sd_one, 2)), 2)',
    ),
    "lx1c_r21n02_lab3_largest_change_by_value_not_size.py": (
        lab3,
        "# Student error: the 'largest by size' line takes the largest signed change, not the largest in absolute size.\n",
        "biggest_month, biggest = max(window, key=lambda item: abs(item[1]))",
        "biggest_month, biggest = max(window, key=lambda item: item[1])",
    ),
    "lx1c_r21n03_lab3_log_change_sign_reversed.py": (
        lab3,
        "# Student error: the log change is written as ln(S_(m-1) / S_m), with the sign reversed.\n",
        "math.log(float(rate / previous))",
        "-math.log(float(rate / previous))",
    ),
    "lx1c_r21n04_lab1_burden_ends_at_period_four.py": (
        lab1,
        "# Student error: the burden change runs from period 0 to period 4, not to period 5 (an off-by-one end index).\n",
        "change = burden_change_percent(path[0], path[-1])",
        "change = burden_change_percent(path[0], path[-2])",
    ),
}
for name, (base, header, old, new) in edits.items():
    assert base.count(old) == 1, (name, base.count(old))
    text = base.replace(old, new)
    # keep the twin's first docstring line; put the error note as the first line
    (out / name).write_text(header + text, encoding="utf-8")
    print("wrote", name)
