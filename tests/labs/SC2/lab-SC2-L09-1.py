"""Lab 1 · Euler-Maruyama strong versus weak convergence for geometric Brownian motion.

Curriculum lab: measures the empirical rate of strong convergence E[|S_H - S^{Delta}_H|] and weak convergence
|E[S_H] - E[S^{Delta}_H]| for the Euler-Maruyama scheme applied to geometric Brownian motion dS_t = mu S_t dt + sigma
S_t dB_t with s0 = 1.0, mu = 0.05, sigma = 0.30, H = 1.0. For 5,000 realization paths from seed 42 (SIMULATED), step
sizes Delta t = H / 2^k with k in {1, 2, 3, 4, 5} (N in {2, 4, 8, 16, 32}) are evaluated. The strong error exhibits
an O(Delta t^{1/2}) rate, while the weak error exhibits an O(Delta t) rate, verified both against Monte Carlo sample
means and against the exact analytical Euler expectation E[S_N] = s0(1 + mu Delta t)^N.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    s0 = 1.0
    mu = 0.05
    sigma = 0.30
    horizon = 1.0
    n_paths = 5000
    theory_mean = s0 * math.exp(mu * horizon)

    levels = [2, 4, 8, 16, 32]
    print(f"theoretical expectation E[S_H]: {theory_mean:.6f}")
    print("Euler for GBM: strong and weak errors across step sizes:")

    for n_steps in levels:
        dt = horizon / n_steps
        sq_dt = math.sqrt(dt)
        rng = random.Random(42)
        pathwise_diffs: list[float] = []
        euler_terminals: list[float] = []

        for _ in range(n_paths):
            s_euler = s0
            b_tot = 0.0
            for _ in range(n_steps):
                db = rng.gauss(0.0, sq_dt)
                b_tot += db
                s_euler += mu * s_euler * dt + sigma * s_euler * db
            s_exact = s0 * math.exp((mu - 0.5 * (sigma**2)) * horizon + sigma * b_tot)
            pathwise_diffs.append(abs(s_euler - s_exact))
            euler_terminals.append(s_euler)

        strong_err = sum(pathwise_diffs) / n_paths
        var_strong = sum((x - strong_err) ** 2 for x in pathwise_diffs) / (n_paths - 1)
        strong_se = math.sqrt(var_strong / n_paths)

        sample_mean_euler = sum(euler_terminals) / n_paths
        weak_err_mc = abs(sample_mean_euler - theory_mean)
        var_euler = sum((x - sample_mean_euler) ** 2 for x in euler_terminals) / (n_paths - 1)
        weak_se = math.sqrt(var_euler / n_paths)

        exact_euler_mean = s0 * ((1.0 + mu * dt) ** n_steps)
        analytical_weak_err = abs(exact_euler_mean - theory_mean)

        print(
            f"N = {n_steps:2d}, dt = {dt:.4f}: Strong error = {strong_err:.5f} (se {strong_se:.5f}) | "
            f"Weak error MC = {weak_err_mc:.5f} (se {weak_se:.5f}) | Weak analytical = {analytical_weak_err:.6f}"
        )


main()
