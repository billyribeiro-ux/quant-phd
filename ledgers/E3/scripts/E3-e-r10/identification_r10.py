"""Round-10: the Identification convention (project.html Conventions): a lottery with no gain (or no loss) among its
positive-probability prizes has a certainty equivalent that does not depend on lambda; a mixed lottery does."""

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
import reference as ref  # noqa: E402

cases = {
    "no gain, zero prize with prob 1/3": ([-100, 0, -40], [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]),
    "no loss, prize 0 and gains": ([0, 300, 900], [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]),
    "all losses": ([-500, -200], [Fraction(1, 2), Fraction(1, 2)]),
    "mixed gain and loss": ([600, -400], [Fraction(1, 2), Fraction(1, 2)]),
    "gain with prob 0 and loss": ([500, -400], [Fraction(0), Fraction(1)]),
}
for name, (prizes, probs) in cases.items():
    values = [round(ref._prospect_ce(prizes, probs, 0.4, lam), 9) for lam in (0.5, 2.0, 7.0)]
    print(f"{name}: CE at lambda 0.5, 2, 7 = {values}; lambda-free: {len(set(values)) == 1}")
