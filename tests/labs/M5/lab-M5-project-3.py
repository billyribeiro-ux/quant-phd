"""Rung 3 reference numbers: the solver's output on the report's illustrative instance, and the report's checks.

Standard library only. The inputs are illustrative, not data: beta = 0.9, alpha = 0.3, the ten grid points
0.45, 0.70, 0.95 and so on up to 2.70, and the tolerance 1e-10. The model is the one in the specification: output
k**alpha, feasible savings kp <= k**alpha, utility sqrt of consumption, and value iteration from the zero vector.
The random pairs use the seed 7.

Copy this file into report/run_report.py, replace the operator and solver calls with calls to your
contraction_solver module, and print the same lines. The numbers are the ones the report quotes.
"""

import math
import random

BETA = 0.9
ALPHA = 0.3
GRID = [0.45 + 0.25 * j for j in range(10)]
TOL = 1e-10


def resources(k: float) -> float:
    """Output available from capital k: k to the power alpha."""
    return float(k**ALPHA)


def bellman(values: list[float]) -> list[float]:
    """One application of the discounted Bellman operator: max over feasible kp of sqrt(k**alpha - kp) + beta V(kp)."""
    out = []
    for k in GRID:
        best = max(math.sqrt(resources(k) - kp) + BETA * values[j] for j, kp in enumerate(GRID) if kp <= resources(k))
        out.append(best)
    return out


def sup_distance(a: list[float], b: list[float]) -> float:
    """The sup norm of a difference: the largest absolute entry."""
    return max(abs(x - y) for x, y in zip(a, b, strict=False))


def main() -> None:
    # The smallest gap between a grid point and a resource level k**alpha: a gap near zero would make the
    # feasibility test a near-tie.
    gap = min(abs(kp - resources(k)) for k in GRID for kp in GRID)
    print(f"instance: beta {BETA}, alpha {ALPHA}, {len(GRID)} grid points from {GRID[0]} to {GRID[-1]}")
    print(f"smallest gap between a grid point and a resource level: {gap:.6f} | clear of a tie: {gap > 1e-6}")
    # Value iteration from zero, stopped at the first certified error at most TOL.
    values = [0.0] * len(GRID)
    sweeps = 0
    certified = math.inf
    change = math.inf
    while certified > TOL:
        new = bellman(values)
        change = sup_distance(new, values)
        certified = BETA / (1 - BETA) * change
        values = new
        sweeps += 1
    print(f"sweeps: {sweeps} | last change: {change:.3e} | certified error: {certified:.3e}")
    # The a priori count: the least n with beta**n * U / (1 - beta) at most TOL, where U = sqrt(max grid**alpha).
    bound_u = math.sqrt(max(GRID) ** ALPHA)
    n_apriori = 0
    while BETA**n_apriori * bound_u / (1 - BETA) > TOL:
        n_apriori += 1
    print(f"a priori count: {n_apriori} | sweeps within the count plus one: {sweeps <= n_apriori + 1}")
    # The residual of the output: |BV - V| is at most (1 + beta) times the certified error.
    residual = sup_distance(bellman(values), values)
    print(
        f"residual: {residual:.3e} | at most (1 + beta) times the certified error: {residual <= (1 + BETA) * certified}"
    )
    # The contraction ratio on seeded random pairs: the largest sup|BV - BW| / sup|V - W| seen is at most beta.
    rng = random.Random(7)
    worst = 0.0
    for _ in range(200):
        v = [rng.uniform(0.0, 4.0) for _ in GRID]
        w = [rng.uniform(0.0, 4.0) for _ in GRID]
        worst = max(worst, sup_distance(bellman(v), bellman(w)) / sup_distance(v, w))
    print(f"largest observed contraction ratio over 200 pairs: {worst:.6f} | at most beta: {worst <= BETA + 1e-12}")
    # The value at each grid point.
    for k, value in zip(GRID, values, strict=False):
        print(f"V({k}) = {value:.6f}")


main()
