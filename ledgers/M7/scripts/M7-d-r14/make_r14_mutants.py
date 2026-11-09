"""Write the round-14 student-error mutants of the M7 reference solution into ledgers/M7/mutants/.

Run from the repository root: python -I ledgers/M7/scripts/M7-d-r14/make_r14_mutants.py
Each replacement must match exactly once in the reference, or the script stops.
"""

from pathlib import Path

ref = Path("course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
out = Path("ledgers/M7/mutants")
MUTANTS = [
    (
        "w14d_01_complementary_slackness_uses_the_raw_sector_sum.py",
        "Student error w14d-01: the sector complementary-slackness term multiplies the multiplier by the raw sector "
        "weight instead of the gap to the cap.",
        "*[sector_sum[k] - problem.caps[k] for k in range(len(problem.caps))],",
        "*[sector_sum[k] for k in range(len(problem.caps))],",
    ),
    (
        "w14d_02_active_set_gradient_taken_at_the_starting_portfolio.py",
        "Student error w14d-02: the active-set gradient is evaluated at the starting portfolio, not at the current iterate.",
        "gradient = [_dot(hessian[i], x) - problem.mu[i] for i in range(n)]",
        "gradient = [_dot(hessian[i], problem.w0) - problem.mu[i] for i in range(n)]",
    ),
    (
        "w14d_03_zero_turnover_limit_drops_the_turnover_rows.py",
        "Student error w14d-03: a zero turnover limit is treated as no limit, so the turnover rows are dropped from the search.",
        "    for signs in product((1, -1), repeat=n):",
        "    for signs in (product((1, -1), repeat=n) if problem.tau > 0 else []):",
    ),
]
for name, description, old, new in MUTANTS:
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    head, sep, rest = body.partition('"""')
    assert sep, name
    doc_rest = rest.split('"""', 1)
    text = (
        '"""' + description + "\n\nMutant of the reference solution (course/modules/M/M7/grader/reference.py).\n" + doc_rest[0]
        + '"""' + doc_rest[1]
    )
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
