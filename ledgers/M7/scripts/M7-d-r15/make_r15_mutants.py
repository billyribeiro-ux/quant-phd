"""Write three verifier-authored student-error mutants of the M7 reference (round 15). Run from the repository root."""
from pathlib import Path

REF = Path("course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("ledgers/M7/mutants")
SPECS = [
    (
        "r15_01_sector_cap_start_tolerance_1e-8.py",
        "Student error r15_01: the starting sector-cap check uses a tolerance of 1e-8 where the page states 1e-9, so a start 2e-9 above its cap is accepted.",
        "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
        "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + Fraction(1, 10**8):",
    ),
    (
        "r15_02_start_budget_check_tolerance_1e-6.py",
        "Student error r15_02: the starting-portfolio budget check accepts a sum off by up to 1e-6 where the page states 1e-9, so a start whose weights sum to 1 + 2e-9 is accepted.",
        "    if abs(sum(w0, Fraction(0)) - 1) > TOL:",
        "    if abs(sum(w0, Fraction(0)) - 1) > Fraction(1, 10**6):",
    ),
    (
        "r15_03_only_first_sector_cap_checked_at_start.py",
        "Student error r15_03: the starting-portfolio sector-cap loop stops after the first sector, so a start that breaks the cap of a later sector is accepted.",
        "    for k, cap in enumerate(caps):\n        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
        "    for k, cap in enumerate(caps[:1]):\n        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
    ),
]
for name, first_line, old, new in SPECS:
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    # the mutant docstring's first line names the error; the reference's own docstring follows it
    body = body.replace('"""Reference solution', '"""' + first_line + "\n\nReference solution", 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
