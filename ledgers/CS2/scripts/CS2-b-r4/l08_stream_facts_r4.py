"""Verifier round 4: facts about the L08 twin's seeded stream that page prose states.

Loads the twin's classes (everything before its trailing main() call) and replays Part B's stream,
recording, for each step, whether a live order existed before the message (E1 claim: steps with a live
order = 398, and only the first and third messages have none), and the book's level count at the end.
Run: python3 -I l08_stream_facts_r4.py <path-to-twin>
"""
import sys

src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0]
ns: dict = {"__name__": "twin"}
exec(compile(src, sys.argv[1], "exec"), ns)  # the twin's own definitions only

Lcg, Book, Reference, MESSAGES, CANCEL_PERCENT, MID, HALF_RANGE, MAX_QTY, SEED = (
    ns[k] for k in ("Lcg", "Book", "Reference", "MESSAGES", "CANCEL_PERCENT", "MID", "HALF_RANGE", "MAX_QTY", "SEED")
)

gen = Lcg(SEED)
book, ref = Book(), Reference()
next_id = 1
no_live_steps = []
cancels = 0
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
        bt = book.submit(side, price, qty, next_id)
        rt = ref.submit(side, price, qty, next_id)
        assert bt == rt
        next_id += 1
print("steps with no live order before the message (0-based):", no_live_steps, "count", len(no_live_steps))
print("steps with a live order:", MESSAGES - len(no_live_steps), "cancels", cancels, "share of all", round(100 * cancels / MESSAGES, 2), "share of live steps", round(100 * cancels / (MESSAGES - len(no_live_steps)), 2))
print("book levels at end (both sides):", sum(len(v) for v in book.levels.values()), "resting orders", len(book.live))
print("counts:", book.counts)
print("search_log entries:", len(book.search_log), "max comparisons", max(c for _, c in book.search_log))
print("levels created", book.counts.levels_created, "removed", book.counts.levels_removed)
