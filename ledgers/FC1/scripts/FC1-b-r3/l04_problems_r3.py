"""Verifier (FC1-b r3): checks the L04 problem-set cases by the rules of Remark 1.2 (independent of the lab code).

R1 cascade, M3 stop-trigger case, R2 crossed-start case, P2 conservation case, and the Example 1.4 stop.
"""
from fractions import Fraction


class Book:
    def __init__(self):
        self.bids, self.asks, self.stops, self.fills, self.last = [], [], [], [], None

    def limit_or_market(self, side, qty, limit=None):
        """side +1 buy, -1 sell. Fills against opposite side best-first, arrival order within price."""
        opp = self.asks if side == 1 else self.bids
        opp.sort(key=lambda o: (o["p"], o["seq"]) if side == 1 else (-o["p"], o["seq"]))
        rem = qty
        while rem and opp:
            o = opp[0]
            if limit is not None and ((side == 1 and o["p"] > limit) or (side == -1 and o["p"] < limit)):
                break
            f = min(rem, o["q"])
            self.fills.append((o["p"], f))
            self.last = o["p"]
            rem -= f
            o["q"] -= f
            if o["q"] == 0:
                opp.pop(0)
        if rem and limit is not None:
            (self.bids if side == 1 else self.asks).append({"p": limit, "q": rem, "seq": len(self.fills) + 1000})

    def trigger(self):
        fired = []
        changed = True
        while changed:
            changed = False
            for s in list(self.stops):
                if self.last is None:
                    break
                if (s["side"] == 1 and self.last >= s["stop"]) or (s["side"] == -1 and self.last <= s["stop"]):
                    self.stops.remove(s)
                    fired.append(s["name"])
                    self.limit_or_market(s["side"], s["q"])
                    changed = True
                    break
        return fired


# R1: ask 100@990; bids 100@985, 100@980; sell stop A 100 stop 990; sell stop B 100 stop 985
b = Book()
b.asks.append({"p": 990, "q": 100, "seq": 0})
b.bids += [{"p": 985, "q": 100, "seq": 1}, {"p": 980, "q": 100, "seq": 2}]
b.stops += [{"name": "A", "side": -1, "stop": 990, "q": 100}, {"name": "B", "side": -1, "stop": 985, "q": 100}]
b.limit_or_market(1, 100)
fired = b.trigger()
print("R1 fills", b.fills, "fired", fired)

# M3: sell stop at 1000; last 1005; buy arrives with last fill 1001 -> no; second buy last fill 1000 -> yes
b = Book()
b.last = 1005
b.stops.append({"name": "S", "side": -1, "stop": 1000, "q": 10})
b.asks.append({"p": 1001, "q": 5, "seq": 0})
b.limit_or_market(1, 5)
print("M3 after first buy: last", b.last, "fired", b.trigger())
b.asks.append({"p": 1000, "q": 5, "seq": 1})
b.limit_or_market(1, 5)
print("M3 after second buy: last", b.last, "fired", b.trigger())

# R2: best bid 1005 and best ask 1000 (crossed start), limit buy 5 at 999 rests
b = Book()
b.bids.append({"p": 1005, "q": 5, "seq": 0})
b.asks.append({"p": 1000, "q": 5, "seq": 1})
b.limit_or_market(1, 5, 999)
print("R2 crossed after event:", max(o["p"] for o in b.bids) >= min(o["p"] for o in b.asks), "fills", b.fills)

# P2 (L04): ask 100@1000 only; market buy 150 -> G=250, X=100, C=50, R=0
b = Book()
b.asks.append({"p": 1000, "q": 100, "seq": 0})
b.limit_or_market(1, 150)
G = 150 + 100
X = sum(q for _, q in b.fills)
C = 150 - X
R = sum(o["q"] for o in b.bids + b.asks)
print("P2", "G", G, "X", X, "C", C, "R", R, "R+2X+C", R + 2 * X + C)

# Example 1.4 stop: ask 100@990, bids 100@985 and 100@980; sell stop 100 stop 990
b = Book()
b.asks.append({"p": 990, "q": 100, "seq": 0})
b.bids += [{"p": 985, "q": 100, "seq": 1}, {"p": 980, "q": 100, "seq": 2}]
b.stops.append({"name": "S", "side": -1, "stop": 990, "q": 100})
b.limit_or_market(1, 100)
print("Ex1.4 fired", b.trigger(), "fills", b.fills)
