"""Lab 1 · Milstein scheme versus Euler-Maruyama for multiplicative noise (GBM).

When the diffusion coefficient sigma(X) is state-dependent, the Euler-Maruyama scheme attains only strong order 1/2.
The Milstein scheme incorporates the second-order diffusion correction (1/2) sigma(X_k) sigma'(X_k) ((Delta B_k)^2 -
Delta t), restoring strong order 1. For GBM dS_t = mu S_t dt + sigma S_t dB_t, sigma(S) = sigma S and sigma'(S) = sigma,
so the correction is (1/2) sigma^2 S_k ((Delta B_k)^2 - Delta t). This lab simulates 2,000 paths of GBM with s0 = 1.0,
mu = 0.10, sigma = 0.40 over [0, 1] from seed 42 (SIMULATED), computes terminal RMS error against the exact Itô solution
for step counts N in {4, 8, 16, 32}, prints a sample Milstein correction term, and displays the expanding Euler/Milstein
error ratio.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    s0 = 1.0
    mu = 0.10
    sigma = 0.40
    horizon = 1.0
    n_paths = 2000
    seed = 42

    levels = [4, 8, 16, 32]
    print("Comparing Euler vs Milstein strong error for GBM:")

    for n_steps in levels:
        dt = horizon / n_steps
        sq_dt = math.sqrt(dt)
        rng = random.Random(seed)
        euler_errs: list[float] = []
        milstein_errs: list[float] = []
        sample_correction = 0.0

        for path_idx in range(n_paths):
            s_euler = s0
            s_milstein = s0
            b_tot = 0.0
            for step_idx in range(n_steps):
                db = rng.gauss(0.0, sq_dt)
                b_tot += db
                corr = 0.5 * (sigma**2) * s_milstein * (db * db - dt)
                if path_idx == 0 and step_idx == 0:
                    sample_correction = corr
                s_euler += mu * s_euler * dt + sigma * s_euler * db
                s_milstein += mu * s_milstein * dt + sigma * s_milstein * db + corr

            s_exact = s0 * math.exp((mu - 0.5 * (sigma**2)) * horizon + sigma * b_tot)
            euler_errs.append((s_euler - s_exact) ** 2)
            milstein_errs.append((s_milstein - s_exact) ** 2)

        rms_euler = math.sqrt(sum(euler_errs) / n_paths)
        rms_milstein = math.sqrt(sum(milstein_errs) / n_paths)
        ratio = rms_euler / rms_milstein
        print(
            f"N = {n_steps:2d}, dt = {dt:.4f}: Euler RMS = {rms_euler:.5f}, "
            f"Milstein RMS = {rms_milstein:.5f}, Ratio E/M = {ratio:.2f}"
        )

    print(f"sample initial Milstein correction (path 0, step 0, N=32): {sample_correction:.6e}")


main()
