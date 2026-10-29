"""Round 13: smallest inequality multiplier of the reference certificate, seeds 0-49, read from the current checkout."""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GRADER = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "course", "modules", "M", "M7", "grader"))
sys.path.insert(0, GRADER)
import reference as ref
from instance import make_instance
zeros = 0
positive = []
vals = []
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = ref.allocate(copy.deepcopy(case))
    m = out["multipliers"]
    mins = min(min(m["lower"]), min(m["upper"]), min(m["sector"]), min(m["turnover_plus"]), min(m["turnover_minus"]), m["turnover_total"])
    vals.append(mins)
    zeros += mins == 0
    if mins > 0:
        positive.append(seed)
print("seeds with min inequality multiplier == 0:", zeros, "of 50")
print("seeds with min inequality multiplier > 0:", positive)
print("smallest min over seeds:", min(vals), " largest min over seeds:", max(vals))
