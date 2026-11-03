"""Round-2 check: reference solver on seeds 0-299, exact multiplier minimum, and start-portfolio answers."""
import sys
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/grader")
import reference as R
from instance import make_instance
import json

start_eq = []
min_zero = []
min_nonzero = []
iters = {}
for seed in range(300):
    case = json.loads(make_instance(seed)["payload"])
    prob = R._parse(case)
    rows = R._inequalities(prob)
    x, mult, budget = R._active_set(prob, rows)
    sol = R._solve(prob)
    mins = min([*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]])
    if seed < 50:
        (min_zero if mins == 0 else min_nonzero).append(seed)
    if all(x[i] == prob.w0[i] for i in range(prob.n)):
        start_eq.append(seed)
    if min(mins, 0) < 0:
        print("NEGATIVE MIN", seed, mins)
print("seeds 0-49 min multiplier exactly 0:", len(min_zero), "nonzero:", min_nonzero)
print("answer equals starting portfolio (exact) on seeds 0-299:", start_eq)
