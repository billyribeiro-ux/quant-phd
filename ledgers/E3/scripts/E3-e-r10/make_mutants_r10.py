"""Round-10 student-error mutants of the E3 reference engine (one edit each, complete modules).

Each mutant is grader/reference.py with exactly one replacement; every replacement must match exactly once. The first
docstring line of each mutant names the student error. Output: ledgers/E3/mutants/r10e_*.py.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"
HEAD = '"""Reference solution for the E3 project: elicit.py, the preference-elicitation engine.'

MUTANTS = {
    "r10e_01_likelihood_uses_certainty_equivalents_rounded_to_cents.py": (
        "Student error: the likelihood uses certainty equivalents rounded to whole cents, not the unrounded values the conventions require.",
        [
            (
                "        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)\n        ce_b = _prospect_ce(prizes_b, probs_b, gamma, lam)\n        z = kappa",
                "        ce_a = float(_half_up(_prospect_ce(prizes_a, probs_a, gamma, lam)))\n        ce_b = float(_half_up(_prospect_ce(prizes_b, probs_b, gamma, lam)))\n        z = kappa",
            ),
        ],
    ),
    "r10e_02_reported_lambda_clamped_at_ten.py": (
        "Student error: the reported loss aversion is clamped at 10 (a bound the page never states).",
        [("    lam = math.exp(a)\n    kappa = math.exp(b)\n", "    lam = min(math.exp(a), 10.0)\n    kappa = math.exp(b)\n")],
    ),
    "r10e_03_three_newton_iterations_then_report_the_last_iterate.py": (
        "Student error: the maximiser runs three Newton iterations and reports the last iterate without a convergence check.",
        [
            ("    for _ in range(_MAX_ITER):\n        grad, hess", "    for _ in range(3):\n        grad, hess"),
            ('    raise RuntimeError("the likelihood maximisation did not converge")', "    return xi"),
        ],
    ),
    "r10e_04_zero_probability_prize_refused.py": (
        "Student error: a prize with probability exactly zero is refused, although the page allows a probability of zero.",
        [("    if any(p < 0 for p in probs) or sum(probs", "    if any(p <= 0 for p in probs) or sum(probs")],
    ),
}

for name, (first_line, edits) in MUTANTS.items():
    text = REF.replace(HEAD, '"""' + first_line)
    assert text.count('"""' + first_line) == 1, name
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
