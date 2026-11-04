"""Independent re-implementation of the seeded numbers of SC1 labs L02 and L03 (verifier round 1).

Uses its own hat evaluation (piecewise linear interpolation of the hat's breakpoints) and its own draws, so it does
not import or copy the lab twins. The same seed and draw order as the page's description are used: xi_0 first, then the
level-m coefficients m = 1..8 in order of j. Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r1/recompute_lab_L02_L03.py
"""

import math
import random
from fractions import Fraction

SEED_L02 = 20260101
rng = random.Random(SEED_L02)
xi0 = rng.gauss(0.0, 1.0)
coef = {}
for m in range(1, 9):
    for j in range(1, 2 ** (m - 1) + 1):
        coef[(m, j)] = rng.gauss(0.0, 1.0)


def hat_piecewise(m, j, t):
    # breakpoints (2j-2)2^-m (value 0), (2j-1)2^-m (value 1), 2j 2^-m (value 0); linear in between, zero outside
    a = (2 * j - 2) / 2**m
    c = (2 * j - 1) / 2**m
    b = (2 * j) / 2**m
    if t <= a or t >= b:
        return 0.0
    if t <= c:
        return (t - a) / (c - a)
    return (b - t) / (b - c)


def term(m, t):
    s = 0.0
    for j in range(1, 2 ** (m - 1) + 1):
        s += coef[(m, j)] * 2 ** (-(m + 1) / 2) * hat_piecewise(m, j, t)
    return s


grid = [i / 1024 for i in range(1025)]
print("observed sup per level (grid of 2^-10) vs closed formula and bound:")
for m in range(1, 9):
    grid_sup = max(abs(term(m, t)) for t in grid)
    closed = max(abs(coef[(m, j)]) for j in range(1, 2 ** (m - 1) + 1)) * 2 ** (-(m + 1) / 2)
    bound = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
    print(f"  m={m} grid_sup={grid_sup:.6f} closed={closed:.6f} bound={bound:.6f} within={closed <= bound}")


def S(M, t):
    return xi0 * t + sum(term(m, t) for m in range(1, M + 1))


tail = max(abs(S(8, t) - S(4, t)) for t in grid)
print(f"grid sup |S_8 - S_4| = {tail:.6f} (page 0.348139)")

# dyadic equality: values at depth n equal values at all levels M >= n (exact in floats here, compare with tolerance 1e-15)
cnt = 0
tot = 0
for n in range(5):
    for k in range(2**n + 1):
        t = k / 2**n
        for M in range(n, 9):
            tot += 1
            cnt += abs(S(M, t) - S(n, t)) < 1e-12
print(f"dyadic values fixed from level n on: {cnt} of {tot} (page 216 of 216)")

print("== L03 (own draws with its own seed; SE and z recomputed from the page's formulas)")
SEED_L03 = 20260503
r3 = random.Random(SEED_L03)
for H in (1.0, 2.0):
    for k in range(8):
        N = 2**k
        sums = []
        for _ in range(400):
            tot_q = 0.0
            sd = math.sqrt(H / N)
            for _ in range(N):
                x = r3.gauss(0.0, sd)
                tot_q += x * x
            sums.append(tot_q)
        mean = sum(sums) / 400
        var = sum((v - mean) ** 2 for v in sums) / 399
        se = math.sqrt(var / 400)
        print(f"  H={H:g} N={N:3d} mean={mean:.4f} se={se:.4f} z={(mean - H) / se:+.2f}")
