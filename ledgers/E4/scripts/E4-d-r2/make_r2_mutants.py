"""Write the verifier's round-2 student-error mutants (slice d) as complete solver modules.

Each mutant is grader/reference.py at pin 67c47689 with one replacement; every target must occur exactly once.
Output: ledgers/E4/mutants/mutant_r2_<name>.py (first docstring line names the student error).
Usage: python -I ledgers/E4/scripts/E4-d-r2/make_r2_mutants.py <repo-root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

GRID_OLD = (
    "        low, high = 0.0, 1.0  # invariant: the gap is positive at low (its limit, at 0) and negative at high\n"
    "        steps = 0\n"
    "        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:\n"
    "            mid = 0.5 * (low + high)\n"
    "            if indifference_gap(mid, sd, cost) > 0.0:\n"
    "                low = mid\n"
    "            else:\n"
    "                high = mid\n"
    "            steps += 1\n"
    "        lam = 0.5 * (low + high)\n"
)
GRID_NEW = (
    "        grid = [k / 100.0 for k in range(1, 100)]\n"
    "        lam = next((g for g in grid if indifference_gap(g, sd, cost) <= 0.0), 1.0)\n"
)

MUTANTS = [
    (
        "grid_scan_no_refinement",
        "Grid scan without refinement: the fraction is the first point of a 0.01 grid where the gap is nonpositive, with no bisection.",
        GRID_OLD,
        GRID_NEW,
    ),
    (
        "rounded_fraction",
        "Rounds the informed fraction to four decimals inside the solver, although the page requires full floating-point precision.",
        '        "informed_fraction": lam,\n',
        '        "informed_fraction": round(lam, 4),\n',
    ),
    (
        "cost_must_be_positive",
        "Rejects an information cost of exactly zero with the nonnegative-cost ValueError, although zero cost is valid.",
        "    if not (math.isfinite(cost) and cost >= 0.0):",
        "    if not (math.isfinite(cost) and cost > 0.0):",
    ),
    (
        "informativeness_is_posterior_variance",
        "Reports the posterior variance 1 / (tau_v + tau_y) of the payoff as the informativeness, not the squared correlation.",
        "    return tau_y / (PRIOR_PRECISION + tau_y)\n",
        "    return 1.0 / (PRIOR_PRECISION + tau_y)\n",
    ),
]

for name, description, old, new in MUTANTS:
    count = ref.count(old)
    if count != 1:
        raise SystemExit(f"{name}: target occurs {count} times, expected 1")
    body = ref.replace(old, new)
    _, _, rest = body.partition('"""\n\n')
    text = f'"""{description}\n\nSingle edit of grader/reference.py, written by the verifier (slice d, round 2).\n"""\n\n{rest}'
    (out_dir / f"mutant_r2_{name}.py").write_text(text, encoding="utf-8")
    print("wrote", f"mutant_r2_{name}.py")
