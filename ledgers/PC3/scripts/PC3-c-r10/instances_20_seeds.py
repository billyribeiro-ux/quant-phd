"""Round 10 verifier: sample 20 seeds (0-19 and 848197495 among them is not needed); check every instance is valid and
that the reference rule's replay numbers differ across seeds (the answers change, not only the labels). Reads the repo
grader files by path; stdlib only; writes nothing."""

import importlib.util
import sys

GRADER = "/Users/billyribeiro/.fanout/wt/verifyE10-PC3-c/course/modules/PC/PC3/grader"
sys.path.insert(0, GRADER)
import engine  # noqa: E402
import instance  # noqa: E402
import reference  # noqa: E402

rows = []
for seed in range(20):
    inst = instance.make_instance(seed)
    path = inst["fair_path_cents"]
    assert len(path) == 21 and path[0] == 10_000 and all(v > 0 for v in path)
    assert all(abs(path[i + 1] - path[i]) == 5 for i in range(20))
    assert len(inst["arrivals"]) == 20 and set(inst["arrivals"]) <= set(instance.ARRIVAL_NAMES)
    log = engine.play(reference.quote, seed)
    out = reference.replay(log)
    rows.append((seed, path[-1], out["cash_flow_cents"], out["inventory_end"], out["pnl_cents"]))
for r in rows:
    print("seed %2d settlement %5d cash_flow %6d inventory_end %2d pnl %5d" % r)
print("distinct pnl over 20 seeds:", len({r[4] for r in rows}), "| distinct settlements:", len({r[1] for r in rows}))
