"""M2 lab L15: two functions of two variables sampled near the origin, on circles and along a sequence.

Standard library only. The function g(x, y) = x y / (x^2 + y^2) and f(x, y) = x^2 y / (x^2 + y^2) are
set to 0 at the origin. For each radius r = 10^-k the lab samples 360 points on the circle of radius
r at one-degree steps. It prints the largest absolute value of g over those samples, and the largest
absolute value of f over those samples divided by r.
It also evaluates both functions on the sequence (1/n, 1/n). Every value is a sample, so the output
describes the sampled points only. It does not prove or disprove continuity. Nothing is random.
"""

from __future__ import annotations

import math
from collections.abc import Callable

Point = tuple[float, float]


def g(x: float, y: float) -> float:
    """g(x, y) = x y / (x^2 + y^2) for (x, y) != (0, 0), and g(0, 0) = 0."""
    if x == 0.0 and y == 0.0:
        return 0.0
    return x * y / (x * x + y * y)


def f(x: float, y: float) -> float:
    """f(x, y) = x^2 y / (x^2 + y^2) for (x, y) != (0, 0), and f(0, 0) = 0."""
    if x == 0.0 and y == 0.0:
        return 0.0
    return x * x * y / (x * x + y * y)


def circle_points(r: float, count: int = 360) -> list[Point]:
    """count points on the circle of radius r about the origin, at angles 0, 2 pi/count, 4 pi/count, ..."""
    return [(r * math.cos(2.0 * math.pi * k / count), r * math.sin(2.0 * math.pi * k / count)) for k in range(count)]


def circle_max(fn: Callable[[float, float], float], r: float) -> float:
    """The largest absolute value of fn over the sampled points of the circle of radius r."""
    return max(abs(fn(x, y)) for x, y in circle_points(r))


def main() -> None:
    print("radius r, sampled max |g| on circle, sampled max |f| on circle divided by r")
    for k in range(1, 7):
        r = 10.0 ** (-k)
        mg = circle_max(g, r)
        mf = circle_max(f, r)
        print(f"1e-{k:02d} {mg:.6f} {mf / r:.4f}")
    print("sequence (1/n, 1/n): g value, f value")
    for n in (10, 100, 1000, 10000):
        x = 1.0 / n
        print(f"n = {n}: {g(x, x):.6f} {f(x, x):.9f}")
    print(f"g(0, 0) by definition: {g(0.0, 0.0):.1f}")


main()
