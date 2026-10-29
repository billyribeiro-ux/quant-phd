"""List the message indices (0-based) of Part B that begin with no live order, replaying the seeded stream."""
import importlib.util
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b"
spec = importlib.util.spec_from_file_location("twin_l08", f"{ROOT}/tests/labs/CS2/lab-CS2-L08-1.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["twin_l08"] = mod
src = open(spec.origin, encoding="utf-8").read().replace("\nmain()", "\n")
exec(compile(src, spec.origin, "exec"), mod.__dict__)
gen = mod.Lcg(mod.SEED)
ref = mod.Reference()
next_id = 1
empty_steps = []
for step in range(mod.MESSAGES):
    live_ids = sorted(r.oid for r in ref.resting)
    if not live_ids:
        empty_steps.append(step)
    if live_ids and gen.below(100) < mod.CANCEL_PERCENT:
        oid = live_ids[gen.below(len(live_ids))]
        ref.cancel(oid)
    else:
        side = "B" if gen.below(2) == 0 else "S"
        price = mod.MID - mod.HALF_RANGE + gen.below(2 * mod.HALF_RANGE + 1)
        qty = 1 + gen.below(mod.MAX_QTY)
        ref.submit(side, price, qty, next_id)
        next_id += 1
print("steps (0-based) with no live order before the message:", empty_steps)
