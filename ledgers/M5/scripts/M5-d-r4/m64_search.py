"""Search for an instance where the last-point change differs from the sup-norm change (m64 witness hunt).

Usage: python -I m64_search.py  (stdlib only). Prints the first witnesses found over random instances.
"""
import math
import random

def sweep(beta, alpha, grid, values):
    out = []
    for k in grid:
        av = k**alpha
        out.append(max(math.sqrt(av - s) + beta * c for s, c in zip(grid, values) if s <= av))
    return out

rng = random.Random(1)
found = 0
trials = 0
for _ in range(3000):
    beta = rng.randrange(80, 96) / 100
    alpha = rng.randrange(30, 71) / 100
    m = rng.randint(2, 12)
    first = rng.uniform(0.2, 0.9)
    steps = [rng.uniform(0.05, 0.4) for _ in range(m - 1)]
    grid = [first]
    for s in steps:
        grid.append(grid[-1] + s)
    if grid[0] > 1:
        continue
    trials += 1
    v = [0.0] * m
    for n in range(1, 60):
        new = sweep(beta, alpha, grid, v)
        sup = max(abs(a - b) for a, b in zip(new, v))
        last = abs(new[-1] - v[-1])
        if last < sup * (1 - 1e-9):
            found += 1
            if found <= 3:
                print("witness: beta", beta, "alpha", alpha, "grid", [round(g, 4) for g in grid], "sweep", n,
                      "sup change", sup, "last-point change", last)
            break
        v = new
print("trials", trials, "instances where last-point change < sup change within 59 sweeps:", found)
