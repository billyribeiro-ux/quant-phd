"""Verifier control (round 17): the sweep checker must reject perturbed outputs."""
import copy
import json
import sys
from pathlib import Path

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD17-M7-d"
sys.argv = ["v17_sweep.py", ROOT, "0", "0"]
sys.path.insert(0, str(Path(ROOT, "ledgers/M7/scripts/M7-d-r17")))
import v17_sweep as sw  # noqa: E402
from instance import make_instance  # noqa: E402

for seed in (0, 5, 17):
    case = json.loads(make_instance(seed)["payload"])
    out = sw.ref.allocate(copy.deepcopy(case))
    base = sw.check(case, out)
    o1 = copy.deepcopy(out); o1["weights"][0] += 1e-7
    o2 = copy.deepcopy(out); o2["certificate"]["complementary_slackness"] += 1e-8
    o3 = copy.deepcopy(out); o3["multipliers"]["budget"] += 1e-6
    print(seed, "base", base, "| w+1e-7", sw.check(case, o1)[:2], "| cs+1e-8", sw.check(case, o2)[:2], "| budget+1e-6", sw.check(case, o3)[:2])
