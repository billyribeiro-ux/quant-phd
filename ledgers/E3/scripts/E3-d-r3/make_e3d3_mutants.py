"""Round-3 verifier (E3-d): writes four new student-error mutants of the reference into ledgers/E3/mutants/.

Each mutant is the reference solution with one change. The module docstring's first line names the student error,
as ledgers/E3/mutants requires (architect ruling 9). Run from the repository root:
    .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/make_e3d3_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

DOC_OLD = REF[: REF.index('"""', REF.index('"""') + 3) + 3]
assert DOC_OLD.startswith('"""Reference solution'), "unexpected reference docstring"

MUTANTS = {
    "e3d3_01_probability_text_read_through_float.py": (
        "Probability text is read through float() before Fraction, so \"1/3\" is refused as not a number.",
        ('                probs.append(Fraction(p))', '                probs.append(Fraction(float(p)))'),
    ),
    "e3d3_02_prospect_model_ignores_the_lambda_parameter.py": (
        "The prospect model ignores the lambda parameter and uses loss aversion 1 in every certainty equivalent.",
        ('    lam = float(params["lambda"])\n    _check_prospect(gamma, lam)\n    return _half_up',
         '    lam = 1.0\n    _check_prospect(gamma, float(params["lambda"]))\n    return _half_up'),
    ),
    "e3d3_03_observed_information_keeps_only_the_diagonal.py": (
        "The observed information drops its off-diagonal terms, so the covariances between the parameters are ignored.",
        ("    _, hess = _gradient_and_hessian(f, theta)\n",
         "    _, hess = _gradient_and_hessian(f, theta)\n"
         "    hess = [[hess[i][j] if i == j else 0.0 for j in range(3)] for i in range(3)]\n"),
    ),
    "e3d3_04_se_lambda_applies_the_loss_factor_twice.py": (
        "The standard error of lambda multiplies by lambda twice, as if the coordinate change were exp(2 a).",
        ('        "se_lambda": lam * math.sqrt(cov_diag[1]),', '        "se_lambda": lam * lam * math.sqrt(cov_diag[1]),'),
    ),
}

for name, (description, (old, new)) in MUTANTS.items():
    body = REF.replace(DOC_OLD, f'"""{description}\n\nSingle-change copy of the reference solution (verifier E3-d, round 3).\n"""', 1)
    assert body.count(old) == 1, f"{name}: replacement site not unique"
    body = body.replace(old, new, 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
