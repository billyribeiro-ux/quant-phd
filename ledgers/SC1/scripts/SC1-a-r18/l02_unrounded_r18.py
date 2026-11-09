"""SC1-a round 18: unrounded values of the seeded L02 lab sample (seed 20260101), for the E3 exercise and the tail line."""

import math
import random

SEED, LEVELS, GRID_DEPTH = 20260101, 8, 10


def hat(m, j, t):
    c = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0**m * abs(t - c))


def psum(xi0, coeffs, levels, t):
    tot = xi0 * t
    for m in range(1, levels + 1):
        sc = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            tot += coeffs[m - 1][j - 1] * sc * hat(m, j, t)
    return tot


rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
print(f"xi_0 = {xi0!r}")
print(f"xi_11 = {coeffs[0][0]!r}; |xi_11| = {abs(coeffs[0][0]):.9f}; |xi_11| rounded to 6 dp = {abs(coeffs[0][0]):.6f}")
sup1 = abs(coeffs[0][0]) * 2 ** (-1)
print(f"level-1 sup (unrounded) = {sup1:.10f}; printed 6 dp = {sup1:.6f}")
grid = [i / 2**GRID_DEPTH for i in range(2**GRID_DEPTH + 1)]
sups = [max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2) for m in range(1, LEVELS + 1)]
bounds = [math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(1, LEVELS + 1)]
print("sups:   " + " ".join(f"{s:.6f}" for s in sups))
print("bounds: " + " ".join(f"{b:.6f}" for b in bounds))
print(f"sum of bounds m=5..8 (unrounded) = {sum(bounds[4:]):.6f}")
tail = max(abs(psum(xi0, coeffs, 8, t) - psum(xi0, coeffs, 4, t)) for t in grid)
print(f"grid sup |Sigma_8 - Sigma_4| = {tail:.6f}")
