"""Rung 3 reference numbers: contract-pinned simulation values on seed 0.

Evaluates the Itô derivations engine on seed 0 (SIMULATED) under the frozen path-major draw-order contract.
Transform 1 (log price on GBM) produces an exact pathwise residual of zero to machine precision.
Transform 7 (square of OU process Y = X^2) produces sample residual statistics pinned by the acceptance suite:
mean -6.042148e-05 and standard error 4.397907e-05 across 387 paths and 58 steps.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Seed 0 parameters (SIMULATED)
    s0 = 0.815
    x0 = -0.085
    mu = 0.065
    sigma = 0.107
    kappa = 0.948
    theta = -0.169
    horizon = 0.427
    n_steps = 58
    n_paths = 387
    seed = 0

    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)

    # 1. Transform 1: Y = log S
    drift_1 = mu - 0.5 * (sigma**2)
    diff_1 = sigma
    gbm_drift = (mu - 0.5 * (sigma**2)) * dt
    gbm_vol = sigma * sq_dt

    rng1 = random.Random(seed)
    res_1: list[float] = []
    for _ in range(n_paths):
        s = s0
        y0 = math.log(s)
        ito_sum = 0.0
        for _ in range(n_steps):
            z = rng1.gauss(0.0, 1.0)
            db = sq_dt * z
            ito_sum += drift_1 * dt + diff_1 * db
            s *= math.exp(gbm_drift + gbm_vol * z)
        yn = math.log(s)
        res_1.append((yn - y0) - ito_sum)

    max_abs_1 = max(abs(r) for r in res_1)

    # 2. Transform 7: Y = X^2 on OU base
    rng7 = random.Random(seed)
    res_7: list[float] = []
    for _ in range(n_paths):
        x = x0
        y0 = x * x
        ito_sum = 0.0
        for _ in range(n_steps):
            z = rng7.gauss(0.0, 1.0)
            db = sq_dt * z
            drift_7 = 2.0 * kappa * x * (theta - x) + (sigma**2)
            diff_7 = 2.0 * sigma * x
            ito_sum += drift_7 * dt + diff_7 * db
            x += kappa * (theta - x) * dt + sigma * db
        yn = x * x
        res_7.append((yn - y0) - ito_sum)

    mean_7 = sum(res_7) / n_paths
    var_7 = sum((r - mean_7) ** 2 for r in res_7) / (n_paths - 1)
    se_7 = math.sqrt(var_7 / n_paths)

    print(f"seed 0 transform 1 maximum absolute residual: {max_abs_1:.2e}")
    print(f"seed 0 transform 7 residual mean: {mean_7:.6e}")
    print(f"seed 0 transform 7 residual se: {se_7:.6e}")
    print("pinned agreement within 1e-11:", abs(mean_7 - (-6.0421482183347994e-05)) < 1e-11)


main()
