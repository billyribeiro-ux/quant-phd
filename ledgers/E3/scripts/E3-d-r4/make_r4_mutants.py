"""Writes four new student-error mutants of the E3 reference engine into ledgers/E3/mutants/ (round 4, slice d).

Each mutant is the full reference module with one edit; the first docstring line names the error.
Run from the checkout: python3 ledgers/E3/scripts/E3-d-r4/make_r4_mutants.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

EDITS = {
    "r4_probability_sum_tolerance_1e12": (
        "Probabilities accepted when their exact sum is within 1e-12 of one, judged in floating point.",
        "    if any(p < 0 for p in probs) or sum(probs, Fraction(0)) != 1:",
        "    if any(p < 0 for p in probs) or abs(float(sum(probs, Fraction(0))) - 1.0) > 1e-12:",
    ),
    "r4_prospect_uses_wealth": (
        "Prospect certainty equivalent computed on final wealth (wealth plus each prize), then the wealth taken back off.",
        "    return _half_up(_prospect_ce(prizes, probs, gamma, lam))",
        "    return _half_up(_prospect_ce([x + wealth_cents for x in prizes], probs, gamma, lam) - wealth_cents)",
    ),
    "r4_zero_probability_rejected": (
        "Probability exactly zero refused as not positive, though the page allows it.",
        "    if any(p < 0 for p in probs) or sum(probs, Fraction(0)) != 1:",
        "    if any(p <= 0 for p in probs) or sum(probs, Fraction(0)) != 1:",
    ),
    "r4_newton_capped_at_five_steps": (
        "Newton search capped at five iterations, so a start far from the maximum stops before the score is zero.",
        "    for _ in range(_MAX_ITER):",
        "    for _ in range(5):",
    ),
}

for name, (first_line, old, new) in EDITS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new, 1)
    head, rest = body.split('"""', 2)[1], body
    # Replace the module docstring's first line so the description names the error.
    start = body.index('"""') + 3
    first_end = body.index("\n", start)
    doc_first = body[start:first_end]
    body = body[:start] + first_line + body[first_end:]
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name, "| replaced docstring line:", doc_first[:60])
