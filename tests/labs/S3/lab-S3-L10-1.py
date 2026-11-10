"""Lab S3-L10-1: Markov-switching models and the Hamilton filter.

Exact for stationary regime distribution; SIMULATED for empirical state
frequencies and Hamilton filter regime classification accuracy.
"""

from __future__ import annotations

import math
import random


def normal_pdf(x: float, mean: float, std: float) -> float:
    """Compute univariate normal probability density."""
    diff = (x - mean) / std
    return (1.0 / (math.sqrt(2.0 * math.pi) * std)) * math.exp(-0.5 * diff * diff)


def main() -> None:
    # 2-state Markov chain transition matrix:
    # P = [[p11, p12], [p21, p22]] = [[0.90, 0.10], [0.20, 0.80]]
    p11, p12 = 0.90, 0.10
    p21, p22 = 0.20, 0.80

    # Exact stationary distribution:
    # pi1 = p21 / (p12 + p21) = 0.20 / 0.30 = 2/3
    pi1_theo = p21 / (p12 + p21)
    pi2_theo = p12 / (p12 + p21)
    duration_1 = 1.0 / p12
    duration_2 = 1.0 / p21

    print("Part 1: Exact Markov Chain Stationary Properties:")
    print(f"  Regime 1 stationary probability pi1: {pi1_theo:.6f} (2/3)")
    print(f"  Regime 2 stationary probability pi2: {pi2_theo:.6f} (1/3)")
    print(f"  Expected duration in Regime 1:      {duration_1:.1f} periods (1/p12)")
    print(f"  Expected duration in Regime 2:      {duration_2:.1f} periods (1/p21)")

    # Part 2: Seeded simulation and Hamilton filter
    rng = random.Random(42)
    n = 3000
    mu1, mu2 = 2.0, -2.0
    sigma = 1.0

    states: list[int] = []
    observations: list[float] = []
    state = 1 if rng.random() < pi1_theo else 2

    for _ in range(n):
        if state == 1:
            state = 1 if rng.random() < p11 else 2
        elif rng.random() >= p22:
            state = 1
        else:
            state = 2
        states.append(state)
        mean_obs = mu1 if state == 1 else mu2
        observations.append(rng.gauss(mean_obs, sigma))

    emp_pi1 = sum(1 for s in states if s == 1) / n
    emp_pi2 = 1.0 - emp_pi1

    # Hamilton filter recursion
    xi_filtered: list[float] = []
    xi_curr = pi1_theo
    correct_classifications = 0

    for t in range(n):
        # 1. Prediction step
        xi_pred = p11 * xi_curr + p21 * (1.0 - xi_curr)

        # 2. Update step
        lik1 = normal_pdf(observations[t], mu1, sigma)
        lik2 = normal_pdf(observations[t], mu2, sigma)
        numerator = xi_pred * lik1
        denominator = numerator + (1.0 - xi_pred) * lik2
        xi_curr = numerator / denominator if denominator > 0.0 else 0.5
        xi_filtered.append(xi_curr)

        inferred = 1 if xi_curr > 0.5 else 2
        if inferred == states[t]:
            correct_classifications += 1

    accuracy = correct_classifications / n

    print("\nPart 2: Seeded Hamilton Filter Performance (T=3000, seed=42):")
    print(f"  Empirical frequency Regime 1: {emp_pi1:.4f} (theoretical: {pi1_theo:.4f})")
    print(f"  Empirical frequency Regime 2: {emp_pi2:.4f} (theoretical: {pi2_theo:.4f})")
    print(f"  Filter regime classification accuracy: {accuracy:.4%}")
    print(f"  First 5 filtered probabilities P(S_t=1|Y_t): {[round(p, 4) for p in xi_filtered[:5]]}")


main()
