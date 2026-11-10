"""Lab AP2-L02-1: Tangency portfolio and two-fund separation.

Hypothetical parameters (3 assets), not real data.
Computes the tangency portfolio weights w_T in exact Fraction arithmetic,
verifies proportionality Sigma @ w_T proportional to mu - r_f * iota,
and checks two-fund separation against the GMV portfolio.
"""

from __future__ import annotations

import random
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
    iota = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]

    inv = invert_3x3(cov)
    excess = [mu[i] - r_f for i in range(3)]
    inv_excess = [sum((inv[i][j] * excess[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_t = sum(inv_excess, Fraction(0, 1))
    w_t = [inv_excess[i] / denom_t for i in range(3)]

    print(f"Excess returns: [{excess[0]}, {excess[1]}, {excess[2]}]")
    print(f"w_T: [{w_t[0]}, {w_t[1]}, {w_t[2]}]")
    print(f"sum(w_T): {sum(w_t, Fraction(0, 1))}")

    # Proportionality check: Sigma @ w_T = c * excess
    sig_wt = [sum((cov[i][j] * w_t[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    props = [sig_wt[i] / excess[i] for i in range(3)]
    print(f"Proportionality constants: [{props[0]}, {props[1]}, {props[2]}]")
    print(f"Proportionality holds: {props[0] == props[1] == props[2]}")

    # GMV portfolio
    inv_iota = [sum((inv[i][j] * iota[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    denom_gmv = sum(inv_iota, Fraction(0, 1))
    w_gmv = [inv_iota[i] / denom_gmv for i in range(3)]
    mu_gmv = sum((w_gmv[i] * mu[i] for i in range(3)), Fraction(0, 1))
    mu_t = sum((w_t[i] * mu[i] for i in range(3)), Fraction(0, 1))

    # Two-fund separation check on a seeded random target return
    rng = random.Random(42)
    alpha = Fraction(rng.randint(2, 8), 10)  # mix 20% to 80%
    target_mu = (Fraction(1, 1) - alpha) * mu_gmv + alpha * mu_t
    w_separated = [(Fraction(1, 1) - alpha) * w_gmv[i] + alpha * w_t[i] for i in range(3)]

    # Compute frontier weights directly for target_mu
    scalar_a = denom_gmv
    scalar_b = sum((iota[i] * inv_excess[i] for i in range(3)), Fraction(0, 1)) + r_f * scalar_a
    inv_mu_term = [sum((inv[i][j] * mu[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    scalar_c = sum((mu[i] * inv_mu_term[i] for i in range(3)), Fraction(0, 1))
    scalar_d = scalar_a * scalar_c - scalar_b * scalar_b
    l1 = (scalar_c - scalar_b * target_mu) / scalar_d
    l2 = (scalar_a * target_mu - scalar_b) / scalar_d
    inv_mu = [sum((inv[i][j] * mu[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    w_frontier = [l1 * inv_iota[i] + l2 * inv_mu[i] for i in range(3)]

    print(f"Alpha: {alpha}")
    print(f"Target mu: {target_mu}")
    print(f"w_separated: [{w_separated[0]}, {w_separated[1]}, {w_separated[2]}]")
    print(f"w_frontier:  [{w_frontier[0]}, {w_frontier[1]}, {w_frontier[2]}]")
    print(f"Separation exact match: {w_separated == w_frontier}")


main()
