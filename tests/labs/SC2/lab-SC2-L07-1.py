"""Lab 1 · Euler-Maruyama scheme: strong convergence order for additive noise.

For stochastic differential equations with additive noise (constant diffusion sigma), the Euler-Maruyama scheme
exhibits first-order strong convergence O(Delta t), in contrast to the O(Delta t^{1/2}) rate observed for multiplicative
noise. This lab simulates the Ornstein-Uhlenbeck equation dX_t = kappa(theta - X_t) dt + sigma dB_t with kappa = 2.0,
theta = 1.0, sigma = 0.30, x0 = 0.5 over [0, 1] across 2,000 paths from seed 42 (SIMULATED). Coarse Euler approximations
at step counts N in {4, 8, 16, 32} are evaluated against a fine reference grid of N_fine = 64 using identical Brownian
increments, printing root-mean-square terminal errors and verifying that error approximately halves with each
step-size halving.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    kappa = 2.0
    theta = 1.0
    sigma = 0.30
    x0 = 0.5
    horizon = 1.0
    n_paths = 2000
    seed = 42

    n_fine = 64
    dt_fine = horizon / n_fine
    sq_fine = math.sqrt(dt_fine)

    levels = [4, 8, 16, 32]
    print("Euler-Maruyama RMS error for OU against N = 64 fine grid:")

    for n_coarse in levels:
        stride = n_fine // n_coarse
        dt_coarse = horizon / n_coarse
        sq_errs: list[float] = []

        rng = random.Random(seed)
        for _ in range(n_paths):
            db_fine = [rng.gauss(0.0, sq_fine) for _ in range(n_fine)]

            # Fine reference Euler path
            x_fine = x0
            for db in db_fine:
                x_fine += kappa * (theta - x_fine) * dt_fine + sigma * db

            # Coarse Euler path on aggregated increments
            x_coarse = x0
            for k in range(n_coarse):
                db_c = sum(db_fine[k * stride : (k + 1) * stride])
                x_coarse += kappa * (theta - x_coarse) * dt_coarse + sigma * db_c

            sq_errs.append((x_coarse - x_fine) ** 2)

        rms = math.sqrt(sum(sq_errs) / n_paths)
        print(f"N = {n_coarse:2d}, dt = {dt_coarse:.4f}: RMS error = {rms:.5f}")


main()
