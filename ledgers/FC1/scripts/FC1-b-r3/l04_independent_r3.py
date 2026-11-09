"""Verifier (FC1-b r3): independent order-book re-derivation of every number printed or quoted in L04.

Own data structures (heap-free, explicit lists re-sorted per event) and own rules. Same RNG call order as the
lesson's flow, which is the only shared element. Prints every quantity so the output can be compared to the page.
"""
import random
from collections import Counter
from fractions import Fraction

SEED, MID, OFF, EVENTS = 2026, 10000, 20, 300


class Book:
    def __init__(self):
        self.rest = []  # dicts: side, price, qty, seq (resting limit orders, both sides)
        self.stops = []  # pending stops: dict(side, qty, stop, seq)
        self.last = None
        self.trades = []  # (price, qty)
        self.traded = 0
        self.cancelled = 0
        self.submitted = 0
        self.activations = 0
        self.seq = 0

    def _opp(self, side):
        # opposite side resting orders, sorted by the order an arriving order meets first
        if side == 1:  # buy meets asks: lowest price, then earliest
            return sorted([r for r in self.rest if r["side"] == -1], key=lambda r: (r["price"], r["seq"]))
        return sorted([r for r in self.rest if r["side"] == 1], key=lambda r: (-r["price"], r["seq"]))

    def arrive(self, side, qty, limit=None):
        """Market (limit=None) or limit arrival. Returns nothing; updates book."""
        self.submitted += qty
        remaining = qty
        for r in self._opp(side):
            if remaining == 0:
                break
            if limit is not None:
                if side == 1 and r["price"] > limit:
                    break
                if side == -1 and r["price"] < limit:
                    break
            f = min(remaining, r["qty"])
            r["qty"] -= f
            remaining -= f
            self.traded += f
            self.trades.append((r["price"], f))
            self.last = r["price"]
            if r["qty"] == 0:
                self.rest.remove(r)
        if remaining:
            if limit is not None:
                self.seq += 1
                self.rest.append({"side": side, "price": limit, "qty": remaining, "seq": self.seq})
            else:
                self.cancelled += remaining

    def arrive_stop(self, side, qty, stop):
        self.seq += 1
        self.stops.append({"side": side, "qty": qty, "stop": stop, "seq": self.seq})

    def activate_all(self):
        n = 0
        while self.last is not None:
            hit = None
            for s in sorted(self.stops, key=lambda s: s["seq"]):
                if (s["side"] == 1 and self.last >= s["stop"]) or (s["side"] == -1 and self.last <= s["stop"]):
                    hit = s
                    break
            if hit is None:
                break
            self.stops.remove(hit)
            self.arrive(hit["side"], hit["qty"], None)
            self.submitted  # stop counted at activation via arrive()
            n += 1
        self.activations += n
        return n

    def best_bid(self):
        b = [r["price"] for r in self.rest if r["side"] == 1]
        return max(b) if b else None

    def best_ask(self):
        a = [r["price"] for r in self.rest if r["side"] == -1]
        return min(a) if a else None

    def resting_shares(self):
        return sum(r["qty"] for r in self.rest)


def fixtures():
    b = Book()
    b.arrive(-1, 60, 1000)
    b.arrive(-1, 100, 1100)
    b.arrive(1, 150, None)
    cost = sum(p * q for p, q in b.trades)
    qty = sum(q for _, q in b.trades)
    A = dict(trades=b.trades, cost=cost, qty=qty, avg=Fraction(cost, qty), ask1100=sum(r["qty"] for r in b.rest if r["side"] == -1 and r["price"] == 1100))
    b = Book()
    b.arrive(-1, 100, 990)
    b.arrive(1, 100, 985)
    b.arrive(1, 100, 980)
    b.arrive_stop(-1, 100, 990)
    n0 = b.activate_all()  # last is None: must be 0
    b.arrive(1, 100, None)
    n1 = b.activate_all()
    B = dict(trades=b.trades, activated_first=n0, activated_second=n1)
    return A, B


def flow():
    rng = random.Random(SEED)
    book = Book()
    kinds = Counter()
    crossed = 0
    conserv_fail = 0
    trace = []
    for seq in range(EVENTS):
        side = rng.choice((1, -1))
        qty = 10 * rng.randint(1, 10)
        roll = rng.random()
        if roll < 0.6:
            kind = "limit"
            price = MID - side * rng.randint(0, OFF)
            kinds[kind] += 1
            book.arrive(side, qty, price)
        elif roll < 0.85:
            kind = "market"
            kinds[kind] += 1
            book.arrive(side, qty, None)
        else:
            kind = "stop"
            stop = MID + side * rng.randint(0, OFF)
            kinds[kind] += 1
            book.arrive_stop(side, qty, stop)
        book.activate_all()
        bb, ba = book.best_bid(), book.best_ask()
        if bb is not None and ba is not None and bb >= ba:
            crossed += 1
        R = book.resting_shares()
        if book.submitted != R + 2 * book.traded + book.cancelled:
            conserv_fail += 1
        if seq < 8:
            trace.append((seq, kind, side, bb, ba, book.last))
    return book, kinds, crossed, conserv_fail, trace


A, B = fixtures()
print("A trades", A["trades"], "cost", A["cost"], "qty", A["qty"], "avg", A["avg"], "ask1100 left", A["ask1100"])
print("B trades", B["trades"], "activated first", B["activated_first"], "second", B["activated_second"])
book, kinds, crossed, cf, trace = flow()
for t in trace:
    print("trace", t)
print("kinds", dict(kinds), "limit", kinds["limit"], "market", kinds["market"], "stop", kinds["stop"])
print("trades", len(book.trades), "shares traded", book.traded, "activations", book.activations, "pending", len(book.stops))
print("cancelled", book.cancelled, "resting", book.resting_shares())
print("crossed", crossed, "conservation failures", cf)
print("end best bid", book.best_bid(), "best ask", book.best_ask())
print("avg shares per trade (exact)", Fraction(book.traded, len(book.trades)), float(Fraction(book.traded, len(book.trades))))
print("stop arrivals check activated+pending", book.activations + len(book.stops))
