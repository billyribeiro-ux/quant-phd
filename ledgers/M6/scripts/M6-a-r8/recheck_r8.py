"""Independent exact recomputation of the numbers in the round-8 changed hunks (M6-a).

Run from the checkout root: .venv/bin/python -I ledgers/M6/scripts/M6-a-r8/recheck_r8.py
"""

from fractions import Fraction
from itertools import product

# L02 numeric item and E1 / quiz item: additivity failures for nu(A) = (|A|/6)^2 over disjoint ordered pairs.
omega = range(6)
subsets = [frozenset(i for i in omega if (m >> i) & 1) for m in range(64)]


def nu(a: frozenset[int]) -> Fraction:
    return Fraction(len(a), 6) ** 2


pairs = [(a, b) for a, b in product(subsets, repeat=2) if not (a & b)]
fail = [(a, b) for a, b in pairs if nu(a | b) != nu(a) + nu(b)]
empty_pairs = sum(1 for a, b in pairs if not a or not b)
print(f"disjoint ordered pairs: {len(pairs)} (3^6 = {3**6})")
print(f"pairs with an empty member: {empty_pairs} (64 + 64 - 1 = 127)")
print(f"additivity failures: {len(fail)}; 729 - 127 = {729 - 127}")
print(f"failures are exactly the pairs with both members non-empty: {all(a and b for a, b in fail)}")

# L02 numeric item: P({1,2}) + P({2,3}) on the fair die and 2/3 to six places.
p = lambda a: Fraction(len(a), 6)  # noqa: E731
s = p(frozenset({0, 1})) + p(frozenset({1, 2}))
print(f"P({{1,2}}) + P({{2,3}}) = {s}; to six places: {float(s):.6f}")

# L04 R2 solution: g = floor(x^(-1/2)) equals n on (1/(n+1)^2, 1/n^2]; its integral sum is finite and the length formula holds.
for n in range(1, 6):
    length = Fraction(1, n * n) - Fraction(1, (n + 1) ** 2)
    assert length == Fraction(2 * n + 1, n * n * (n + 1) ** 2)
    assert Fraction(2 * n + 1, n * (n + 1) ** 2) <= Fraction(3, n * n)
print("R2: interval length (2n+1)/(n^2 (n+1)^2) and term bound 3/n^2 hold for n = 1..5")

# L04 lab partial sums: sum of 1/(n+1), n = 1..N, rounded from the exact value.
for big_n in (10, 100):
    total = sum((Fraction(1, n + 1) for n in range(1, big_n + 1)), Fraction(0))
    print(f"N = {big_n}: exact sum of 1/(n+1) to six places = {float(total):.6f}")

# L04 Part A zero pattern: f_n(1/5) = n for n <= 5 and 0 for n >= 6.
x = Fraction(1, 5)
print("f_n(1/5), n = 1..8:", [n if x <= Fraction(1, n) else 0 for n in range(1, 9)])
