"""Check every instance for seeds 0-49 against the instance.py docstring ranges, ties and variety (round 2)."""

import importlib.util
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
spec = importlib.util.spec_from_file_location("instance", os.path.join(REPO, "course/modules/M/M5/grader/instance.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def solve(beta, alpha, grid, tol):
    v = [0.0] * len(grid)
    n = 0
    while True:
        n += 1
        new = []
        for k in grid:
            cap = k**alpha
            new.append(max(math.sqrt(cap - kp) + beta * v[j] for j, kp in enumerate(grid) if kp <= cap))
        change = max(abs(a - b) for a, b in zip(new, v))
        v = new
        if (beta / (1 - beta)) * change <= tol:
            return tuple(round(x, 9) for x in v), n


bad = []
betas, alphas, sizes, vectors = set(), set(), set(), set()
for seed in range(50):
    inst = mod.make_instance(seed)
    b, a, g, t = inst["beta"], inst["alpha"], inst["grid"], inst["tol"]
    ok = (
        inst["label"] == "SIMULATED"
        and 0.80 <= b <= 0.95 and 0.30 <= a <= 0.70
        and 8 <= len(g) <= 24
        and 0.20 <= g[0] <= 0.90
        and all(0.05 - 1e-12 <= g[i + 1] - g[i] <= 0.40 + 1e-12 for i in range(len(g) - 1))
        and g[-1] > 1.0
        and all(g[i] < g[i + 1] for i in range(len(g) - 1))
        and t in (1e-6, 1e-8, 1e-10)
        and all(abs(p - k**a) > 1e-6 for k in g for p in g)
    )
    if not ok:
        bad.append(seed)
    betas.add(b); alphas.add(a); sizes.add(len(g))
    v, n = solve(b, a, g, t)
    vectors.add(v)
print("invalid seeds", bad)
print("distinct betas", len(betas), "alphas", len(alphas), "sizes", len(sizes), "distinct solved vectors (9dp)", len(vectors))
print("sample seed 0:", mod.make_instance(0))
print("sample seed 7919:", mod.make_instance(7919))
