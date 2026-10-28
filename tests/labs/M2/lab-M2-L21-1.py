"""M2 lab L21: the derivative of an implicitly defined function, against finite differences of its root.

SIMULATED: the relation F(x, y) = y**3 + x * y - 1 = 0 is a test equation chosen for this lab. It is not market data.
For each x in a fixed list the lab finds the root y(x) > 0 by Newton's method, which is not a closed form here. It then
compares the implicit derivative dy/dx = -F_x / F_y, evaluated at the root, with a central difference of the computed
roots at step h = 1e-5. On this relation F_y = 3 y**2 + x is positive at every x > 0 used, so the hypothesis of the
implicit-function theorem (F_y not zero at the point) holds at each listed point.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

X_VALUES: tuple[float, ...] = (0.25, 0.5, 1.0, 2.0)
STEP = 1e-5
TOLERANCE = 1e-15
MAX_ITERATIONS = 100


def relation(x: float, y: float) -> float:
    """F(x, y) = y**3 + x * y - 1."""
    return y * y * y + x * y - 1.0


def relation_y(x: float, y: float) -> float:
    """The partial derivative F_y(x, y) = 3 y**2 + x."""
    return 3.0 * y * y + x


def root(x: float) -> float:
    """The root y > 0 of F(x, y) = 0 for a given x > 0, by Newton's method from y = 1.

    Starting at y = 1 is to the right of the root for every x > 0, because F(x, 1) = x > 0 and F is increasing
    in y there, so the iterates decrease to the root. A non-convergent run raises RuntimeError.
    """
    if x <= 0.0:
        raise ValueError(f"this lab takes x > 0, got {x}")
    y = 1.0
    for _ in range(MAX_ITERATIONS):
        step = relation(x, y) / relation_y(x, y)
        y -= step
        if abs(step) < TOLERANCE:
            return y
    raise RuntimeError(f"Newton's method did not converge at x = {x}")


def implicit_derivative(x: float, y: float) -> float:
    """dy/dx = -F_x / F_y at (x, y), with F_x = y for this relation and F_y = 3 y**2 + x."""
    return -y / relation_y(x, y)


def central_difference_of_root(x: float, h: float) -> float:
    """The central difference (y(x + h) - y(x - h)) / (2 h) of the computed root. The step h must be positive."""
    if h <= 0.0:
        raise ValueError(f"the step must be positive, got {h}")
    return (root(x + h) - root(x - h)) / (2.0 * h)


def main() -> None:
    print("relation F(x, y) = y^3 + x*y - 1, root y > 0, step h = 1e-5")
    for x in X_VALUES:
        y = root(x)
        residual = relation(x, y)
        formula = implicit_derivative(x, y)
        fd = central_difference_of_root(x, STEP)
        print(
            f"x = {x:<5} y = {y:.10f} residual {residual: .1e} F_y = {relation_y(x, y):.6f} "
            f"dy/dx formula {formula:.10f} central difference {fd:.10f} difference {abs(formula - fd):.1e}"
        )


main()
