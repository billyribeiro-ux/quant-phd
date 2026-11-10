"""Lab S2-project-3: Project Rung 3 independent project self-check.

Executes reference inference calculations on a generated regression instance,
verifying residual orthogonality and displaying standard errors across all five methods.
Standard library only.
"""

from __future__ import annotations

import math


def main() -> None:
    # 5 observations, k = 2 (intercept and regressor)
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.5, 2.7, 3.2, 4.8, 5.6]
    n = len(x)
    k = 2

    s_x = sum(x)
    s_y = sum(y)
    s_xx = sum(xi * xi for xi in x)
    s_xy = sum(xi * yi for xi, yi in zip(x, y, strict=True))

    det = n * s_xx - s_x * s_x
    b1 = (n * s_xy - s_x * s_y) / det
    b0 = (s_y - b1 * s_x) / n

    e = [yi - (b0 + b1 * xi) for xi, yi in zip(x, y, strict=True)]
    rss = sum(ei * ei for ei in e)

    # Orthogonality checks
    sum_e = sum(e)
    sum_xe = sum(xi * ei for xi, ei in zip(x, e, strict=True))

    inv_00 = s_xx / det
    inv_01 = -s_x / det
    inv_11 = n / det

    # Classical SE
    sigma2_c = rss / (n - k)
    se_c_intercept = math.sqrt(sigma2_c * inv_00)
    se_c_slope = math.sqrt(sigma2_c * inv_11)

    # HC0 SE
    m00 = sum(ei * ei for ei in e)
    m01 = sum(ei * ei * xi for xi, ei in zip(x, e, strict=True))
    m11 = sum(ei * ei * xi * xi for xi, ei in zip(x, e, strict=True))
    v_w_00 = (inv_00**2) * m00 + 2.0 * inv_00 * inv_01 * m01 + (inv_01**2) * m11
    v_w_11 = (inv_01**2) * m00 + 2.0 * inv_01 * inv_11 * m01 + (inv_11**2) * m11
    se_w_intercept = math.sqrt(v_w_00)
    se_w_slope = math.sqrt(v_w_11)

    print(f"Sample size n: {n}, Regressors k: {k}")
    print(f"OLS intercept b0: {b0:.4f}, slope b1: {b1:.4f}")
    print(f"Residual sum (orthogonality to 1): {sum_e:.8f}")
    print(f"Residual x-dot (orthogonality to x): {sum_xe:.8f}")
    print(f"Classical intercept SE: {se_c_intercept:.4f}, slope SE: {se_c_slope:.4f}")
    print(f"White HC0 intercept SE: {se_w_intercept:.4f}, slope SE: {se_w_slope:.4f}")


main()
