"""Verifier PC3-b round 1: enumerate Proposition 3.1 (expected trade term from inventory zero) over random integer
quotes and fair values, for several informed shares p, with exact Fractions, and compare with the closed form.
Also checks Corollary 3.3 (p=1/2, v>=a) and the Problem R1 distance d=(1-p)h/p. Independent of the lab twins.
Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r1/prop31_b.py
"""
from __future__ import annotations

import random
from fractions import Fraction


def enum_term(v: int, a: int, b: int, p: Fraction, limit: int = 10) -> Fraction:
    total = Fraction(0)
    # uninformed buy and sell, probability (1-p)/2 each; both fill from inventory 0 (limit >= 1)
    total += (1 - p) / 2 * ((a - v) + (v - b))
    # informed: buys at ask if v > a, sells at bid if v < b, else nothing
    if v > a:
        total += p * (a - v)
    elif v < b:
        total += p * (v - b)
    return total


def closed(v: int, a: int, b: int, p: Fraction) -> Fraction:
    h = Fraction(a - b, 2)
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))


rng = random.Random(7)
n_cases = 0
for _ in range(5000):
    b = rng.randint(1, 20000)
    h = rng.randint(1, 50)
    a = b + 2 * h
    v = rng.randint(1, 20000)
    p = rng.choice([Fraction(1, 3), Fraction(1, 2), Fraction(3, 5), Fraction(7, 10)])
    assert enum_term(v, a, b, p) == closed(v, a, b, p), (v, a, b, p)
    n_cases += 1
print("Proposition 3.1 enumeration equals closed form on", n_cases, "random cases (exact Fractions)")

# Corollary 3.3: p=1/2, v>=a -> zero iff v=a+h
for h in range(1, 30):
    a, b = 10000, 10000 - 2 * h + 2 * h  # placeholder, rebuilt below
    for v in range(a, a + 60):
        b = a - 2 * h
        zero = closed(v, a, b, Fraction(1, 2)) == 0
        assert zero == (v == a + h), (h, v)
print("Corollary 3.3 holds for h in 1..29 and v in [a, a+60)")

# Problem R1: p=3/5, h=10, v=a+d, E=(1-p)h - p d, zero at d=(1-p)h/p
p = Fraction(3, 5)
d = (1 - p) * 10 / p
print("R1 d =", d, float(d), "E at d:", (1 - p) * 10 - p * d)
