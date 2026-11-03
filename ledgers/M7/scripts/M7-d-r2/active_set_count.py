"""Round-2 check of the floor claim (page: spec 'Rung 3' dual-residual paragraph): on seeds 0-299, the reference's
working set has at most n-1 inequality rows, at least n+1 of its 2n bound multipliers are zero, and the smallest
inequality multiplier is exactly zero."""
import json, sys, pathlib
G = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/grader")
sys.path.insert(0, str(G))
import reference as R
from instance import make_instance
bad_size = bad_bound = bad_min = 0
worst = 0
for seed in range(300):
    case = json.loads(make_instance(seed)["payload"])
    prob = R._parse(case)
    rows = R._inequalities(prob)
    x, mult, budget = R._active_set(prob, rows)
    n = prob.n
    worked = len(mult)
    worst = max(worst, worked - (n - 1))
    if worked > n - 1:
        bad_size += 1
    nonzero_bounds = sum(1 for k in mult if k[0] in ("lower", "upper") and mult[k] != 0)
    if 2 * n - nonzero_bounds < n + 1:
        bad_bound += 1
    sol = R._solve(prob)
    mins = min([*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]])
    if mins != 0:
        bad_min += 1
print("seeds 0-299: working set > n-1 rows:", bad_size, "| fewer than n+1 zero bound multipliers:", bad_bound,
      "| smallest multiplier != 0:", bad_min, "| max(working - (n-1)):", worst)
