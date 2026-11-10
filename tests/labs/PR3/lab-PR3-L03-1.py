"""Lab PR3-L03-1: Fractional Kelly Sizing, Volatility Drag, and Drawdown Risk.

SIMULATED: Monte Carlo evaluation of growth-volatility trade-off and drawdown probabilities.
"""

from __future__ import annotations

import numpy as np


def simulate_fractional_kelly(
    c_values: list[float],
    mu: float = 0.10,
    r: float = 0.02,
    sigma: float = 0.20,
    d_threshold: float = 0.50,
    t_years: float = 5.0,
    n_steps: int = 1260,
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[float, dict[str, float]]:
    """Simulate wealth paths under different fractional Kelly multipliers."""
    rng = np.random.default_rng(seed)
    dt = t_years / float(n_steps)
    f_star = (mu - r) / (sigma**2)  # full Kelly leverage
    results: dict[float, dict[str, float]] = {}

    # Common random standard normal increments across fractions
    z = rng.standard_normal((n_paths, n_steps))

    for c in c_values:
        f = c * f_star
        drift = (r + f * (mu - r) - 0.5 * (f**2) * (sigma**2)) * dt
        diff = f * sigma * np.sqrt(dt) * z
        log_increments = drift + diff
        # Prepend zero for initial log wealth
        log_paths = np.column_stack([np.zeros(n_paths), np.cumsum(log_increments, axis=1)])
        wealth_paths = np.exp(log_paths)

        # Track running maximum and drawdowns
        running_max = np.maximum.accumulate(wealth_paths, axis=1)
        drawdown_paths = (running_max - wealth_paths) / running_max
        max_drawdowns = np.max(drawdown_paths, axis=1)

        # Empirical drawdown probability
        emp_dd_prob = float(np.mean(max_drawdowns >= d_threshold))

        # Theoretical asymptotic drawdown probability: (1 - d)^(2/c - 1)
        if 0.0 < c < 2.0:
            theo_dd_prob = float((1.0 - d_threshold) ** ((2.0 / c) - 1.0))
        elif c <= 0.0:
            theo_dd_prob = 0.0
        else:
            theo_dd_prob = 1.0

        # Excess growth rate and volatility
        theo_excess_g = float(c * (mu - r) * f_star - 0.5 * (c**2) * (f_star**2) * (sigma**2))
        realized_g = float(np.median(log_paths[:, -1]) / t_years)
        port_vol = float(f * sigma)

        results[c] = {
            "leverage": float(f),
            "port_vol": port_vol,
            "theo_excess_g": theo_excess_g,
            "realized_g": realized_g,
            "emp_dd_prob": emp_dd_prob,
            "theo_dd_prob": theo_dd_prob,
            "median_max_dd": float(np.median(max_drawdowns)),
        }

    return results


def main() -> None:
    mu = 0.10
    r = 0.02
    sigma = 0.20
    d_target = 0.50  # 50% drawdown
    c_values = [1.0, 0.75, 0.50, 0.25]

    res = simulate_fractional_kelly(
        c_values, mu=mu, r=r, sigma=sigma, d_threshold=d_target, t_years=5.0, n_steps=1260, n_paths=3000, seed=42
    )

    f_star = (mu - r) / (sigma**2)
    max_excess_g = 0.5 * ((mu - r) ** 2) / (sigma**2)

    print(f"Fractional Kelly Analysis (mu={mu:.2f}, r={r:.2f}, sigma={sigma:.2f}, f*={f_star:.2f}):")
    print(f"Max Excess Growth Rate (Full Kelly): {max_excess_g:.4f}\n")
    print(
        f"{'c':<6} {'Lev f':<8} {'Vol':<8} {'% Growth':<10} {'Median MaxDD':<14} "
        f"{'Emp P(DD>=50%)':<16} {'Theo P(DD>=50%)':<16}"
    )
    print("-" * 80)

    for c in c_values:
        d = res[c]
        pct_growth = (d["theo_excess_g"] / max_excess_g) * 100.0
        pct_str = f"{pct_growth:5.1f}%"
        print(
            f"{c:<6.2f} {d['leverage']:<8.2f} {d['port_vol']:<8.3f} {pct_str:<10} "
            f"{d['median_max_dd']:<14.3f} {d['emp_dd_prob']:<16.4f} {d['theo_dd_prob']:<16.4f}"
        )


main()
