"""Round 17: |reported gap - oracle gap at the reported fraction| for the reference solver at interior fractions, with
the suite's own oracle (test_project.oracle_gap, imported from a scratch workspace by suite_workspace_r17.py).
Inputs: 150 pairs sampled from the autograder box (seed 17) plus the point (0.6697478991596639, 0.12436974789915967).
Usage: oracle_gap_precision.py <checkout>"""
import importlib.util as u
import random
import sys
from pathlib import Path

root = sys.argv[1]
sys.path.insert(0, str(Path(root, "ledgers/E4/scripts/E4-d-r17")))
from suite_workspace_r17 import make_workspace  # noqa: E402

make_workspace(root, f"{root}/course/modules/E/E4/grader/reference.py")
import test_project as T  # noqa: E402  (the suite's oracle)

spec = u.spec_from_file_location("ref", f"{root}/course/modules/E/E4/grader/reference.py")
R = u.module_from_spec(spec)
spec.loader.exec_module(R)
rng = random.Random(17)
cases = [(round(rng.uniform(0.5, 0.75), 3), round(rng.uniform(0.12, 0.15), 3)) for _ in range(150)]
cases.append((0.6697478991596639, 0.12436974789915967))
worst = (0.0, None)
interior = 0
above = 0
for sd, c in cases:
    out = R.solve_model(sd, c)
    lam = out["informed_fraction"]
    if not (0.0 < lam < 1.0):
        continue
    interior += 1
    d = abs(out["indifference_gap"] - T.oracle_gap(lam, sd, c))
    if d > 1e-14:
        above += 1
    if d > worst[0]:
        worst = (d, (sd, c, lam))
print("interior cases", interior, "of", len(cases))
print("largest |reported - oracle| at reported fraction", worst[0], "at (sd, c, lambda) =", worst[1])
print("count above 1e-14:", above)
