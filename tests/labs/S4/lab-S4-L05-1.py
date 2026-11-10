"""Lab S4-L05-1: Realized volatility and microstructure noise signature plot.

SIMULATED: simulates high-frequency intraday prices with additive microstructure noise
and computes realized variance at sampling intervals from 5 seconds to 30 minutes.
Demonstrates the volatility signature plot bias: ultra-high frequency sampling is
dominated by noise variance 2*M*sigma_eta^2.
"""

from __future__ import annotations

import math
import random


def simulate_day_path(
    n_seconds: int = 23400, sigma_day: float = 0.015, noise_std: float = 0.0002, seed: int = 42
) -> tuple[list[float], list[float]]:
    """Simulate 1 second diffusion path with additive microstructure noise."""
    rng = random.Random(seed)
    dt = 1.0 / n_seconds
    sigma_step = sigma_day * math.sqrt(dt)

    p_star = [0.0]
    for _ in range(n_seconds):
        p_star.append(p_star[-1] + rng.gauss(0.0, sigma_step))

    p_obs = [p + rng.gauss(0.0, noise_std) for p in p_star]
    return p_star, p_obs


def main() -> None:
    p_star, p_obs = simulate_day_path(seed=42)
    true_iv = sum((p_star[t] - p_star[t - 1]) ** 2 for t in range(1, len(p_star)))

    sampling_intervals = [5, 30, 60, 300, 900, 1800]
    print(f"True Integrated Variance (IV): {true_iv:.6e}")
    print("Interval (s) | Subsamples M | Realized Variance | Relative to IV | Noise Bias")
    print("-" * 75)

    for delta in sampling_intervals:
        sub_prices = p_obs[::delta]
        rv = sum((sub_prices[k] - sub_prices[k - 1]) ** 2 for k in range(1, len(sub_prices)))
        ratio = rv / true_iv
        bias = rv - true_iv
        print(
            f"    {delta:5d}    |     {len(sub_prices) - 1:5d}    |   {rv:.6e}    |     {ratio:.3f}x    | {bias:+.4e}"
        )


main()
