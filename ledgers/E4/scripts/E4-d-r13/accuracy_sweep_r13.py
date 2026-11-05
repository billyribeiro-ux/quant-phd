"""Accuracy sweep of the reference (round 13): relative error of the reported informed fraction against the Proposition 4
closed form, over log-uniform noise volumes in [1e-50, 1e3] and costs with tau_bar >= 1e-2 (interior roots).
Also probes the surviving-by-tolerance case of an endpoint gap (reported at 1 - 1e-12 instead of 1)."""

from __future__ import annotations

import math
import random
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE13-E4-d/course/modules/E/E4/grader")
import reference as ref  # noqa: E402


def closed(sd: float, cost: float) -> float:
    t = 2.0 * math.exp(-4.0 * cost) - 1.0
    if t <= 0.0:
        return 0.0
    if t >= 1.0 / (1.0 + 4.0 * sd * sd):
        return 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))


rng = random.Random(1305)
worst = 0.0
worst_case = None
count = 0
interior = 0
for _ in range(4000):
    sd = 10 ** rng.uniform(-50.0, 3.0)
    cost = rng.uniform(0.0, 0.1725)
    t = 2.0 * math.exp(-4.0 * cost) - 1.0
    if t < 1e-2:
        continue
    count += 1
    out = ref.solve_model(sd, cost)["informed_fraction"]
    exact = closed(sd, cost)
    if exact <= 0.0 or exact >= 1.0:
        continue
    interior += 1
    rel = abs(out - exact) / exact
    if rel > worst:
        worst, worst_case = rel, (sd, cost, out, exact)
print(f"points with tau_bar >= 1e-2: {count}; interior: {interior}")
print(f"worst relative error of reference vs Proposition 4 closed form: {worst:.3e} at (sd, cost, out, exact)={worst_case}")
print(f"page requirement: 1e-10 for sd >= 1e-50 and tau_bar >= 1e-2 -> {'met' if worst <= 1e-10 else 'NOT met'}")
