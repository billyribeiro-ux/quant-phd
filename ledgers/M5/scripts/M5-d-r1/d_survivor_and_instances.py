"""Slice d round 1: instance validity and answer variety (seeds 0-49), and the top-grid-point survivor.

Run: python3 -I ledgers/M5/scripts/M5-d-r1/d_survivor_and_instances.py   (from the checkout root)
Imports the grader's instance.py and reference.py and the mutant d1_01 by file path; prints the observed values.
"""

import importlib.util
import math
import os
import random

ROOT = os.getcwd()


def load(name: str, path: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


inst = load("instance_mod", os.path.join(ROOT, "course/modules/M/M5/grader/instance.py"))
ref = load("ref_mod", os.path.join(ROOT, "course/modules/M/M5/grader/reference.py"))
mut = load("mut_mod", os.path.join(ROOT, "ledgers/M5/mutants/d1_01_top_grid_point_never_a_successor.py"))

print("== instance validity, seeds 0-49")
betas, alphas, sizes, tols, ends, stars = set(), set(), set(), set(), [], []
bad = []
for seed in range(50):
    i = inst.make_instance(seed)
    g, b, a, t = i["grid"], i["beta"], i["alpha"], i["tol"]
    ok = (
        0.80 <= b <= 0.95 and 0.30 <= a <= 0.70 and 8 <= len(g) <= 24 and all(g[j] < g[j + 1] for j in range(len(g) - 1))
        and 0.20 <= g[0] <= 0.90 and g[0] <= 1 and g[-1] > 1 and t in (1e-6, 1e-8, 1e-10)
        and all(x > 0 for x in g) and all(0.05 - 1e-12 <= g[j + 1] - g[j] <= 0.40 + 1e-12 for j in range(len(g) - 1))
    )
    # clear of ties: no grid point within 1e-6 of a resource level
    clear = all(abs(p - k**a) > 1e-6 for k in g for p in g)
    if not (ok and clear):
        bad.append(seed)
    betas.add(b), alphas.add(a), sizes.add(len(g)), tols.add(t)
    ends.append(g[-1])
    stars.append(tuple(ref.solve({"beta": b, "alpha": a}, g, t, 100000)["value"]))
print("invalid seeds:", bad)
print("distinct betas:", len(betas), "distinct alphas:", len(alphas), "distinct sizes:", len(sizes), "distinct tols:", sorted(tols))
print("distinct solved value vectors:", len(set(stars)), "of 50")
print("last grid point range:", min(ends), max(ends))

print("== top grid point is never feasible on grader instances (k' <= k**alpha < k_m for all states)")
equal_all = True
rng = random.Random(12345)
for seed in range(50):
    i = inst.make_instance(seed)
    p = {"beta": i["beta"], "alpha": i["alpha"]}
    for _ in range(5):
        v = [rng.uniform(0.0, 4.0) for _ in i["grid"]]
        if ref.bellman_operator(p, i["grid"], v) != mut.bellman_operator(p, i["grid"], v):
            equal_all = False
print("reference and mutant d1_01 agree on all 50 instances x 5 random vectors:", equal_all)

print("== a grid wholly in (0, 1] distinguishes them (spec: maximum over the feasible grid points; (0,1] grids valid)")
p = {"beta": 0.9, "alpha": 0.5}
g = [0.5, 1.0]
v = [0.0, 10.0]
print("reference:", ref.bellman_operator(p, g, v))
print("mutant d1_01:", mut.bellman_operator(p, g, v))
print("solve reference (value, iterations, converged):", ref.solve(p, g, 1e-6, 1000)["value"][1], ref.solve(p, g, 1e-6, 1000)["converged"])
print("solve mutant:", mut.solve(p, g, 1e-6, 1000)["value"][1], mut.solve(p, g, 1e-6, 1000)["converged"])
print("analytic check: from k=1.0 the saving 1.0 leaves consumption 0, so the value is sqrt(0) + 0.9*10 =", math.sqrt(0) + 0.9 * 10)
