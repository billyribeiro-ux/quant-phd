"""Compare the reference solver with the two stop-rule and reporting variants (mutants 08 and 09) on random inputs.

Usage: python -I equivalence_within_tolerance_r6.py <checkout-root>
Reports, for each variant, the largest relative difference of informed_fraction on interior outputs, the largest absolute
difference of the other two outputs, and the count of exact (bitwise) equal outputs.
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def load(name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("ref_r6", root / "course/modules/E/E4/grader/reference.py")
m08 = load("m08_r6", root / "ledgers/E4/mutants/mutant_r6_08_bracket_reports_lower_end.py")
m09 = load("m09_r6", root / "ledgers/E4/mutants/mutant_r6_09_stop_rule_never_relative.py")
rng = random.Random(6)
cases = []
for _ in range(20000):
    sd = 10 ** rng.uniform(-12, math.log10(5.0))
    cost = rng.uniform(0.0, 0.4)
    cases.append((sd, cost))
# add the boundary-adjacent cases: costs that put tau_bar at the interior limits for several sd values
for sd in (1e-12, 1e-9, 1e-6, 0.5, 0.75, 2.0):
    for cost in (0.0, 0.12, 0.13, 0.15, 0.3):
        cases.append((sd, cost))
for name, mod in (("mutant_08 (lower end)", m08), ("mutant_09 (no relative stop)", m09)):
    worst_rel = 0.0
    worst_abs = 0.0
    exact = 0
    interior = 0
    for sd, cost in cases:
        a = ref.solve_model(sd, cost)  # type: ignore[attr-defined]
        b = mod.solve_model(sd, cost)  # type: ignore[attr-defined]
        if a == b:
            exact += 1
        lam_a = a["informed_fraction"]
        if 0.0 < lam_a < 1.0:
            interior += 1
            worst_rel = max(worst_rel, abs(a["informed_fraction"] - b["informed_fraction"]) / lam_a)
        worst_abs = max(worst_abs, abs(a["indifference_gap"] - b["indifference_gap"]),
                        abs(a["price_informativeness"] - b["price_informativeness"]))
    print(f"{name}: cases={len(cases)} exact_equal={exact} interior={interior} "
          f"worst_rel_diff_fraction={worst_rel:.3e} worst_abs_diff_other_outputs={worst_abs:.3e}")
