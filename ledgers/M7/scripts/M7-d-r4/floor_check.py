"""Smallest inequality multiplier of the reference solution over seeds 0-999 and the hand cases of test_project.py."""
import sys, json, copy, re, math
grader = sys.argv[1]
sys.path.insert(0, grader)
import reference as ref
from instance import make_instance

def smallest(out):
    m = out["multipliers"]
    vals = m["lower"] + m["upper"] + m["sector"] + m["turnover_plus"] + m["turnover_minus"] + [m["turnover_total"]]
    return min(vals)

zero_seeds, positive_seeds, nonzero_neg = [], [], []
for s in range(1000):
    case = json.loads(make_instance(s)["payload"])
    out = ref.allocate(case)
    mn = smallest(out)
    if mn > 0:
        positive_seeds.append((s, mn))
    elif mn == 0:
        zero_seeds.append(s)
    else:
        nonzero_neg.append((s, mn))
print("seeds 0-999: min multiplier == 0:", len(zero_seeds), "; > 0:", len(positive_seeds), positive_seeds[:10], "; < 0:", len(nonzero_neg))
print("first 50 seeds all zero:", all(s in zero_seeds for s in range(50)))

# hand cases copied from test_project.py source by exec of the HAND_CASES block
src = open(grader + "/test_project.py", encoding="utf-8").read()
start = src.index("def hand_case(")
end = src.index("# ----", src.index("HAND_CASES"))
ns = {"Any": object, "__builtins__": __builtins__}
exec("from typing import Any\n" + src[start:end], ns)
for name, (case, expected) in ns["HAND_CASES"].items():
    out = ref.allocate(copy.deepcopy(case))
    print("hand", name, "weights", out["weights"], "expected", expected, "smallest multiplier", smallest(out),
          "multipliers", {k: v for k, v in out["multipliers"].items()})
