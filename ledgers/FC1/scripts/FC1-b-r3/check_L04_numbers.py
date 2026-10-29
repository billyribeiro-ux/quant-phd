"""Independent checks for L04 (FC1-b round 3). Reads the twin's code path, does not trust its printed numbers.

Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-b-r3/check_L04_numbers.py <twin path>
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

twin_path = sys.argv[1]
src = open(twin_path, encoding="utf-8").read().replace("\nmain()\n", "\n")
import types
mod = types.ModuleType("twin")
sys.modules["twin"] = mod
ns = mod.__dict__
exec(compile(src, twin_path, "exec"), ns)  # noqa: S102 - local verifier check of the twin's own classes
Book = ns["Book"]
Order = ns["Order"]
random_order = ns["random_order"]

# Example 1.3 by hand
cost = 60 * 1000 + 90 * 1100
print("E1.3 cost", cost, "avg", Fraction(cost, 150), "float-check", cost / 150)
assert cost == 159000 and Fraction(cost, 150) == 1060

# Example 1.4 and R1 cascade, run through the twin's Book
b = Book()
b.match(Order(0, -1, "limit", 100, price=990))
b.match(Order(1, 1, "limit", 100, price=985))
b.match(Order(2, 1, "limit", 100, price=980))
b.pending.append(Order(3, -1, "stop", 100, stop=990))
b.pending.append(Order(4, -1, "stop", 100, stop=985))
b.match(Order(5, 1, "market", 100))
act = b.activate()
print("R1 cascade activations", act, "fills", b.fills)
assert b.fills == [(990, 100), (985, 100), (980, 100)] and act == 2

# Independent re-implementation of the seed-2026 flow, to compare the printed counts
rng = random.Random(2026)
bids: list[list[int]] = []  # [price, qty, seq]
asks: list[list[int]] = []
pend: list[tuple[int, int, int, int]] = []  # (seq, side, qty, stop)
last = None
trades = 0
traded = 0
cancelled = 0
stops_act = 0
kinds = {"limit": 0, "market": 0, "stop": 0}
submitted = 0
for seq in range(300):
    side = rng.choice((1, -1))
    qty = 10 * rng.randint(1, 10)
    roll = rng.random()
    if roll < 0.6:
        kind, price, stop = "limit", 10000 - side * rng.randint(0, 20), None
    elif roll < 0.85:
        kind, price, stop = "market", None, None
    else:
        kind, price, stop = "stop", None, 10000 + side * rng.randint(0, 20)
    kinds[kind] += 1

    def run(side: int, qty: int, kind: str, price: int | None) -> None:
        global last, trades, traded, cancelled, submitted
        submitted += qty
        while qty > 0:
            book = asks if side > 0 else bids
            if not book:
                break
            if side > 0:
                best = min(book, key=lambda o: (o[0], o[2]))
            else:
                best = min(book, key=lambda o: (-o[0], o[2]))
            if kind == "limit":
                ok = best[0] <= price if side > 0 else best[0] >= price
                if not ok:
                    break
            f = min(qty, best[1])
            best[1] -= f
            qty -= f
            traded += f
            trades += 1
            last = best[0]
            if best[1] == 0:
                book.remove(best)
        if qty > 0 and kind == "limit":
            (bids if side > 0 else asks).append([price, qty, seq])
        elif qty > 0:
            cancelled += qty

    def activate() -> int:
        global last
        n = 0
        while last is not None:
            hit = None
            for i, (s_seq, s_side, s_qty, s_stop) in enumerate(pend):
                if (s_side > 0 and last >= s_stop) or (s_side < 0 and last <= s_stop):
                    hit = i
                    break
            if hit is None:
                break
            s_seq, s_side, s_qty, _ = pend.pop(hit)
            run(s_side, s_qty, "market", None)
            n += 1
        return n

    if kind == "stop":
        pend.append((seq, side, qty, stop))
    else:
        run(side, qty, kind, price)
    stops_act += activate()
    resting = sum(o[1] for o in bids) + sum(o[1] for o in asks)
    assert submitted == resting + 2 * traded + cancelled, seq

print("INDEP kinds", kinds, "trades", trades, "traded", traded, "stops_act", stops_act, "pending", len(pend), "cancelled", cancelled)
resting = sum(o[1] for o in bids) + sum(o[1] for o in asks)
print("INDEP resting", resting, "best bid", max((o[0] for o in bids), default=None), "best ask", min((o[0] for o in asks), default=None))
assert kinds == {"limit": 181, "market": 77, "stop": 42}
assert (trades, traded, stops_act, len(pend), cancelled, resting) == (173, 5600, 24, 18, 220, 4710)
print("E3 5600/173 =", Fraction(5600, 173), "=", 5600 / 173)
print("E1 24+18 =", 24 + 18, "stop arrivals", kinds["stop"])
print("L04 numbers: PASS")
