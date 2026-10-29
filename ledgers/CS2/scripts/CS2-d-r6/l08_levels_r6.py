"""Count the price levels and resting orders left in the L08 Part C book (same stream as Part B)."""
import sys
src = open(sys.argv[1], encoding="utf-8").read()
src = src.rsplit("\nmain()", 1)[0] if "\nmain()" in src else src
import types
mod = types.ModuleType("twin")
sys.modules["twin"] = mod
ns = mod.__dict__
exec(compile(src, sys.argv[1], "exec"), ns)
Book, Lcg, SEED, MESSAGES, CANCEL_PERCENT = ns["Book"], ns["Lcg"], ns["SEED"], ns["MESSAGES"], ns["CANCEL_PERCENT"]
MID, HALF_RANGE, MAX_QTY, Reference = ns["MID"], ns["HALF_RANGE"], ns["MAX_QTY"], ns["Reference"]
gen = Lcg(SEED); book, ref = Book(), Reference(); next_id = 1
for _ in range(MESSAGES):
    live_ids = sorted(r.oid for r in ref.resting)
    if live_ids and gen.below(100) < CANCEL_PERCENT:
        oid = live_ids[gen.below(len(live_ids))]
        book.cancel(oid); ref.cancel(oid)
    else:
        side = "B" if gen.below(2) == 0 else "S"
        price = MID - HALF_RANGE + gen.below(2 * HALF_RANGE + 1)
        qty = 1 + gen.below(MAX_QTY)
        book.submit(side, price, qty, next_id); ref.submit(side, price, qty, next_id)
        next_id += 1
levels_now = sum(len(v) for v in book.levels.values())
print("levels created", book.counts.levels_created, "removed", book.counts.levels_removed, "levels present", levels_now,
      "price lists", {k: len(v) for k, v in book.prices.items()}, "live orders", len(book.live))
print("best", book.best("B"), book.best("S"))
