"""Sample seeds 0-19 and 100-119: validity of each instance, and whether the reference P&L differs across seeds.

Usage: python -I sample_instances_r16.py <grader dir>
"""
import sys

sys.path.insert(0, sys.argv[1])
import engine  # noqa: E402
import reference  # noqa: E402
from instance import make_instance  # noqa: E402

seeds = list(range(20)) + list(range(100, 120))
pnls = {}
ok = True
for s in seeds:
    inst = make_instance(s)
    path, arr = inst["fair_path_cents"], inst["arrivals"]
    valid = len(path) == 21 and path[0] == 10_000 and all(abs(b - a) == 5 for a, b in zip(path, path[1:])) and len(arr) == 20 and set(arr) <= {"uninformed-buy", "uninformed-sell", "informed"} and all(v > 0 for v in path)
    ok = ok and valid
    log = engine.play(reference.quote, s)
    r = reference.replay(log)
    pnls[s] = (r["pnl_cents"], r["cash_flow_cents"], r["inventory_end"], tuple(path[-3:]))
print("all valid:", ok)
print("distinct (pnl, cash, inventory, last fair values):", len({v for v in pnls.values()}), "of", len(seeds))
print("distinct pnl:", len({v[0] for v in pnls.values()}))
print("sample:", {s: pnls[s][0] for s in seeds[:8]})
