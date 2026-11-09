import re, pathlib, sys
src = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b/tests/labs/FC1/lab-FC1-L04-1.py").read_text(encoding="utf-8")
src = src.rsplit("\nmain()", 1)[0] + "\n"
ns = {}
exec(compile(src, "twin_without_main", "exec"), ns)
Order, Book = ns["Order"], ns["Book"]
# R1 cascade: ask 100 @990; bids 100 @985, 100 @980; stop A sell 100 @990; stop B sell 100 @985
b = Book()
b.match(Order(0, -1, "limit", 100, price=990))
b.match(Order(1, 1, "limit", 100, price=985))
b.match(Order(2, 1, "limit", 100, price=980))
b.pending += [Order(3, -1, "stop", 100, stop=990), Order(4, -1, "stop", 100, stop=985)]
b.match(Order(5, 1, "market", 100))
n = b.activate()
print("R1 activations", n, "fills", b.fills)
# M3: sell stop at 1000; last trade 1005; buy with last fill 1001, then buy with last fill 1000
b = Book(); b.last = 1005
b.pending.append(Order(0, -1, "stop", 10, stop=1000))
b.asks.append(Order(1, -1, "limit", 10, price=1001))
b.match(Order(2, 1, "market", 10)); print("M3 after first buy: last", b.last, "activated", b.activate(), "pending", len(b.pending))
b.asks.append(Order(3, -1, "limit", 10, price=1000))
b.match(Order(4, 1, "market", 10)); print("M3 after second buy: last", b.last, "activated", b.activate(), "pending", len(b.pending))
# M2: asks 30@1000, 30@1001, 40@1003; buy limit 50 @1002
b = Book()
for i, (p, q) in enumerate([(1000, 30), (1001, 30), (1003, 40)]):
    b.match(Order(i, -1, "limit", q, price=p))
b.match(Order(3, 1, "limit", 50, price=1002))
print("M2 fills", b.fills, "asks", [(o.price, o.qty) for o in b.asks], "bids", [(o.price, o.qty) for o in b.bids])
# M1: bids 60@995, 100@990; sell market 100
b = Book()
b.match(Order(0, 1, "limit", 60, price=995)); b.match(Order(1, 1, "limit", 100, price=990))
b.match(Order(2, -1, "market", 100))
print("M1 fills", b.fills, "bids", [(o.price, o.qty) for o in b.bids], "cost", sum(p*q for p,q in b.fills))
# R2 crossed start: bid 1005 and ask 1000 then limit buy 5 @999
b = Book(); b.bids.append(Order(0, 1, "limit", 10, price=1005)); b.asks.append(Order(1, -1, "limit", 10, price=1000))
b.match(Order(2, 1, "limit", 5, price=999))
print("R2 best bid", b.best_bid(), "best ask", b.best_ask(), "crossed", b.best_bid() >= b.best_ask())
# P2: ask 100@1000, market buy 150
b = Book(); b.match(Order(0, -1, "limit", 100, price=1000)); b.match(Order(1, 1, "market", 150))
print("P2 X", b.traded, "C", b.cancelled, "R", b.resting(), "submitted", b.submitted, "R+2X+C", b.resting()+2*b.traded+b.cancelled)
# R3 single fill of 60 shares
b = Book(); b.match(Order(0, -1, "limit", 60, price=1000)); b.match(Order(1, 1, "market", 60))
print("R3 traded", b.traded, "2X", 2*b.traded)
