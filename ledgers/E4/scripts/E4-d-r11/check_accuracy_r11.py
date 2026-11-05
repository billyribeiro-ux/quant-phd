"""Check the page's accuracy requirement (project.html Constraints) for each solver file.

Requirement: for an interior root, when noise volume >= 1e-50 and tau-bar >= 1e-2, |lam - root| <= min(1e-10, 1e-8 * root),
where root = 2 sigma sqrt(tb / (1 - tb)) (Proposition 4 with a = 2, tau_e = 1, tau_v = 1), tb = 2 exp(-4c) - 1.
Usage: python3 -I check_accuracy_r11.py <root> <n_random> <seed> <solver.py> [<solver.py> ...]
"""
import importlib.util
import math
import random
import sys

root, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
paths = sys.argv[4:]
rng = random.Random(seed)


def load(path, i):
    spec = importlib.util.spec_from_file_location(f"solver_{i}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def closed(sd, tb):
    return 2.0 * sd * math.sqrt(tb / (1.0 - tb))


cases = []
# log-uniform noise volumes in [1e-50, 1e3] and costs with tau-bar in [1e-2, tau_y(1)) so the root is interior
while len(cases) < n:
    sd = 10 ** rng.uniform(-50, 3)
    c = rng.uniform(0.0, 0.5)
    tb = 2.0 * math.exp(-4.0 * c) - 1.0
    if not (1e-2 <= tb < 1.0 / (1.0 + 4.0 * sd * sd)):
        continue
    cases.extend([(sd, c, tb)])
# the page's box corners and the boundary of the tau-bar range
for sd in (1e-50, 0.5, 0.75, 1e3):
    for tb in (1e-2, 0.0977, 0.2376):
        if tb < 1.0 / (1.0 + 4.0 * sd * sd):
            c = -math.log((tb + 1.0) / 2.0) / 4.0
            cases.append((sd, c, tb))
for i, path in enumerate(paths):
    mod = load(path, i)
    worst = 0.0
    fails = 0
    worst_case = None
    for sd, c, tb in cases:
        lam = mod.solve_model(sd, c)["informed_fraction"]
        exact = closed(sd, tb)
        tol = min(1e-10, 1e-8 * exact)
        ratio = abs(lam - exact) / tol
        if ratio > worst:
            worst, worst_case = ratio, (sd, c, lam, exact)
        if ratio > 1.0:
            fails += 1
    print(f"{path.split('/')[-1]}: cases={len(cases)} fails={fails} worst |err|/tol={worst:.3e} at "
          f"sd={worst_case[0]:.3e} c={worst_case[1]:.6f} lam={worst_case[2]:.6e} closed={worst_case[3]:.6e}")
