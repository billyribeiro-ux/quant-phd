"""M5 L08 lab 1: fixed point of the discounted Bellman operator on a finite grid.

Generated model parameters; not data. The state k is capital on the grid GRID. Output is k ** ALPHA. The planner
chooses next-period capital k' in GRID with k' <= k ** ALPHA, so consumption c = k ** ALPHA - k' is nonnegative,
and utility is u(c) = sqrt(c). The operator is (B V)(k) = max over feasible k' of [u(c) + BETA * V(k')], with ties
broken by the smallest feasible index. Part A iterates B from V_0 = 0 to a fixed point and prints the residual of
the fixed point. Part B draws seeded pairs (V, W) with the standard random module and checks that the sup-norm
ratio ||BV - BW|| / ||V - W|| does not exceed BETA by more than TOL. Part C applies B to a one-point grid, where
the fixed point is u / (1 - BETA) = 5 at BETA = 0.9, and then iterates it at BETA = 1, where the iterates grow
without bound.
Standard library only; no network access. TOL = 1e-12 bounds the stopping gap, the ratio check of Part B and the
iterate checks of Part C. The residual check of Part A and the one-point fixed-point check of Part C use 1e-9.
"""

from __future__ import annotations

import math
import random

ALPHA = 0.5
BETA = 0.9
GRID: tuple[float, ...] = (0.25, 0.5, 0.75, 1.0)
SEED = 20261028
PAIRS = 2000
TOL = 1e-12


def bellman(values: list[float], grid: tuple[float, ...], beta: float) -> tuple[list[float], list[int]]:
    """Apply the operator to values on grid. Return the new values and, for each state, the chosen index."""
    if len(values) != len(grid):
        raise ValueError("values and grid must have equal length")
    new_values: list[float] = []
    policy: list[int] = []
    for k in grid:
        output = k**ALPHA
        feasible = [j for j, kp in enumerate(grid) if kp <= output]
        if not feasible:
            raise AssertionError(f"no feasible successor for state {k}")
        best_value = -math.inf
        best_index = -1
        for j in feasible:
            consumption = output - grid[j]
            candidate = math.sqrt(consumption) + beta * values[j]
            if candidate > best_value:
                best_value, best_index = candidate, j
        new_values.append(best_value)
        policy.append(best_index)
    return new_values, policy


def solve(grid: tuple[float, ...], beta: float) -> tuple[list[float], list[int], int]:
    """Iterate the operator from zero until successive values differ by at most TOL. Return values, policy, count."""
    values = [0.0] * len(grid)
    count = 0
    while True:
        new_values, policy = bellman(values, grid, beta)
        count += 1
        gap = max(abs(a - b) for a, b in zip(new_values, values, strict=True))
        values = new_values
        if gap <= TOL:
            return values, policy, count
        if count > 10000:
            raise AssertionError("no convergence within 10000 iterations")


def part_a() -> None:
    """Solve on GRID and check the residual of the fixed point."""
    values, policy, count = solve(GRID, BETA)
    image, _ = bellman(values, GRID, BETA)
    residual = max(abs(a - b) for a, b in zip(image, values, strict=True))
    if residual > 1e-9:
        raise AssertionError("the computed values are not a fixed point")
    print(f"part A: beta = {BETA}, alpha = {ALPHA}, grid = {GRID}")
    print(f"part A: iterations until the successive gap is at most {TOL:g} = {count}")
    for k, v, j in zip(GRID, values, policy, strict=True):
        print(f"part A: state k = {k:.2f}  V*(k) = {v:.6f}  chosen next capital = {GRID[j]:.2f}")
    print(f"part A: residual max |BV* - V*| = {residual:.3e} (at most 1e-9)")


def part_b() -> None:
    """Check the sup-norm contraction ratio on seeded random pairs."""
    rng = random.Random(SEED)
    worst = 0.0
    for _ in range(PAIRS):
        v = [rng.uniform(-10.0, 10.0) for _ in GRID]
        w = [rng.uniform(-10.0, 10.0) for _ in GRID]
        bv, _ = bellman(v, GRID, BETA)
        bw, _ = bellman(w, GRID, BETA)
        num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
        den = max(abs(a - b) for a, b in zip(v, w, strict=True))
        worst = max(worst, num / den)
    if worst > BETA + TOL:
        raise AssertionError("a sampled contraction ratio exceeds beta")
    print(f"part B: seed = {SEED}, pairs = {PAIRS}, largest sampled ratio = {worst:.6f}, beta = {BETA}")
    print("part B: no sampled pair has ratio above beta by more than 1e-12")


def part_c() -> None:
    """Check the one-point grid: fixed point 5 at beta = 0.9, and unbounded iterates at beta = 1."""
    one = (0.25,)
    values, _, count = solve(one, 0.9)
    print(f"part C: one-point grid, beta = 0.9: V* = {values[0]:.6f} after {count} iterations")
    if abs(values[0] - 5.0) > 1e-9:
        raise AssertionError("one-point fixed point differs from u / (1 - beta) = 5")
    v = [0.0]
    for n in range(1, 1001):
        v, _ = bellman(v, one, 1.0)
        if abs(v[0] - 0.5 * n) > TOL:
            raise AssertionError("iterates at beta = 1 are not n times u")
    print(f"part C: one-point grid, beta = 1: after 1000 iterations V = {v[0]:.6f}, which is 0.5 times 1000")
    print("part C: at beta = 1 the iterates grow linearly, so no finite fixed point is reached")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
