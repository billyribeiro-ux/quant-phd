"""Writes three new student-error mutants of the E3 reference engine into ledgers/E3/mutants/ (round 5, slice d).

Each mutant is the full reference module with one edit; the first docstring line names the error.
Run from the checkout: python3 ledgers/E3/scripts/E3-d-r5/make_r5_mutants.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

EDITS = {
    "r5_mixed_check_counts_only_the_first_lottery": (
        "Identification check looks only at lottery A of each response, so a set whose only mixed lottery is B is refused.",
        "    if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):",
        "    if not any(_mixed(a, pa) for a, pa, b, pb, _ in parsed):",
    ),
    "r5_newton_stops_at_gradient_1e_2": (
        "Newton search stops once the largest gradient component is below 1e-2 instead of 1e-7.",
        "        if max(abs(g) for g in grad) < 1e-7:",
        "        if max(abs(g) for g in grad) < 1e-2:",
    ),
    "r5_se_gamma_applies_delta_factor_twice": (
        "The standard error of gamma applies the delta factor gamma (1 - gamma) twice.",
        '        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),',
        '        "se_gamma": gamma * (1.0 - gamma) * gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),',
    ),
}

for name, (first_line, old, new) in EDITS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new, 1)
    start = body.index('"""') + 3
    first_end = body.index("\n", start)
    body = body[:start] + first_line + body[first_end:]
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
