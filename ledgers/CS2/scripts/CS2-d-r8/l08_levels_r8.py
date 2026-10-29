"""Round-7: state of the L08 book at the end of Part C (card c113: '8 levels remain ... hold the 10 resting orders').

Loads the lab twin's source without its top-level main() call, replays Part C's stream, and reports the number of
price levels still in the book and the live orders they hold. Read-only: the twin file is not modified.
"""

import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
assert src.rstrip().endswith("main()"), "expected the twin to end with a top-level main() call"
body = src.rstrip()[: -len("main()")]
import types
mod = types.ModuleType("l08_twin_r7")
sys.modules["l08_twin_r7"] = mod
ns = mod.__dict__
exec(compile(body, "lab-CS2-L08-1-no-main", "exec"), ns)
gen = ns["Lcg"](ns["SEED"])  # type: ignore[operator]
book, ref = ns["Book"](), ns["Reference"]()  # type: ignore[operator]
next_id = 1
for _ in range(ns["MESSAGES"]):  # type: ignore[index]
    live_ids = sorted(r.oid for r in ref.resting)
    if live_ids and gen.below(100) < ns["CANCEL_PERCENT"]:
        oid = live_ids[gen.below(len(live_ids))]
        book.cancel(oid)
        ref.cancel(oid)
    else:
        side = "B" if gen.below(2) == 0 else "S"
        price = ns["MID"] - ns["HALF_RANGE"] + gen.below(2 * ns["HALF_RANGE"] + 1)
        qty = 1 + gen.below(ns["MAX_QTY"])
        book.submit(side, price, qty, next_id)
        ref.submit(side, price, qty, next_id)
        next_id += 1
levels = {s: len(book.levels[s]) for s in ("B", "S")}
orders_in_levels = sum(lv.live for s in ("B", "S") for lv in book.levels[s].values())
print("levels per side at end of Part C:", levels, "total", sum(levels.values()))
print("created", book.counts.levels_created, "removed", book.counts.levels_removed)
print("live orders in book:", len(book.live), "reference resting:", len(ref.resting))
print("live orders held by the levels:", orders_in_levels)
