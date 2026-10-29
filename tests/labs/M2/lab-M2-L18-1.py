"""M2 lab L18: the Jacobian of a map from R^2 to R^2 by central differences, against its closed form.

Standard library only. The map is F(x, y) = (x^2 - y^2, 2 x y). Its Jacobian array of partial
derivatives is [[2x, -2y], [2y, 2x]]. The lab fills the array by a central difference in each
variable, at 25 grid points (x and y in {-1, -0.5, 0, 0.5, 1}), with step h = 10^-5, and reports whether
the largest absolute entry error is below 1e-6. It also checks the remainder F(a + k u) - F(a) - J(a) (k u)
at a = (1, 2) for the unit vector u = (0.6, 0.8) and k = 10^-1 to 10^-4, dividing the remainder by the length
|k u| of the step.
Nothing is random.
"""

from __future__ import annotations

import math

H = 1e-5
A = (1.0, 2.0)


def big_f(x: float, y: float) -> tuple[float, float]:
    """F(x, y) = (x^2 - y^2, 2 x y), the map that sends the complex number x + i y to its square."""
    return (x * x - y * y, 2.0 * x * y)


def jacobian_closed(x: float, y: float) -> list[list[float]]:
    """The closed-form Jacobian array of F: row i holds the partial derivatives of component i."""
    return [[2.0 * x, -2.0 * y], [2.0 * y, 2.0 * x]]


def jacobian_fd(x: float, y: float, h: float) -> list[list[float]]:
    """The Jacobian array filled by central differences: entry (i, j) is the central difference of F_i in x_j."""
    up_x, down_x = big_f(x + h, y), big_f(x - h, y)
    up_y, down_y = big_f(x, y + h), big_f(x, y - h)
    columns = [
        [(up_x[i] - down_x[i]) / (2.0 * h) for i in range(2)],
        [(up_y[i] - down_y[i]) / (2.0 * h) for i in range(2)],
    ]
    return [[columns[0][0], columns[1][0]], [columns[0][1], columns[1][1]]]


def apply(matrix: list[list[float]], v: tuple[float, float]) -> tuple[float, float]:
    """The product of a 2 by 2 array with a vector in R^2."""
    return (matrix[0][0] * v[0] + matrix[0][1] * v[1], matrix[1][0] * v[0] + matrix[1][1] * v[1])


def remainder_ratio(k: float) -> float:
    """|F(a + k u) - F(a) - J(a) k u| divided by |k u|, for the unit direction u = (0.6, 0.8)."""
    ax, ay = A
    u = (0.6, 0.8)
    step = (k * u[0], k * u[1])
    fa = big_f(ax, ay)
    fk = big_f(ax + step[0], ay + step[1])
    lin = apply(jacobian_closed(ax, ay), step)
    diff = (fk[0] - fa[0] - lin[0], fk[1] - fa[1] - lin[1])
    return math.hypot(*diff) / math.hypot(*step)


def main() -> None:
    grid = [-1.0, -0.5, 0.0, 0.5, 1.0]
    worst = 0.0
    points = 0
    for x in grid:
        for y in grid:
            points += 1
            fd = jacobian_fd(x, y, H)
            cf = jacobian_closed(x, y)
            for i in range(2):
                for j in range(2):
                    worst = max(worst, abs(fd[i][j] - cf[i][j]))
    print(f"grid points: {points}")
    print(f"max entry error of the central-difference Jacobian below 1e-6: {worst < 1e-6}")
    fd_a = jacobian_fd(A[0], A[1], H)
    print("Jacobian at (1, 2) by central difference:")
    print(f"row 1: {fd_a[0][0]:.6f} {fd_a[0][1]:.6f}")
    print(f"row 2: {fd_a[1][0]:.6f} {fd_a[1][1]:.6f}")
    for k in (1e-1, 1e-2, 1e-3, 1e-4):
        print(f"remainder over step length, k = {k:.0e}: {remainder_ratio(k):.4e}")


main()
