"""Check the L04 Section 5 claim m_t = 10000 - 10*I_(t-1) under the Example 1.3 rule, on many seeds (PC3 slice d, round 1)."""
import random
from fractions import Fraction
bad = 0
checked = 0
for seed in range(2000):
    rng = random.Random(seed)
    inv, last, cash = 0, None, 0
    for t in range(1, 21):
        move = 5 if rng.random() < 0.5 else -5
        draw = rng.random()
        arrival = "ub" if draw < 0.25 else ("us" if draw < 0.5 else "inf")
        pass
    # independent generator: per-turn draws for the quote and arrivals, enumerated as a random walk
for seed in range(2000):
    rng = random.Random(seed)
    v = 10000
    inv, last = 0, None
    for t in range(1, 21):
        mid = 10000 if last is None else last
        checked += 1
        if mid != 10000 - 10 * inv:
            bad += 1
        bid, ask = mid - 10, mid + 10
        move = 5 if rng.random() < 0.5 else -5
        v += move
        arrival = rng.choice(["ub", "us", "inf", "inf"])
        side = 0
        if arrival == "ub":
            side = -1
        elif arrival == "us":
            side = 1
        elif v > ask:
            side = -1
        elif v < bid:
            side = 1
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            inv += side
            last = price
print("turn-quotes checked:", checked, "violations of m_t = 10000 - 10 I_(t-1):", bad)
