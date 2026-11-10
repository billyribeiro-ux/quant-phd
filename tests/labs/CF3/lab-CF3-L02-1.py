"""CF3 lab L02-1: Lintner partial-adjustment model and dividend smoothing.

Model: John Lintner (1956) partial adjustment model of corporate dividends:
Delta D_t = a_0 + c * (r * E_t - D_{t-1}) + u_t
Estimates speed of adjustment (c), target payout ratio (r), and half-life of adjustment
using multivariate OLS regression on corporate earnings and dividend histories.
Standard library only; deterministic simulated 20-year panel.
"""

from __future__ import annotations

import math
import random


def simulate_lintner_history(
    years: int,
    true_r: float,
    true_c: float,
    true_a0: float,
    seed: int = 42,
) -> tuple[list[float], list[float], list[float]]:
    """Simulate annual earnings and dividend time series following Lintner dynamics."""
    rng = random.Random(seed)
    earnings: list[float] = []
    dividends: list[float] = []
    delta_div: list[float] = []

    # Initial period earnings and dividend
    e_curr = 100.0  # Millions
    d_curr = true_r * e_curr  # Initially on target
    earnings.append(e_curr)
    dividends.append(d_curr)

    for _ in range(1, years):
        # Earnings grow with drift + cyclical shocks
        growth = 0.05 + rng.gauss(0.0, 0.12)
        e_curr = max(20.0, e_curr * (1.0 + growth))

        target_d = true_r * e_curr
        # Lintner partial adjustment with noise
        noise = rng.gauss(0.0, 1.20)
        delta_d = true_a0 + true_c * (target_d - d_curr) + noise

        # Ensure dividends are non-negative
        d_next = max(1.0, d_curr + delta_d)
        actual_delta = d_next - d_curr

        earnings.append(round(e_curr, 2))
        dividends.append(round(d_next, 2))
        delta_div.append(round(actual_delta, 2))
        d_curr = d_next

    return earnings, dividends, delta_div


def ols_lintner_regression(
    earnings: list[float],
    dividends: list[float],
) -> dict[str, float]:
    """Estimate Delta D_t = b0 + b1 * E_t + b2 * D_{t-1} using linear algebra in pure Python.

    Lintner identification:
    b1 = c * r  =>  r = b1 / c = -b1 / b2
    b2 = -c     =>  c = -b2
    """
    n = len(earnings) - 1
    # Y vector: Delta D_t for t = 1 .. n
    y = [dividends[t] - dividends[t - 1] for t in range(1, n + 1)]
    # X matrix: [1, E_t, D_{t-1}]
    x = [[1.0, earnings[t], dividends[t - 1]] for t in range(1, n + 1)]

    # Compute X^T X (3x3) and X^T Y (3x1)
    xtx = [[sum(x[i][j] * x[i][k] for i in range(n)) for k in range(3)] for j in range(3)]
    xty = [sum(x[i][j] * y[i] for i in range(n)) for j in range(3)]

    # Invert 3x3 symmetric matrix via Cramer's rule / adjoint
    det = (
        xtx[0][0] * (xtx[1][1] * xtx[2][2] - xtx[1][2] * xtx[2][1])
        - xtx[0][1] * (xtx[1][0] * xtx[2][2] - xtx[1][2] * xtx[2][0])
        + xtx[0][2] * (xtx[1][0] * xtx[2][1] - xtx[1][1] * xtx[2][0])
    )
    if abs(det) < 1e-12:
        raise ValueError("Singular matrix in Lintner regression")

    inv = [
        [
            (xtx[1][1] * xtx[2][2] - xtx[1][2] * xtx[2][1]) / det,
            (xtx[0][2] * xtx[2][1] - xtx[0][1] * xtx[2][2]) / det,
            (xtx[0][1] * xtx[1][2] - xtx[0][2] * xtx[1][1]) / det,
        ],
        [
            (xtx[1][2] * xtx[2][0] - xtx[1][0] * xtx[2][2]) / det,
            (xtx[0][0] * xtx[2][2] - xtx[0][2] * xtx[2][0]) / det,
            (xtx[0][2] * xtx[1][0] - xtx[0][0] * xtx[1][2]) / det,
        ],
        [
            (xtx[1][0] * xtx[2][1] - xtx[1][1] * xtx[2][0]) / det,
            (xtx[0][1] * xtx[2][0] - xtx[0][0] * xtx[2][1]) / det,
            (xtx[0][0] * xtx[1][1] - xtx[0][1] * xtx[1][0]) / det,
        ],
    ]

    # beta = (X^T X)^{-1} X^T Y
    beta = [sum(inv[j][k] * xty[k] for k in range(3)) for j in range(3)]
    b0, b1, b2 = beta

    # Structural parameters
    c_speed = -b2
    r_target = b1 / c_speed if abs(c_speed) > 1e-6 else 0.0
    half_life = math.log(0.5) / math.log(1.0 - c_speed) if 0.0 < c_speed < 1.0 else float("nan")

    # Goodness of fit
    y_mean = sum(y) / n
    tss = sum((yi - y_mean) ** 2 for yi in y)
    rss = sum((y[i] - sum(x[i][j] * beta[j] for j in range(3))) ** 2 for i in range(n))
    r_squared = 1.0 - (rss / tss) if tss > 0 else 0.0

    return {
        "b0": b0,
        "b1": b1,
        "b2": b2,
        "c_speed": c_speed,
        "r_target": r_target,
        "half_life": half_life,
        "r_squared": r_squared,
        "n": float(n),
    }


def main() -> None:
    print("CF3 Lab L02-1: The Lintner Partial-Adjustment Model")
    print("==================================================")

    true_r = 0.40  # 40% target payout ratio
    true_c = 0.32  # 32% annual adjustment speed toward target
    true_a0 = 0.50  # Modest positive drift (reluctance to cut)
    years = 25

    print(f"True Lintner parameters: r* = {true_r:.2%}, c* = {true_c:.2%}, a0* = ${true_a0:.2f}M")
    true_hl = math.log(0.5) / math.log(1.0 - true_c)
    print(f"True half-life of deviation: {true_hl:.2f} years")

    earnings, dividends, _ = simulate_lintner_history(years, true_r, true_c, true_a0, seed=101)
    res = ols_lintner_regression(earnings, dividends)

    print(f"\nEstimated regression over {int(res['n'])} periods:")
    print("  Model: Delta D_t = b0 + b1 * E_t + b2 * D_{t-1} + u_t")
    print(f"  Estimated b0 (drift):        {res['b0']:.4f}")
    print(f"  Estimated b1 (c * r):        {res['b1']:.4f}")
    print(f"  Estimated b2 (-c):           {res['b2']:.4f}")
    print(f"  Model R-squared:             {res['r_squared']:.4f}")

    print("\nRecovered structural Lintner parameters:")
    print(f"  Speed of adjustment (c_hat = -b2):  {res['c_speed']:.4f} ({res['c_speed']:.2%})")
    print(f"  Target payout ratio (r_hat = b1/c): {res['r_target']:.4f} ({res['r_target']:.2%})")
    print(f"  Estimated half-life of deviation:   {res['half_life']:.2f} years")


main()
