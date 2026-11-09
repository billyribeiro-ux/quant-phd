"""Round-16 fixer: writes ten single-change student-error mutants of the FIXED reference into ledgers/M7/mutants/.
Each replacement must match exactly once in the reference (asserted). Run from the repository root:
.venv/bin/python ledgers/M7/scripts/M7-d-r16/make_r16_mutants.py"""
import pathlib

ROOT = pathlib.Path.cwd()
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
HEAD = '"""Reference solution'
assert REF.count(HEAD) == 1

MUTANTS = [
    ("r16_01_start_row_slack_up_to_tolerance_admitted",
     "a row whose slack is up to the starting tolerance is admitted to the initial working set",
     "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) == 0 and",
     "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) <= TOL and"),
    ("r16_02_start_used_without_snapping",
     "the starting portfolio is used as it is, so a bound it breaks by up to the tolerance stays broken",
     "    x = _snapped_start(problem)\n", "    x = list(problem.w0)\n"),
    ("r16_03_lower_start_not_snapped_up",
     "a weight below its lower bound at the start is left below the bound",
     "    x = [min(max(problem.w0[i], problem.lower[i]), problem.upper[i]) for i in range(n)]\n",
     "    x = [min(problem.w0[i], problem.upper[i]) for i in range(n)]\n"),
    ("r16_04_sector_excess_taken_from_first_member",
     "a sector's excess over its cap is taken from its first member alone, whatever that member's room",
     "        for i in members:\n            x[i] -= excess * (x[i] - problem.lower[i]) / room\n",
     "        x[members[0]] -= excess\n"),
    ("r16_05_sector_excess_left_in_place",
     "a sector that breaks its cap by up to the tolerance is not moved back onto the cap",
     "        for i in members:\n            x[i] -= excess * (x[i] - problem.lower[i]) / room\n",
     "        for i in members:\n            x[i] -= 0 * excess\n"),
    ("r16_06_snap_taken_beyond_the_turnover_limit",
     "the snapped start is used even when it moves the portfolio further from w0 than the turnover limit",
     "    return x if moved <= problem.tau else list(problem.w0)\n",
     "    return x\n"),
    ("r16_07_starting_tolerance_one_millionth",
     "the starting portfolio is checked to one millionth instead of one billionth",
     "TOL = Fraction(1, 10**9)", "TOL = Fraction(1, 10**6)"),
    ("r16_08_turnover_row_loosened_by_tolerance",
     "the turnover limit is loosened by the starting tolerance in the sign constraints",
     "problem.tau + _dot(a, problem.w0), (\"turn\", signs))",
     "problem.tau + TOL + _dot(a, problem.w0), (\"turn\", signs))"),
    ("r16_09_sector_start_cap_check_loosened_to_1e-8",
     "the starting sector weight is checked against its cap to 1e-8 instead of 1e-9",
     "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
     "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + Fraction(1, 10**8):"),
    ("r16_10_bound_start_check_loosened_to_1e-8",
     "the starting weight is checked against its bounds to 1e-8 instead of 1e-9",
     "    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
     "    if any(w0[i] < lower[i] - Fraction(1, 10**8) or w0[i] > upper[i] + Fraction(1, 10**8) for i in range(n)):"),
]

for name, desc, old, new in MUTANTS:
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new, 1)
    head = f'"""Student error ({name[:3]}): {desc}.\n\nReference solution'
    text = text.replace(HEAD, head, 1)
    (ROOT / "ledgers/M7/mutants" / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
