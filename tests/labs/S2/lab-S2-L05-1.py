"""Lab S2-L05-1: Omitted-variable bias exact formula and Monte Carlo validation.

Evaluates the short-regression slope against beta_1 + beta_2 * delta
on a seeded design under Monte Carlo sampling. Standard library only.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(42)
    n = 100
    replications = 2000

    # True population parameters:
    # y = alpha + beta_1 * x1 + beta_2 * x2 + eps
    alpha = 1.00
    beta1 = 1.50
    beta2 = 2.00

    # Auxiliary relationship: x2 = gamma_0 + delta * x1 + eta
    delta = 0.60
    gamma0 = 0.50

    # Theoretical omitted-variable bias for short regression of y on x1:
    # plim b1_short = beta1 + beta2 * delta = 1.50 + 2.00 * 0.60 = 2.70
    expected_short_b1 = beta1 + beta2 * delta
    theoretical_bias = beta2 * delta

    b1_short_draws: list[float] = []
    b1_long_draws: list[float] = []
    b2_long_draws: list[float] = []
    delta_draws: list[float] = []

    for _ in range(replications):
        # Draw x1
        x1 = [rng.gauss(2.0, 1.5) for _ in range(n)]
        # Draw x2 correlated with x1
        x2 = [gamma0 + delta * xi + rng.gauss(0.0, 1.0) for xi in x1]
        # Draw response y
        eps = [rng.gauss(0.0, 1.2) for _ in range(n)]
        y = [alpha + beta1 * xi1 + beta2 * xi2 + ei for xi1, xi2, ei in zip(x1, x2, eps, strict=True)]

        # 1. Short regression: y on x1
        x1_bar = sum(x1) / n
        y_bar = sum(y) / n
        s_x1x1 = sum((xi - x1_bar) ** 2 for xi in x1)
        s_x1y = sum((xi - x1_bar) * (yi - y_bar) for xi, yi in zip(x1, y, strict=True))
        b1_short = s_x1y / s_x1x1
        b1_short_draws.append(b1_short)

        # 2. Auxiliary regression: x2 on x1
        x2_bar = sum(x2) / n
        s_x1x2 = sum((xi1 - x1_bar) * (xi2 - x2_bar) for xi1, xi2 in zip(x1, x2, strict=True))
        delta_hat = s_x1x2 / s_x1x1
        delta_draws.append(delta_hat)

        # 3. Long regression: y on [x1, x2]
        s_x2x2 = sum((xi - x2_bar) ** 2 for xi in x2)
        s_x2y = sum((xi - x2_bar) * (yi - y_bar) for xi, yi in zip(x2, y, strict=True))

        det = s_x1x1 * s_x2x2 - s_x1x2 * s_x1x2
        b1_long = (s_x2x2 * s_x1y - s_x1x2 * s_x2y) / det
        b2_long = (s_x1x1 * s_x2y - s_x1x2 * s_x1y) / det
        b1_long_draws.append(b1_long)
        b2_long_draws.append(b2_long)

    mean_short = sum(b1_short_draws) / replications
    mean_long1 = sum(b1_long_draws) / replications
    mean_long2 = sum(b2_long_draws) / replications
    mean_delta = sum(delta_draws) / replications

    empirical_bias = mean_short - beta1

    print(f"True beta_1: {beta1:.4f}, True beta_2: {beta2:.4f}, True delta: {delta:.4f}")
    print(f"Theoretical short-regression slope: {expected_short_b1:.4f}")
    print(f"Theoretical omitted-variable bias: {theoretical_bias:.4f}")
    print(f"Empirical mean short slope b1: {mean_short:.4f}")
    print(f"Empirical mean long slope b1: {mean_long1:.4f}")
    print(f"Empirical mean long slope b2: {mean_long2:.4f}")
    print(f"Empirical mean delta: {mean_delta:.4f}")
    print(f"Empirical omitted-variable bias: {empirical_bias:.4f}")


main()
