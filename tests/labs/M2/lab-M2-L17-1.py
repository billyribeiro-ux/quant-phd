"""M2 lab L17: the directional derivative equals the gradient dotted with the unit vector.

Standard library only. The function is F(x, y) = x^2 y + sin(y), with gradient
(2 x y, x^2 + cos y). At the point a = (1, 0.5) the lab takes 360 unit vectors u at angles of one
degree. For each u it compares a central difference of F along the line a + t u, with t = 1e-6,
against the dot product of the gradient with u. It then finds the angle at which the central
difference is largest and reports it beside the angle of the gradient. Nothing is random.
"""

from __future__ import annotations

import math


def big_f(x: float, y: float) -> float:
    """F(x, y) = x^2 y + sin(y)."""
    return x * x * y + math.sin(y)


def gradient(x: float, y: float) -> tuple[float, float]:
    """The gradient (F_x, F_y) = (2 x y, x^2 + cos y)."""
    return (2.0 * x * y, x * x + math.cos(y))


def unit(angle_deg: int) -> tuple[float, float]:
    """The unit vector at the given angle in degrees, measured from the positive x-axis."""
    theta = math.radians(angle_deg)
    return (math.cos(theta), math.sin(theta))


def directional_central(a: tuple[float, float], u: tuple[float, float], t: float) -> float:
    """(F(a + t u) - F(a - t u)) / (2 t), a central difference along the line through a in direction u."""
    x0, y0 = a
    ux, uy = u
    plus = big_f(x0 + t * ux, y0 + t * uy)
    minus = big_f(x0 - t * ux, y0 - t * uy)
    return (plus - minus) / (2.0 * t)


def main() -> None:
    a = (1.0, 0.5)
    t = 1e-6
    gx, gy = gradient(*a)
    worst = 0.0
    best_angle = 0
    best_value = -math.inf
    for angle in range(360):
        u = unit(angle)
        numeric = directional_central(a, u, t)
        exact = gx * u[0] + gy * u[1]
        worst = max(worst, abs(numeric - exact))
        if numeric > best_value:
            best_value = numeric
            best_angle = angle
    grad_angle = math.degrees(math.atan2(gy, gx))
    magnitude = math.hypot(gx, gy)
    print("directions tested: 360, one degree apart")
    print(f"max error of central difference against gradient dot u below 1e-6: {worst < 1e-6}")
    print(f"gradient at (1, 0.5): ({gx:.6f}, {gy:.6f})")
    print(f"gradient magnitude: {magnitude:.6f}")
    print(f"angle of the gradient: {grad_angle:.2f} degrees")
    print(f"sampled direction of largest directional derivative: {best_angle} degrees")
    agrees = abs(best_value - magnitude) < 1e-4
    print(f"largest sampled directional derivative agrees with the magnitude to 1e-4: {agrees}")


main()
