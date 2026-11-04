"""Seed sweep for the L02 lab identities: the dyadic count and the grid-supremum equality should hold for every seed.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r4/seed_sweep_L02.py
"""
import random

LEVELS = 8
GRID = [i / 2**10 for i in range(2**10 + 1)]


def hat(m, j, t):
    return max(0.0, 1.0 - 2.0**m * abs(t - (2 * j - 1) / 2.0**m))


def make(seed):
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
    return xi0, coeffs


def partial(xi0, coeffs, levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total


dy_fail = 0
sup_fail = 0
within_counts = []
SEEDS = range(200)
for seed in SEEDS:
    xi0, coeffs = make(seed)
    eq = 0
    cases = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = partial(xi0, coeffs, n, t)
            for levels in range(n, LEVELS + 1):
                cases += 1
                eq += partial(xi0, coeffs, levels, t) == base
    if eq != cases or cases != 216:
        dy_fail += 1
    for m in range(1, LEVELS + 1):
        scale = 2 ** (-(m + 1) / 2)
        gs = max(abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * scale) for t in GRID)
        formula = max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
        if gs != formula:
            sup_fail += 1
            break
    within = sum(
        max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2) <= __import__("math").sqrt(4 * m * __import__("math").log(2)) * 2 ** (-(m + 1) / 2)
        for m in range(1, LEVELS + 1)
    )
    within_counts.append(within)
print(f"seeds 0..{len(SEEDS) - 1}: dyadic identity failures {dy_fail}; grid-sup identity failures {sup_fail}")
print("levels within bound, over seeds: min", min(within_counts), "max", max(within_counts),
      "seeds with all 8 within:", sum(1 for w in within_counts if w == 8))
