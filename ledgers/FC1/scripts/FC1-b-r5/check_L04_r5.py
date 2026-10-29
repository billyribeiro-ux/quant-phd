import sys, types
from fractions import Fraction
import random
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()\n", "\n")
mod = types.ModuleType("twin_defs")
sys.modules["twin_defs"] = mod
exec(compile(src, sys.argv[1], "exec"), mod.__dict__)
Order, Book = mod.Order, mod.Book
# (1) round-4 counterexample under the revised rule
b = Book()
b.match(Order(0, 1, "limit", 100, 1010))
b.match(Order(1, 1, "limit", 10, 1000))
b.pending.append(Order(2, 1, "stop", 5, None, 1005))
b.match(Order(3, -1, "market", 110))
print("C1 fills", b.fills, "last", b.last, "activated", b.activate(), "pending", len(b.pending))
# (2) the trace: replay the seeded flow, record state for events 0..8 with bid side contents
rng = random.Random(mod.SEED)
book = Book()
for seq in range(mod.EVENTS):
    o = mod.random_order(rng, seq)
    if seq in (5, 6, 7):
        print("event", seq, o.kind, o.side, o.qty, "bids before", [(x.price, x.qty) for x in book.bids], "asks", [(x.price, x.qty) for x in book.asks], "last", book.last)
    if o.kind == "stop":
        book.pending.append(o)
    else:
        book.match(o)
    book.activate()
    if seq == 7:
        print("after event 7 bids", [(x.price, x.qty) for x in book.bids], "fills tail", book.fills[-3:])
        break
# (3) independent re-implementation of the flow (sorted lists, own code) for the printed totals
rng = random.Random(2026)
bids, asks, pending = [], [], []
last = None
seqn = 0
trades = traded = cancelled = submitted = activations = 0
kinds = {"limit": 0, "market": 0, "stop": 0}
def fill(order_side, order_qty, price_limit, kind):
    global last, trades, traded, submitted, cancelled
    qty = order_qty
    while qty > 0:
        if order_side > 0:
            cands = sorted([x for x in asks], key=lambda x: (x[0], x[2]))
        else:
            cands = sorted([x for x in bids], key=lambda x: (-x[0], x[2]))
        if not cands:
            break
        px, q, sq = cands[0]
        if kind == "limit":
            if order_side > 0 and px > price_limit: break
            if order_side < 0 and px < price_limit: break
        f = min(qty, q)
        qty -= f
        traded += f
        trades += 1
        last = px
        book_side = asks if order_side > 0 else bids
        book_side[book_side.index(cands[0])] = (px, q - f, sq)
        if q - f == 0:
            book_side.remove((px, 0, sq))
    return qty
def arrive(order_side, qty, price, kind, seq):
    global cancelled, submitted
    submitted += qty
    rem = fill(order_side, qty, price, kind)
    if rem > 0 and kind == "limit":
        (bids if order_side > 0 else asks).append((price, rem, seq))
    elif rem > 0:
        cancelled += rem
def activate():
    global activations, pending
    n = 0
    while last is not None:
        idx = None
        for i, (side, qty, stop, seq) in enumerate(pending):
            if (side > 0 and last >= stop) or (side < 0 and last <= stop):
                idx = i
                break
        if idx is None: break
        side, qty, stop, seq = pending.pop(idx)
        arrive(side, qty, None, "market", seq)
        n += 1
    return n
for seq in range(300):
    side = rng.choice((1, -1))
    qty = 10 * rng.randint(1, 10)
    roll = rng.random()
    if roll < 0.6:
        kinds["limit"] += 1
        arrive(side, qty, 10000 - side * rng.randint(0, 20), "limit", seq)
    elif roll < 0.85:
        kinds["market"] += 1
        arrive(side, qty, None, "market", seq)
    else:
        kinds["stop"] += 1
        pending.append((side, qty, 10000 + side * rng.randint(0, 20), seq))
    activations += activate()
    bb = max((p for p, q, s in bids), default=None)
    ba = min((p for p, q, s in asks), default=None)
    assert not (bb is not None and ba is not None and bb >= ba)
    resting = sum(q for _, q, _ in bids) + sum(q for _, q, _ in asks)
    assert submitted == resting + 2 * traded + cancelled
print("INDEP kinds", kinds, "trades", trades, "traded", traded, "activations", activations, "pending", len(pending), "cancelled", cancelled, "resting", sum(q for _, q, _ in bids) + sum(q for _, q, _ in asks))
