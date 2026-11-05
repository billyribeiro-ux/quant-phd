"""Round-11 verifier: writes three new student-error mutants of the project labs (complete modules, one error each)
from the twins under tests/labs/LX1/. Each replacement must match exactly once or the script exits non-zero.
Argument 1 is the checkout root."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
TWIN = root / "tests/labs/LX1"
OUT = root / "ledgers/LX1/mutants"

SPECS = [
    ("lx1c_r11n01_lab3_log10_instead_of_ln.py",
     "lab-LX1-project-3.py",
     "Student takes the base-10 logarithm where the page defines the natural log, so every change and the dispersion "
     "are scaled by 1 / ln(10). LX1 project lab 3 (rung 3 check).",
     [("(month, math.log(float(rate / previous)))", "(month, math.log10(float(rate / previous)))")]),
    ("lx1c_r11n02_lab3_window_three_is_calendar_2025.py",
     "lab-LX1-project-3.py",
     "Student reads the twelve months ending at the last month as calendar 2025, so window three holds 2025-01 to "
     "2025-12 rather than 2025-10 to 2026-09. LX1 project lab 3 (rung 3 check).",
     [("window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]",
       "window_three = [item for item in changes if WINDOW_THREE_FROM <= item[0] < \"2026-01\"]"),
      ("WINDOW_THREE_FROM = \"2025-10\"", "WINDOW_THREE_FROM = \"2025-01\"")]),
    ("lx1c_r11n03_lab3_first_month_counted_as_zero_change.py",
     "lab-LX1-project-3.py",
     "Student adds the first month as a change with a log change of zero, so window one holds 669 changes rather "
     "than 668. LX1 project lab 3 (rung 3 check).",
     [("    changes = log_changes(rows)", "    changes = [(rows[0][0], 0.0)] + log_changes(rows)")]),
]

for name, twin, doc, reps in SPECS:
    text = (TWIN / twin).read_text(encoding="utf-8")
    end = text.index('"""', text.index('"""') + 3) + 3
    body = text[end:]
    for old, new in reps:
        n = body.count(old)
        if n != 1:
            sys.exit(f"{name}: replacement target found {n} times: {old!r}")
        body = body.replace(old, new)
    (OUT / name).write_text(f'"""{doc}"""' + body, encoding="utf-8")
    print("wrote", name)
