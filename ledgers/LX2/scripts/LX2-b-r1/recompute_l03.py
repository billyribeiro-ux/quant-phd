"""Independent re-implementation of the L03 order-flow simulation (not an import of the lab).

Mirrors the generator's draw order as written in the lab code: per event, the trader, then either a cancel of one of
that trader's resting orders (chosen from the bids in priority order followed by the asks in priority order) or an
order (side, quantity, market flag, price). Prints every figure that L03 prose cites.
"""

import random
from fractions import Fraction

SEED, EVENTS, TRADERS = 2026, 400, 6
REF, BAND, UNIT, STEPS, MKT = 10000, 20, 10, 5, 10
CANCEL = [5, 10, 25, 40, 60, 85]

rng = random.Random(SEED)
resting = []  # dicts: trader, side (+1 buy, -1 sell), price, rem, seq
orders = [0] * TRADERS
fills = [0] * TRADERS
cancels = [0] * TRADERS
executions = 0
traded = 0
mkt_cancel = 0
trader_cancel = 0
entered = 0
crossed_events = 0
identity_fail = 0
log = []
seq = 0


def bids_sorted():
    return sorted([o for o in resting if o["side"] > 0], key=lambda o: (-o["price"], o["seq"]))


def asks_sorted():
    return sorted([o for o in resting if o["side"] < 0], key=lambda o: (o["price"], o["seq"]))


for ev in range(EVENTS):
    trader = rng.randrange(TRADERS)
    own = [o for o in bids_sorted() + asks_sorted() if o["trader"] == trader]
    if own and rng.randrange(100) < CANCEL[trader]:
        target = own[rng.randrange(len(own))]
        resting.remove(target)
        trader_cancel += target["rem"]
        cancels[trader] += 1
        log.append(("cancel", trader))
    else:
        side = 1 if rng.randrange(2) == 0 else -1
        qty = UNIT * rng.randrange(1, STEPS + 1)
        is_mkt = rng.randrange(100) < MKT
        price = REF + rng.randrange(-BAND, BAND + 1)
        log.append(("market" if is_mkt else "limit", trader))
        o = {"trader": trader, "side": side, "price": price, "rem": qty, "seq": seq, "mkt": is_mkt}
        seq += 1
        entered += qty
        orders[trader] += 1
        # match against the opposite side in priority order
        while o["rem"] > 0:
            opp = asks_sorted() if side > 0 else bids_sorted()
            if not opp:
                break
            best = opp[0]
            if is_mkt:
                ok = True
            elif side > 0:
                ok = best["price"] <= price
            else:
                ok = best["price"] >= price
            if not ok:
                break
            q = min(o["rem"], best["rem"])
            o["rem"] -= q
            best["rem"] -= q
            traded += q
            executions += 1
            fills[trader] += 1
            fills[best["trader"]] += 1
            if best["rem"] == 0:
                resting.remove(best)
        if o["rem"] > 0:
            if is_mkt:
                mkt_cancel += o["rem"]
            else:
                resting.append(o)
    bids, asks = bids_sorted(), asks_sorted()
    if bids and asks and bids[0]["price"] >= asks[0]["price"]:
        crossed_events += 1
    rest = sum(o["rem"] for o in resting)
    if entered != rest + 2 * traded + mkt_cancel + trader_cancel:
        identity_fail += 1

print("orders", sum(orders), "executions", executions, "traded", traded, "cancel events", sum(cancels))
print("crossed", crossed_events, "identity failures", identity_fail)
print("resting", sum(o["rem"] for o in resting), "market cancelled", mkt_cancel, "trader cancelled", trader_cancel)
print("fills total", sum(fills), "== 2*executions", sum(fills) == 2 * executions)
print("trader table (trader, cancel_pct, orders, cancels, fills, ratio)")
ratios = []
for t in range(TRADERS):
    r = Fraction(cancels[t], fills[t]) if fills[t] else None
    if r is not None:
        ratios.append(r)
    print(t, CANCEL[t], orders[t], cancels[t], fills[t], r, (r > 2) if r is not None else "undefined")
print("max ratio", max(ratios), "flagged at 2", sum(1 for r in ratios if r > 2))
print("ratio check 3/104 < 6/97:", Fraction(3, 104) < Fraction(6, 97), 3 * 97, 6 * 104)
print("ratio check 5/34 < 6/29 diff:", Fraction(6, 29) - Fraction(5, 34), 59 / 986)
print("ratio check 21/37 vs 17/50:", 21 * 50, 17 * 37)
print("identity G = R + 2X + Cm + Ct at end:", entered, sum(o["rem"] for o in resting) + 2 * traded + mkt_cancel + trader_cancel)
