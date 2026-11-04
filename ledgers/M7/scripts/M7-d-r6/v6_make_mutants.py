"""Round 6 (M7-d): write four new student-error mutants of the reference allocator into ledgers/M7/mutants/.

Each mutant is a complete solution module (a copy of grader/reference.py with one change). The first line of each
docstring states the error. Run from the verifier checkout.
"""

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"


def mutant(text: str, old: str, new: str, doc_first_line: str) -> str:
    assert REF.count(old) == 1, f"anchor not unique: {old!r}"
    body = REF.replace(old, new)
    head, rest = body.split('"""', 2)[1], body.split('"""', 2)[2]
    return f'"""{doc_first_line}\n\n{head.split(chr(10), 1)[1].lstrip(chr(10))}"""{rest}'


SPECS = {
    "v6_01_dual_residual_reported_without_the_floor.py": (
        "    dual = max(Fraction(0), -min(mult_ineq))\n",
        "    dual = -min(mult_ineq)\n",
        "Student error v6_01: the dual residual is reported as the negative of the smallest inequality multiplier, with no floor at zero, so it is negative whenever every multiplier is positive.",
    ),
    "v6_02_dual_residual_omits_turnover_multipliers.py": (
        "    dual = max(Fraction(0), -min(mult_ineq))\n",
        "    dual = max(Fraction(0), -min([*sol[\"lower\"], *sol[\"upper\"], *sol[\"sector\"]]))\n",
        "Student error v6_02: the dual residual considers only the bound and sector multipliers and leaves out the turnover multipliers, so a negative turnover multiplier is never reported.",
    ),
    "v6_03_complementary_slackness_bounds_at_starting_weights.py": (
        "                *[problem.lower[i] - w[i] for i in range(n)],\n                *[w[i] - problem.upper[i] for i in range(n)],\n",
        "                *[problem.lower[i] - w0[i] for i in range(n)],\n                *[w0[i] - problem.upper[i] for i in range(n)],\n",
        "Student error v6_03: the complementary-slackness residual evaluates the bound rows at the starting portfolio w0 instead of at the returned weights.",
    ),
    "v6_04_objective_without_the_one_half.py": (
        "        gradient = problem.gamma * _dot(problem.sigma[i], w) - problem.mu[i]\n",
        "        gradient = 2 * problem.gamma * _dot(problem.sigma[i], w) - problem.mu[i]\n",
        "Student error v6_04: the certificate's weight stationarity uses 2 gamma Sigma w - mu, the gradient of gamma w' Sigma w - mu' w, which drops the one half of the objective.",
    ),
}

SPECS_R6B = {
    "v6_05_turnover_sign_forms_skip_last_asset_sells.py": (
        "    for signs in product((1, -1), repeat=n):\n        a = [Fraction(s) for s in signs]\n",
        "    for signs in product((1, -1), repeat=n):\n        if signs[-1] == -1:\n            continue\n        a = [Fraction(s) for s in signs]\n",
        "Student error v6_05: the turnover sign forms are enumerated with the last asset always counted as a buy, so a sale of the last asset is never limited by the turnover constraint.",
    ),
    "v6_06_zero_turnover_limit_read_as_no_limit.py": (
        "    for signs in product((1, -1), repeat=n):\n        a = [Fraction(s) for s in signs]\n",
        "    for signs in product((1, -1), repeat=n):\n        if problem.tau == 0:\n            break\n        a = [Fraction(s) for s in signs]\n",
        "Student error v6_06: a turnover limit of exactly zero is read as no limit, so the turnover sign constraints are dropped and the zero-turnover case is solved without them.",
    ),
}
SPECS.update(SPECS_R6B)
EQUIVALENT_DIR = ROOT / "ledgers/M7/scripts/M7-d-r6/v6_equivalent"
EQUIVALENT_DIR.mkdir(parents=True, exist_ok=True)
EQUIVALENT = {"v6_01_dual_residual_reported_without_the_floor.py", "v6_02_dual_residual_omits_turnover_multipliers.py"}

for name, (old, new, first) in SPECS.items():
    text = REF.replace(old, new)
    assert text != REF
    head_end = text.index('"""', 3)
    doc_body = text[3:head_end]
    lines = doc_body.split("\n")
    text2 = f'"""{first}\n' + "\n".join(lines[1:]) + text[head_end:]
    target = EQUIVALENT_DIR if name in EQUIVALENT else OUT
    (target / name).write_text(text2, encoding="utf-8")
    print("wrote", target / name)
