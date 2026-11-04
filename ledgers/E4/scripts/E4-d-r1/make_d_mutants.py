"""Write the verifier's own student-error mutants (slice d, round 1) as complete solver modules.

Each mutant is reference.py with one replacement. Every target string must occur exactly once, or the script stops.
Output: ledgers/E4/mutants/mutant_d<NN>_<name>.py (the first docstring line names the student error).
Usage: python -I ledgers/E4/scripts/E4-d-r1/make_d_mutants.py <repo-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = [
    (
        "d11_gap_sign_reversed",
        "Gap sign reversed: the solver returns exp(a c) F_I minus F_U, the negative of the informed-minus-uninformed gap.",
        "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "    return math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd) - uninformed_term(lam, noise_sd)",
    ),
    (
        "d12_informativeness_is_correlation",
        "Informativeness reported as the correlation, not its square: the square root of tau_y / (tau_v + tau_y) is returned.",
        "    return tau_y / (PRIOR_PRECISION + tau_y)\n",
        "    return math.sqrt(tau_y / (PRIOR_PRECISION + tau_y))\n",
    ),
    (
        "d13_informed_ignores_price_noise",
        "Informed investors ignore the noise in the price: the variance of their conditional-mean gap omits the b_u squared term.",
        "    var_gap = slope * slope * var_signal + b_u * b_u * noise_sd * noise_sd",
        "    var_gap = slope * slope * var_signal",
    ),
    (
        "d14_negative_cost_clamped",
        "Negative information cost clamped to zero instead of rejected with the named ValueError.",
        '        raise ValueError("information cost must be nonnegative")',
        "        cost = 0.0",
    ),
    (
        "d15_bisection_update_inverted",
        "Bisection brackets updated on the wrong side: a positive gap moves the upper end, so the search converges to a boundary.",
        "            if indifference_gap(mid, sd, cost) > 0.0:\n                low = mid\n            else:\n                high = mid",
        "            if indifference_gap(mid, sd, cost) > 0.0:\n                high = mid\n            else:\n                low = mid",
    ),
    (
        "d16_zero_fraction_gap_reported_as_zero",
        "Gap at a zero fraction reported as 0.0 instead of the limit of Proposition 3 that the page requires.",
        "    gap = indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else (gap_0 if lam == 0.0 else gap_1)",
        "    gap = 0.0 if lam == 0.0 else (indifference_gap(lam, sd, cost) if 0.0 < lam < 1.0 else gap_1)",
    ),
    (
        "d17_tolerance_1e-6",
        "Bisection stops at a relative bracket width of 1e-6 instead of the 1e-12 that the page states.",
        "BISECTION_TOLERANCE = 1e-12  #",
        "BISECTION_TOLERANCE = 1e-6  #",
    ),
    (
        "d18_tolerance_1e-4",
        "Bisection stops at a relative bracket width of 1e-4 instead of the 1e-12 that the page states.",
        "BISECTION_TOLERANCE = 1e-12  #",
        "BISECTION_TOLERANCE = 1e-4  #",
    ),
]

for name, description, old, new in MUTANTS:
    count = ref.count(old)
    if count != 1:
        raise SystemExit(f"{name}: target occurs {count} times, expected 1")
    body = ref.replace(old, new)
    head, _, tail = body.partition('"""\n')
    # Keep the reference module's code and replace its docstring with the one-line error description.
    _, _, rest = body.partition('"""\n\n')
    text = f'"""{description}\n\nSingle edit of grader/reference.py, written by the verifier (slice d, round 1).\n"""\n\n{rest}'
    if name == "d12_informativeness_is_correlation" and "math" not in rest.split("\n")[0:20].__str__():
        pass
    (out_dir / f"mutant_{name}.py").write_text(text, encoding="utf-8")
    print("wrote", f"mutant_{name}.py")
