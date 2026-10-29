"""M2 lab L16: partial derivatives by central difference, against their closed forms.

Standard library only. The function is F(x, y) = x^2 y + exp(x y). Its partial derivatives are
F_x = 2 x y + y exp(x y) and F_y = x^2 + x exp(x y). For each partial the lab takes a central
difference in that variable alone, with step h = 10^-5, at 12 grid points (x in {0.5, 1, 1.5, 2},
y in {-1, 0, 1}), and reports whether the largest absolute error is below 1e-6. The lab also tests the axis
quotients of g(x, y) = x y / (x^2 + y^2) at the origin, where g(0, 0) = 0. Nothing is random.
"""

from __future__ import annotations

import math
from collections.abc import Callable

H = 1e-5


def big_f(x: float, y: float) -> float:
    """F(x, y) = x^2 y + exp(x y)."""
    return x * x * y + math.exp(x * y)


def fx_closed(x: float, y: float) -> float:
    """The closed-form partial derivative of F with respect to x: 2 x y + y exp(x y)."""
    return 2.0 * x * y + y * math.exp(x * y)


def fy_closed(x: float, y: float) -> float:
    """The closed-form partial derivative of F with respect to y: x^2 + x exp(x y)."""
    return x * x + x * math.exp(x * y)


def partial_x(fn: Callable[[float, float], float], x: float, y: float, h: float) -> float:
    """Central difference in x with y held fixed: (fn(x + h, y) - fn(x - h, y)) / (2 h)."""
    return (fn(x + h, y) - fn(x - h, y)) / (2.0 * h)


def partial_y(fn: Callable[[float, float], float], x: float, y: float, h: float) -> float:
    """Central difference in y with x held fixed: (fn(x, y + h) - fn(x, y - h)) / (2 h)."""
    return (fn(x, y + h) - fn(x, y - h)) / (2.0 * h)


def g(x: float, y: float) -> float:
    """g(x, y) = x y / (x^2 + y^2) for (x, y) != (0, 0), and g(0, 0) = 0."""
    if x == 0.0 and y == 0.0:
        return 0.0
    return x * y / (x * x + y * y)


def grid() -> list[tuple[float, float]]:
    """The 12 grid points with x in {0.5, 1, 1.5, 2} and y in {-1, 0, 1}."""
    return [(x, y) for x in (0.5, 1.0, 1.5, 2.0) for y in (-1.0, 0.0, 1.0)]


def main() -> None:
    worst_x = 0.0
    worst_y = 0.0
    for x, y in grid():
        worst_x = max(worst_x, abs(partial_x(big_f, x, y, H) - fx_closed(x, y)))
        worst_y = max(worst_y, abs(partial_y(big_f, x, y, H) - fy_closed(x, y)))
    print(f"grid points: {len(grid())}")
    print(f"max error in F_x by central difference below 1e-6: {worst_x < 1e-6}")
    print(f"max error in F_y by central difference below 1e-6: {worst_y < 1e-6}")
    x0, y0 = 1.0, 2.0
    print(f"F_x(1, 2) by central difference: {partial_x(big_f, x0, y0, H):.6f}")
    print(f"F_x(1, 2) closed form: {fx_closed(x0, y0):.6f}")
    print(f"F_y(1, 2) by central difference: {partial_y(big_f, x0, y0, H):.6f}")
    print(f"F_y(1, 2) closed form: {fy_closed(x0, y0):.6f}")
    for t in (1e-3, 1e-6):
        along_x = (g(t, 0.0) - g(0.0, 0.0)) / t
        along_y = (g(0.0, t) - g(0.0, 0.0)) / t
        print(f"g quotients at the origin, t = {t:.0e}: along x {along_x:.1f}, along y {along_y:.1f}")


main()
