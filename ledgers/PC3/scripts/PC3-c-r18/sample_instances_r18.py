"""Round 18, PC3 slice c. Samples 20 seeds: each instance valid, and instances differ materially (paths and arrivals)."""

from __future__ import annotations

import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c/course/modules/PC/PC3/grader")

from instance import ARRIVAL_NAMES, make_instance  # noqa: E402

SEEDS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 49, 50, 77, 100, 255, 1000, 4096, 7919, 77314143, 2061445586, 123456789]
paths: set[tuple[int, ...]] = set()
arrivals: set[tuple[str, ...]] = set()
for s in SEEDS:
    inst = make_instance(s)
    p = inst["fair_path_cents"]
    a = inst["arrivals"]
    assert len(p) == 21 and p[0] == 10_000 and all(type(v) is int and v > 0 for v in p), s
    assert all(abs(p[i + 1] - p[i]) == 5 for i in range(20)), s
    assert len(a) == 20 and set(a) <= set(ARRIVAL_NAMES), s
    assert inst["settlement_cents"] == p[20] and inst["seed"] == s, s
    assert make_instance(s) == inst, s
    paths.add(tuple(p))
    arrivals.add(tuple(a))
    print(f"seed {s}: settlement {p[20]} cents, moves up {sum(1 for i in range(20) if p[i+1] > p[i])}, "
          f"informed {a.count('informed')}, uninformed-buy {a.count('uninformed-buy')}, "
          f"uninformed-sell {a.count('uninformed-sell')}")
print(f"valid: 20 of 20 sampled seeds; distinct fair paths: {len(paths)}; distinct arrival sequences: {len(arrivals)}")
