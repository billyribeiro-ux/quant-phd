"""Lab 1 · Geometric Brownian motion: exact closed form versus Euler discretization.

The geometric Brownian motion dS_t = mu S_t dt + sigma S_t dB_t has the exact Itô solution S_t = s0 exp((mu -
sigma^2/2)t + sigma B_t), with mean E[S_t] = s0 exp(mu t). The standard Euler discretization S_{k+1} = S_k(1 + mu
Delta t + sigma Delta B_k) introduces discretization bias on discrete price paths. This lab simulates 5,000 paths on a
50-step grid over [0, 1] with s0 = 100, mu = 0.05, sigma = 0.20 from seed 42 (SIMULATED), comparing exact pathwise
terminals with Euler terminals and verifying the closed-form expectation against Monte Carlo standard error.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    s0 = 100.0
    mu = 0.05
    sigma = 0.20
    horizon = 1.0
    n_steps = 50
    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    n_paths = 5000
    seed = 42

    exact_drift = (mu - 0.5 * sigma * sigma) * dt
    exact_vol = sigma * sq_dt

    rng = random.Random(seed)
    exact_terminals: list[float] = []
    euler_terminals: list[float] = []
    abs_errors: list[float] = []

    for _ in range(n_paths):
        s_exact = s0
        s_euler = s0
        for _ in range(n_steps):
            z = rng.gauss(0.0, 1.0)
            db = sq_dt * z
            s_exact *= math.exp(exact_drift + exact_vol * z)
            s_euler += mu * s_euler * dt + sigma * s_euler * db
        exact_terminals.append(s_exact)
        euler_terminals.append(s_euler)
        abs_errors.append(abs(s_exact - s_euler))

    theory_mean = s0 * math.exp(mu * horizon)
    sample_mean_exact = sum(exact_terminals) / n_paths
    var_exact = sum((x - sample_mean_exact) ** 2 for x in exact_terminals) / (n_paths - 1)
    se_exact = math.sqrt(var_exact / n_paths)

    sample_mean_euler = sum(euler_terminals) / n_paths
    mae = sum(abs_errors) / n_paths

    print(f"theoretical expectation E[S_H]: {theory_mean:.6f}")
    print(f"exact solution sample mean: {sample_mean_exact:.6f} (se {se_exact:.6f})")
    print(f"Euler approximation sample mean: {sample_mean_euler:.6f}")
    print(f"mean absolute pathwise error: {mae:.6f}")
    print("exact sample mean within 5*se of theory:", abs(sample_mean_exact - theory_mean) <= 5.0 * se_exact)


main()
