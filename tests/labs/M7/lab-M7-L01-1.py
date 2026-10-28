"""M7 lab L01: convexity of two quadratic functions, checked exactly on a grid.

Standard library only. No randomness and no network. Every number is a fractions.Fraction or an integer,
so nothing is rounded and the output is the same on every run.

SIMULATED: the two quadratic forms Q1 and Q2 are illustrative inputs written on this page, not data.

The lab checks four things on the grid {-2, -1, 0, 1, 2} in each coordinate (25 points):
1. the identity f(l x + (1 - l) y) = l f(x) + (1 - l) f(y) - l (1 - l) (x - y)' Q (x - y), for f(x) = x' Q x,
   on every ordered pair (x, y) of grid points and every weight l in {0, 1/4, 1/2, 3/4, 1};
2. the chord inequality f(l x + (1 - l) y) <= l f(x) + (1 - l) f(y) on the same cases, for Q1 and for Q2;
3. the eigenvalues of the Hessian H = 2 Q, in closed form for each 2 x 2 symmetric matrix;
4. the explicit example x = (1, 0), y = (0, 1), l = 1/2 for Q2.

A check over a finite grid is evidence about the grid only. It does not prove convexity on the plane. The
plane-wide claim rests on the eigenvalue test, which is a theorem on the page (Proposition 3.2 of the lesson).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import isqrt

GRID = (-2, -1, 0, 1, 2)
WEIGHTS = (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1))
Q1 = ((2, 1), (1, 2))
Q2 = ((1, 2), (2, 1))
Point = tuple[int, int]
Matrix = tuple[tuple[int, int], tuple[int, int]]


def quad(q: Matrix, x: tuple[Fraction, Fraction]) -> Fraction:
    """The value x' Q x of the quadratic form with symmetric 2 x 2 matrix Q, at the point x."""
    return sum((Fraction(q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2)), Fraction(0))


def combine(weight: Fraction, x: Point, y: Point) -> tuple[Fraction, Fraction]:
    """The point weight * x + (1 - weight) * y, with exact coordinates."""
    return (
        weight * x[0] + (1 - weight) * y[0],
        weight * x[1] + (1 - weight) * y[1],
    )


def identity_holds(q: Matrix, x: Point, y: Point, weight: Fraction) -> bool:
    """Exact check of f(z) = w f(x) + (1 - w) f(y) - w (1 - w) (x - y)' Q (x - y), with z = w x + (1 - w) y."""
    z = combine(weight, x, y)
    d = (Fraction(x[0] - y[0]), Fraction(x[1] - y[1]))
    lhs = quad(q, z)
    rhs = weight * quad(q, (Fraction(x[0]), Fraction(x[1]))) + (1 - weight) * quad(q, (Fraction(y[0]), Fraction(y[1])))
    rhs -= weight * (1 - weight) * quad(q, d)
    return lhs == rhs


def chord_holds(q: Matrix, x: Point, y: Point, weight: Fraction) -> bool:
    """True when f at the weighted point does not exceed the weighted chord of f at x and y."""
    z = combine(weight, x, y)
    chord = weight * quad(q, (Fraction(x[0]), Fraction(x[1]))) + (1 - weight) * quad(
        q, (Fraction(y[0]), Fraction(y[1]))
    )
    return quad(q, z) <= chord


def cases() -> list[tuple[Point, Point, Fraction]]:
    """Every ordered pair of grid points, with every weight. Pairs with x equal to y are included."""
    points = list(product(GRID, GRID))
    return [(x, y, w) for x in points for y in points for w in WEIGHTS]


def hessian_eigenvalues(q: Matrix) -> tuple[Fraction, Fraction]:
    """The two eigenvalues of H = 2 Q, larger first, from the closed form for a 2 x 2 symmetric matrix.

    For [[a, b], [b, c]] the eigenvalues are ((a + c) +/- sqrt((a - c)^2 + 4 b^2)) / 2. The square root must be an
    integer here, and the function raises ValueError if it is not.
    """
    a, b, c = 2 * q[0][0], 2 * q[0][1], 2 * q[1][1]
    disc = (a - c) ** 2 + 4 * b * b
    root = isqrt(disc)
    if root * root != disc:
        raise ValueError(f"discriminant {disc} is not a perfect square, so the eigenvalues are not integers")
    return Fraction(a + c + root, 2), Fraction(a + c - root, 2)


def is_psd_by_eigenvalues(q: Matrix) -> bool:
    """True when both eigenvalues of the Hessian 2 Q are non-negative."""
    return all(e >= 0 for e in hessian_eigenvalues(q))


def main() -> None:
    all_cases = cases()
    total = len(all_cases)
    points = len(GRID) ** 2
    print(f"grid {{-2, ..., 2}}^2: {points} points, {points * points} ordered pairs, {len(WEIGHTS)} weights,")
    print(f"{total} cases per function")

    for name, q in (("Q1", Q1), ("Q2", Q2)):
        ok = sum(identity_holds(q, x, y, w) for x, y, w in all_cases)
        print(f"{name} identity holds in {ok} of {total} cases")

    chord_q1 = sum(chord_holds(Q1, x, y, w) for x, y, w in all_cases)
    chord_q2 = sum(chord_holds(Q2, x, y, w) for x, y, w in all_cases)
    print(f"Q1 chord inequality holds in {chord_q1} of {total} cases")
    print(f"Q2 chord inequality holds in {chord_q2} of {total} cases")

    negative_pairs = sum(
        1
        for x, y in product(product(GRID, GRID), repeat=2)
        if quad(Q2, (Fraction(x[0] - y[0]), Fraction(x[1] - y[1]))) < 0
    )
    failures_q2 = total - chord_q2
    print(f"Q2 ordered pairs with (x - y)' Q2 (x - y) < 0: {negative_pairs}")
    print(f"Q2 failures equal 3 times that count: {failures_q2 == 3 * negative_pairs}")

    x, y, w = (1, 0), (0, 1), Fraction(1, 2)
    z = combine(w, x, y)
    midpoint = quad(Q2, z)
    chord = w * quad(Q2, (Fraction(1), Fraction(0))) + (1 - w) * quad(Q2, (Fraction(0), Fraction(1)))
    d = (Fraction(1), Fraction(-1))
    term = w * (1 - w) * quad(Q2, d)
    print(
        f"Q2 at x = (1, 0), y = (0, 1), weight 1/2: midpoint value {midpoint}, chord {chord}, "
        f"chord minus midpoint {chord - midpoint}"
    )
    print(f"identity term (1/4) (x - y)' Q2 (x - y) = {term}")

    for name, q in (("Q1", Q1), ("Q2", Q2)):
        high, low = hessian_eigenvalues(q)
        print(f"Hessian eigenvalues of {name} (H = 2 Q): {high} and {low}")
    print(f"Q1 eigenvalue test (both eigenvalues >= 0): {is_psd_by_eigenvalues(Q1)}")
    print(f"Q2 eigenvalue test (both eigenvalues >= 0): {is_psd_by_eigenvalues(Q2)}")


main()
