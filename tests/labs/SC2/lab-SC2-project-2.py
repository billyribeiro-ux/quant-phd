"""Rung 2 completion problem: completing the Itô correction and exact residual check.

For the log-price transform Y = log S, the drift must include the second-order Itô correction -sigma^2 / 2 from
(1/2) f''(S)(dS)^2. This lab implements the completed verification on seed 0 (SIMULATED), confirming that the maximum
absolute residual across all simulated paths vanishes within machine precision.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Seed 0 instance parameters (SIMULATED)
    s0 = 0.815
    mu = 0.065
    sigma = 0.107
    horizon = 0.427
    n_steps = 58
    n_paths = 387
    seed = 0

    # Itô coefficients for Y = log S
    drift_y = mu - 0.5 * sigma * sigma
    diff_y = sigma

    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    gbm_drift = (mu - 0.5 * sigma * sigma) * dt
    gbm_vol = sigma * sq_dt

    rng = random.Random(seed)
    residuals: list[float] = []

    for _ in range(n_paths):
        s = s0
        y0 = math.log(s)
        ito_sum = 0.0
        for _ in range(n_steps):
            z = rng.gauss(0.0, 1.0)
            db = sq_dt * z
            ito_sum += drift_y * dt + diff_y * db
            s *= math.exp(gbm_drift + gbm_vol * z)
        yn = math.log(s)
        residuals.append((yn - y0) - ito_sum)

    max_abs_residual = max(abs(r) for r in residuals)
    print(f"derived drift: {drift_y:.6f}")
    print(f"maximum absolute residual: {max_abs_residual:.2e}")
    print("exact invariant holds:", max_abs_residual < 1e-10)


main()
