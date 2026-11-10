"""Deterministic problem instance generator for X3 Kilian SVAR oil-shock decomposition."""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, realistic 3-variable monthly oil market instance.

    Variables:
      0: delta_prod - percentage growth rate of global crude oil production (monthly %)
      1: rea - index of global real economic activity (Kilian freight-rate proxy, index points)
      2: rpo - real price of crude oil (log price index)
    """
    rng = random.Random(seed)
    n_obs = 140
    p = 2
    k_vars = 3

    # Stationary VAR(2) matrices with slight per-seed jitter
    b1 = [
        [0.15 + rng.uniform(-0.02, 0.02), 0.01 + rng.uniform(-0.002, 0.002), -0.05 + rng.uniform(-0.01, 0.01)],
        [0.50 + rng.uniform(-0.05, 0.05), 0.70 + rng.uniform(-0.02, 0.02), -0.50 + rng.uniform(-0.05, 0.05)],
        [0.02 + rng.uniform(-0.005, 0.005), 0.008 + rng.uniform(-0.001, 0.001), 0.82 + rng.uniform(-0.02, 0.02)],
    ]
    b2 = [
        [0.05 + rng.uniform(-0.01, 0.01), 0.005 + rng.uniform(-0.001, 0.001), -0.02 + rng.uniform(-0.005, 0.005)],
        [-0.20 + rng.uniform(-0.02, 0.02), 0.15 + rng.uniform(-0.02, 0.02), -0.20 + rng.uniform(-0.02, 0.02)],
        [-0.01 + rng.uniform(-0.002, 0.002), 0.002 + rng.uniform(-0.001, 0.001), 0.06 + rng.uniform(-0.01, 0.01)],
    ]

    # Unconditional means: delta_prod ~ 0.1%, rea ~ 0.0, rpo ~ 4.0
    mu = [0.10, 0.0, 4.0]
    i_minus_b = [
        [1.0 - b1[0][0] - b2[0][0], -b1[0][1] - b2[0][1], -b1[0][2] - b2[0][2]],
        [-b1[1][0] - b2[1][0], 1.0 - b1[1][1] - b2[1][1], -b1[1][2] - b2[1][2]],
        [-b1[2][0] - b2[2][0], -b1[2][1] - b2[2][1], 1.0 - b1[2][2] - b2[2][2]],
    ]
    intercepts = [sum(i_minus_b[i][j] * mu[j] for j in range(k_vars)) for i in range(k_vars)]

    # Lower-triangular Cholesky impact matrix P (A_0^-1)
    p_mat = [
        [1.20, 0.0, 0.0],
        [0.60 + rng.uniform(-0.05, 0.05), 8.00, 0.0],
        [-0.03 + rng.uniform(-0.005, 0.005), 0.04 + rng.uniform(-0.005, 0.005), 0.12],
    ]

    burn = 100
    total_steps = burn + n_obs
    y = [mu[:] for _ in range(p)]
    for t in range(p, total_steps):
        eps = [rng.gauss(0.0, 1.0) for _ in range(k_vars)]
        e = [sum(p_mat[i][j] * eps[j] for j in range(k_vars)) for i in range(k_vars)]
        yt = [
            intercepts[i]
            + sum(b1[i][j] * y[t - 1][j] for j in range(k_vars))
            + sum(b2[i][j] * y[t - 2][j] for j in range(k_vars))
            + e[i]
            for i in range(k_vars)
        ]
        y.append(yt)

    data = [[round(val, 6) for val in row] for row in y[burn:]]
    return {
        "seed": seed,
        "n_obs": n_obs,
        "lags": p,
        "horizon": 24,
        "variable_names": ["delta_prod", "rea", "rpo"],
        "data": data,
    }
