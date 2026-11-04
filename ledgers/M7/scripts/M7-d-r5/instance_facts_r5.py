"""Instance facts over seeds 0-49: asset counts, sector counts, feasibility as exact decimals, distinct weight vectors."""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD5-M7-d/course/modules/M/M7/grader")
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD5-M7-d/ledgers/M7/scripts/M7-d-r5")
from instance import make_instance  # noqa: E402

counts = Counter()
feasible = 0
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    n = len(case["mu"])
    counts[n] += 1
    w0 = [F(repr(v)) for v in case["w0"]]
    lo = [F(repr(v)) for v in case["lower"]]
    up = [F(repr(v)) for v in case["upper"]]
    caps = [F(repr(v)) for v in case["sector_caps"]]
    ok = sum(w0) == 1 and all(lo[i] <= w0[i] <= up[i] for i in range(n))
    for k, c in enumerate(caps):
        ok = ok and sum(w0[i] for i in range(n) if case["sector"][i] == k) <= c
    ok = ok and case["turnover_limit"] >= 0 and len(caps) == 2 and sorted(set(case["sector"])) == [0, 1]
    feasible += bool(ok)
    assert case["gamma"] > 0
print("asset counts", dict(sorted(counts.items())), "sectors", 2, "feasible exact", feasible, "of 50")
