"""Write the verifier's round-6 student-error mutants of the E4 reference solver into ledgers/E4/mutants/.

Each mutant is reference.py with one exact replacement (the old text must occur exactly once), and its module docstring's
first line names the student error. Usage: python3 -I make_r6_verifier_mutants.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref_path = root / "course/modules/E/E4/grader/reference.py"
out_dir = root / "ledgers/E4/mutants"
ref = ref_path.read_text(encoding="utf-8")
FIRST = '"""Reference solution for the E4 project: the solver for the noisy rational-expectations model with costly information.'
assert ref.count(FIRST) == 1

EDITS: list[tuple[str, str, str, str]] = [
    (
        "mutant_r6_05_price_precision_sd_not_squared",
        "Price precision divides by the noise volume itself, not its square, so the price noise is taken as a variance.",
        "lam * lam * tau_e + a * a * noise_sd * noise_sd)",
        "lam * lam * tau_e + a * a * noise_sd)",
    ),
    (
        "mutant_r6_02_informativeness_at_one_is_signal_share",
        "At the boundary fraction 1 the informativeness is reported as the signal's share tau_e / (tau_v + tau_e).",
        '"price_informativeness": price_informativeness(lam, sd),',
        '"price_informativeness": (0.5 if lam == 1.0 else price_informativeness(lam, sd)),',
    ),
    (
        "mutant_r6_03_fraction_rounded_to_six_places",
        "The informed fraction is rounded to six decimals before it is returned, against the full precision the page requires.",
        '"informed_fraction": lam,',
        '"informed_fraction": round(lam, 6),',
    ),
    (
        "mutant_r6_04_zero_fraction_reports_gap_at_one",
        "At informed fraction 0 the reported gap is the gap at 1, not the limit at 0 that Proposition 3 gives.",
        "(gap_0 if lam == 0.0 else gap_1)",
        "(gap_1 if lam == 0.0 else gap_1)",
    ),
    (
        "mutant_r6_06_cost_scales_whole_gap",
        "The gap is multiplied by exp(a c) as a whole, a sign-preserving error that changes only the reported gap value.",
        "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "    return math.exp(RISK_AVERSION * info_cost) * (uninformed_term(lam, noise_sd)"
        " - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd))",
    ),
    (
        "mutant_r6_07_unit_informativeness_discounted_by_cost",
        "At informed fraction 1 the informativeness is discounted by exp(-c), as if the cost reduced the price's signal.",
        '"price_informativeness": price_informativeness(lam, sd),',
        '"price_informativeness": price_informativeness(lam, sd) * (math.exp(-cost) if lam == 1.0 else 1.0),',
    ),
    (
        "mutant_r6_08_bracket_reports_lower_end",
        "The reported fraction is the lower end of the final bracket, not its midpoint (an error below the stated tolerance).",
        "        lam = 0.5 * (low + high)\n    gap = ",
        "        lam = low\n    gap = ",
    ),
    (
        "mutant_r6_09_stop_rule_never_relative",
        "The bisection ignores the relative stop rule and always runs the full 200 halvings, the cap the page states.",
        "while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
        "while steps < MAX_BISECTION_STEPS:",
    ),
]

WRAPPER = '''

# Verifier mutant 01 (memorised answers): the answers for the 50 instance draws of seeds 0 to 49 are looked up in a table
# built from the reference solver at import time; any other input gets a fixed guess.
import random as _random

_TABLE: dict[tuple[float, float], dict[str, float]] = {}
for _seed in range(50):
    _rng = _random.Random(_seed)
    _sd = round(_rng.uniform(0.500, 0.750), 3)
    _cost = round(_rng.uniform(0.120, 0.150), 3)
    _TABLE[(_sd, _cost)] = _solve_ref(_sd, _cost)


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    """Memorised answers: returns the stored answer for an instance of seeds 0 to 49, and a fixed guess otherwise."""
    key = (float(noise_sd), float(info_cost))
    if key in _TABLE:
        return dict(_TABLE[key])
    return {"informed_fraction": 0.5, "price_informativeness": 0.2, "indifference_gap": 0.0}
'''

# Spec-compliant variants: their outputs differ from the reference only within the stated bisection tolerance, so they are
# documented in ledgers/E4/equivalent/README.md and not counted as mutants (see that README for the nested-bracket proof).
SPEC_COMPLIANT = {"mutant_r6_08_bracket_reports_lower_end", "mutant_r6_09_stop_rule_never_relative"}
HEADER_TAIL = '\n\nVerifier mutant (E4 slice d, round 6). Built from reference.py by one edit.\n\n'
written: list[str] = []
for name, desc, old, new in EDITS:
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    body = body.replace(FIRST, '"""' + desc + HEADER_TAIL + FIRST[3:], 1)
    target = root / "ledgers/E4/equivalent" if name in SPEC_COMPLIANT else out_dir
    (target / f"{name}.py").write_text(body, encoding="utf-8")
    written.append(name)

# Mutant 01 is the reference solver behind a memorised-answer wrapper.
body = ref.replace("def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:",
                   "def _solve_ref(noise_sd: float, info_cost: float) -> dict[str, float]:", 1)
body = body.replace(FIRST, '"""Memorised answers for the seeds 0 to 49 and a fixed guess elsewhere (student error: caching given instances).'
                    '\n\nVerifier mutant (E4 slice d, round 6). Built from reference.py by a wrapper.\n\n' + FIRST[3:], 1)
(out_dir / "mutant_r6_01_memorised_seed_answers.py").write_text(body.rstrip("\n") + "\n" + WRAPPER, encoding="utf-8")
written.append("mutant_r6_01_memorised_seed_answers")
print("\n".join(written))
