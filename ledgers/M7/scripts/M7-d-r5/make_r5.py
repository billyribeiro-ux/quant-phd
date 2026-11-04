"""Write round-5 student-error mutants (one change each, from grader/reference.py) and one correct alternative."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD5-M7-d")
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/M7/mutants"
ALT = ROOT / "ledgers/M7/scripts/M7-d-r5/alts"
DOC_OLD = REF.split('"""', 2)[1]
DOC_START = REF.index('"""')
DOC_END = REF.index('"""', DOC_START + 3) + 3


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


def with_doc(text: str, line: str) -> str:
    return '"""' + line + '\n\nMutant of grader/reference.py: one change, as the first line states.\n"""' + text[DOC_END:]


MUTANTS = {
    "r5_01_gamma_missing_from_the_solver_hessian.py": (
        "Student error r5-01: the solver's Hessian is Sigma without gamma, so the solution is the minimizer for gamma = 1.",
        ("hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]",
         "hessian = [[problem.sigma[i][j] for j in range(n)] for i in range(n)]"),
    ),
    "r5_02_sector_multiplier_sign_flipped_in_the_weight_residual.py": (
        "Student error r5-02: the certificate's weight stationarity subtracts the sector multiplier where the page adds it.",
        ('r_w = gradient + sol["budget"] - sol["lower"][i] + sol["upper"][i] + sol["sector"][problem.sector[i]]',
         'r_w = gradient + sol["budget"] - sol["lower"][i] + sol["upper"][i] - sol["sector"][problem.sector[i]]'),
    ),
    "r5_03_starting_budget_checked_by_exact_equality.py": (
        "Student error r5-03: the starting-portfolio budget is checked by exact equality, so a sum inside the 1e-9 tolerance is refused.",
        ("if abs(sum(w0, Fraction(0)) - 1) > TOL:", "if sum(w0, Fraction(0)) != 1:"),
    ),
    "r5_04_zero_risk_aversion_accepted.py": (
        "Student error r5-04: the risk-aversion check refuses only negative values, so gamma = 0 is accepted.",
        ("    if gamma <= 0:\n", "    if gamma < 0:\n"),
    ),
    "r5_05_weights_rounded_to_six_decimals.py": (
        "Student error r5-05: the returned weights are rounded to six decimals, so the budget and stationarity residuals are about 1e-7.",
        ('"weights": [float(v) for v in sol["w"]],', '"weights": [round(float(v), 6) for v in sol["w"]],'),
    ),
}

for name, (line, (old, new)) in MUTANTS.items():
    text = replace_once(REF, old, new)
    (MUT / name).write_text(with_doc(text, line), encoding="utf-8")

ALT.mkdir(parents=True, exist_ok=True)
alt = replace_once(REF, "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) <= TOL and",
                   "    for j, (a, b, _) in reversed(list(enumerate(rows))):\n        if b - _dot(a, x) <= TOL and")
alt = replace_once(alt, "working.pop(min(negative)[1])", "working.pop(max(negative)[1])")
(ALT / "alt_r5_exact_reversed_order_max_drop.py").write_text(alt, encoding="utf-8")
print("written", len(MUTANTS), "mutants and 1 alternative")
