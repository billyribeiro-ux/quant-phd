"""Write three verifier-authored student-error mutants of the E3 reference (verifier E3-e, round 2).

Each mutant is a complete module: the reference solution with one change. The first docstring line names the error.
Run from the checkout root: python -I ledgers/E3/scripts/E3-e-r2/make_mutants_r2.py
"""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-E3-e")
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"


def swap(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"anchor found {text.count(old)} times: {old[:60]!r}")
    return text.replace(old, new)


# 1. The likelihood skips the probability checks (the table's sum-to-one and non-negative rows) in log_likelihood only.
lenient = swap(
    REF,
    "    return _logit_sum([_parse(r) for r in responses], gamma, lam, kappa)",
    "    return _logit_sum([_parse_unchecked(r) for r in responses], gamma, lam, kappa)",
)
lenient = swap(
    lenient,
    "def _mixed(prizes: list[int], probs: list[Fraction]) -> bool:",
    '''def _parse_unchecked(response: Mapping[str, Any]) -> Parsed:
    prizes_a = [int(x) for x in response["prizes_a"]]
    probs_a = [Fraction(str(s)) for s in response["probs_a"]]
    prizes_b = [int(x) for x in response["prizes_b"]]
    probs_b = [Fraction(str(s)) for s in response["probs_b"]]
    return prizes_a, probs_a, prizes_b, probs_b, str(response["choice"])


def _mixed(prizes: list[int], probs: list[Fraction]) -> bool:''',
)
lenient = '"""log_likelihood trusts its input: the probability checks (non-negative, sum exactly 1) are skipped."""\n' + lenient.split(
    '"""', 2
)[2].lstrip("\n").join(["", ""]) if False else lenient
(OUT / "e2_01_log_likelihood_skips_the_probability_checks.py").write_text(
    '"""log_likelihood trusts its input: the probability checks (non-negative, sum exactly 1) are skipped."""\n'
    + lenient.split('"""', 2)[2],
    encoding="utf-8",
)

# 2. The observed information for the standard errors is taken by central differences of step 1e-3.
step = swap(
    REF,
    "    _, hess = _gradient_and_hessian(f, theta)\n    lower = _cholesky([[-h for h in row] for row in hess])",
    "    global _H\n    _H = 1e-3\n    _, hess = _gradient_and_hessian(f, theta)\n    lower = _cholesky([[-h for h in row] for row in hess])",
)
(OUT / "e2_02_observed_information_by_central_differences_of_step_1e3.py").write_text(
    '"""The standard errors use the observed information by central differences of step 1e-3, not 1e-5 or 1e-6."""\n'
    + step.split('"""', 2)[2],
    encoding="utf-8",
)

# 3. The prospect model refuses a final wealth of zero or below, as if it used wealth.
wealth = swap(
    REF,
    "    lam = float(params[\"lambda\"])\n    _check_prospect(gamma, lam)\n    return _half_up(_prospect_ce(prizes, probs, gamma, lam))",
    "    lam = float(params[\"lambda\"])\n    _check_prospect(gamma, lam)\n    if any(wealth_cents + x <= 0 for x in prizes):\n        raise ValueError(\"wealth plus prize must stay positive\")\n    return _half_up(_prospect_ce(prizes, probs, gamma, lam))",
)
(OUT / "e2_03_prospect_refuses_nonpositive_final_wealth.py").write_text(
    '"""The prospect model refuses a final wealth (wealth plus prize) of zero or below, although it does not use wealth."""\n'
    + wealth.split('"""', 2)[2],
    encoding="utf-8",
)
print("wrote 3 mutants")
