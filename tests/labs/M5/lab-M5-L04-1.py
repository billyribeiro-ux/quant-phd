"""M5 L04 lab 1: the metric axioms, checked exhaustively on finite samples.

Standard library only. No randomness and no network: every sample is enumerated, so every run prints the same lines.
A check on a finite sample tests that sample only. The output is evidence about the sample and says nothing about the
whole space.

Part A: the Euclidean distance on the 25 points (i/2, j/2) with i, j in {-2, -1, 0, 1, 2}, in R^2. Floats are used,
and the triangle inequality is tested with a slack of 1e-12 for floating-point
error. Nonnegativity, identity and symmetry are tested on all pairs; the triangle inequality is tested on all triples.
Part B: the sup distance max_k |f_k - g_k| on the 27 vectors of length 3 with entries in {0, 1, 2}. Entries are exact
Fractions, so the slack is zero.
Part C: the squared Euclidean distance on the three points 0, 1, 2 of R. It is symmetric and zero only at equal points,
and it fails the triangle inequality. The printed numbers are the exact values at the failing triple.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from fractions import Fraction
from itertools import product
from math import sqrt

Number = float | Fraction
Point = tuple[float, float]
Vector = tuple[Fraction, ...]

SLACK = 1e-12
AXIOMS = ("nonnegative", "identity", "symmetry", "triangle")


def euclidean(x: Point, y: Point) -> float:
    """The Euclidean distance in R^2, in the units of the coordinates."""
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def sup_distance(f: Vector, g: Vector) -> Fraction:
    """The maximum over k of |f_k - g_k|, exact. Both vectors have the same length."""
    return max(abs(a - b) for a, b in zip(f, g, strict=True))


def squared_distance(x: int, y: int) -> int:
    """The squared difference (x - y)^2 on the integers. It is a candidate distance, and it is not a metric."""
    return (x - y) ** 2


def axiom_failures[P](points: Sequence[P], dist: Callable[[P, P], Number], slack: Number) -> dict[str, int]:
    """Count, for each metric axiom, the sample tuples on which it fails.

    Nonnegativity and identity use pairs, symmetry uses pairs, and the triangle inequality uses triples
    (x, y, z) with d(x, z) <= d(x, y) + d(y, z) + slack. The count for each axiom is returned in AXIOMS order.
    """
    failures = dict.fromkeys(AXIOMS, 0)
    for x, y in product(points, repeat=2):
        d = dist(x, y)
        if d < 0:
            failures["nonnegative"] += 1
        if (d == 0) != (x == y):
            failures["identity"] += 1
        if d != dist(y, x):
            failures["symmetry"] += 1
    for x, y, z in product(points, repeat=3):
        if dist(x, z) > dist(x, y) + dist(y, z) + slack:
            failures["triangle"] += 1
    return failures


def report[P](label: str, points: Sequence[P], dist: Callable[[P, P], Number], slack: Number) -> dict[str, int]:
    """Print the number of pairs and triples checked, then the failure count for each axiom."""
    failures = axiom_failures(points, dist, slack)
    print(f"{label} points {len(points)} pairs {len(points) ** 2} triples {len(points) ** 3}")
    print("failures " + " ".join(f"{name} {failures[name]}" for name in AXIOMS))
    return failures


def main() -> None:
    """Run Parts A, B and C. Every line is a count, a flag or an exact value, so the output is reproducible."""
    grid = [(i / 2, j / 2) for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2)]
    print("Part A: Euclidean distance on a 5 by 5 grid of R^2, slack 1e-12")
    report("euclidean", grid, euclidean, SLACK)

    vectors = [tuple(Fraction(v) for v in combo) for combo in product((0, 1, 2), repeat=3)]
    print("Part B: sup distance max_k |f_k - g_k| on vectors of length 3 with entries in {0, 1, 2}, exact")
    report("sup", vectors, sup_distance, Fraction(0))

    integers = [0, 1, 2]
    print("Part C: squared distance (x - y)^2 on the points 0, 1, 2, exact")
    failures = report("squared", integers, squared_distance, 0)
    print(f"squared_triangle_failures {failures['triangle']}")
    print(f"d(0,2) {squared_distance(0, 2)} d(0,1)+d(1,2) {squared_distance(0, 1) + squared_distance(1, 2)}")


main()
