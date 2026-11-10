"""Lab AP2-L03-1: The Capital Market Line and Sharpe ratio.

Hypothetical parameters (3 assets), not real data.
Constructs the Capital Market Line combining the riskless asset and tangency portfolio,
evaluates a grid of allocations, and verifies that the slope equals the tangency Sharpe ratio.
"""

from __future__ import annotations

import math
from fractions import Fraction


def invert_3x3(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert 3x3 matrix using exact row elimination."""
    n = 3
    aug = [[mat[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def main() -> None:
    cov = [
        [Fraction(4, 100), Fraction(1, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(5, 100), Fraction(2, 100)],
        [Fraction(1, 100), Fraction(2, 100), Fraction(6, 100)],
    ]
    mu = [Fraction(6, 100), Fraction(10, 100), Fraction(12, 100)]
    r_f = Fraction(2, 100)

    inv = invert_3x3(cov)
    excess = [mu[i] - r_f for i in range(3)]
    inv_excess = [sum((inv[i][j] * excess[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_t = sum(inv_excess, Fraction(0, 1))
    w_t = [inv_excess[i] / denom_t for i in range(3)]

    mu_t_frac = sum((w_t[i] * mu[i] for i in range(3)), Fraction(0, 1))
    sig_w_term = [sum((cov[i][j] * w_t[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    var_t_frac = sum((w_t[i] * sig_w_term[i] for i in range(3)), Fraction(0, 1))

    mu_t = float(mu_t_frac)
    sigma_t = math.sqrt(float(var_t_frac))
    r_f_float = float(r_f)
    sr_t = (mu_t - r_f_float) / sigma_t

    print(f"Tangency expected return: {mu_t:.6f}")
    print(f"Tangency volatility: {sigma_t:.6f}")
    print(f"Tangency Sharpe ratio (CML slope): {sr_t:.6f}")

    # Grid of tangency allocations w_T
    grid_w = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    for w in grid_w:
        e_p = (1.0 - w) * r_f_float + w * mu_t
        sigma_p = w * sigma_t
        cml_predicted = r_f_float + sr_t * sigma_p
        diff = abs(e_p - cml_predicted)
        print(f"w_T={w:.2f}: sigma_p={sigma_p:.6f}, E[r_p]={e_p:.6f}, CML={cml_predicted:.6f}, diff={diff:.2e}")


main()
