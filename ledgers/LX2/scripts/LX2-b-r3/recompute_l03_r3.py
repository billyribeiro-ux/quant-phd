# Independent re-implementation of Lab 1 (L03) written from the page prose, not from the twin code.
# Usage: python3 -I recompute_l03_r3.py [ask_first]   (ask_first mutant: cancel list puts asks before bids)
import random, sys
from fractions import Fraction
ASK_FIRST = len(sys.argv) > 1 and sys.argv[1] == "ask_first"
SEED, EVENTS, NT = 2026, 400, 6
REF, BAND, UNIT, STEPS, MKT = 10000, 20, 10, 5, 10
CANCEL = [5, 10, 25, 40, 60, 85]
rng = random.Random(SEED)
resting = []  # dicts: trader, side, price, rem, seq
orders = [0]*NT; fills = [0]*NT; cancels = [0]*NT
entered = traded = executions = mcancel = tcancel = crossed = idfail = 0
for seq in range(EVENTS):
    t = rng.randrange(NT)
    own_b = sorted([o for o in resting if o["trader"] == t and o["side"] > 0], key=lambda o: (-o["price"], o["seq"]))
    own_a = sorted([o for o in resting if o["trader"] == t and o["side"] < 0], key=lambda o: (o["price"], o["seq"]))
    own = (own_a + own_b) if ASK_FIRST else (own_b + own_a)
    if own and rng.randrange(100) < CANCEL[t]:
        target = own[rng.randrange(len(own))]
        resting.remove(target)
        tcancel += target["rem"]; cancels[t] += 1; target["rem"] = 0
    else:
        side = 1 if rng.randrange(2) == 0 else -1
        qty = UNIT * rng.randrange(1, STEPS + 1)
        market = rng.randrange(100) < MKT
        price = REF + rng.randrange(-BAND, BAND + 1)
        o = {"trader": t, "side": side, "price": price, "rem": qty, "seq": seq}
        orders[t] += 1; entered += qty
        opp = [x for x in resting if x["side"] == -side]
        # best opposite first: lowest ask for a buy, highest bid for a sell; earliest arrival breaks ties
        opp.sort(key=(lambda x: (x["price"], x["seq"])) if side > 0 else (lambda x: (-x["price"], x["seq"])))
        for x in opp:
            if o["rem"] == 0: break
            if not market:
                if side > 0 and x["price"] > price: break
                if side < 0 and x["price"] < price: break
            q = min(o["rem"], x["rem"])
            o["rem"] -= q; x["rem"] -= q; traded += q; executions += 1
            fills[t] += 1; fills[x["trader"]] += 1
            if x["rem"] == 0: resting.remove(x)
        if o["rem"] > 0:
            if market: mcancel += o["rem"]; o["rem"] = 0
            else: resting.append(o)
    bids = [x["price"] for x in resting if x["side"] > 0]; asks = [x["price"] for x in resting if x["side"] < 0]
    if bids and asks and max(bids) >= min(asks): crossed += 1
    res = sum(x["rem"] for x in resting)
    if entered != res + 2*traded + mcancel + tcancel: idfail += 1
print("orders", sum(orders), "executions", executions, "traded", traded, "cancel events", sum(cancels))
print("crossed", crossed, "identity failures", idfail, "resting", sum(x["rem"] for x in resting), "market cancelled", mcancel, "trader cancelled", tcancel)
print("fills", sum(fills), "= 2 x executions:", sum(fills) == 2*executions)
for t in range(NT):
    r = "none" if fills[t] == 0 else str(Fraction(cancels[t], fills[t]))
    print(t, CANCEL[t], orders[t], cancels[t], fills[t], r, "yes" if fills[t] and Fraction(cancels[t], fills[t]) > 2 else "no")
