"""Sample 20 seeds (0,3,...,57 mod 50 spread) and report the reference answers, to see that the answers change with the seed."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/PC/PC3/grader"))
import engine, reference, instance  # noqa: E401,E402

seeds = [0, 2, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 3, 9, 21, 33]
rows = []
for s in seeds:
    log = engine.play(reference.quote, s)
    out = reference.replay(log)
    inst = instance.make_instance(s)
    rows.append((s, len([t for t in log["turns"] if t["filled"]]), out["cash_flow_cents"], out["inventory_end"], out["pnl_cents"], inst["settlement_cents"]))
for r in rows:
    print("seed %2d fills %2d cash %6d inv %2d pnl %5d settlement %6d" % r)
print("distinct pnl over 20 sampled seeds:", len({r[4] for r in rows}), "of", len(rows))
print("distinct pnl over 50 fixed seeds:", len({reference.replay(engine.play(reference.quote, s))["pnl_cents"] for s in range(50)}))
