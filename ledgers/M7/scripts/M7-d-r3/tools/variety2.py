import json, sys
sys.path.insert(0, sys.argv[1])
import constrained_allocator as ref
from instance import make_instance
from collections import Counter
kinds = Counter(); patterns = set(); per_kind_seeds = {"lower": set(), "upper": set(), "sector": set(), "turn": set()}
for s in range(50):
    case = json.loads(make_instance(s)["payload"])
    out = ref.allocate(case)
    m = out["multipliers"]
    active = []
    for name in ("lower", "upper", "sector"):
        for idx, v in enumerate(m[name]):
            if v != 0:
                active.append((name, idx))
                per_kind_seeds[name].add(s)
    if any(v != 0 for v in m["turnover_plus"] + m["turnover_minus"]) or m["turnover_total"] != 0:
        per_kind_seeds["turn"].add(s)
        active.append(("turn", m["turnover_total"] != 0))
    patterns.add(tuple(active))
print("distinct active-set patterns over seeds 0-49 (by multiplier index):", len(patterns))
print("seeds where each kind has a nonzero multiplier:", {k: len(v) for k, v in per_kind_seeds.items()})
