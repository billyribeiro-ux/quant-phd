"""Lab PR3-L01-1: Discrete Kelly Criterion and Growth Rate Maximization.

SIMULATED: Monte Carlo evaluation of geometric compounding under Kelly sizing.
"""

from __future__ import annotations

import numpy as np


def run_betting_simulation(
    p: float,
    b: float,
    fractions: list[float],
    n_tosses: int = 500,
    n_paths: int = 1000,
    seed: int = 42,
) -> dict[float, dict[str, float]]:
    """Simulate repeated coin tossing across multiple bet fractions."""
    rng = np.random.default_rng(seed)
    results: dict[float, dict[str, float]] = {}

    # Pre-generate Bernoulli outcomes: 1 with prob p, 0 with prob 1-p
    outcomes = rng.random((n_paths, n_tosses)) < p

    for f in fractions:
        # Multipliers: (1 + b * f) on win, (1 - f) on loss
        multipliers = np.where(outcomes, 1.0 + b * f, 1.0 - f)
        # Check for non-positive wealth (ruin)
        if np.any(multipliers <= 0):
            ruined = True
            log_returns = np.zeros(n_paths)
            terminal_wealth = np.zeros(n_paths)
        else:
            ruined = False
            log_mults = np.log(multipliers)
            log_terminal = np.sum(log_mults, axis=1)
            terminal_wealth = np.exp(log_terminal)
            log_returns = log_terminal / float(n_tosses)

        median_w = float(np.median(terminal_wealth)) if not ruined else 0.0
        mean_log_g = float(np.mean(log_returns)) if not ruined else -np.inf
        ruin_rate = float(np.mean(terminal_wealth < 1e-4)) if not ruined else 1.0

        # Theoretical expected log growth rate: p * ln(1 + b*f) + (1-p) * ln(1 - f)
        q = 1.0 - p
        theo_g = p * np.log(1.0 + b * f) + q * np.log(1.0 - f) if 0.0 <= f < 1.0 else -np.inf

        results[f] = {
            "median_wealth": median_w,
            "mean_log_g": mean_log_g,
            "theo_g": float(theo_g),
            "ruin_rate": ruin_rate,
        }

    return results


def main() -> None:
    p = 0.55
    b = 1.0
    q = 1.0 - p
    f_star = (b * p - q) / b  # 0.10

    fractions = [0.025, 0.05, f_star, 0.20, 0.25]
    sim = run_betting_simulation(p, b, fractions, n_tosses=500, n_paths=1000, seed=42)

    print(f"Discrete Kelly Simulation (p={p:.2f}, b={b:.2f}, f*={f_star:.3f}):")
    print(f"{'Fraction':<10} {'Median Wealth':<15} {'Realized g':<12} {'Theoretical g':<15} {'Ruin Prob':<10}")
    print("-" * 65)

    for f in fractions:
        r = sim[f]
        print(
            f"{f:<10.3f} {r['median_wealth']:<15.2f} {r['mean_log_g']:<12.5f} "
            f"{r['theo_g']:<15.5f} {r['ruin_rate']:<10.4f}"
        )


main()
