# Independent re-implementation of the L03 seeded order book (not an import of the lab).
# Books are kept as flat lists of [trader, side, price, seq, remaining]; best quotes are found by scan.
import random
from fractions import Fraction

SEED = 2026
N_EV = 400
NT = 6
REF = 10000
BAND = 20
UNIT = 10
STEPS = 5
MKT = 10
CANCEL = [5, 10, 25, 40, 60, 85]

rng = random.Random(SEED)
rest = []  # resting orders: dict(trader, side, price, seq, rem)
orders = [0] * NT
fills = [0] * NT
cancels = [0] * NT
entered = resting_sh = traded = mkt_cx = trd_cx = execs = 0
log = []
crossed = 0
ident_bad = 0

def best(side):
    cand = [o for o in rest if o["side"] == side]
    if not cand:
        return None
    if side > 0:
        return max(cand, key=lambda o: (o["price"], -o["seq"]))
    return min(cand, key=lambda o: (o["price"], o["seq"]))

for seq in range(N_EV):
    tr = rng.randrange(NT)
    # own resting orders in the order the lab's generator indexes them: bids by price desc then seq, then asks by price asc then seq
    bids_sorted = sorted([o for o in rest if o["side"] > 0], key=lambda o: (-o["price"], o["seq"]))
    asks_sorted = sorted([o for o in rest if o["side"] < 0], key=lambda o: (o["price"], o["seq"]))
    mine = [o for o in bids_sorted + asks_sorted if o["trader"] == tr]
    if mine and rng.randrange(100) < CANCEL[tr]:
        pick = mine[rng.randrange(len(mine))]
        rest.remove(pick)
        trd_cx += pick["rem"]
        cancels[tr] += 1
        log.append(("c", tr))
    else:
        side = 1 if rng.randrange(2) == 0 else -1
        q = UNIT * rng.randrange(1, STEPS + 1)
        is_mkt = rng.randrange(100) < MKT
        px = REF + rng.randrange(-BAND, BAND + 1)
        orders[tr] += 1
        log.append(("m" if is_mkt else "l", tr))
        entered += q
        inc = {"trader": tr, "side": side, "price": px, "seq": seq, "rem": q}
        while inc["rem"] > 0:
            opp = [o for o in rest if o["side"] == -side]
            if not opp:
                break
            b = best(-side)
            if not is_mkt:
                if side > 0 and not (b["price"] <= inc["price"]):
                    break
                if side < 0 and not (b["price"] >= inc["price"]):
                    break
            x = min(inc["rem"], b["rem"])
            inc["rem"] -= x
            b["rem"] -= x
            traded += x
            execs += 1
            fills[tr] += 1
            fills[b["trader"]] += 1
            if b["rem"] == 0:
                rest.remove(b)
        if inc["rem"] > 0:
            if is_mkt:
                mkt_cx += inc["rem"]
            else:
                rest.append(inc)
    bb, ba = best(1), best(-1)
    if bb is not None and ba is not None and bb["price"] >= ba["price"]:
        crossed += 1
    resting_sh = sum(o["rem"] for o in rest)
    if entered != resting_sh + 2 * traded + mkt_cx + trd_cx:
        ident_bad += 1

# tally from log
t_orders = [0] * NT
t_cancels = [0] * NT
for k, t in log:
    if k == "c":
        t_cancels[t] += 1
    else:
        t_orders[t] += 1
disagree = sum(t_orders[i] != orders[i] for i in range(NT)) + sum(t_cancels[i] != cancels[i] for i in range(NT))

print("orders", sum(orders), "executions", execs, "traded", traded, "cancel events", sum(cancels))
print("crossed", crossed, "identity failures", ident_bad, "tally disagreements", disagree)
print("resting", resting_sh, "market cancelled", mkt_cx, "trader cancelled", trd_cx)
print("fills total", sum(fills), "== 2*execs", sum(fills) == 2 * execs)
for t in range(NT):
    if fills[t] == 0:
        print(t, CANCEL[t], orders[t], cancels[t], fills[t], "none")
    else:
        r = Fraction(cancels[t], fills[t])
        print(t, CANCEL[t], orders[t], cancels[t], fills[t], r, "flag" if r > 2 else "no", float(r))
