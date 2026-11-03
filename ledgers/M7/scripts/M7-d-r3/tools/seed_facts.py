import json, sys
sys.path.insert(0, sys.argv[1])  # scratch dir holding instance.py and reference as constrained_allocator.py
from instance import make_instance
import constrained_allocator as ref
from fractions import Fraction
# (1) smallest inequality multiplier exactly zero on seeds 0..49 (page claim: 50 of 50)
zero = 0; ok = 0
for s in range(50):
    case = json.loads(make_instance(s)["payload"])
    out = ref.allocate(case)
    m = out["multipliers"]
    ineq = m["lower"] + m["upper"] + m["sector"] + m["turnover_plus"] + m["turnover_minus"] + [m["turnover_total"]]
    if min(ineq) == 0.0:
        zero += 1
    if out["certificate"]["dual_residual"] == 0.0:
        ok += 1
print("seeds 0-49: smallest inequality multiplier == 0 in", zero, "of 50; dual_residual == 0 in", ok, "of 50")
# (2) seeds where the reference answer equals the starting portfolio, among 0..299
hits = []
for s in range(300):
    case = json.loads(make_instance(s)["payload"])
    out = ref.allocate(case)
    w = out["weights"]
    if max(abs(a - b) for a, b in zip(w, case["w0"])) <= 1e-12:
        hits.append(s)
print("answer equals start (|dw|<=1e-12) for seeds in 0..299:", hits)
