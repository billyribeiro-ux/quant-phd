"""Round-8 re-derivation of the sin ratio claim (project.html:226): plain central quotient at the instance points x0 of seeds 0-49 (two instances per seed)."""
import math
import sys

sys.path.insert(0, sys.argv[1])
from instance import make_instance  # noqa: E402

pts = []
for seed in range(50):
    for s in (seed, seed + 7919):
        pts.append(make_instance(s)["x0"])
lo, hi = float("inf"), 0.0
ratios = []
for x0 in pts:
    e1 = abs((math.sin(x0 + 1e-2) - math.sin(x0 - 1e-2)) / 2e-2 - math.cos(x0))
    e2 = abs((math.sin(x0 + 5e-3) - math.sin(x0 - 5e-3)) / 1e-2 - math.cos(x0))
    r = e1 / e2
    lo, hi = min(lo, r), max(hi, r)
print("points:", len(pts), "distinct:", len(set(pts)))
print(f"central-quotient error ratio (step 1e-2 over step 5e-3): min {lo:.7f} max {hi:.7f}")
