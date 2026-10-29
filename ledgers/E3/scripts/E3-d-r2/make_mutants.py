"""Writes the verifier's round-2 student-error mutants (ledgers/E3/mutants/w01-w07) from grader/reference.py.

Each mutant is the reference engine with one plausible student error and a one-line description as its module
docstring. Every replacement must match exactly once, or the script fails. Usage: python3 make_mutants.py
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "E" / "E3" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "E3" / "mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "w01_crra_uses_prize_as_final_wealth": (
        "CRRA utility is evaluated at the prize, not at wealth plus the prize, so the wealth is left out of the utility.",
        [("    finals = [wealth + x for x in prizes]", "    finals = [x for x in prizes]")],
    ),
    "w02_loglik_chosen_b_uses_log_pa": (
        "A response that chose B contributes log P(A) (the logit for A) instead of log(1 - P(A)).",
        [('total += -_log1pexp(-z) if choice == "A" else -_log1pexp(z)', 'total += -_log1pexp(-z)')],
    ),
    "w03_estimate_needs_every_response_mixed": (
        "estimate refuses unless every response has a mixed-sign lottery, which is stricter than the page's condition.",
        [("    if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):",
          "    if not all(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):")],
    ),
    "w04_prospect_loss_inverse_multiplies_lambda": (
        "The prospect inverse for a negative lottery value multiplies by lambda where it should divide by lambda.",
        [("    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))", "    return -math.pow(-total * lam, 1.0 / (1.0 - gamma))")],
    ),
    "w05_half_cent_away_from_zero": (
        "An exact half cent is rounded away from zero, so -0.5 cents gives -1 instead of 0 (the page says toward plus infinity).",
        [("    return math.floor(y + 0.5)",
          "    return math.floor(y + 0.5) if y >= 0 else math.ceil(y - 0.5)")],
    ),
    "w06_likelihood_uses_rounded_cents": (
        "The logit uses the certainty equivalents rounded to whole cents, not the unrounded values the page requires.",
        [("        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)\n        ce_b = _prospect_ce(prizes_b, probs_b, gamma, lam)",
          "        ce_a = float(_half_up(_prospect_ce(prizes_a, probs_a, gamma, lam)))\n"
          "        ce_b = float(_half_up(_prospect_ce(prizes_b, probs_b, gamma, lam)))")],
    ),
    "w07_estimate_returns_eta_as_gamma": (
        "estimate reports the transformed coordinate eta = log(gamma/(1-gamma)) as gamma_hat instead of gamma.",
        [('"gamma_hat": gamma,', '"gamma_hat": theta[0],')],
    ),
}


def main() -> int:
    source = REF.read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(source), clean=False)
    assert doc is not None
    doc_text = '"""' + doc + '"""'
    if source.count(doc_text) != 1:
        print("FAIL: module docstring not found exactly once")
        return 1
    for name, (desc, reps) in MUTANTS.items():
        text = source.replace(doc_text, f'"""{desc}"""', 1)
        for old, new in reps:
            count = text.count(old)
            if count != 1:
                print(f"FAIL {name}: pattern matched {count} times: {old[:60]!r}")
                return 1
            text = text.replace(old, new, 1)
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print(f"wrote {name}.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
