import re, types
def load(path):
    src = open(path, encoding="utf-8").read()
    src = re.sub(r"\nmain\(\)\s*$", "\n", src)
    mod = types.ModuleType("twin")
    import sys; sys.modules["twin"] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod
base = "/Users/billyribeiro/.fanout/wt/verifyB6-CS2-b/tests/labs/CS2/"
l07 = load(base + "lab-CS2-L07-1.py")
g = l07.Lcg(l07.SEED); l07.make_lcs_instances(g); cases = l07.make_coin_instances(g)
print("L07 impossible (lab order of generator)", sum(1 for d, a in cases if l07.coins_table(d, a)[0] is None), "of", len(cases))

l08 = load(base + "lab-CS2-L08-1.py")
# Scenario: a level emptied by fills, after a cancelled front entry.
b = l08.Book()
b.submit("S", 10000, 1, 1)   # order 1 rests
b.submit("S", 10000, 1, 2)   # order 2 rests behind it
b.cancel(1)                  # order 1 becomes a dead entry at the head
print("before buy: queue_steps", b.counts.queue_steps, "levels_removed", b.counts.levels_removed)
b.submit("B", 10000, 1, 3)   # fills order 2 (the last live order at the level)
print("after fill-emptied level: queue_steps", b.counts.queue_steps, "levels_removed", b.counts.levels_removed, "levels now", b.prices["S"])

# Full stream from Part B/C: levels remaining and how many queue steps happened at levels later removed by a fill.
g = l08.Lcg(l08.SEED); book = l08.Book(); ref = l08.Reference(); nid = 1
for _ in range(l08.MESSAGES):
    live = sorted(r.oid for r in ref.resting)
    if live and g.below(100) < l08.CANCEL_PERCENT:
        oid = live[g.below(len(live))]; book.cancel(oid); ref.cancel(oid)
    else:
        side = "B" if g.below(2) == 0 else "S"
        price = l08.MID - l08.HALF_RANGE + g.below(2 * l08.HALF_RANGE + 1)
        qty = 1 + g.below(l08.MAX_QTY)
        book.submit(side, price, qty, nid); ref.submit(side, price, qty, nid); nid += 1
c = book.counts
print("stream: orders", c.orders_added, "queue_steps", c.queue_steps, "levels created", c.levels_created, "removed", c.levels_removed)
print("levels remaining", len(book.prices["B"]) + len(book.prices["S"]), "live", len(book.live))
print("binary searches", len(book.search_log), "max cmp", max(x for _, x in book.search_log))
