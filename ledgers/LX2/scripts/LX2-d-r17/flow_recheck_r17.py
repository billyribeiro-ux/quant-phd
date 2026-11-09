# Independent re-implementation of the L03 seeded SIMULATED order flow (written from the lesson's stated rules,
# not copied from the lab). Prints the same counts the lesson prints, for comparison.
# Run: python -I -W error ledgers/LX2/scripts/LX2-d-r16/flow_recheck_r16.py
import random
from fractions import Fraction

rng = random.Random(2026)
cancel_pct = [5, 10, 25, 40, 60, 85]
bids = []   # dicts: trader, price, seq, rem
asks = []
orders = [0] * 6
fills = [0] * 6
cancels = [0] * 6
executions = traded = mkt_cancel = trd_cancel = entered = 0
crossed = 0
ident_fail = 0
n_events = 400


def resting_total():
    return sum(o["rem"] for o in bids) + sum(o["rem"] for o in asks)


for seq in range(n_events):
    trader = rng.randrange(6)
    own = [o for o in bids if o["trader"] == trader]
    own += [o for o in asks if o["trader"] == trader]
    # ordering from the stated rule: bids highest price then earliest; asks lowest price then earliest
    own = sorted([o for o in bids if o["trader"] == trader], key=lambda o: (-o["price"], o["seq"])) + \
        sorted([o for o in asks if o["trader"] == trader], key=lambda o: (o["price"], o["seq"]))
    if own and rng.randrange(100) < cancel_pct[trader]:
        target = own[rng.randrange(len(own))]
        if target in bids:
            bids.remove(target)
        else:
            asks.remove(target)
        trd_cancel += target["rem"]
        cancels[trader] += 1
        target["rem"] = 0
    else:
        side = 1 if rng.randrange(2) == 0 else -1
        qty = 10 * rng.randrange(1, 6)
        market = rng.randrange(100) < 10
        price = 10000 + rng.randrange(-20, 21)
        orders[trader] += 1
        entered += qty
        rem = qty
        if side > 0:
            book_opp = asks
        else:
            book_opp = bids
        def crosses(r_price):
            if market:
                return True
            return r_price <= price if side > 0 else r_price >= price
        while rem > 0 and book_opp:
            best = (sorted(book_opp, key=lambda o: (o["price"], o["seq"])) if side > 0
                    else sorted(book_opp, key=lambda o: (-o["price"], o["seq"])))[0]
            if not crosses(best["price"]):
                break
            q = min(rem, best["rem"])
            rem -= q
            best["rem"] -= q
            traded += q
            executions += 1
            fills[trader] += 1
            fills[best["trader"]] += 1
            if best["rem"] == 0:
                book_opp.remove(best)
        if rem > 0:
            if market:
                mkt_cancel += rem
                rem = 0
            else:
                rest = {"trader": trader, "price": price, "seq": seq, "rem": rem}
                (bids if side > 0 else asks).append(rest)
    bb = max((o["price"] for o in bids), default=None)
    ba = min((o["price"] for o in asks), default=None)
    if bb is not None and ba is not None and bb >= ba:
        crossed += 1
    if entered != resting_total() + 2 * traded + mkt_cancel + trd_cancel:
        ident_fail += 1

print(f"orders {sum(orders)}, executions {executions}, shares traded {traded}, trader cancel events {sum(cancels)}")
print(f"events with a crossed book: {crossed}")
print(f"identity failures: {ident_fail}")
print(f"shares resting {resting_total()}, market shares cancelled {mkt_cancel}, trader shares cancelled {trd_cancel}")
print(f"fills total {sum(fills)}, 2*executions {2 * executions}")
for t in range(6):
    r = Fraction(cancels[t], fills[t]) if fills[t] else None
    print(f"trader {t} cancel_pct {cancel_pct[t]} orders {orders[t]} cancels {cancels[t]} fills {fills[t]} ratio {r}")
