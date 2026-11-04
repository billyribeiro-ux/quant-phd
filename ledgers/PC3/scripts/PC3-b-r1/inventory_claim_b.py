"""Verifier PC3-b round 1: L04 Remark 4.2 says 'for a given quote the expected gain of the spread does not depend on
the position'. Enumerate the one-turn trade term c_t + sigma_t * v_t exactly under A1, A4 and A5 (fill refused when
|I| would exceed L = 10) for several inventories, quote 9990/10010 (h = 10), p = 1/2, fair value 10000.
Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r1/inventory_claim_b.py
"""
from __future__ import annotations

from fractions import Fraction

L = 10
P = Fraction(1, 2)
BID, ASK, SIZE = 9990, 10010, 1


def trade_term(inventory: int, v: int) -> Fraction:
    total = Fraction(0)
    outcomes: list[tuple[Fraction, int]] = [
        ((1 - P) / 2, -1),  # uninformed buy: maker sells one unit at the ask
        ((1 - P) / 2, +1),  # uninformed sell: maker buys one unit at the bid
    ]
    for prob, side in outcomes:
        filled = SIZE >= 1 and abs(inventory + side) <= L
        if filled:
            price = ASK if side < 0 else BID
            total += prob * (-side * price + side * v)
    # informed (A4): buy at ask if v > ask, sell at bid if v < bid, else nothing
    if v > ASK:
        side, price = -1, ASK
    elif v < BID:
        side, price = 1, BID
    else:
        side = 0
    if side != 0 and SIZE >= 1 and abs(inventory + side) <= L:
        total += P * (-side * price + side * v)
    return total


for inv in (0, 1, 9, 10, -10):
    print("inventory", inv, "expected trade term at v=10000:", trade_term(inv, 10000), "cents")
print("inventory 0 equals (1-p)h = 5 cents:", trade_term(0, 10000) == Fraction(5))
print("inventory 10 differs from inventory 0:", trade_term(10, 10000) != trade_term(0, 10000))
