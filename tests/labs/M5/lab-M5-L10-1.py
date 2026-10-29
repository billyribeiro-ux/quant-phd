"""M5 L10 lab 1: Riemann-Stieltjes sums for the integral of f against dG on [0, 1].

Generated inputs, not data. Part A uses f(x) = x and G(x) = x^2. The integral is I = integral from 0 to 1 of
x * 2x dx = 2/3, the value that Corollary 3.2 of this lesson gives for a continuously differentiable integrator,
under Assumption 1 of this lesson.
Part D uses the same f with the identity integrator G(x) = x, which gives the ordinary Riemann sums of x.

Part A: uniform partitions into n parts, with left tags and with right tags, computed exactly in Fraction
arithmetic. The lab checks the closed forms derived on the page:
  right-tag sum  S_right(n) = (n + 1)(4n - 1) / (6 n^2),  so S_right(n) - 2/3 = (3n - 1)/(6 n^2)
  left-tag sum   S_left(n)  = (4 n^2 - 3 n - 1) / (6 n^2), so S_left(n) - 2/3 = -(3n + 1)/(6 n^2)

Part B: 200 random tagged partitions of [0, 1], drawn with random.Random(20261028). For each one the lab checks
the bound |S - 2/3| <= 2 * mesh, where mesh is the largest subinterval length. The constant 2 is max |G'| = 2.

Part C: a step integrator G(x) = 0 for x < 1/2 and G(x) = 1 for x >= 1/2, with f(x) = 1 for x >= 1/2 and
f(x) = 0 otherwise. On uniform partitions that contain 1/2, the lab prints the sum with the left tag and the
sum with the right tag of the one interval on which G jumps. Both tagged partitions are the same partition.

Only Part B computes with floats; its checks allow 1e-12 for floating-point error. Parts A, C and D use exact
Fractions and integers. No network. Standard library only.
"""

from __future__ import annotations

import itertools
import random
from collections.abc import Callable
from fractions import Fraction

SEED = 20261028
PARTS_A = (4, 10, 100, 1000)
PARTS_B = 200
MAX_INTERIOR = 30
SLACK = 1e-12
IDENTITY_N = 1000


def f(x: Fraction) -> Fraction:
    """The integrand f(x) = x."""
    return x


def g(x: Fraction) -> Fraction:
    """The integrator G(x) = x^2."""
    return x * x


def identity(x: Fraction) -> Fraction:
    """The integrator G(x) = x."""
    return x


def rs_sum(points: list[Fraction], tags: list[Fraction], integrator: Callable[[Fraction], Fraction]) -> Fraction:
    """Riemann-Stieltjes sum: the sum of f(tag_i) times the increment of the integrator over subinterval i."""
    total = Fraction(0)
    for i, tag in enumerate(tags, start=1):
        total += f(tag) * (integrator(points[i]) - integrator(points[i - 1]))
    return total


def uniform(n: int) -> list[Fraction]:
    """The uniform partition of [0, 1] into n parts."""
    return [Fraction(i, n) for i in range(n + 1)]


def part_a() -> None:
    """Exact left and right uniform sums for G = x^2, checked against the closed forms of the page."""
    print("part A: uniform partitions, exact, G(x) = x^2")
    target = Fraction(2, 3)
    for n in PARTS_A:
        pts = uniform(n)
        right = rs_sum(pts, pts[1:], g)
        left = rs_sum(pts, pts[:-1], g)
        right_formula = Fraction((n + 1) * (4 * n - 1), 6 * n * n)
        left_formula = Fraction(4 * n * n - 3 * n - 1, 6 * n * n)
        right_err = right - target
        left_err = left - target
        print(
            f"n {n} right {float(right):.12f} left {float(left):.12f} "
            f"right_err {float(right_err):.12f} left_err {float(left_err):.12f} "
            f"right_formula_matches {right == right_formula} left_formula_matches {left == left_formula} "
            f"right_err_formula_matches {right_err == Fraction(3 * n - 1, 6 * n * n)} "
            f"left_err_formula_matches {left_err == -Fraction(3 * n + 1, 6 * n * n)}"
        )


def part_b() -> None:
    """Random tagged partitions: the sum is within 2 times the mesh of 2/3."""
    print("part B: random tagged partitions, seeded")
    rng = random.Random(SEED)
    worst_ratio = 0.0
    max_mesh = 0.0
    all_within = True
    for _ in range(PARTS_B):
        m = rng.randint(1, MAX_INTERIOR)
        interior = sorted(rng.random() for _ in range(m))
        bounds = [0.0, *interior, 1.0]
        tags = [lo + rng.random() * (hi - lo) for lo, hi in itertools.pairwise(bounds)]
        total = 0.0
        for i, tag in enumerate(tags, start=1):
            total += tag * (bounds[i] ** 2 - bounds[i - 1] ** 2)
        mesh = max(hi - lo for lo, hi in itertools.pairwise(bounds))
        err = abs(total - 2 / 3)
        all_within = all_within and err <= 2 * mesh + SLACK
        worst_ratio = max(worst_ratio, err / mesh)
        max_mesh = max(max_mesh, mesh)
    print(
        f"partitions {PARTS_B} largest_mesh {max_mesh:.6f} largest_error_over_mesh {worst_ratio:.6f} "
        f"all_within_2_mesh {all_within}"
    )


def part_c() -> None:
    """A step integrator: the sum depends on the tag at the jump, so the sums do not settle as the mesh shrinks."""
    print("part C: step integrator at 1/2, uniform partitions containing 1/2")
    half = Fraction(1, 2)

    def step(x: Fraction) -> int:
        return 1 if x >= half else 0

    for n in (10, 100):
        pts = uniform(n)
        k = n // 2
        left_total = 0
        right_total = 0
        jumps = 0
        for i in range(1, n + 1):
            d_g = step(pts[i]) - step(pts[i - 1])
            if d_g != 0:
                jumps += 1
            if i == k:
                left_total += step(pts[i - 1]) * d_g
                right_total += step(pts[i]) * d_g
        print(
            f"n {n} mesh {float(Fraction(1, n)):.6f} jumps {jumps} "
            f"left_tag_sum {left_total} right_tag_sum {right_total}"
        )


def part_d() -> None:
    """The identity integrator G(x) = x: the sums of f = x are the Riemann sums of x on [0, 1]."""
    print("part D: identity integrator, uniform partitions, exact")
    pts = uniform(IDENTITY_N)
    right = rs_sum(pts, pts[1:], identity)
    left = rs_sum(pts, pts[:-1], identity)
    print(
        f"n {IDENTITY_N} right {float(right):.12f} left {float(left):.12f} "
        f"right_formula_matches {right == Fraction(IDENTITY_N + 1, 2 * IDENTITY_N)} "
        f"left_formula_matches {left == Fraction(IDENTITY_N - 1, 2 * IDENTITY_N)}"
    )


def main() -> None:
    """Run the four parts in order."""
    part_a()
    part_b()
    part_c()
    part_d()


main()
