import sys
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/quant-b2/course/modules/M/M7/grader")
import instance, reference as R

rows = []
for seed in range(0, 300):
    case = __import__("json").loads(instance.make_instance(seed)["payload"])
    p = R._parse(case)
    sol = R._solve(p)
    box = sol["lower"] + sol["upper"]
    ineq = box + sol["sector"] + sol["plus"] + sol["minus"] + [sol["kappa"]]
    zeros_box = sum(1 for v in box if v == 0)
    budget_gap = sum(sol["w"], Fraction(0)) - 1
    cert = R._certificate(p, sol)
    rows.append((seed, p.n, min(ineq), zeros_box, p.n + 1, budget_gap, cert["complementary_slackness"], cert["dual_residual"], min(sol["kappa"], 0)))
bad = [r for r in rows if r[2] != 0 or r[3] < r[4] or r[5] != 0 or r[6] != 0.0 or r[7] != 0.0]
print("seeds checked:", len(rows))
print("min inequality multiplier > 0 on any seed:", any(r[2] > 0 for r in rows))
print("min zero-box count minus (n+1) over seeds:", min(r[3] - r[4] for r in rows))
print("exact budget gap nonzero on seeds:", sum(1 for r in rows if r[5] != 0))
print("CS nonzero:", sum(1 for r in rows if r[6] != 0.0), "dual nonzero:", sum(1 for r in rows if r[7] != 0.0))
print("kappa negative:", sum(1 for r in rows if r[8] < 0))
print("bad:", bad[:5])
print("seeds 0-49 min multiplier==0 count:", sum(1 for r in rows[:50] if r[2] == 0))
