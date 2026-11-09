"""Slice d round 1: the fixed point on the grid [0.06, 0.07, 0.24] (wholly in (0, 1]) by an independent loop.

Run from the checkout root: python3 -I ledgers/M5/scripts/M5-d-r1/d_top_point_fixed_point.py
Compares this file's own value iteration with the reference solver and the survivor mutant d1_01.
"""

import importlib.util
import math
import os

ROOT = os.getcwd()


def load(name, path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


ref = load("ref_mod", os.path.join(ROOT, "course/modules/M/M5/grader/reference.py"))
mut = load("mut_mod", os.path.join(ROOT, "ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py"))

beta, alpha = 0.83, 0.53
grid = [0.06, 0.07, 0.24]
V = [0.0] * 3
for _ in range(100000):
    new = []
    for k in grid:
        r = k**alpha
        new.append(max(math.sqrt(r - kp) + beta * V[j] for j, kp in enumerate(grid) if kp <= r))
    change = max(abs(a - b) for a, b in zip(new, V))
    V = new
    if beta / (1 - beta) * change <= 1e-12:
        break
print("own fixed point:", [repr(x) for x in V])
print("reference value:", [repr(x) for x in ref.solve({"beta": beta, "alpha": alpha}, grid, 1e-12, 100000)["value"]])
print("mutant d1_01 value:", [repr(x) for x in mut.solve({"beta": beta, "alpha": alpha}, grid, 1e-12, 100000)["value"]])
r = grid[2] ** alpha
print("from k=0.24 resources", repr(r), "saving 0.24 feasible:", 0.24 <= r, "value of saving 0.24:", repr(math.sqrt(r - 0.24) + beta * V[2]), "value of saving 0.07:", repr(math.sqrt(r - 0.07) + beta * V[1]))
