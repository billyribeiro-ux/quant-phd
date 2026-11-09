# Round-2: hand problems of L04 re-run through the independent Book of v2_l04_numbers.py, plus property checks
# of Propositions 2.2 (uncrossed from empty, A1) and 2.3 (conservation under A2) over many seeded flows.
# Side convention: add_resting(seq, +1, ...) puts a BID; add_resting(seq, -1, ...) puts an ASK. take(+1) is a buy.
import sys, random
sys.path.insert(0, sys.argv[1])
from v2_l04_numbers import Book, draw

# M1: bids 60@995, 100@990; market sell 100
b = Book(); b.add_resting(0, 1, 995, 60); b.add_resting(1, 1, 990, 100); b.take(-1, "market", 100)
print("M1 fills", b.fills, "cost", sum(p*q for p,q in b.fills), "avg", sum(p*q for p,q in b.fills)/100,
      "bid 990 left", [q for _, q in b.bid_levels.get(990, [])])
# M2: asks 30@1000, 30@1001, 40@1003; buy limit 50@1002
b = Book(); b.add_resting(0, -1, 1000, 30); b.add_resting(1, -1, 1001, 30); b.add_resting(2, -1, 1003, 40)
b.take(1, "limit", 50, limit=1002, seq=3)
print("M2 fills", b.fills, "asks left", {p: [q for _, q in dq] for p, dq in b.ask_levels.items()},
      "bids", {p: [q for _, q in dq] for p, dq in b.bid_levels.items()})
# P2: ask 100@1000 only; market buy 150
b = Book(); b.add_resting(0, -1, 1000, 100); b.take(1, "market", 150)
G = 100 + 150
X = b.traded; C = b.cancelled; R = b.resting_shares()
print("P2 G", G, "X", X, "C", C, "R", R, "R+2X+C", R + 2*X + C)
# R1 cascade: ask 100@990; bids 100@985, 100@980; sell stops A (stop 990) and B (stop 985)
b = Book(); b.add_resting(0, -1, 990, 100); b.add_resting(1, 1, 985, 100); b.add_resting(2, 1, 980, 100)
b.pending += [(3, -1, 100, 990), (4, -1, 100, 985)]
b.take(1, "market", 100); n = b.check_stops()
print("R1 fills", b.fills, "activations", n)
# R2: best bid 1005 rests, best ask 1000; buy limit 5 @999 does not trade and rests
b = Book(); b.add_resting(0, 1, 1005, 5); b.add_resting(1, -1, 1000, 5); b.take(1, "limit", 5, limit=999, seq=2)
print("R2 bid", b.best_bid(), "ask", b.best_ask(), "crossed", b.best_bid() >= b.best_ask(), "fills", b.fills)
print("R3 filled parts for one 60-share fill:", 60 + 60)
# Remark 1.2: buy stop 1005; last 1000 does not trigger, last 1010 does
b = Book(); b.pending.append((0, 1, 10, 1005)); b.last = 1000
print("Remark1.2 last 1000 -> activations", b.check_stops(), "(0 expected)")
b.last = 1010; print("Remark1.2 last 1010 -> activations", b.check_stops(), "(1 expected)")
# L04q6 / misconception 3: 100@1000 arrived first, 10@1000 later; market buy 10
b = Book(); b.add_resting(0, -1, 1000, 100); b.add_resting(1, -1, 1000, 10); b.take(1, "market", 10)
print("misconception3 fills", b.fills, "left", [(p, [q for _, q in dq]) for p, dq in b.ask_levels.items()])

# Property checks: 2.2 under A1 (empty start), 2.3 under A2 (no withdrawals): 200 seeded flows x 300 events.
bad_cross = 0; bad_cons = 0; events = 0
for seed in range(200):
    rng = random.Random(seed)
    b = Book()
    for e in range(300):
        kind, s, side, qty, price, stop = draw(rng, e)
        if kind == "stop":
            b.pending.append((s, side, qty, stop))
        elif kind == "market":
            b.take(side, "market", qty)
        else:
            b.take(side, "limit", qty, limit=price, seq=s)
        b.check_stops()
        events += 1
        bb, ba = b.best_bid(), b.best_ask()
        if bb is not None and ba is not None and bb >= ba: bad_cross += 1
        if b.submitted != b.resting_shares() + 2*b.traded + b.cancelled: bad_cons += 1
print(f"property flows: runs=200 events={events} crossed={bad_cross} conservation_failures={bad_cons}")

# Sensitivity: a withdrawal breaks the identity (A2 is needed).
b = Book(); b.add_resting(0, 1, 1000, 50); b.add_resting(1, -1, 1100, 30)
b.submitted += 80
b.bid_levels.pop(1000)  # withdrawal: removed without trading or cancelling
print("withdrawal sensitivity: submitted", b.submitted, "resting+2X+C", b.resting_shares() + 2*b.traded + b.cancelled)
