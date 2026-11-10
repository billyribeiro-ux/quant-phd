"""Per-learner instances for the AP2 autograder (CAPM on trial).

make_instance(seed) is deterministic, produces only valid instances, and changes the answers (not just labels)
from seed to seed: the number of assets, expected returns, covariance matrix, riskless rate, target return,
and return series panel all vary with the seed. All data are SIMULATED.

The economy consists of n in {3, 4, 5} assets and a riskless lending/borrowing rate r_f.
The covariance matrix Sigma is constructed as (M'M + d*I) / scale, which is symmetric positive definite (A1).
Expected returns mu are distinct rational fractions (A2). The riskless rate r_f is strictly less than min(mu) (A3).
The tangency portfolio exists and is unique (A4). The panel contains T = 60 simple excess returns per asset
and for the market portfolio.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible, SIMULATED market instance for seed."""
    rng = random.Random(f"AP2-capm-instance/{int(seed)}")
    n = 3 + (seed % 3)  # n in {3, 4, 5}

    while True:
        # Generate integer matrix m_mat with entries in [-2, 3]
        m_mat = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(n)]
        # Covariance raw: M^T M + d * I
        cov_raw = [[sum(m_mat[k][i] * m_mat[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        diag_load = rng.randint(3, 7)
        for i in range(n):
            cov_raw[i][i] += diag_load

        # Scale down: divisor 2000 keeps variances around 0.002 - 0.006 (monthly-scale)
        scale = 2000
        cov_frac = [[Fraction(cov_raw[i][j], scale) for j in range(n)] for i in range(n)]

        # Distinct expected returns mu
        base = rng.randint(16, 28)
        mu_frac = [Fraction(base + (i + 1) * rng.randint(3, 7), 2000) for i in range(n)]
        if len(set(mu_frac)) != n:
            continue

        # Riskless rate r_f strictly below min(mu)
        r_f_frac = Fraction(rng.randint(2, 6), 2000)
        if r_f_frac >= min(mu_frac):
            continue

        # Check tangency portfolio existence: sum(Sigma^-1 (mu - r_f * iota)) != 0
        try:
            inv = _invert_exact(cov_frac)
        except ValueError:
            continue

        excess = [mu_frac[i] - r_f_frac for i in range(n)]
        z_unscaled = [sum(inv[i][j] * excess[j] for j in range(n)) for i in range(n)]
        denom = sum(z_unscaled)
        if denom == 0:
            continue

        # Check condition-number proxy (ratio of max to min diagonal elements)
        diags = [cov_frac[i][i] for i in range(n)]
        if max(diags) / min(diags) > Fraction(10, 1):
            continue

        target_frac = (min(mu_frac) + max(mu_frac)) / Fraction(2, 1)
        break

    # Time series panel: t_periods = 60 periods of simple excess returns
    t_periods = 60
    # Market excess return series: mean ~ 0.008, std ~ 0.04
    mkt = [round(rng.gauss(0.008, 0.04), 6) for _ in range(t_periods)]

    # Asset excess return series: r_it = alpha_i + beta_i * r_mt + eps_it
    asset_returns: list[list[float]] = []
    asset_fracs: list[list[str]] = []
    for i in range(n):
        true_beta = 0.5 + 0.3 * (i + 1) + rng.uniform(-0.1, 0.1)
        true_alpha = rng.uniform(-0.002, 0.002)
        series = [round(true_alpha + true_beta * mkt[t] + rng.gauss(0, 0.02), 6) for t in range(t_periods)]
        asset_returns.append(series)
        asset_fracs.append([str(Fraction(str(v))) for v in series])

    mkt_fracs = [str(Fraction(str(v))) for v in mkt]

    return {
        "seed": int(seed),
        "label": f"SIMULATED market instance seed {int(seed)} with {n} assets and T={t_periods}",
        "n": n,
        "mu": [str(x) for x in mu_frac],
        "cov": [[str(x) for x in row] for row in cov_frac],
        "r_f": str(r_f_frac),
        "target": str(target_frac),
        "T": t_periods,
        "asset_excess_returns": asset_returns,
        "market_excess_returns": mkt,
        "asset_excess_returns_fraction": asset_fracs,
        "market_excess_returns_fraction": mkt_fracs,
    }


def _invert_exact(matrix_a: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert square matrix matrix_a using exact Gauss-Jordan elimination."""
    n = len(matrix_a)
    aug = [[matrix_a[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        pivot = i
        while pivot < n and aug[pivot][i] == 0:
            pivot += 1
        if pivot == n:
            raise ValueError("matrix is singular")
        if pivot != i:
            aug[i], aug[pivot] = aug[pivot], aug[i]
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]
