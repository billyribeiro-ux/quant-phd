r"""Lab 1 · Merton fraction vs. simulated expected utility.

Simulates CRRA utility of terminal wealth across portfolio allocation fractions pi in [0.0, 1.0],
demonstrating that the sample expected utility peaks exactly at the theoretical Merton fraction
pi* = (mu - r) / (gamma * sigma^2).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Model parameters (SIMULATED)
    seed = 42
    rng = random.Random(seed)

    r = 0.03
    mu = 0.09
    sigma = 0.20
    gamma = 3.0
    t_horiz = 1.0
    w0 = 1.0

    # Theoretical Merton fraction
    pi_star = (mu - r) / (gamma * (sigma**2))
    print(f"theoretical Merton fraction pi*: {pi_star:.4f}")

    n_paths = 30000
    z_draws = [rng.gauss(0.0, 1.0) for _ in range(n_paths)]

    pi_grid = [round(0.1 * i, 2) for i in range(11)]
    results: list[tuple[float, float, float]] = []

    for pi in pi_grid:
        drift = (r + pi * (mu - r) - 0.5 * (pi * sigma) ** 2) * t_horiz
        vol = pi * sigma * math.sqrt(t_horiz)

        sample_utilities: list[float] = []
        for z in z_draws:
            w_t = w0 * math.exp(drift + vol * z)
            u = (w_t ** (1.0 - gamma)) / (1.0 - gamma)
            sample_utilities.append(u)

        mean_u = sum(sample_utilities) / n_paths

        # Exact theoretical expected utility:
        # E[W^(1-gamma)] = exp((1-gamma)*drift + 0.5*(1-gamma)^2 * vol^2)
        exact_exp = math.exp((1.0 - gamma) * drift + 0.5 * ((1.0 - gamma) ** 2) * (vol**2))
        exact_u = exact_exp / (1.0 - gamma)

        results.append((pi, mean_u, exact_u))
        print(f"pi = {pi:4.2f}: sample E[U] = {mean_u:.6f}, exact E[U] = {exact_u:.6f}")

    best_sample_pi = max(results, key=lambda x: x[1])[0]
    best_exact_pi = max(results, key=lambda x: x[2])[0]

    print(f"sample optimal fraction: {best_sample_pi:.2f}")
    print(f"exact analytical optimal fraction: {best_exact_pi:.2f}")
    print(f"sample peak coincides with Merton fraction: {abs(best_sample_pi - pi_star) < 1e-6}")


main()
