"""Round 6 (M7-d): per seed 0-49, the instance shape (n, sector labels, caps), the reference answer's binding constraints
(count of non-zero inequality multipliers and of the bound and turnover rows that bind), and whether the answer differs
from the seed's starting portfolio. Uses the grader's reference and instance modules, read-only, under python -I."""

import json
import sys

sys.path.insert(0, sys.argv[1])
import reference as ref  # noqa: E402
from instance import make_instance  # noqa: E402

rows = []
distinct = set()
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = ref.allocate(case)
    n = len(case["mu"])
    m = out["multipliers"]
    nonzero = sum(1 for key in ("lower", "upper", "sector", "turnover_plus", "turnover_minus") for v in m[key] if v != 0) + (1 if m["turnover_total"] != 0 else 0)
    turn_binding = abs(sum(abs(w - w0) for w, w0 in zip(out["weights"], case["w0"])) - case["turnover_limit"]) <= 1e-12
    moved = max(abs(w - w0) for w, w0 in zip(out["weights"], case["w0"])) > 1e-9
    distinct.add(tuple(round(w, 9) for w in out["weights"]))
    rows.append((seed, n, len(case["sector_caps"]), nonzero, turn_binding, moved, out["certificate"]["stationarity_residual"] <= 1e-8))
print("seed n Z nonzero_multipliers turnover_binding answer_differs_from_w0 certificate_ok")
for r in rows:
    print(*r)
print("distinct answers over seeds 0-49:", len(distinct))
print("seeds with turnover binding:", sum(r[4] for r in rows), " seeds with >=1 nonzero multiplier:", sum(1 for r in rows if r[3] > 0))
print("seeds with n=3,4,5:", {k: sum(1 for r in rows if r[1] == k) for k in (3, 4, 5)})
