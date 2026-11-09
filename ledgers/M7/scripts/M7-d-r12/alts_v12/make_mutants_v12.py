"""Write the verifier's four new student-error mutants (round 12) from the reference, one replaced line each.

Usage: python -I make_mutants_v12.py <repo_root>. Each replacement must match exactly once (asserted).
"""

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
ref = (repo / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
mutants = {
    "v12_02_hessian_uses_only_the_variances_of_sigma": (
        "    hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]\n",
        "    hessian = [[problem.gamma * problem.sigma[i][j] if i == j else Fraction(0) for j in range(n)] for i in range(n)]\n",
        "Student error v12_02: the active-set solve uses only the diagonal of Sigma (the variances), so the covariances are "
        "dropped from the stationarity equations the solver enforces.",
    ),
    "v12_03_sector_caps_left_out_of_the_search": (
        "    for k, cap in enumerate(problem.caps):\n        rows.append(",
        "    for k, cap in enumerate([]):\n        rows.append(",
        "Student error v12_03: the sector caps are left out of the constraint rows the search uses, so an answer can break "
        "a sector cap.",
    ),
    "v12_05_sector_cap_only_for_the_first_sector": (
        "    for k, cap in enumerate(problem.caps):\n        rows.append(",
        "    for k, cap in enumerate(problem.caps[:1]):\n        rows.append(",
        "Student error v12_05: the search applies the sector cap of sector 0 only, so the cap of any later sector can be "
        "broken by an answer.",
    ),
    "v12_04_starting_portfolio_tolerance_1e-8": (
        "TOL = Fraction(1, 10**9)  # the tolerance",
        "TOL = Fraction(1, 10**8)  # the tolerance",
        "Student error v12_04: the starting-portfolio tolerance is 1e-8, not the 1e-9 the page states, so a starting sum "
        "2e-9 off one is accepted.",
    ),
}
for name, (old, new, description) in mutants.items():
    count = ref.count(old)
    assert count == 1, (name, count)
    text = ref.replace(old, new)
    assert text.startswith('"""Reference solution'), name
    text = '"""' + description + "\n\n" + text[len('"""'):]
    out = repo / "ledgers/M7/mutants" / f"{name}.py"
    out.write_text(text, encoding="utf-8")
    print("wrote", out.name)
