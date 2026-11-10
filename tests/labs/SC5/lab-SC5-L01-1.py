"""Lab 1 · Compensated compound Poisson process martingale property and variance identity.

A compound Poisson process X_t = sum_{k=1}^{N_t} Y_k has jump intensity lambda and i.i.d. jump sizes Y_k.
Its expectation is E[X_t] = lambda * t * E[Y], and its variance is Var(X_t) = lambda * t * E[Y^2].
The compensated process M_t = X_t - lambda * t * E[Y] is a continuous-time martingale with E[M_t] = 0.
This lab simulates 5,000 independent realization paths on [0, H] (SIMULATED) using seed 42,
evaluates the terminal sample mean and sample variance of M_H, and verifies agreement with
the theoretical moment identities within 3 standard errors.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    seed = 42
    rng = random.Random(seed)

    horizon = 1.0
    lam = 2.5
    mu_y = -0.05
    sigma_y = 0.15

    # Theoretical moments
    e_y = mu_y
    e_y2 = sigma_y**2 + mu_y**2
    theoretical_mean_x = lam * horizon * e_y
    theoretical_var_x = lam * horizon * e_y2

    n_paths = 5000
    terminal_m: list[float] = []

    for _ in range(n_paths):
        # Simulate number of jumps N_H ~ Poisson(lambda * H)
        # Using inverse transform / Poisson generator
        l_param = lam * horizon
        p = 1.0
        k = 0
        l_exp = math.exp(-l_param)
        while True:
            p *= rng.random()
            if p <= l_exp:
                break
            k += 1
        n_jumps = k

        # Sum jump sizes
        jump_sum = sum(rng.gauss(mu_y, sigma_y) for _ in range(n_jumps))
        compensated_val = jump_sum - lam * horizon * e_y
        terminal_m.append(compensated_val)

    sample_mean_m = sum(terminal_m) / n_paths
    sample_var_m = sum((x - sample_mean_m) ** 2 for x in terminal_m) / (n_paths - 1)
    se_mean = math.sqrt(sample_var_m / n_paths)
    se_var = math.sqrt(2.0 * (sample_var_m**2) / (n_paths - 1))

    print(f"simulated paths (SIMULATED): {n_paths}, horizon H: {horizon:.2f}, intensity: {lam:.2f}")
    print(f"theoretical X moments: mean = {theoretical_mean_x:.6f}, variance = {theoretical_var_x:.6f}")
    print(f"compensated process M_H sample mean: {sample_mean_m:.6f} (se {se_mean:.6f})")
    print(f"compensated process M_H sample variance: {sample_var_m:.6f} (se {se_var:.6f})")
    print("martingale zero-mean condition inside 3*se:", abs(sample_mean_m) <= 3.0 * se_mean)
    print(
        "variance identity inside 3*se:",
        abs(sample_var_m - theoretical_var_x) <= 3.0 * se_var,
    )


main()
