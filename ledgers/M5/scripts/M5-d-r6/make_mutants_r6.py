"""Write the three round-6 student-error mutants of the M5 reference solution (slice d, round 6).

Each mutant replaces the reference's module docstring with a one-paragraph description and changes one line.
Usage: make_mutants_r6.py <repo-root>
"""
import sys
from pathlib import Path

REPO = Path(sys.argv[1])
REF = REPO / "course/modules/M/M5/grader/reference.py"
OUT = REPO / "ledgers/M5/mutants"
text = REF.read_text(encoding="utf-8")
head_end = text.index('"""', text.index('"""') + 3) + 3  # end of the module docstring
body = text[head_end:]

MUTANTS = [
    (
        "r6_01_stop_only_when_certified_error_strictly_below_tol.py",
        '"""Student-error mutant (M5 slice d round 6): solve stops only when the certified error is strictly below tol, '
        'so a sweep whose certified error equals tol exactly is not accepted."""',
        [("        if certified <= target:", "        if certified < target:"),
         ('        "converged": certified <= target,', '        "converged": certified < target,')],
    ),
    (
        "r6_02_saving_must_leave_strictly_positive_consumption.py",
        '"""Student-error mutant (M5 slice d round 6): a saving equal to k**alpha, which leaves zero consumption, is '
        "treated as infeasible, so the feasible set is the strict inequality k' < k**alpha.\"\"\"",
        [("            if successor <= available:", "            if successor < available:")],
    ),
    (
        "r6_03_solve_starts_from_the_ones_vector.py",
        '"""Student-error mutant (M5 slice d round 6): solve starts value iteration from the vector of ones instead of '
        'the zero vector the page names as V_0."""',
        [("    values = [0.0] * len(points)", "    values = [1.0] * len(points)")],
    ),
]
for name, doc, edits in MUTANTS:
    new = body
    for old, repl in edits:
        assert new.count(old) == 1, (name, old, new.count(old))
        new = new.replace(old, repl)
    (OUT / name).write_text(doc + new, encoding="utf-8")
    print("wrote", name)
