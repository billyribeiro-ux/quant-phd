import sys, json
sys.path.insert(0, "/tmp/m7d_r14_collect")
import constrained_allocator as sol
from instance import make_instance
same = []; minmult_pos = []; cs_nonzero = []; minzero_fail = []; errs = []
for seed in range(300):
    case = json.loads(make_instance(seed)["payload"])
    try:
        out = sol.allocate(case)
    except Exception as e:
        errs.append((seed, repr(e))); continue
    w = out["weights"]; m = out["multipliers"]
    if all(abs(a - b) == 0 for a, b in zip(w, case["w0"])):
        same.append(seed)
    ineq = list(m["lower"]) + list(m["upper"]) + list(m["sector"]) + list(m["turnover_plus"]) + list(m["turnover_minus"]) + [m["turnover_total"]]
    if min(ineq) > 0: minmult_pos.append(seed)
    if min(ineq) != 0: minzero_fail.append((seed, min(ineq)))
    if out["certificate"]["complementary_slackness"] != 0: cs_nonzero.append(seed)
print("seeds run 0-299 errors:", errs)
print("w == w0 seeds:", same)
print("seeds with all inequality multipliers positive:", minmult_pos)
print("seeds with min inequality multiplier != 0:", minzero_fail[:5], len(minzero_fail))
print("seeds with CS certificate != 0:", cs_nonzero[:5], len(cs_nonzero))
