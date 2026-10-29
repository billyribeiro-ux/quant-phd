"""Re-derive L08 Lab 1 stream claims (E1 live-order steps, E2 dead-entry passes) from the twin code.

Usage: python -I this.py <path-to-twin>. Loads the twin without its final main() call.
"""
import sys
import pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
assert src.rstrip().endswith("main()")
src = src.rstrip()[: -len("main()")]
import types
mod = types.ModuleType("twin_noMain")
sys.modules["twin_noMain"] = mod
ns = mod.__dict__
exec(compile(src, "twin", "exec"), ns)
MESSAGES, CANCEL_PERCENT, SEED, MID, HALF_RANGE, MAX_QTY = (ns[k] for k in ["MESSAGES", "CANCEL_PERCENT", "SEED", "MID", "HALF_RANGE", "MAX_QTY"])
Lcg, Book, Reference = ns["Lcg"], ns["Book"], ns["Reference"]
print("MESSAGES", MESSAGES, "CANCEL_PERCENT", CANCEL_PERCENT)

gen = Lcg(SEED)
book, ref = Book(), Reference()
next_id = 1
live_steps = 0
no_live_steps = []
cancels = 0
cancel_on_live = 0
for step in range(MESSAGES):
    live_ids = sorted(r.oid for r in ref.resting)
    if not live_ids:
        no_live_steps.append(step)
    if live_ids and gen.below(100) < CANCEL_PERCENT:
        oid = live_ids[gen.below(len(live_ids))]
        assert book.cancel(oid) and ref.cancel(oid)
        cancels += 1
    else:
        side = "B" if gen.below(2) == 0 else "S"
        price = MID - HALF_RANGE + gen.below(2 * HALF_RANGE + 1)
        qty = 1 + gen.below(MAX_QTY)
        book.submit(side, price, qty, next_id)
        ref.submit(side, price, qty, next_id)
        next_id += 1
print("cancels", cancels, "new orders", next_id - 1, "total", cancels + next_id - 1)
print("steps with no live order before the step:", no_live_steps)
print("steps with a live order:", MESSAGES - len(no_live_steps), "cancel share of those:", f"{cancels}/{MESSAGES - len(no_live_steps)} = {100*cancels/(MESSAGES-len(no_live_steps)):.4f}%")
print("cancel share of all messages:", f"{cancels}/{MESSAGES} = {100*cancels/MESSAGES:.4f}%")
print("queue_steps", book.counts.queue_steps, "orders_added", book.counts.orders_added)
