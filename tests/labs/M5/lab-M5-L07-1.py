"""M5 L07 lab 1: Banach iteration for cos on [0, 1], the sampled contraction ratio, and a map with no fixed point.

Part A iterates x_{n+1} = cos(x_n) from x_0 = 0 and checks the error |x_n - x*| against the a priori bound of
Theorem 2.1, beta**n * d(x_0, x_1) / (1 - beta), with beta = sin(1) and d(x_0, x_1) = 1. Part B samples the
difference quotient |cos x - cos y| / |x - y| over all pairs of a grid on [0, 1] and checks that no pair exceeds
sin(1), which is sup |f'| on [0, 1] by Example 3.3. Part C applies the same sampling to f(x) = sqrt(x*x + 1) on
[-L, L] for two windows, and checks that f(x) - x is positive at every grid point. A grid check does not prove that
f has no fixed point; the page proves that analytically.
Standard library only; no randomness and no network access. The float tolerance is TOL = 1e-12 in Parts A and B;
Part C tests the sign of f(x) - x in floating point with no tolerance.
"""

from __future__ import annotations

import math

BETA = math.sin(1.0)
GRID_N = 200
ITER_STEPS = 300
TOL = 1e-12
WINDOWS = (5.0, 50.0)


def cos_fixed_point() -> float:
    """Return cos iterated ITER_STEPS times from 0; the iterates converge to the fixed point of cos on [0, 1]."""
    x = 0.0
    for _ in range(ITER_STEPS):
        x = math.cos(x)
    return x


def part_a() -> None:
    """Check the a priori error bound for the Banach iteration of cos from x_0 = 0."""
    xstar = cos_fixed_point()
    d01 = abs(0.0 - math.cos(0.0))  # d(x_0, x_1) = |0 - 1| = 1
    print(f"part A: modulus beta = sin(1) = {BETA:.6f}; fixed point x* = {xstar:.6f}")
    x = 0.0
    for n in range(31):
        err = abs(x - xstar)
        bound = BETA**n * d01 / (1.0 - BETA)
        if err > bound + TOL:
            raise AssertionError(f"a priori bound fails at n = {n}")
        if n in (0, 1, 2, 5, 10, 20, 30):
            print(f"part A: n = {n:2d}  x_n = {x:.6f}  error = {err:.6e}  bound = {bound:.6e}")
        x = math.cos(x)
    print("part A: the error is at most the a priori bound for n = 0 to 30")


def part_b() -> None:
    """Sample the difference quotient of cos over all grid pairs on [0, 1] and compare it with sin(1)."""
    xs = [i / GRID_N for i in range(GRID_N + 1)]
    if not all(0.0 <= math.cos(x) <= 1.0 for x in xs):
        raise AssertionError("cos does not map the grid into [0, 1]")
    best = 0.0
    for i, x in enumerate(xs):
        for y in xs[i + 1 :]:
            best = max(best, abs(math.cos(x) - math.cos(y)) / (y - x))
    if best > BETA + TOL:
        raise AssertionError("a sampled difference quotient exceeds sin(1)")
    print(f"part B: grid of {GRID_N + 1} points on [0, 1]; largest sampled ratio = {best:.6f}; sin(1) = {BETA:.6f}")
    print("part B: cos maps the grid into [0, 1], and no sampled pair has ratio above sin(1)")


def window_ratio(half: float) -> tuple[float, float]:
    """Return the largest sampled ratio of f(x) = sqrt(x*x + 1) on [-half, half], and the minimum of f(x) - x."""
    xs = [-half + 2.0 * half * i / GRID_N for i in range(GRID_N + 1)]

    def f(x: float) -> float:
        return math.sqrt(x * x + 1.0)

    best = 0.0
    for i, x in enumerate(xs):
        for y in xs[i + 1 :]:
            best = max(best, abs(f(x) - f(y)) / (y - x))
    gap = min(f(x) - x for x in xs)
    return best, gap


def part_c() -> None:
    """Print the sampled ratio of f on each window, and check that f(x) - x is positive at every grid point."""
    for half in WINDOWS:
        best, gap = window_ratio(half)
        if gap <= 0.0:
            raise AssertionError("f(x) - x vanishes on the grid")
        print(f"part C: window [-{half:g}, {half:g}]: largest sampled ratio = {best:.6f}; min of f(x) - x = {gap:.6f}")
    print("part C: f(x) - x is positive at every grid point on either window")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
