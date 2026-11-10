"""Lab M8-L05-1: Natural cubic spline interpolation and numerical quadrature convergence.

Standard library only. Demonstrates O(h^4) convergence of cubic splines,
O(h^2) for composite trapezoid, and O(h^4) for composite Simpson's rule.
"""

from __future__ import annotations

import math


def natural_cubic_spline(
    x_nodes: list[float], y_nodes: list[float]
) -> tuple[list[float], list[float], list[float], list[float]]:
    """Fit natural cubic spline passing through given nodes.

    Returns coefficients (a, b, c, d) for each interval i:
    S_i(x) = a_i + b_i*(x - x_i) + c_i*(x - x_i)^2 + d_i*(x - x_i)^3.
    """
    n = len(x_nodes) - 1
    h = [x_nodes[i + 1] - x_nodes[i] for i in range(n)]

    # Tridiagonal system for c_i = M_i / 2:
    # h_{i-1} c_{i-1} + 2(h_{i-1} + h_i) c_i + h_i c_{i+1} = 3 ((y_{i+1} - y_i)/h_i - (y_i - y_{i-1})/h_{i-1})
    alpha = [0.0] * (n + 1)
    for i in range(1, n):
        alpha[i] = 3.0 * ((y_nodes[i + 1] - y_nodes[i]) / h[i] - (y_nodes[i] - y_nodes[i - 1]) / h[i - 1])

    # Thomas algorithm for tridiagonal system with c_0 = c_n = 0
    l_diag = [1.0] * (n + 1)
    mu = [0.0] * (n + 1)
    z = [0.0] * (n + 1)

    for i in range(1, n):
        l_diag[i] = 2.0 * (x_nodes[i + 1] - x_nodes[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l_diag[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l_diag[i]

    c = [0.0] * (n + 1)
    b = [0.0] * n
    d = [0.0] * n
    a = [y_nodes[i] for i in range(n)]

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y_nodes[j + 1] - y_nodes[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    return a, b, c[:n], d


def eval_spline(
    x: float,
    x_nodes: list[float],
    a: list[float],
    b: list[float],
    c: list[float],
    d: list[float],
) -> float:
    n = len(x_nodes) - 1
    # Locate interval
    if x <= x_nodes[0]:
        idx = 0
    elif x >= x_nodes[-1]:
        idx = n - 1
    else:
        idx = 0
        for i in range(n):
            if x_nodes[i] <= x <= x_nodes[i + 1]:
                idx = i
                break
    dx = x - x_nodes[idx]
    return a[idx] + b[idx] * dx + c[idx] * (dx**2) + d[idx] * (dx**3)


def composite_trapezoid(f_vals: list[float], h: float) -> float:
    """Composite trapezoid rule."""
    return h * (0.5 * f_vals[0] + sum(f_vals[1:-1]) + 0.5 * f_vals[-1])


def composite_simpson(f_vals: list[float], h: float) -> float:
    """Composite Simpson's rule (requires even number of intervals)."""
    n = len(f_vals) - 1
    assert n % 2 == 0
    s_odd = sum(f_vals[i] for i in range(1, n, 2))
    s_even = sum(f_vals[i] for i in range(2, n, 2))
    return (h / 3.0) * (f_vals[0] + 4.0 * s_odd + 2.0 * s_even + f_vals[-1])


def main() -> None:
    print("=== Part A: Natural Cubic Spline Interpolation of sin(x) on [0, pi] ===")
    fine_x = [math.pi * i / 1000.0 for i in range(1001)]
    true_fine = [math.sin(x) for x in fine_x]

    prev_err_spline = 0.0
    for n in [4, 8, 16, 32]:
        x_nodes = [math.pi * i / n for i in range(n + 1)]
        y_nodes = [math.sin(x) for x in x_nodes]
        a, b, c, d = natural_cubic_spline(x_nodes, y_nodes)

        max_err = max(
            abs(eval_spline(x, x_nodes, a, b, c, d) - y_true) for x, y_true in zip(fine_x, true_fine, strict=False)
        )
        order_str = f"{math.log2(prev_err_spline / max_err):.2f}" if prev_err_spline > 0 else "-"
        print(f"n={n:2d} panels: max error = {max_err:.8e}, order = {order_str}")
        prev_err_spline = max_err

    print("\n=== Part B: Numerical Quadrature of int_0^1 exp(x) dx ===")
    true_integral = math.e - 1.0
    print(f"Exact integral e - 1: {true_integral:.16f}")
    print(" n    Trap Error     Trap Order    Simp Error     Simp Order")

    prev_trap_err = 0.0
    prev_simp_err = 0.0

    for n in [2, 4, 8, 16, 32]:
        h = 1.0 / n
        f_vals = [math.exp(i * h) for i in range(n + 1)]
        trap_val = composite_trapezoid(f_vals, h)
        simp_val = composite_simpson(f_vals, h)

        trap_err = abs(trap_val - true_integral)
        simp_err = abs(simp_val - true_integral)

        trap_order = f"{math.log2(prev_trap_err / trap_err):.2f}" if prev_trap_err > 0 else "   -  "
        simp_order = f"{math.log2(prev_simp_err / simp_err):.2f}" if prev_simp_err > 0 else "   -  "

        print(f"{n:2d}   {trap_err:.8e}    {trap_order}    {simp_err:.8e}    {simp_order}")
        prev_trap_err = trap_err
        prev_simp_err = simp_err


main()
