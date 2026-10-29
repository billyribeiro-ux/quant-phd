"""Round 11: smallest inequality multiplier of the reference certificate, seeds 0-49 (reference.py, unchanged since e8b10b8)."""
import copy, json, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB11-M7-d/course/modules/M/M7/grader")
import reference as ref
from instance import make_instance
zeros = 0
vals = []
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = ref.allocate(copy.deepcopy(case))
    m = out["multipliers"]
    mins = min(min(m["lower"]), min(m["upper"]), min(m["sector"]), min(m["turnover_plus"]), min(m["turnover_minus"]), m["turnover_total"])
    vals.append(mins)
    zeros += mins == 0
print("seeds with min inequality multiplier == 0:", zeros, "of 50")
print("smallest min over seeds:", min(vals), " largest min over seeds:", max(vals))
