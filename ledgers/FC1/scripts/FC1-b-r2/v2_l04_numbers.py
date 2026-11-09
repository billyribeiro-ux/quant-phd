# Round-2 independent re-derivation for L04 (Lab 1 numbers, Examples, Problems, Propositions 2.2 and 2.3).
# Own book: price -> FIFO deque per side (not the lab's list/min-key code). RNG draw order copied from the lesson's generator.
import random
import sys
from collections import deque

class Book:
    def __init__(self):
        self.bid_levels = {}   # price -> deque of [seq, qty]
        self.ask_levels = {}
        self.pending = []      # stops: [seq, side, qty, stop]
        self.last = None
        self.traded = 0        # shares traded (sum of fills)
        self.fills = []        # (price, qty) per fill, one per resting-order match
        self.submitted = 0
        self.cancelled = 0

    def _levels(self, side):   # side +1 buy meets asks
        return self.ask_levels if side > 0 else self.bid_levels

    def best(self, levels, want_max):
        ps = [p for p, q in levels.items() if q]
        if not ps:
            return None
        return max(ps) if want_max else min(ps)

    def best_bid(self):
        return self.best(self.bid_levels, True)

    def best_ask(self):
        return self.best(self.ask_levels, False)

    def resting_shares(self):
        return sum(q for lv in (self.bid_levels, self.ask_levels) for dq in lv.values() for _, q in dq)

    def add_resting(self, seq, side, price, qty):
        lv = self.bid_levels if side > 0 else self.ask_levels
        lv.setdefault(price, deque()).append([seq, qty])

    def take(self, side, kind, qty, limit=None, seq=None):
        """Market/limit buy (side>0) walks asks ascending; sell walks bids descending. Returns residual qty."""
        self.submitted += qty
        opp = self.ask_levels if side > 0 else self.bid_levels
        while qty > 0:
            ps = [p for p, dq in opp.items() if dq]
            if not ps:
                break
            p = min(ps) if side > 0 else max(ps)
            if kind == "limit":
                if side > 0 and p > limit:
                    break
                if side < 0 and p < limit:
                    break
            dq = opp[p]
            head = dq[0]
            f = min(qty, head[1])
            head[1] -= f
            qty -= f
            self.traded += f
            self.fills.append((p, f))
            self.last = p
            if head[1] == 0:
                dq.popleft()
            if not dq:
                del opp[p]
        if qty > 0 and kind == "limit":
            self.add_resting(seq, side, limit, qty)
            qty = 0 if False else qty  # residual rests, not cancelled
            return qty
        if qty > 0:
            self.cancelled += qty
        return 0

    def check_stops(self):
        """Repeat: first pending stop (arrival order) whose trigger the last trade price has reached."""
        n = 0
        while self.last is not None:
            hit = None
            for i, (seq, side, qty, stop) in enumerate(self.pending):
                if (side > 0 and self.last >= stop) or (side < 0 and self.last <= stop):
                    hit = i
                    break
            if hit is None:
                break
            seq, side, qty, stop = self.pending.pop(hit)
            self.take(side, "market", qty)
            n += 1
        return n

def draw(rng, seq):
    side = rng.choice((1, -1))
    qty = 10 * rng.randint(1, 10)
    roll = rng.random()
    if roll < 0.6:
        return ("limit", seq, side, qty, 10000 - side * rng.randint(0, 20), None)
    if roll < 0.85:
        return ("market", seq, side, qty, None, None)
    return ("stop", seq, side, qty, None, 10000 + side * rng.randint(0, 20))

def run_flow(seed=2026, events=300, trace=8, verbose=True):
    rng = random.Random(seed)
    b = Book()
    kinds = {"limit": 0, "market": 0, "stop": 0}
    activated = 0
    crossed = 0
    cons_fail = 0
    trace_lines = []
    for seq in range(events):
        kind, s, side, qty, price, stop = draw(rng, seq)
        kinds[kind] += 1
        if kind == "stop":
            b.pending.append((s, side, qty, stop))
            b.submitted += 0  # stop not entered yet
        elif kind == "market":
            b.take(side, "market", qty)
        else:
            b.take(side, "limit", qty, limit=price, seq=s)
        activated += b.check_stops()
        bb, ba = b.best_bid(), b.best_ask()
        if bb is not None and ba is not None and bb >= ba:
            crossed += 1
        if b.submitted != b.resting_shares() + 2 * b.traded + b.cancelled:
            cons_fail += 1
        if seq < trace:
            lab = lambda v: "none" if v is None else str(v)
            trace_lines.append(f"event {seq}: {kind} {'buy' if side > 0 else 'sell'}, best bid {lab(bb)}, best ask {lab(ba)}, last trade {lab(b.last)}")
    res = dict(kinds=kinds, trades=len(b.fills), traded=b.traded, activated=activated,
               pending=len(b.pending), cancelled=b.cancelled, resting=b.resting_shares(),
               crossed=crossed, cons_fail=cons_fail, end_bid=b.best_bid(), end_ask=b.best_ask(), trace=trace_lines)
    return res

def fixture_a():
    b = Book()
    b.take(-1, "limit", 60, limit=1000, seq=0)
    b.take(-1, "limit", 100, limit=1100, seq=1)
    b.take(1, "market", 150)
    cost = sum(p * q for p, q in b.fills)
    return b.fills, cost, cost / 150, sum(q for dq in b.ask_levels.get(1100, []) for _, q in [dq] ) if False else b.ask_levels[1100][0][1]

def fixture_b():
    b = Book()
    b.take(-1, "limit", 100, limit=990, seq=0)
    b.take(1, "limit", 100, limit=985, seq=1)
    b.take(1, "limit", 100, limit=980, seq=2)
    b.pending.append((3, -1, 100, 990))
    a1 = b.check_stops()
    b.take(1, "market", 100)
    a2 = b.check_stops()
    return b.fills, a1 + a2

if __name__ == "__main__":
    r = run_flow()
    for k, v in r.items():
        if k != "trace":
            print(f"{k} = {v}")
    for line in r["trace"]:
        print(line)
    print("E1 activated+pending =", r["activated"] + r["pending"], "arrivals(stop) =", r["kinds"]["stop"])
    print("E3 5600/173 =", 5600 / 173, "as fraction", f"{5600}/{173}")
    fa = fixture_a(); print("Fixture A fills", fa[0], "cost", fa[1], "avg", fa[2], "left at 1100", fa[3])
    fb = fixture_b(); print("Fixture B fills", fb[0], "activations", fb[1])
