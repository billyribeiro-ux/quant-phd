"""Lab PR5-L01-1: Maximum Drawdown Distribution vs Sharpe Ratio.

SIMULATED: Monte Carlo evaluation of Brownian maximum drawdown scaling across Sharpe ratios.
"""

from __future__ import annotations

import math

import numpy as np


def simulate_mdd_distribution(
    sharpe_ratios: list[float],
    sigma: float = 0.20,
    t_years: float = 1.0,
    n_steps: int = 252,
    n_paths: int = 5000,
    seed: int = 42,
) -> dict[float, dict[str, float]]:
    """Simulate maximum drawdown distributions for geometric/arithmetic Brownian motion across Sharpe ratios."""
    rng = np.random.default_rng(seed)
    dt = t_years / float(n_steps)
    sqrt_dt = math.sqrt(dt)

    results: dict[float, dict[str, float]] = {}

    for sr in sharpe_ratios:
        mu = sr * sigma
        # Generate Gaussian increments
        z = rng.standard_normal((n_paths, n_steps))
        # Daily arithmetic log return increments
        dx = (mu - 0.5 * sigma**2) * dt + sigma * sqrt_dt * z
        # Cumulative wealth log-paths
        x = np.cumsum(dx, axis=1)
        # Prepend initial log-wealth 0
        x = np.hstack([np.zeros((n_paths, 1)), x])
        wealth = np.exp(x)

        # Running maximum wealth
        peaks = np.maximum.accumulate(wealth, axis=1)
        # Drawdown process D(t) = 1 - W(t)/M(t)
        drawdowns = (peaks - wealth) / peaks
        # Maximum drawdown per path
        mdds = np.max(drawdowns, axis=1)

        mean_mdd = float(np.mean(mdds))
        median_mdd = float(np.median(mdds))
        p95_mdd = float(np.percentile(mdds, 95))
        prob_exceed_15 = float(np.mean(mdds >= 0.15))
        prob_exceed_25 = float(np.mean(mdds >= 0.25))

        results[sr] = {
            "mean_mdd": mean_mdd,
            "median_mdd": median_mdd,
            "p95_mdd": p95_mdd,
            "prob_exceed_15": prob_exceed_15,
            "prob_exceed_25": prob_exceed_25,
        }

    return results


def main() -> None:
    sigma = 0.20
    t_years = 1.0
    sharpe_ratios = [0.0, 0.5, 1.0, 1.5, 2.0]

    # Theoretical expectation for zero drift Brownian motion (Magdon-Ismail et al. 2004)
    theo_mdd_zero_drift = sigma * math.sqrt(math.pi * t_years / 2.0)

    sim = simulate_mdd_distribution(sharpe_ratios, sigma=sigma, t_years=t_years, seed=42)

    print("Drawdown Distribution vs. Sharpe Ratio (T=1.0 yr, sigma=20.0%):")
    print(f"Magdon-Ismail Zero-Drift Theoretical Expectation: {theo_mdd_zero_drift:.4f}")
    print("=" * 72)
    print(f"{'Sharpe':<8} {'Mean MDD':<12} {'Median MDD':<12} {'95th Pct':<12} {'P(MDD>=15%)':<14} {'P(MDD>=25%)':<12}")
    print("-" * 72)

    for sr in sharpe_ratios:
        r = sim[sr]
        print(
            f"{sr:<8.1f} {r['mean_mdd']:<12.4f} {r['median_mdd']:<12.4f} "
            f"{r['p95_mdd']:<12.4f} {r['prob_exceed_15']:<14.4f} {r['prob_exceed_25']:<12.4f}"
        )


main()
