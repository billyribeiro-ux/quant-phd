"""Round 6 (M7-d) verifier mutants: one change each to grader/reference.py, written as complete modules."""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-M7-d")
SRC = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS = {
    "q01_upper_multiplier_sign_reversed_in_certificate.py": (
        "Student error q01: the upper-bound multiplier enters the certificate's weight stationarity with a minus sign.",
        'r_w = gradient + sol["budget"] - sol["lower"][i] + sol["upper"][i] + sol["sector"][problem.sector[i]]',
        'r_w = gradient + sol["budget"] - sol["lower"][i] - sol["upper"][i] + sol["sector"][problem.sector[i]]',
    ),
    "q02_missing_field_raises_key_error.py": (
        "Student error q02: a missing case field raises KeyError, where the page names ValueError for a missing field.",
        'raise ValueError(f"the instance has no {key!r} field")',
        "raise KeyError(key)",
    ),
    "q03_certificate_gradient_uses_half_gamma.py": (
        "Student error q03: the certificate's gradient uses gamma / 2 in the quadratic term, a factor-two error.",
        "gradient = problem.gamma * _dot(problem.sigma[i], w) - problem.mu[i]",
        "gradient = problem.gamma / 2 * _dot(problem.sigma[i], w) - problem.mu[i]",
    ),
    "q04_dual_residual_without_zero_floor.py": (
        "Student error q04: the dual residual is the negative of the smallest multiplier with no floor at zero.",
        "dual = max(Fraction(0), -min(mult_ineq))",
        "dual = -min(mult_ineq)",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new, 1)
    body = body.replace('"""Reference solution', '"""' + doc + "\n\nReference solution", 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
