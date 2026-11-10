"""Deterministic instance generator for the S2 project autograder.

Generates regression design matrices, responses, cluster labels, and
monte carlo draws for coverage evaluation. All data is SIMULATED.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid parameter set and regression problem from seed."""
    rng = random.Random(seed)

    # Number of observations n in [45, 90], number of regressors k in {2, 3, 4}
    n = 45 + (seed * 7) % 46
    k = 2 + (seed % 3)
    lags = 1 + (seed % 3)

    # Regressors: column 0 is constant 1.0 (intercept), columns 1..k-1 are seeded random draws
    # Values rounded to 2 decimal places (exact in fractions.Fraction)
    x_mat: list[list[float]] = []
    for _ in range(n):
        row = [1.0]
        for _ in range(k - 1):
            row.append(round(rng.gauss(0.0, 1.0), 2))
        x_mat.append(row)

    # True parameter vector beta
    base_betas = [1.50, -0.80, 0.40, 1.20]
    beta_true = [round(base_betas[j] + 0.10 * ((seed + j) % 5), 2) for j in range(k)]

    # Clusters: A has 6-10 clusters, B has 4-7 clusters
    g_a = 6 + (seed % 5)
    g_b = 4 + (seed % 4)
    cluster_a = [i % g_a for i in range(n)]
    cluster_b = [(i // 3) % g_b for i in range(n)]

    # Error structure depending on seed % 4
    mode = seed % 4
    err: list[float] = [0.0] * n
    if mode == 0:
        # Homoskedastic
        err = [round(rng.gauss(0.0, 1.0), 2) for _ in range(n)]
    elif mode == 1:
        # Heteroskedastic: variance scales with |x_{i, 1}|
        err = [round(rng.gauss(0.0, 0.5 + 0.8 * abs(x_mat[i][1])), 2) for i in range(n)]
    elif mode == 2:
        # AR(1) autocorrelated
        innov = [rng.gauss(0.0, 1.0) for _ in range(n)]
        val = innov[0]
        err[0] = round(val, 2)
        for t in range(1, n):
            val = 0.6 * val + innov[t]
            err[t] = round(val, 2)
    else:
        # Clustered error: cluster shock + individual shock
        shocks = [rng.gauss(0.0, 1.2) for _ in range(g_a)]
        err = [round(shocks[cluster_a[i]] + rng.gauss(0.0, 0.8), 2) for i in range(n)]

    # Observed response y
    y: list[float] = []
    for i in range(n):
        y_val = sum(x_mat[i][j] * beta_true[j] for j in range(k)) + err[i]
        y.append(round(y_val, 2))

    # Pre-generate 50 response vectors for coverage study draws
    draws_y: list[list[float]] = []
    for _ in range(50):
        if mode == 0:
            e_draw = [round(rng.gauss(0.0, 1.0), 2) for _ in range(n)]
        elif mode == 1:
            e_draw = [round(rng.gauss(0.0, 0.5 + 0.8 * abs(x_mat[i][1])), 2) for i in range(n)]
        elif mode == 2:
            innov = [rng.gauss(0.0, 1.0) for _ in range(n)]
            v = innov[0]
            e_draw = [round(v, 2)]
            for t in range(1, n):
                v = 0.6 * v + innov[t]
                e_draw.append(round(v, 2))
        else:
            shocks = [rng.gauss(0.0, 1.2) for _ in range(g_a)]
            e_draw = [round(shocks[cluster_a[i]] + rng.gauss(0.0, 0.8), 2) for i in range(n)]

        y_d = [round(sum(x_mat[i][j] * beta_true[j] for j in range(k)) + e_draw[i], 2) for i in range(n)]
        draws_y.append(y_d)

    return {
        "seed": seed,
        "label": "SIMULATED",
        "n": n,
        "k": k,
        "X": x_mat,
        "y": y,
        "beta_true": beta_true,
        "lags": lags,
        "cluster_a": cluster_a,
        "cluster_b": cluster_b,
        "draws_y": draws_y,
    }
