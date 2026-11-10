"""Lab M8-L03-1: Bisection step count invariant and Newton's quadratic convergence.

Standard library only. Demonstrates theoretical bisection step count bound
and Newton-Raphson quadratic error recursion on f(x) = x^2 - 2.
"""

from __future__ import annotations

import math


def bisection(a: float, b: float, tol: float) -> tuple[float, int]:
    """Bisection root finder tracking iteration count."""
    fa = a * a - 2.0
    fb = b * b - 2.0
    if fa * fb > 0.0:
        raise ValueError("Root not bracketed")

    steps = 0
    while (b - a) > tol:
        steps += 1
        m = a + 0.5 * (b - a)
        fm = m * m - 2.0
        if fm == 0.0:
            return m, steps
        if fa * fm < 0.0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm
    return a + 0.5 * (b - a), steps


def newton(x0: float, max_iter: int = 7) -> list[tuple[int, float, float, float]]:
    """Newton-Raphson iteration on f(x) = x^2 - 2 with error tracking."""
    root = math.sqrt(2.0)
    x = x0
    history: list[tuple[int, float, float, float]] = []

    for k in range(max_iter):
        err = abs(x - root)
        prev_err = history[-1][2] if history else 0.0
        ratio = (err / (prev_err * prev_err)) if prev_err > 1e-15 else 0.0
        history.append((k, x, err, ratio))

        # f'(x) = 2x
        fx = x * x - 2.0
        dfx = 2.0 * x
        if abs(fx) < 1e-16 or dfx == 0.0:
            break
        x = x - fx / dfx

    return history


def main() -> None:
    print("=== Part A: Bisection Step Count Invariant ===")
    a, b = 1.0, 2.0
    width = b - a

    for tol in [1e-3, 1e-6, 1e-10, 1e-12]:
        theoretical_steps = math.ceil(math.log2(width / tol))
        approx_root, actual_steps = bisection(a, b, tol)
        print(
            f"tol={tol:.0e}: theoretical={theoretical_steps:2d}, "
            f"actual={actual_steps:2d}, root={approx_root:.12f}, "
            f"match={actual_steps == theoretical_steps}"
        )

    print("\n=== Part B: Newton's Quadratic Convergence on x^2 - 2 = 0 ===")
    # f''(root) / (2 f'(root)) = 2 / (2 * 2 * sqrt(2)) = 1 / (2 sqrt(2)) ~ 0.353553
    history = newton(x0=1.0)
    print(f"Theoretical asymptotic error ratio M = f''(x*)/(2 f'(x*)) = {1.0 / (2.0 * math.sqrt(2.0)):.6f}")
    print("Iter  Estimate x_k        Absolute Error e_k  Ratio e_k / (e_{k-1})^2")
    for k, x, err, ratio in history:
        ratio_str = f"{ratio:.6f}" if k > 0 and ratio > 0.0 else "      -"
        print(f" {k:2d}   {x:.16f}  {err:.16e}    {ratio_str}")


main()
