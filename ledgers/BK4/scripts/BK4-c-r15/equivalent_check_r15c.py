"""Equivalence check for the float-floor cover (r15c): math.floor(10000*c/S) vs 10000*c//S.

Exhaustive for every 0 <= c <= S <= 2000, and random spot checks for S up to 10**7 (the largest list a
learner can hold in memory). The proof is the argument in fragment row proj-mutant-r15c-equivalent.
"""
import math
import random

bad = 0
checked = 0
for s in range(1, 2001):
    for c in range(0, s + 1):
        checked += 1
        if math.floor(10_000 * c / s) != 10_000 * c // s:
            bad += 1
print(f"exhaustive S<=2000: {checked} pairs, disagreements {bad}")
rng = random.Random(15)
spot = 0
for _ in range(200_000):
    s = rng.randint(1, 10_000_000)
    c = rng.randint(0, s)
    spot += 1
    if math.floor(10_000 * c / s) != 10_000 * c // s:
        bad += 1
print(f"random S<=10^7: {spot} pairs, disagreements {bad}")
