"""Write the verifier's round-3 student-error mutants as full solver modules (single-edit copies of grader/reference.py).

Usage: python3 -I ledgers/E4/scripts/E4-d-r3/make_r3_mutants.py <repo-root>
Each mutant is written to ledgers/E4/mutants/ with a one-line docstring naming the error, and each edit is asserted to
match exactly once in the reference, so no mutant is silently a no-op.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_r3_tolerance_1e-9": (
        "Bisection stops at a relative bracket width of 1e-9 instead of the 1e-12 that the page states.",
        [("BISECTION_TOLERANCE = 1e-12", "BISECTION_TOLERANCE = 1e-9")],
    ),
    "mutant_r3_boundary_rule_swapped": (
        "Boundary rule swapped: the fraction is 1 when the gap at 0 is nonpositive and 0 when the gap at 1 is nonnegative.",
        [
            ("    if gap_0 <= 0.0:\n        lam = 0.0\n    elif gap_1 >= 0.0:\n        lam = 1.0\n",
             "    if gap_0 <= 0.0:\n        lam = 1.0\n    elif gap_1 >= 0.0:\n        lam = 0.0\n"),
        ],
    ),
    "mutant_r3_cost_discounted_in_gap": (
        "Information cost discounts the informed utility: the gap multiplies the informed term by exp(-a c), not exp(a c).",
        [("    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
          "    return uninformed_term(lam, noise_sd) - math.exp(-RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)")],
    ),
    "mutant_r3_price_precision_linear_in_lambda": (
        "Price precision uses lam once in the numerator, not lam squared: tau_y = lam tau_e^2 / (lam^2 tau_e + a^2 sd^2).",
        [("    return lam * lam * tau_e * tau_e / (lam * lam * tau_e + a * a * noise_sd * noise_sd)",
          "    return lam * tau_e * tau_e / (lam * lam * tau_e + a * a * noise_sd * noise_sd)")],
    ),
    "mutant_r3_closed_form_cost_sign_flipped": (
        "Closed-form fraction with the cost sign flipped: tau_bar = (tau_v + tau_e) exp(+2 a c) - tau_v, used as the answer.",
        [
            ("        low, high = 0.0, 1.0  # invariant: the gap is positive at low (its limit, at 0) and negative at high\n"
             "        steps = 0\n"
             "        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:\n"
             "            mid = 0.5 * (low + high)\n"
             "            if indifference_gap(mid, sd, cost) > 0.0:\n"
             "                low = mid\n"
             "            else:\n"
             "                high = mid\n"
             "            steps += 1\n"
             "        lam = 0.5 * (low + high)\n",
             "        tau_bar = (PRIOR_PRECISION + SIGNAL_PRECISION) * math.exp(2 * RISK_AVERSION * cost) - PRIOR_PRECISION\n"
             "        lam = _closed_fraction(sd, tau_bar)\n"),
            ("def price_precision(lam: float, noise_sd: float) -> float:",
             "def _closed_fraction(sd: float, t: float) -> float:\n"
             "    if t <= 0.0:\n"
             "        return 0.0\n"
             "    if t >= SIGNAL_PRECISION * SIGNAL_PRECISION / (SIGNAL_PRECISION + RISK_AVERSION**2 * sd * sd):\n"
             "        return 1.0\n"
             "    return RISK_AVERSION * sd * math.sqrt(t / (SIGNAL_PRECISION * (SIGNAL_PRECISION - t)))\n\n\n"
             "def price_precision(lam: float, noise_sd: float) -> float:"),
        ],
    ),
}

for name, (doc, edits) in MUTANTS.items():
    src = ref
    for old, new in edits:
        n = src.count(old)
        assert n == 1, (name, n, old[:60])
        src = src.replace(old, new)
    # replace the reference's module docstring with the mutant's one-line description
    start = src.index('"""')
    end = src.index('"""', start + 3) + 3
    src = f'"""{doc}\n\nSingle edit of grader/reference.py, written by the verifier (slice d, round 3).\n"""' + src[end:]
    (out_dir / f"{name}.py").write_text(src, encoding="utf-8")
    print("wrote", f"ledgers/E4/mutants/{name}.py")
