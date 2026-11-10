"""Lab S2-L01-1: Exact OLS normal equations and residual orthogonality.

Evaluates OLS projection, normal equations, and residual orthogonality
using exact rational arithmetic (fractions.Fraction). Standard library only.
"""

from __future__ import annotations

from fractions import Fraction


def solve_2x2(
    a: Fraction, b: Fraction, c: Fraction, d: Fraction, y1: Fraction, y2: Fraction
) -> tuple[Fraction, Fraction]:
    """Solve 2x2 linear system [[a, b], [c, d]] [b0, b1]' = [y1, y2]' in exact rational arithmetic."""
    det = a * d - b * c
    if det == 0:
        raise ValueError("Singular matrix")
    x1 = (d * y1 - b * y2) / det
    x2 = (-c * y1 + a * y2) / det
    return x1, x2


def main() -> None:
    # Seeded integer design: n = 5 observations, k = 2 (constant intercept and regressor x)
    x = [Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)]
    y = [Fraction(2), Fraction(3), Fraction(5), Fraction(4), Fraction(6)]
    n = Fraction(len(x))

    # Compute inner products for normal equations
    s_x = sum(x, Fraction(0))
    s_y = sum(y, Fraction(0))
    s_xx = sum((xi * xi for xi in x), Fraction(0))
    s_xy = sum((xi * yi for xi, yi in zip(x, y, strict=True)), Fraction(0))

    # Normal equations:
    # [[n, s_x], [s_x, s_xx]] [b0, b1]' = [s_y, s_xy]'
    b0, b1 = solve_2x2(n, s_x, s_x, s_xx, s_y, s_xy)

    # Fitted values and residuals
    y_hat = [b0 + b1 * xi for xi in x]
    e = [yi - yhat_i for yi, yhat_i in zip(y, y_hat, strict=True)]

    # Orthogonality checks: X'e must be identically zero
    orthog_const = sum(e, Fraction(0))
    orthog_x = sum((xi * ei for xi, ei in zip(x, e, strict=True)), Fraction(0))

    # Hat matrix diagonal elements: h_ii = x_i' (X'X)^{-1} x_i
    det = n * s_xx - s_x * s_x
    inv_00 = s_xx / det
    inv_01 = -s_x / det
    inv_11 = n / det

    h_diag = [inv_00 + Fraction(2) * inv_01 * xi + inv_11 * xi * xi for xi in x]
    trace_h = sum(h_diag, Fraction(0))

    print(f"OLS intercept b0: {b0} ({float(b0):.4f})")
    print(f"OLS slope b1: {b1} ({float(b1):.4f})")
    print(f"Residual orthogonality to 1 (sum e): {orthog_const}")
    print(f"Residual orthogonality to x (sum x*e): {orthog_x}")
    print(f"Trace of hat matrix H: {trace_h} (k = 2)")
    print(f"Residuals: {[str(ei) for ei in e]}")


main()
