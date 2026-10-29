"""L04 activation timing: the twin activates a stop only after the arriving order finishes its sweep.

Definition 1.1 says a buy stop activates when a trade occurs at or above its stop. This script runs the twin's Book
on a book where an intermediate fill of one market buy reaches a buy stop's trigger, and compares it with a variant
that checks the stops after every fill. Run: .venv/bin/python -I <this file> <twin path>
"""

from __future__ import annotations

import sys
import types

twin_path = sys.argv[1]
src = open(twin_path, encoding="utf-8").read().replace("\nmain()\n", "\n")
mod = types.ModuleType("twin")
sys.modules["twin"] = mod
ns = mod.__dict__
exec(compile(src, twin_path, "exec"), ns)
Book, Order = ns["Book"], ns["Order"]


def build() -> object:
    b = Book()
    b.match(Order(0, -1, "limit", 60, price=1000))
    b.match(Order(1, -1, "limit", 100, price=1010))
    b.match(Order(2, -1, "limit", 100, price=1020))
    b.pending.append(Order(3, 1, "stop", 50, stop=1005))  # buy stop, trigger: a trade at or above 1005
    return b


# Twin behaviour: stops are checked only after the whole arriving order has matched.
b = build()
b.match(Order(4, 1, "market", 250))
b.activate()
print("twin      fills", b.fills, "pending", len(b.pending), "cancelled", b.cancelled)

# Variant: check the stops after every fill, as Definition 1.1 reads (activation at the trade itself).
class Immediate(Book):  # type: ignore[misc, valid-type]
    def match(self, order):  # type: ignore[no-untyped-def]
        before = len(self.fills)
        self.submitted += order.qty
        while order.qty > 0:
            best = self.best_resting(order.side)
            if best is None or best.price is None:
                break
            fill = min(order.qty, best.qty)
            best.qty -= fill
            order.qty -= fill
            self.traded += fill
            self.last = best.price
            self.fills.append((best.price, fill))
            if best.qty == 0:
                (self.asks if order.side > 0 else self.bids).remove(best)
            # check stops right after this trade
            pending_before = list(self.pending)
            for s in pending_before:
                if s in self.pending and ((s.side > 0 and self.last >= s.stop) or (s.side < 0 and self.last <= s.stop)):
                    self.pending.remove(s)
                    s.kind = "market"
                    self.match(s)
        if order.qty > 0 and order.kind == "limit":
            (self.bids if order.side > 0 else self.asks).append(order)
        elif order.qty > 0:
            self.cancelled += order.qty
            order.qty = 0
        return before


ib = Immediate()
for o in [Order(0, -1, "limit", 60, price=1000), Order(1, -1, "limit", 100, price=1010), Order(2, -1, "limit", 100, price=1020)]:
    Book.match(ib, o)  # set-up orders rest with the twin's rule
ib.pending.append(Order(3, 1, "stop", 50, stop=1005))
ib.match(Order(4, 1, "market", 250))
print("immediate fills", ib.fills, "pending", len(ib.pending), "cancelled", ib.cancelled)
