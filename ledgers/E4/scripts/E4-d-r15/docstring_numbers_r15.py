"""Round-15 check of numbers quoted in grader/test_project.py docstrings, using the suite's own oracles.

The suite is imported from a scratch workspace holding reference.py as solver.py, so the oracles are the suite's.
Usage: python -I docstring_numbers_r15.py
"""
import importlib
import math
import shutil
import sys
import tempfile
from pathlib import Path

GRADER = Path("course/modules/E/E4/grader").resolve()
work = Path(tempfile.mkdtemp(prefix="e4doc-"))
shutil.copy(GRADER / "test_project.py", work / "test_project.py")
shutil.copy(GRADER / "instance.py", work / "instance.py")
shutil.copy(GRADER / "reference.py", work / "solver.py")
sys.path.insert(0, str(work))
import os  # noqa: E402

os.environ.setdefault("QF_SEED", "0")
T = importlib.import_module("test_project")
ref = T.sol

print("test_gap_at_zero... docstring: gap at 1e-12 vs limit, and oracle vs limit (1.1e-16 claim)")
worst_gap_dev = 0.0
worst_oracle_dev = 0.0
for sd, cost in [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]:
    limit = T.oracle_gap(0.0, sd, cost)
    ref_limit = ref.gap_at_zero(sd, cost)
    gap_small = ref.indifference_gap(1e-12, sd, cost)
    dev_small = abs(gap_small - limit)
    dev_oracle = abs(limit - ref_limit)
    print(f"  sd {sd} cost {cost}: |gap(1e-12)-limit| = {dev_small:.3e}; |oracle limit - reference limit| = {dev_oracle:.3e}")
    worst_gap_dev = max(worst_gap_dev, dev_small)
    worst_oracle_dev = max(worst_oracle_dev, dev_oracle)
print(f"  range of |gap(1e-12)-limit|: see above; max {worst_gap_dev:.3e}; max oracle deviation {worst_oracle_dev:.3e}")

print("test_gap_at_an_interior_fraction docstring: 'relative to larger of 1 and gap size at fraction 0'")
for which in ("first", "second"):
    inst = T.INSTANCES[which]
    sd, cost = float(inst["noise_sd"]), float(inst["info_cost"])
    out = ref.solve_model(sd, cost)
    lam = out["informed_fraction"]
    if 0 < lam < 1:
        print(f"  {which}: lambda* {lam:.12f}, |reported gap - oracle gap at lambda*| = {abs(out['indifference_gap'] - T.oracle_gap(lam, sd, cost)):.3e}, oracle gap at 0 = {T.oracle_gap(0.0, sd, cost):+.6e}")
    else:
        print(f"  {which}: lambda* = {lam} (not interior)")

print("test_small_noise / tiny: sample instance gap checks")
for sd, cost in [(1e-6, 0.13), (1e-9, 0.13), (1e-11, 0.15), (1e-40, 0.15)]:
    out = ref.solve_model(sd, cost)
    print(f"  sd {sd} cost {cost}: lambda* {out['informed_fraction']:.6e}")
