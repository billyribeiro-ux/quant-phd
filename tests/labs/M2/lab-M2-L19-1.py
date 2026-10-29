"""M2 lab L19: the gradient, the Hessian and the second-order Taylor expansion of a two-variable function.

SIMULATED: the function f(x, y) = exp(x) * y + x * y**2 is a test function chosen for this lab. It is not
market data and it models no security.
Part A checks the closed-form gradient and Hessian of f against central differences, and reports the
symmetry of the finite-difference Hessian. Part B measures the error of the first-order and the second-order
Taylor expansions of f along one fixed unit direction, at step sizes s, s/2, s/4 and s/8, and prints the ratio
of successive errors. Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math

Point = tuple[float, float]
Matrix = tuple[tuple[float, float], tuple[float, float]]

BASE: Point = (0.5, 0.25)
DIRECTION: Point = (0.6, -0.8)  # a unit vector: 0.6 * 0.6 + 0.8 * 0.8 = 1
STEPS: tuple[float, ...] = (0.1, 0.05, 0.025, 0.0125)


def f(p: Point) -> float:
    """The test function f(x, y) = exp(x) * y + x * y**2."""
    x, y = p
    return math.exp(x) * y + x * y * y


def gradient_closed(p: Point) -> Point:
    """The closed-form gradient (f_x, f_y) at p."""
    x, y = p
    return (math.exp(x) * y + y * y, math.exp(x) + 2.0 * x * y)


def hessian_closed(p: Point) -> Matrix:
    """The closed-form Hessian [[f_xx, f_xy], [f_yx, f_yy]] at p."""
    x, y = p
    e = math.exp(x)
    return ((e * y, e + 2.0 * y), (e + 2.0 * y, 2.0 * x))


def fd_hessian(p: Point, h: float) -> Matrix:
    """Hessian by central differences of the closed gradient: entry (i, j) differentiates gradient component i along j.

    The step h must be positive; a step of zero or less raises ValueError.
    """
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    rows: list[list[float]] = []
    for i in range(2):
        row: list[float] = []
        for j in range(2):
            up = [p[0], p[1]]
            down = [p[0], p[1]]
            up[j] += h
            down[j] -= h
            plus = gradient_closed((up[0], up[1]))[i]
            minus = gradient_closed((down[0], down[1]))[i]
            row.append((plus - minus) / (2.0 * h))
        rows.append(row)
    return ((rows[0][0], rows[0][1]), (rows[1][0], rows[1][1]))


def along(p: Point, d: Point, s: float) -> Point:
    """The point p + s * d."""
    return (p[0] + s * d[0], p[1] + s * d[1])


def first_order_error(p: Point, d: Point, s: float) -> float:
    """f(p + s d) minus its first-order Taylor polynomial f(p) + s * grad f(p) . d."""
    g = gradient_closed(p)
    return f(along(p, d, s)) - (f(p) + s * (g[0] * d[0] + g[1] * d[1]))


def second_order_error(p: Point, d: Point, s: float) -> float:
    """f(p + s d) minus its second-order Taylor polynomial f(p) + s grad f(p) . d + (s**2 / 2) * (d H d)."""
    g = gradient_closed(p)
    hess = hessian_closed(p)
    quad = d[0] * (hess[0][0] * d[0] + hess[0][1] * d[1]) + d[1] * (hess[1][0] * d[0] + hess[1][1] * d[1])
    return f(along(p, d, s)) - (f(p) + s * (g[0] * d[0] + g[1] * d[1]) + 0.5 * s * s * quad)


def main() -> None:
    g = gradient_closed(BASE)
    print(f"base point (x, y) = {BASE}")
    print(f"closed-form gradient: f_x = {g[0]:.6f}, f_y = {g[1]:.6f}")

    hess = hessian_closed(BASE)
    print(f"closed-form Hessian: f_xx = {hess[0][0]:.6f}, f_xy = {hess[0][1]:.6f}, f_yy = {hess[1][1]:.6f}")

    h = 1e-5
    fd = fd_hessian(BASE, h)
    hess = hessian_closed(BASE)
    worst = max(abs(fd[i][j] - hess[i][j]) for i in range(2) for j in range(2))
    print(f"central-difference Hessian at step {h:g}: largest error against closed form {worst:.2e}")
    asymmetry = abs(fd[0][1] - fd[1][0])
    print(f"central-difference Hessian asymmetry |f_xy - f_yx| at the same step: {asymmetry:.2e}")

    print(f"unit direction d = {DIRECTION}, norm check {DIRECTION[0] ** 2 + DIRECTION[1] ** 2:.6f}")
    previous_first = previous_second = 0.0
    for k, s in enumerate(STEPS):
        e1 = first_order_error(BASE, DIRECTION, s)
        e2 = second_order_error(BASE, DIRECTION, s)
        line = f"step s = {s:<7g} first-order error {e1: .6e}  second-order error {e2: .6e}"
        if k > 0:
            line += f"  ratios {previous_first / e1:.4f} {previous_second / e2:.4f}"
        print(line)
        previous_first, previous_second = e1, e2


main()
