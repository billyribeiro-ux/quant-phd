"""Lab 1 · The Ornstein-Uhlenbeck process: transient moments and stationary variance limit.

The Ornstein-Uhlenbeck equation dX_t = kappa(theta - X_t) dt + sigma dB_t with X_0 = x0 has the explicit solution
X_t = x0 e^{-kappa t} + theta(1 - e^{-kappa t}) + sigma int_0^t e^{-kappa(t-s)} dB_s. Its expectation is
x0 e^{-kappa t} + theta(1 - e^{-kappa t}) and its variance is (sigma^2 / (2 kappa))(1 - e^{-2 kappa t}), approaching
the stationary variance sigma^2 / (2 kappa) as t -> infinity. This lab simulates 4,000 paths with x0 = 0.5, kappa = 2.0,
theta = 1.0, sigma = 0.30 from seed 42 (SIMULATED), recording sample statistics at times t in {0.25, 0.50, 1.00, 2.00}
and comparing them against closed-form values and the stationary limit.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    x0 = 0.5
    kappa = 2.0
    theta = 1.0
    sigma = 0.30
    stationary_var = (sigma * sigma) / (2.0 * kappa)

    times = [0.25, 0.50, 1.00, 2.00]
    dt = 0.005
    sq_dt = math.sqrt(dt)
    n_paths = 4000
    seed = 42

    time_steps = {t: round(t / dt) for t in times}
    max_steps = max(time_steps.values())
    samples: dict[float, list[float]] = {t: [] for t in times}

    rng = random.Random(seed)
    for _ in range(n_paths):
        x = x0
        for step in range(1, max_steps + 1):
            db = rng.gauss(0.0, sq_dt)
            x += kappa * (theta - x) * dt + sigma * db
            for t_val, target_step in time_steps.items():
                if step == target_step:
                    samples[t_val].append(x)

    print(f"stationary variance limit: {stationary_var:.6f}")
    for t_val in times:
        exact_mean = x0 * math.exp(-kappa * t_val) + theta * (1.0 - math.exp(-kappa * t_val))
        exact_var = stationary_var * (1.0 - math.exp(-2.0 * kappa * t_val))
        vals = samples[t_val]
        m = sum(vals) / n_paths
        v = sum((y - m) ** 2 for y in vals) / (n_paths - 1)
        se_m = math.sqrt(v / n_paths)
        print(
            f"t = {t_val:.2f}: theory mean {exact_mean:.4f}, sample {m:.4f} (se {se_m:.4f}) | "
            f"theory var {exact_var:.5f}, sample {v:.5f}"
        )


main()
