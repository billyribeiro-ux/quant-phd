"""Lab 4 · Variance Gamma path simulation via Gamma subordination versus analytical moments.

Under Madan, Carr & Chang (1998), the Variance Gamma process X_t is obtained by evaluating Brownian motion with
drift theta and volatility sigma at a random time given by an independent Gamma process G_t with mean t and
variance nu * t:
X_t = theta * G_t + sigma * B(G_t),   where G_t ~ Gamma(shape=t/nu, scale=nu).
The analytical moments of X_t are:
E[X_t] = theta * t,
Var(X_t) = (sigma^2 + nu * theta^2) * t.
This lab simulates 10,000 realizations of X_H at horizon H = 0.5 (SIMULATED) using seed 42,
evaluates sample mean, sample variance, and sample skewness, and compares them against theoretical moments
within 3 standard errors.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    seed = 42
    rng = random.Random(seed)

    horizon = 0.5
    sigma = 0.25
    nu = 0.30
    theta = -0.15

    # Theoretical moments
    theo_mean = theta * horizon
    theo_var = (sigma**2 + nu * theta**2) * horizon

    n_paths = 10000
    x_vals: list[float] = []

    for _ in range(n_paths):
        # Sample G ~ Gamma(shape = horizon / nu, scale = nu)
        g = rng.gammavariate(horizon / nu, nu)
        z = rng.gauss(0.0, 1.0)
        x = theta * g + sigma * math.sqrt(g) * z
        x_vals.append(x)

    sample_mean = sum(x_vals) / n_paths
    sample_var = sum((x - sample_mean) ** 2 for x in x_vals) / (n_paths - 1)
    sample_skew = sum((x - sample_mean) ** 3 for x in x_vals) / ((n_paths - 1) * (sample_var**1.5))

    se_mean = math.sqrt(sample_var / n_paths)
    se_var = math.sqrt(2.0 * (sample_var**2) / (n_paths - 1))

    print(f"simulated paths (SIMULATED): {n_paths}, horizon H: {horizon:.2f}")
    print(f"parameters: sigma = {sigma:.2f}, nu = {nu:.2f}, theta = {theta:.2f}")
    print(f"analytical moments: mean = {theo_mean:.6f}, variance = {theo_var:.6f}")
    print(f"sample moments: mean = {sample_mean:.6f} (se {se_mean:.6f})")
    print(f"sample variance = {sample_var:.6f} (se {se_var:.6f})")
    print(f"sample skewness = {sample_skew:.6f}")
    print("mean inside 3*se band:", abs(sample_mean - theo_mean) <= 3.0 * se_mean)
    print("variance inside 3*se band:", abs(sample_var - theo_var) <= 3.0 * se_var)


main()
