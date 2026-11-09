"""For seeds 0-49: the instance shape, and which constraints bind in the reference answer (multipliers > 0 or residual 0).

Usage: python -I instances_v12.py <repo_root>
"""

import json
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402
from reference import allocate  # noqa: E402

distinct = set()
binding_caps = []
binding_turn = 0
for seed in range(50):
    case = json.loads(make_instance(seed)["payload"])
    out = allocate(case)
    w = out["weights"]
    m = out["multipliers"]
    distinct.add(tuple(round(x, 12) for x in w))
    n = len(w)
    at_bound = sum(1 for i in range(n) if abs(w[i] - case["lower"][i]) < 1e-9 or abs(w[i] - case["upper"][i]) < 1e-9)
    cap_bind = []
    for k in range(len(case["sector_caps"])):
        s = sum(w[i] for i in range(n) if case["sector"][i] == k)
        if abs(s - case["sector_caps"][k]) < 1e-9:
            cap_bind.append(k)
    if cap_bind:
        binding_caps.append((seed, cap_bind))
    if m["turnover_total"] > 1e-9:
        binding_turn += 1
    if seed < 6 or seed % 10 == 0:
        print(f"seed {seed}: n={n} Z={len(case['sector_caps'])} gamma={case['gamma']} weights={[round(x, 4) for x in w]} "
              f"at_bound={at_bound} caps_binding={cap_bind} turnover_binding={m['turnover_total'] > 1e-9}")
print("distinct weight vectors over seeds 0-49:", len(distinct))
print("seeds with a sector cap binding in the reference answer:", len(binding_caps), binding_caps[:12])
print("seeds with turnover constraint binding (kappa > 0):", binding_turn)
