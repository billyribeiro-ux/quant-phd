"""Exact enumeration of the one-turn trade term (c_t + sigma_t v) at inventory I, quote bid/ask, size 1, limit 10.

Usage: python -I remark42_enum.py. Uses fractions only; implements A1, A4, A5 as stated on L04 page.
"""
from fractions import Fraction

L = 10
P = {"ub": Fraction(1, 4), "us": Fraction(1, 4), "inf": Fraction(1, 2)}


def term(inv: int, v: int, b: int, a: int) -> Fraction:
    total = Fraction(0)
    for arr, pr in P.items():
        if arr == "ub":
            side = -1
        elif arr == "us":
            side = 1
        else:
            side = -1 if v > a else (1 if v < b else 0)
        if side == 0:
            continue
        if abs(inv + side) > L:  # A5: refused
            continue
        price = a if side < 0 else b
        total += pr * (-side * price + side * v)
    return total


b, a = 9990, 10010
for inv in (0, 1, 3, 9, 10, -10):
    print("I", inv, "E[trade term] at v=10000:", term(inv, 10000, b, a))
# inventory-invariance for |I| <= L-1 over a fair-value grid
ok = all(term(i, v, b, a) == term(0, v, b, a) for i in range(-9, 10) for v in range(9900, 10101, 5))
print("for |I|<=9 the trade term equals the I=0 value on the grid 9900..10100 step 5:", ok)
bad = [(i, v) for i in (-10, 10) for v in range(9900, 10101, 5) if term(i, v, b, a) != term(0, v, b, a)]
print("at |I|=10 the grid points where the term differs from I=0:", len(bad), "of", 2 * len(range(9900, 10101, 5)))
