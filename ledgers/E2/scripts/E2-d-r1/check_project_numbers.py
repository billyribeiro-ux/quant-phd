"""Verifier check of the arithmetic printed in course/modules/E/E2/project.html and the cards' exact claims.

Usage: .venv/bin/python -I ledgers/E2/scripts/E2-d-r1/check_project_numbers.py
"""

from __future__ import annotations

import itertools
from fractions import Fraction

# Lab 1 (rung 1) values
print("lab1 gap share", round(100 * 1700 / 9600, 1))
# Lab 3 (rung 3 check) values
print("lab3 gap share", round(100 * 3100 / 18600, 1), "efficiency", round(100 * 22800 / 23700, 1))
# A3 expected order statistics for n = 2..5, first and second price
for n in range(2, 6):
    e1 = 1 - Fraction(1, n + 1)
    e2 = 1 - Fraction(1, n + 1) - Fraction(1, n + 1)
    first = Fraction(n - 1, n) * e1
    print("n", n, "E[V1]", e1, "E[V2]", e2, "first", first, "equal", first == e2)
# symmetric bid, half up, exact integers vs Fraction
for n in range(2, 6):
    for v in range(0, 10001):
        exact = Fraction((n - 1) * v, n)
        import math

        assert (2 * (n - 1) * v + n) // (2 * n) == math.floor(exact + Fraction(1, 2))
print("symmetric bid integer formula equals half-up Fraction rounding on n 2..5, v 0..10000")
# Four-bidder, two-unit count of profiles with bids in {0..3}
eq = hi = lo = 0
for b in itertools.product(range(4), repeat=4):
    s = sorted(b, reverse=True)
    d, u = s[0] + s[1], 2 * s[2]
    eq, hi, lo = (eq + (d == u), hi + (d > u), lo + (d < u))
print("profiles equal, higher, lower", eq, hi, lo)
