"""Write two round-3 correct alternatives (over-constraint probes) as solver modules, from grader/reference.py.

Usage: python3 -I ledgers/E4/scripts/E4-d-r3/make_r3_alternatives.py <repo-root>
alt_r3_closed_form: the informed fraction from the closed form of Proposition 4 (no bisection); must pass.
alt_r3_absolute_bracket: bisection stopped on an absolute bracket width of 1e-13 with a 300-step cap; must pass.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/E4/scripts/E4-d-r3/candidates"

closed = ref.replace(
    "        low, high = 0.0, 1.0  # invariant: the gap is positive at low (its limit, at 0) and negative at high\n"
    "        steps = 0\n"
    "        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:\n"
    "            mid = 0.5 * (low + high)\n"
    "            if indifference_gap(mid, sd, cost) > 0.0:\n"
    "                low = mid\n"
    "            else:\n"
    "                high = mid\n"
    "            steps += 1\n"
    "        lam = 0.5 * (low + high)\n",
    "        tau_bar = (PRIOR_PRECISION + SIGNAL_PRECISION) * math.exp(-2 * RISK_AVERSION * cost) - PRIOR_PRECISION\n"
    "        lam = 0.0 if tau_bar <= 0.0 else min(1.0, RISK_AVERSION * sd * math.sqrt(\n"
    "            tau_bar / (SIGNAL_PRECISION * (SIGNAL_PRECISION - tau_bar))) if tau_bar < SIGNAL_PRECISION else 1.0)\n",
)
assert closed != ref
(out / "alt_r3_closed_form.py").write_text(closed, encoding="utf-8")

absb = ref.replace(
    "while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
    "while high - low > 1e-13 and steps < 300:",
)
assert absb != ref
(out / "alt_r3_absolute_bracket.py").write_text(absb, encoding="utf-8")
print("wrote", sorted(p.name for p in out.glob("alt_r3_*.py")))
