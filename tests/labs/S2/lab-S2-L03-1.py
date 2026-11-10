"""Lab S2-L03-1: Exact coefficient of determination R^2 and squared correlation identity.

Evaluates TSS, ESS, RSS decomposition and verifies that R^2 = 1 - RSS/TSS
equals the squared sample correlation of y and y_hat in exact rational arithmetic.
Standard library only.
"""

from __future__ import annotations

from fractions import Fraction


def solve_2x2(
    a: Fraction, b: Fraction, c: Fraction, d: Fraction, y1: Fraction, y2: Fraction
) -> tuple[Fraction, Fraction]:
    """Solve 2x2 linear system in exact rational arithmetic."""
    det = a * d - b * c
    if det == 0:
        raise ValueError("Singular matrix")
    return (d * y1 - b * y2) / det, (-c * y1 + a * y2) / det


def main() -> None:
    # Seeded integer design: n = 6 observations, k = 2 (intercept and regressor x)
    x = [Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5), Fraction(6)]
    y = [Fraction(2), Fraction(4), Fraction(5), Fraction(4), Fraction(7), Fraction(8)]
    n = Fraction(len(x))

    # OLS estimation
    s_x = sum(x, Fraction(0))
    s_y = sum(y, Fraction(0))
    s_xx = sum((xi * xi for xi in x), Fraction(0))
    s_xy = sum((xi * yi for xi, yi in zip(x, y, strict=True)), Fraction(0))

    b0, b1 = solve_2x2(n, s_x, s_x, s_xx, s_y, s_xy)

    # Fitted values and residuals
    y_hat = [b0 + b1 * xi for xi in x]
    e = [yi - yhat_i for yi, yhat_i in zip(y, y_hat, strict=True)]

    # Means
    y_bar = s_y / n
    yhat_bar = sum(y_hat, Fraction(0)) / n

    # Sum of squares
    tss = sum(((yi - y_bar) ** 2 for yi in y), Fraction(0))
    ess = sum(((yhat_i - y_bar) ** 2 for yhat_i in y_hat), Fraction(0))
    rss = sum((ei * ei for ei in e), Fraction(0))

    # Pythagorean check: TSS = ESS + RSS
    orthog_sum = ess + rss
    tss_diff = tss - orthog_sum

    # R-squared definition: 1 - RSS / TSS
    r2_def = Fraction(1) - (rss / tss)

    # Sample correlation r(y, y_hat):
    # Cov(y, y_hat) = sum((y - y_bar)(y_hat - yhat_bar))
    # Var(y) = sum((y - y_bar)^2) = TSS
    # Var(y_hat) = sum((y_hat - yhat_bar)^2) = ESS
    # Cov(y, y_hat) = sum(y * y_hat) - n * y_bar^2
    # In OLS with intercept, Cov(y, y_hat) = sum(y_hat^2) - n * y_bar^2 = ESS!
    cov_y_yhat = sum(((yi - y_bar) * (yhat_i - yhat_bar) for yi, yhat_i in zip(y, y_hat, strict=True)), Fraction(0))
    # Squared correlation: Cov^2 / (Var(y) * Var(y_hat)) = ESS^2 / (TSS * ESS) = ESS / TSS = r2_def
    sq_corr = (cov_y_yhat * cov_y_yhat) / (tss * ess)

    r2_diff = r2_def - sq_corr

    print(f"OLS coefficients: b0 = {b0} ({float(b0):.4f}), b1 = {b1} ({float(b1):.4f})")
    print(f"TSS: {tss} ({float(tss):.4f})")
    print(f"ESS: {ess} ({float(ess):.4f})")
    print(f"RSS: {rss} ({float(rss):.4f})")
    print(f"TSS - (ESS + RSS): {tss_diff}")
    print(f"R^2 (1 - RSS/TSS): {r2_def} ({float(r2_def):.6f})")
    print(f"Squared correlation r(y, y_hat)^2: {sq_corr} ({float(sq_corr):.6f})")
    print(f"Exact difference (R^2 - sq_corr): {r2_diff}")


main()
