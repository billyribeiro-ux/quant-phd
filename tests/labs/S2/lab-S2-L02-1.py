"""Lab S2-L02-1: Exact Frisch-Waugh-Lovell partialling out identity.

Evaluates the Frisch-Waugh-Lovell theorem using exact rational arithmetic
(fractions.Fraction). Verifies that the partialled-out slope equals the
multivariate regression coefficient identically. Standard library only.
"""

from __future__ import annotations

from fractions import Fraction


def solve_3x3(mat: list[list[Fraction]], rhs: list[Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    """Solve 3x3 linear system A * b = rhs using Gaussian elimination in exact rational arithmetic."""
    a = [[Fraction(val.numerator, val.denominator) for val in row] for row in mat]
    b = [Fraction(val.numerator, val.denominator) for val in rhs]

    # Forward elimination with partial pivoting
    for i in range(3):
        # Pivot selection
        pivot = i
        for r in range(i + 1, 3):
            if abs(a[r][i]) > abs(a[pivot][i]):
                pivot = r
        if a[pivot][i] == Fraction(0):
            raise ValueError("Singular matrix")
        a[i], a[pivot] = a[pivot], a[i]
        b[i], b[pivot] = b[pivot], b[i]

        for r in range(i + 1, 3):
            factor = a[r][i] / a[i][i]
            for c in range(i, 3):
                a[r][c] -= factor * a[i][c]
            b[r] -= factor * b[i]

    # Back substitution
    ans = [Fraction(0), Fraction(0), Fraction(0)]
    for i in range(2, -1, -1):
        s = sum((a[i][j] * ans[j] for j in range(i + 1, 3)), Fraction(0))
        ans[i] = (b[i] - s) / a[i][i]

    return ans[0], ans[1], ans[2]


def solve_2x2(
    a: Fraction, b: Fraction, c: Fraction, d: Fraction, y1: Fraction, y2: Fraction
) -> tuple[Fraction, Fraction]:
    """Solve 2x2 linear system in exact rational arithmetic."""
    det = a * d - b * c
    if det == 0:
        raise ValueError("Singular matrix")
    return (d * y1 - b * y2) / det, (-c * y1 + a * y2) / det


def main() -> None:
    # Seeded integer design: n = 6 observations, k = 3 (intercept 1, regressor x1, regressor x2)
    # y = response
    x1 = [Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5), Fraction(6)]
    x2 = [Fraction(2), Fraction(1), Fraction(4), Fraction(3), Fraction(7), Fraction(5)]
    y = [Fraction(3), Fraction(5), Fraction(8), Fraction(7), Fraction(13), Fraction(11)]
    n = Fraction(len(y))

    # --- Step 1: Full multivariate OLS regression: y = b0 + b1*x1 + b2*x2 ---
    # Construct normal equations (X'X) b = X'y
    s_x1 = sum(x1, Fraction(0))
    s_x2 = sum(x2, Fraction(0))
    s_y = sum(y, Fraction(0))

    s_x1x1 = sum((xi * xi for xi in x1), Fraction(0))
    s_x2x2 = sum((xi * xi for xi in x2), Fraction(0))
    s_x1x2 = sum((xi * xj for xi, xj in zip(x1, x2, strict=True)), Fraction(0))

    s_x1y = sum((xi * yi for xi, yi in zip(x1, y, strict=True)), Fraction(0))
    s_x2y = sum((xi * yi for xi, yi in zip(x2, y, strict=True)), Fraction(0))

    gram = [
        [n, s_x1, s_x2],
        [s_x1, s_x1x1, s_x1x2],
        [s_x2, s_x1x2, s_x2x2],
    ]
    rhs = [s_y, s_x1y, s_x2y]

    b0, b1, b2 = solve_3x3(gram, rhs)

    # --- Step 2: Partialling out via Frisch-Waugh-Lovell ---
    # Auxiliary regression A: Regress y on [1, x1] -> residuals y_tilde = M1 * y
    gamma_y0, gamma_y1 = solve_2x2(n, s_x1, s_x1, s_x1x1, s_y, s_x1y)
    y_tilde = [yi - (gamma_y0 + gamma_y1 * xi) for xi, yi in zip(x1, y, strict=True)]

    # Auxiliary regression B: Regress x2 on [1, x1] -> residuals x2_tilde = M1 * x2
    gamma_x0, gamma_x1 = solve_2x2(n, s_x1, s_x1, s_x1x1, s_x2, s_x1x2)
    x2_tilde = [xi2 - (gamma_x0 + gamma_x1 * xi1) for xi1, xi2 in zip(x1, x2, strict=True)]

    # Bivariate regression of y_tilde on x2_tilde without intercept (since M1 is mean-zero projection)
    num = sum((xi * yi for xi, yi in zip(x2_tilde, y_tilde, strict=True)), Fraction(0))
    den = sum((xi * xi for xi in x2_tilde), Fraction(0))
    b2_partial = num / den

    # Also regress raw y on x2_tilde
    num_raw = sum((xi * yi for xi, yi in zip(x2_tilde, y, strict=True)), Fraction(0))
    b2_raw = num_raw / den

    # Exact difference check
    diff = b2 - b2_partial

    print(f"Full regression b0: {b0} ({float(b0):.6f}), b1: {b1} ({float(b1):.6f})")
    print(f"Full regression b2: {b2} ({float(b2):.6f})")
    print(f"Partialled-out residual regression b2: {b2_partial} ({float(b2_partial):.6f})")
    print(f"Raw y on x2_tilde regression: {b2_raw} ({float(b2_raw):.6f})")
    print(f"Exact difference (b2 - b2_partial): {diff}")


main()
