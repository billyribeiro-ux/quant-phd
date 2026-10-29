import copy, json, sys
sys.path.insert(0, "/tmp/m7d_r8_minmult")
from instance import make_instance
import constrained_allocator as sol
worst = []
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = sol.allocate(copy.deepcopy(case))
    m = out["multipliers"]
    vals = list(m["lower"]) + list(m["upper"]) + list(m["sector"]) + list(m["turnover_plus"]) + list(m["turnover_minus"]) + [m["turnover_total"]]
    worst.append((min(float(v) for v in vals), seed))
print("seeds (of 0-49) with min inequality multiplier > 0:", [s for v, s in worst if v > 0])
print("smallest min multiplier over 50 seeds:", min(worst))
print("seeds with min == 0.0:", sum(1 for v, s in worst if v == 0.0), "of 50")
