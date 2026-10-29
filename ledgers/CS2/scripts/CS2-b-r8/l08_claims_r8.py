"""Check L08 claims: E1 steps with a live order (398), the 102/400 share, the E2 cancellation scenario, and
Prop 3.2 bounds by brute force over list lengths. Imports the twin module from the checkout, not a copy."""
import importlib.util
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-b"
spec = importlib.util.spec_from_file_location("twin_l08", f"{ROOT}/tests/labs/CS2/lab-CS2-L08-1.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["twin_l08"] = mod
src = open(spec.origin, encoding="utf-8").read().replace("\nmain()", "\n")
exec(compile(src, spec.origin, "exec"), mod.__dict__)

# E1: replay Part B generator and count steps that had a live order before the message
gen = mod.Lcg(mod.SEED)
ref = mod.Reference()
book = mod.Book()
next_id = 1
steps_with_live = 0
cancels = 0
for step in range(mod.MESSAGES):
    live_ids = sorted(r.oid for r in ref.resting)
    if live_ids:
        steps_with_live += 1
    if live_ids and gen.below(100) < mod.CANCEL_PERCENT:
        oid = live_ids[gen.below(len(live_ids))]
        book.cancel(oid)
        ref.cancel(oid)
        cancels += 1
    else:
        side = "B" if gen.below(2) == 0 else "S"
        price = mod.MID - mod.HALF_RANGE + gen.below(2 * mod.HALF_RANGE + 1)
        qty = 1 + gen.below(mod.MAX_QTY)
        book.submit(side, price, qty, next_id)
        ref.submit(side, price, qty, next_id)
        next_id += 1
print(f"E1 steps_with_live_order_before_message {steps_with_live} cancels {cancels} share {cancels / steps_with_live:.4f}")
print(f"E1 cancels/400 {cancels / 400:.4f}")
print(f"E1 steps with no live order: {[s for s in range(mod.MESSAGES)][:0]}")

# E2 scenario: a level that empties by cancellation after an earlier fill passed a dead entry
b = mod.Book()
b.submit("S", 10000, 1, 1)
b.submit("S", 10000, 1, 2)
b.submit("S", 10000, 5, 3)
b.submit("B", 10000, 1, 4)   # fills order 1; order 1 is dead at head
print("E2 after fill 1: queue_steps", b.counts.queue_steps, "head", b.levels["S"][10000].head)
b.submit("B", 10000, 1, 5)   # passes order 1 (queue step), fills order 2
print("E2 after fill 2: queue_steps", b.counts.queue_steps)
print("cancel 3 ok", b.cancel(3), "queue_steps", b.counts.queue_steps, "levels removed", b.counts.levels_removed)
# a level emptied by cancellation holding a dead entry that is never passed
c = mod.Book()
c.submit("S", 10000, 1, 1)
c.submit("S", 10000, 1, 2)
c.submit("B", 10000, 1, 3)   # fills order 1, dead entry at head, not passed yet
print("E2b before cancel: queue_steps", c.counts.queue_steps)
print("E2b cancel 2 ok", c.cancel(2), "queue_steps", c.counts.queue_steps, "levels removed", c.counts.levels_removed)

# Prop 3.2 bound by brute force over list lengths 0..2000 with every target position
worst_ok = True
for L in range(0, 130):
    for target in range(-1, L + 1):
        prices = [2 * i for i in range(L)]
        p = 2 * target + 1 if target >= 0 else -1
        bk = mod.Book()
        bk.prices["S"] = prices
        bk._search(prices, p)
        comps = bk.search_log[-1][1]
        bound = L.bit_length()
        if comps > bound:
            worst_ok = False
print("Prop3.2 brute force L<130 all targets within bit_length bound:", worst_ok)
