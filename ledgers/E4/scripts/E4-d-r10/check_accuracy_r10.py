"""Round-10 accuracy check (E4 slice d): the reference solver against the closed form of Proposition 4 on the domain the
page states for the accuracy requirement: noise volume from 1e-50 to 1e3, tau-bar at least 1e-2, interior root.

Run: /Users/billyribeiro/dev/quant-phd/.venv/bin/python -I check_accuracy_r10.py > logs/check_accuracy_r10.txt
"""

import importlib.util
import math
import random

REFERENCE = "/Users/billyribeiro/dev/quant-phd/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("reference", REFERENCE)
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def tbar(cost: float) -> float:
    return 2.0 * math.exp(-4.0 * cost) - 1.0


def closed_form(sd: float, cost: float) -> float:
    t = tbar(cost)
    if t <= 0.0:
        return 0.0
    if t >= 1.0 / (1.0 + 4.0 * sd * sd):
        return 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


c_hi = -math.log(0.505) / 4.0  # the cost at which tau-bar equals 0.01
print("cost at which tau-bar = 0.01:", repr(c_hi), "tau-bar there:", repr(tbar(c_hi)))
rng = random.Random(11)
cases = 0
violations = 0
worst = 0.0
worst_case = None
min_root = math.inf
for _ in range(20000):
    sd = 10 ** rng.uniform(-50, 3)
    cost = rng.uniform(1e-9, c_hi)
    if tbar(cost) < 0.01:
        continue
    root = closed_form(sd, cost)
    if not (0.0 < root < 1.0):
        continue
    cases += 1
    min_root = min(min_root, root)
    lam = ref.solve_model(sd, cost)["informed_fraction"]
    err = abs(lam - root)
    tol = min(1e-10, 1e-8 * root)
    if err / tol > worst:
        worst = err / tol
        worst_case = (sd, cost, root, lam)
    if err > tol:
        violations += 1
print("interior cases:", cases)
print("violations of min(1e-10, 1e-8 * root):", violations)
print("largest error as a fraction of the allowed tolerance:", f"{worst:.4f}")
print("worst case (sd, cost, closed form, solver):", worst_case)
print("smallest closed-form root in the sample:", f"{min_root:.3e}")
