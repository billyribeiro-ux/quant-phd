"""Rung 1 worked example: derivation and verification of the log-price transform on seed 0.

For a geometric Brownian motion dS_t = mu S_t dt + sigma S_t dB_t with S_0 = s0 > 0, applying Itô's lemma to
Y_t = f(S_t) = log S_t yields:
    df = f'(S) dS + (1/2) f''(S) (dS)^2 = (1/S)(mu S dt + sigma S dB) + (1/2)(-1/S^2)(sigma^2 S^2 dt)
       = (mu - sigma^2/2) dt + sigma dB.
On the seed 0 SIMULATED instance, this lab evaluates the drift mu_Y = mu - sigma^2/2 and diffusion sigma_Y = sigma,
simulates the exact base GBM paths, and verifies that the discrete Itô residual vanishes pathwise across all paths.
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
    mean_residual = sum(residuals) / n_paths

    print(f"seed 0 parameters: s0 = {s0:.3f}, mu = {mu:.3f}, sigma = {sigma:.3f}, H = {horizon:.3f}")
    print(f"derived coefficients: drift = {drift_y:.6f}, diffusion = {diff_y:.6f}")
    print(f"maximum absolute residual across {n_paths} paths: {max_abs_residual:.2e}")
    print(f"mean residual: {mean_residual:.2e}")
    print("residual vanishes within 1e-10:", max_abs_residual < 1e-10)


main()
