"""Round-21 verifier sweep: the reference's reported fraction against the closed form of Proposition 4.

Domain of the page's accuracy clause: noise volume >= 1e-50 and tau-bar >= 1e-2 (interior roots only).
Usage: python3 -I root_accuracy_sweep_r21.py <path-to-reference.py>
Prints the count of interior points, the worst relative error and the count above 1e-10 relative.
"""

import importlib.util
import math
import sys

spec = importlib.util.spec_from_file_location("ref", sys.argv[1])
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)  # type: ignore[union-attr]

A, TV, TE = 2.0, 1.0, 1.0


def closed(sd: float, cost: float) -> float:
    t = (TV + TE) * math.exp(-2.0 * A * cost) - TV
    if t <= 0.0:
        return 0.0
    if t >= TE * TE / (TE + A * A * sd * sd):
        return 1.0
    return A * sd * math.sqrt(t / (TE * (TE - t)))


n = 0
worst = 0.0
worst_at = None
above = 0
for i in range(200):
    sd = 10 ** (-50 + 52 * i / 199)  # 1e-50 .. 1e2
    for j in range(120):
        cost = 0.0 + 0.4 * j / 119  # 0 .. 0.4
        t = (TV + TE) * math.exp(-2.0 * A * cost) - TV
        if t < 1e-2:
            continue
        exact = closed(sd, cost)
        if not (0.0 < exact < 1.0):
            continue
        lam = ref.solve_model(sd, cost)["informed_fraction"]
        n += 1
        rel = abs(lam - exact) / exact
        if rel > 1e-10:
            above += 1
        if rel > worst:
            worst, worst_at = rel, (sd, cost, exact, lam)
print("interior points", n, "above 1e-10 relative", above, "worst relative", f"{worst:.3e}", "at", worst_at)
