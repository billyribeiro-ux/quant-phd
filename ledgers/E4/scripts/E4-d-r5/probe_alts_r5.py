"""Compare each alternative's solve_model with the reference over small and ordinary inputs.

Usage: python -I probe_alts_r5.py <checkout-root>
Reports the largest relative error in informed_fraction, for inputs where the reference root is interior (0 < lam < 1),
and any boundary mismatch. Also reports the closed form of Proposition 4 where the root is interior.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref_spec = importlib.util.spec_from_file_location("ref", root / "course/modules/E/E4/grader/reference.py")
assert ref_spec and ref_spec.loader
ref = importlib.util.module_from_spec(ref_spec)
ref_spec.loader.exec_module(ref)

TV, TE, A = ref.PRIOR_PRECISION, ref.SIGNAL_PRECISION, ref.RISK_AVERSION


def closed(sd: float, c: float) -> float:
    t = (TV + TE) * math.exp(-2.0 * A * c) - TV
    if t <= 0.0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))


cases = []
for sd in [1e-12, 1e-9, 1e-6, 1e-4, 1e-3, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.0, 5.0]:
    for c in [0.0, 1e-6, 0.01, 0.05, 0.10, 0.12, 0.13, 0.15, 0.2, 0.3, 0.5]:
        cases.append((sd, c))

alt_dir = root / "ledgers/E4/alternatives"
for name in ["alt_1", "alt_2", "alt_3", "alt_4", "alt_5"]:
    spec = importlib.util.spec_from_file_location(name, alt_dir / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    worst_rel = 0.0
    worst_case = None
    mismatches = []
    errors = []
    for sd, c in cases:
        try:
            got = mod.solve_model(sd, c)["informed_fraction"]
        except Exception as e:  # noqa: BLE001
            errors.append((sd, c, repr(e)))
            continue
        exp = ref.solve_model(sd, c)["informed_fraction"]
        if exp in (0.0, 1.0) or got in (0.0, 1.0):
            if exp != got:
                mismatches.append((sd, c, got, exp))
            continue
        rel = abs(got - exp) / exp
        if rel > worst_rel:
            worst_rel, worst_case = rel, (sd, c, got, exp)
    print(f"{name}: worst relative error on interior roots = {worst_rel:.3e} at {worst_case}; "
          f"boundary mismatches = {len(mismatches)} {mismatches[:4]}; exceptions = {len(errors)} {errors[:3]}")

print("reference vs closed form (Proposition 4) on interior roots:")
worst = 0.0
for sd, c in cases:
    exp = ref.solve_model(sd, c)["informed_fraction"]
    if 0.0 < exp < 1.0:
        cf = closed(sd, c)
        worst = max(worst, abs(exp - cf) / cf)
print(f"  max relative |reference - closed| = {worst:.3e}")
