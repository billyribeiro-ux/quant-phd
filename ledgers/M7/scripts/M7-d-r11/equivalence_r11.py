"""Round-11 evidence: value of each term that the certificate mutants drop, on the reference output, seeds 0-49.

Imported from a scratch copy of the reference solver, so the grader directory is not modified.
"""

import copy
import json
import sys

sys.path.insert(0, sys.argv[1])
import constrained_allocator as sol
from instance import make_instance

rows = []
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = sol.allocate(copy.deepcopy(case))
    w, m = out["weights"], out["multipliers"]
    n = len(w)
    d = [w[i] - case["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    turnover_gap = sum(t) - case["turnover_limit"]
    budget_gap = abs(sum(w) - 1.0)
    kappa_term = m["turnover_total"] * turnover_gap
    dual_min_all = min(
        min(m["lower"]),
        min(m["upper"]),
        min(m["sector"]),
        min(m["turnover_plus"]),
        min(m["turnover_minus"]),
        m["turnover_total"],
    )
    dual_min_bounds = min(min(m["lower"]), min(m["upper"]))
    cs_signed = max(
        [m["lower"][i] * (case["lower"][i] - w[i]) for i in range(n)]
        + [m["upper"][i] * (w[i] - case["upper"][i]) for i in range(n)]
        + [m["turnover_plus"][i] * (d[i] - t[i]) for i in range(n)]
        + [m["turnover_minus"][i] * (-d[i] - t[i]) for i in range(n)]
    )
    rows.append(
        (
            seed,
            budget_gap,
            max(turnover_gap, 0.0),
            abs(kappa_term),
            dual_min_all,
            dual_min_bounds,
            cs_signed,
            out["certificate"],
        )
    )
print("max budget gap |sum w - 1|:", max(r[1] for r in rows))
print("max turnover excess max(0, sum|d| - tau):", max(r[2] for r in rows))
print("max |kappa * (sum t - tau)|:", max(r[3] for r in rows))
print("min over all inequality multipliers:", min(r[4] for r in rows))
print("min over lower/upper multipliers:", min(r[5] for r in rows))
print("max of signed CS sum (not absolute), lower/upper/turnover rows:", max(r[6] for r in rows))
print("certificate dual_residual, max over seeds:", max(r[7]["dual_residual"] for r in rows))
print("certificate primal_residual, max over seeds:", max(r[7]["primal_residual"] for r in rows))
