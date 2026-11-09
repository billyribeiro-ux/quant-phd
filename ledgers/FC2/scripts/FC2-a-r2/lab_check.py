"""FC2-a round 2: independent recount of the L01 lab claims (box counts, dominance pairs) and the L03 path claims.

Written separately from tests/labs/FC2/lab-FC2-L01-1.py; uses only integer arithmetic scaled by 10 (prices 9/10 and
1/2 and 1 become integers 9, 5, 10 in tenths; payoffs are integers). Run: python3 -I ledgers/FC2/scripts/FC2-a-r2/lab_check.py
"""

from __future__ import annotations

import itertools
import random

BOX = range(-10, 11)
SMALL = range(-2, 3)
# payoff rows: state u (bond 1, stock 3), state d (bond 1, stock 1); prices in tenths
PAY = {"u": (1, 3), "d": (1, 1)}


def payoff(h: tuple[int, int]) -> tuple[int, int]:
    b, s = h
    return (b * PAY["u"][0] + s * PAY["u"][1], b * PAY["d"][0] + s * PAY["d"][1])


def cost_tenths(h: tuple[int, int], bond: int, stock: int) -> int:
    return h[0] * bond + h[1] * stock


def arbitrage_count(bond: int, stock: int) -> int:
    n = 0
    for h in itertools.product(BOX, BOX):
        c = cost_tenths(h, bond, stock)
        pu, pd = payoff(h)
        if c <= 0 and pu >= 0 and pd >= 0 and (c < 0 or pu > 0 or pd > 0):
            n += 1
    return n


def dominance(bond: int, stock: int) -> tuple[int, int]:
    dom = bad = 0
    for a in itertools.product(SMALL, SMALL):
        pa = payoff(a)
        for b in itertools.product(SMALL, SMALL):
            pb = payoff(b)
            if pa[0] >= pb[0] and pa[1] >= pb[1]:
                dom += 1
                if cost_tenths(a, bond, stock) < cost_tenths(b, bond, stock):
                    bad += 1
    return dom, bad


print("Part A (bond 9/10, stock 1, in tenths 9, 10): arbitrage count in box =", arbitrage_count(9, 10))
print("Part A dominance pairs, misordered =", dominance(9, 10))
print("Part B (bond 9/10, stock 1/2, in tenths 9, 5): arbitrage count in box =", arbitrage_count(9, 5))
print("Part B dominance pairs, misordered =", dominance(9, 5))
zc = [h for h in itertools.product(BOX, BOX) if cost_tenths(h, 9, 5) == 0 and all(x > 0 for x in payoff(h))]
print("Part B zero-cost portfolios with strictly positive payoff in both states, first in lex order =", zc[:1])
print("  count of such portfolios in box =", len(zc))
zc_any = [h for h in itertools.product(BOX, BOX) if cost_tenths(h, 9, 5) == 0 and h != (0, 0)]
print("  zero-cost nonzero holdings in box, count =", len(zc_any), "(multiples of (-5, 9) within the box)")

# L03 Part A: seeded path, exact replication of the page generator
rng = random.Random(20261028)
path = [5000]
for _ in range(10):
    path.append(path[-1] + rng.randint(-40, 40))
print("L03 path:", " ".join(map(str, path)))
margins = [path[i] - path[i - 1] for i in range(1, len(path))]
print("L03 margins:", " ".join(map(str, margins)))
print("L03 balance after day 10:", sum(margins), "settlement minus initial:", path[-1] - path[0])
print("L03 loss days:", sum(1 for m in margins if m < 0))
