"""Slice d round 1: search grids wholly in (0, 1] for a solver-level difference between the reference and mutant d1_01.

Run from the checkout root: python3 -I ledgers/M5/scripts/M5-d-r1/d_search_solver_diff.py
"""

import importlib.util
import os
import random

ROOT = os.getcwd()


def load(name: str, path: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


ref = load("ref_mod", os.path.join(ROOT, "course/modules/M/M5/grader/reference.py"))
mut = load("mut_mod", os.path.join(ROOT, "ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py"))
rng = random.Random(2026)
found = None
trials = 0
op_diff = 0
for trial in range(3000):
    trials += 1
    m = rng.randrange(2, 7)
    grid = sorted(rng.sample([round(rng.uniform(0.05, 1.0), 2) for _ in range(40)], m))
    if len(set(grid)) != m or grid[-1] > 1.0:
        continue
    beta = rng.randrange(80, 96) / 100
    alpha = rng.randrange(30, 71) / 100
    p = {"beta": beta, "alpha": alpha}
    a = ref.solve(p, grid, 1e-10, 100000)
    b = mut.solve(p, grid, 1e-10, 100000)
    if a["value"] != b["value"]:
        found = (grid, beta, alpha, a["value"], b["value"])
        break
    if ref.bellman_operator(p, grid, [0.0] * m) != mut.bellman_operator(p, grid, [0.0] * m):
        op_diff += 1
print("trials:", trials, "operator-at-zero differences seen before stop:", op_diff)
print("first solver-level difference:", found)
