"""Check the project lede's claim that the informed fraction rises with the noise volume (verifier, slice d, round 2).

Usage: python -I ledgers/E4/scripts/E4-d-r2/lede_fraction_check.py <repo-root>
Loads grader/reference.py (the solver) and prints the informed fraction for a sweep of noise volumes at several costs.
A rise with the noise volume is required for the lede's unqualified claim; Proposition 5 gives it on the interior only.
"""

import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("reference", root / "course/modules/E/E4/grader/reference.py")
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

NOISE = (0.5, 0.6, 0.75, 1.0, 2.0)
for cost in (0.0, 0.05, 0.13):
    fractions = [ref.solve_model(sd, cost)["informed_fraction"] for sd in NOISE]
    print(f"cost {cost:.2f}: informed fraction at noise", NOISE, "=", [round(f, 6) for f in fractions])
