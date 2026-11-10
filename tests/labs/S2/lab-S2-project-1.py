"""Lab S2-project-1: Project Rung 1 worked example.

Evaluates OLS beta, classical, White HC0, Newey-West HAC, and cluster-robust standard errors
on a fixed seeded integer/rational design using standard library only.
"""

from __future__ import annotations

import math


def solve_2x2(a: float, b: float, c: float, d: float, y1: float, y2: float) -> tuple[float, float]:
    """Solve 2x2 linear system [[a, b], [c, d]] [x1, x2]' = [y1, y2]'."""
    det = a * d - b * c
    if abs(det) < 1e-12:
        raise ValueError("Singular matrix")
    x1 = (d * y1 - b * y2) / det
    x2 = (-c * y1 + a * y2) / det
    return x1, x2


def main() -> None:
    # Fixed seeded dataset: n = 6 observations, k = 2 (intercept and slope x)
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    y = [2.2, 2.8, 3.7, 4.3, 5.1, 5.9]
    cluster_a = [0, 0, 1, 1, 2, 2]
    cluster_b = [10, 20, 10, 20, 10, 20]
    n = len(x)
    k = 2

    # Normal equations: sum(y) = n*b0 + b1*sum(x); sum(x*y) = b0*sum(x) + b1*sum(x^2)
    s_x = sum(x)
    s_y = sum(y)
    s_xx = sum(xi * xi for xi in x)
    s_xy = sum(xi * yi for xi, yi in zip(x, y, strict=True))

    det = n * s_xx - s_x * s_x
    inv_00 = s_xx / det
    inv_01 = -s_x / det
    inv_11 = n / det

    b0, b1 = solve_2x2(float(n), s_x, s_x, s_xx, s_y, s_xy)
    e = [yi - (b0 + b1 * xi) for xi, yi in zip(x, y, strict=True)]
    rss = sum(ei * ei for ei in e)

    # 1. Classical standard errors
    sigma2_c = rss / (n - k)
    se_c_b0 = math.sqrt(sigma2_c * inv_00)
    se_c_b1 = math.sqrt(sigma2_c * inv_11)

    # 2. White HC0 standard errors
    m00 = sum(ei * ei for ei in e)
    m01 = sum(ei * ei * xi for xi, ei in zip(x, e, strict=True))
    m11 = sum(ei * ei * xi * xi for xi, ei in zip(x, e, strict=True))

    v_w_00 = (inv_00**2) * m00 + 2.0 * inv_00 * inv_01 * m01 + (inv_01**2) * m11
    v_w_11 = (inv_01**2) * m00 + 2.0 * inv_01 * inv_11 * m01 + (inv_11**2) * m11
    se_w_b0 = math.sqrt(v_w_00)
    se_w_b1 = math.sqrt(v_w_11)

    # 3. Newey-West HAC (L = 1)
    # lag 1 autocovariance sum with Bartlett weight w_1 = 1 - 1/2 = 0.5
    w1 = 0.5
    gam1_00 = sum(e[t] * e[t - 1] for t in range(1, n))
    gam1_01 = sum(e[t] * e[t - 1] * x[t - 1] for t in range(1, n))
    gam1_10 = sum(e[t] * e[t - 1] * x[t] for t in range(1, n))
    gam1_11 = sum(e[t] * e[t - 1] * x[t] * x[t - 1] for t in range(1, n))

    omega_00 = m00 + w1 * 2.0 * gam1_00
    omega_01 = m01 + w1 * (gam1_01 + gam1_10)
    omega_11 = m11 + w1 * 2.0 * gam1_11

    v_nw_00 = (inv_00**2) * omega_00 + 2.0 * inv_00 * inv_01 * omega_01 + (inv_01**2) * omega_11
    v_nw_11 = (inv_01**2) * omega_00 + 2.0 * inv_01 * inv_11 * omega_01 + (inv_11**2) * omega_11
    se_nw_b0 = math.sqrt(max(0.0, v_nw_00))
    se_nw_b1 = math.sqrt(max(0.0, v_nw_11))

    # 4. Cluster-robust (cluster_a)
    scores_0: dict[int, float] = {}
    scores_1: dict[int, float] = {}
    for xi, ei, g in zip(x, e, cluster_a, strict=True):
        scores_0[g] = scores_0.get(g, 0.0) + ei
        scores_1[g] = scores_1.get(g, 0.0) + ei * xi

    meat_cl_00 = sum(s0 * s0 for s0 in scores_0.values())
    meat_cl_01 = sum(s0 * s1 for s0, s1 in zip(scores_0.values(), scores_1.values(), strict=True))
    meat_cl_11 = sum(s1 * s1 for s1 in scores_1.values())

    v_cl_00 = (inv_00**2) * meat_cl_00 + 2.0 * inv_00 * inv_01 * meat_cl_01 + (inv_01**2) * meat_cl_11
    v_cl_11 = (inv_01**2) * meat_cl_00 + 2.0 * inv_01 * inv_11 * meat_cl_01 + (inv_11**2) * meat_cl_11
    se_cl_b0 = math.sqrt(max(0.0, v_cl_00))
    se_cl_b1 = math.sqrt(max(0.0, v_cl_11))

    print(f"OLS beta: [{b0:.4f}, {b1:.4f}]")
    print(f"Classical SE: [{se_c_b0:.4f}, {se_c_b1:.4f}]")
    print(f"White HC0 SE: [{se_w_b0:.4f}, {se_w_b1:.4f}]")
    print(f"Newey-West (L=1) SE: [{se_nw_b0:.4f}, {se_nw_b1:.4f}]")
    print(f"Cluster SE (group A): [{se_cl_b0:.4f}, {se_cl_b1:.4f}]")
    print(f"Cluster B labels count: {len(set(cluster_b))}")


main()
