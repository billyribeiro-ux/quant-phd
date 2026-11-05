"""Re-checks the test_draws_depend_on_the_instance_seed comment over the grids the test uses (4, 8, 16, 32, 64) and
seeds 0..49, and reports the smallest own-level tail among seeds 0..49."""

from __future__ import annotations

import math
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-SC1-d/course/modules/SC/SC1/grader")
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

rows = []
for seed in range(50):
    inst = make_instance(seed)
    tail = math.erfc(inst["a"] / math.sqrt(2.0 * inst["H"]))
    zero_grids = [g for g in (4, 8, 16, 32, 64) if ref.discrete_max_exceedance(inst, g)[0] == 0.0]
    rows.append((tail, seed, inst["a"], inst["H"], inst["n_paths"], zero_grids))
rows.sort()
for tail, seed, a, h, n, zg in rows[:6]:
    print(f"seed {seed:2d}: tail {tail:.3e}, a {a}, H {h}, N {n}, grids with zero estimate at own level: {zg}")
print("seeds with at least one zero grid at own level:", [r[1] for r in rows if r[5]])
both = []
for seed in range(50):
    a = make_instance(seed)
    b = make_instance(seed + 7_919)
    for g in (4, 8, 16, 32, 64):
        if ref.discrete_max_exceedance(a, g)[0] == 0.0 and ref.discrete_max_exceedance(b, g)[0] == 0.0:
            both.append((seed, g))
print("(seed, grid) pairs where own-level estimates for seed and seed+7919 are both 0:", both)
