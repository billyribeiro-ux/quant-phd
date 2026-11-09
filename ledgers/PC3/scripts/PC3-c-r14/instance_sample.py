"""Sample 20 fixed seeds: instance validity, distinct paths, and whether the reference answers (P&L, fills) change.

Run as: python -I ledgers/PC3/scripts/PC3-c-r14/instance_sample.py <checkout-root>
"""
import sys

root = sys.argv[1]
sys.path.insert(0, f"{root}/course/modules/PC/PC3/grader")
import engine  # noqa: E402
from instance import make_instance  # noqa: E402

def rule(state):
    mid = 10_000
    for r in state["history"]:
        if r["filled"]:
            mid = r["fill_price_cents"]
    return mid - 10, mid + 10, 1

seeds = list(range(0, 50, 50 // 20 + 0))[:20]  # 0,2,4,...,38
seeds = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 1, 2, 5, 9, 25]
paths, pnls, fills = set(), [], []
for s in seeds:
    inst = make_instance(s)
    path, arr = inst["fair_path_cents"], inst["arrivals"]
    assert len(path) == 21 and path[0] == 10_000 and all(path[i+1]-path[i] in (5, -5) for i in range(20))
    assert set(arr) <= {"uninformed-buy", "uninformed-sell", "informed"} and len(arr) == 20 and min(path) > 0
    paths.add(tuple(path))
    log = engine.play(rule, s)
    cash = inv = 0
    for t in log["turns"]:
        if t["filled"]:
            p = t["fill_price_cents"]; side = 1 if p == t["bid_cents"] else -1
            cash += -side * p; inv += side
    pnls.append(cash + inv * log["settlement_cents"])
    fills.append(sum(t["filled"] for t in log["turns"]))
print("seeds", seeds)
print("distinct paths", len(paths), "of", len(seeds))
print("distinct reference P&L values", len(set(pnls)), "pnl list", pnls)
print("distinct fill counts", sorted(set(fills)), "fills list", fills)
