"""Tests the L02 lab docstring claim that the dyadic count and the grid-supremum identity hold for every seed.
Runs the twin's functions with SEED replaced by seeds 0..299 (and the production seed), counts agreements.
Usage: python -I l02_identities_seeds_r12.py <checkout>"""
import math
import random
import sys

src = open(sys.argv[1] + "/tests/labs/SC1/lab-SC1-L02-1.py", encoding="utf-8").read().rsplit("\nmain()", 1)[0]
ns: dict[str, object] = {}
exec(compile(src, "twin", "exec"), ns)
partial_sum, hat, level_term_sup = ns["partial_sum"], ns["hat"], ns["level_term_sup"]
LEVELS, GRID_DEPTH = ns["LEVELS"], ns["GRID_DEPTH"]

def identities(seed: int) -> tuple[bool, bool, bool]:
    rng = random.Random(seed)
    xi0 = rng.gauss(0.0, 1.0)
    coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, LEVELS + 1)]
    fixed_equal = 0
    cases = 0
    for n in range(5):
        for k in range(2**n + 1):
            t = k / 2**n
            base = partial_sum(xi0, coeffs, n, t)
            for levels in range(n, LEVELS + 1):
                cases += 1
                fixed_equal += partial_sum(xi0, coeffs, levels, t) == base
    grid = [i / 2**GRID_DEPTH for i in range(2**GRID_DEPTH + 1)]
    sup_ok = True
    for m in range(1, LEVELS + 1):
        scale = 2 ** (-(m + 1) / 2)
        grid_sup = max(abs(sum(coeffs[m - 1][j - 1] * hat(m, j, t) for j in range(1, 2 ** (m - 1) + 1)) * scale) for t in grid)
        sup_ok = sup_ok and grid_sup == level_term_sup(coeffs[m - 1], m)
    return fixed_equal == cases, sup_ok, cases == 216

bad = []
for seed in list(range(300)) + [20260101]:
    a, b, c = identities(seed)
    if not (a and b and c):
        bad.append((seed, a, b, c))
print("seeds tested: 301; failures:", bad)
