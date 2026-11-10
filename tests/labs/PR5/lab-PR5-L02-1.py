"""Lab PR5-L02-1: Grossman-Zhou Drawdown-Constrained Cushion Policy.

SIMULATED: Dynamic portfolio simulation under pathwise maximum drawdown constraint.
"""

from __future__ import annotations

import math

import numpy as np


def simulate_grossman_zhou_policy(
    alpha: float = 0.85,
    mu: float = 0.10,
    r: float = 0.02,
    sigma: float = 0.20,
    m_multiplier: float = 2.5,
    t_years: float = 1.0,
    n_steps: int = 252,
    n_paths: int = 2000,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Simulate Grossman-Zhou cushion policy versus unconstrained Merton policy."""
    rng = np.random.default_rng(seed)
    dt = t_years / float(n_steps)
    sqrt_dt = math.sqrt(dt)

    # Pre-generate standard normal innovations
    z = rng.standard_normal((n_paths, n_steps))

    # Risky asset return increments: dS/S = mu*dt + sigma*sqrt(dt)*z
    r_risky = mu * dt + sigma * sqrt_dt * z
    r_rf = r * dt

    # Path arrays for Grossman-Zhou
    w_gz = np.ones((n_paths, n_steps + 1))
    m_gz = np.ones((n_paths, n_steps + 1))

    # Path arrays for Unconstrained Merton (constant fraction f* = (mu-r)/sigma^2)
    f_merton = (mu - r) / (sigma**2)  # 2.0
    w_merton = np.ones((n_paths, n_steps + 1))
    m_merton = np.ones((n_paths, n_steps + 1))

    for t in range(n_steps):
        # 1. Grossman-Zhou step
        cushion = np.maximum(0.0, w_gz[:, t] - alpha * m_gz[:, t])
        # Risky dollar allocation pi = m_multiplier * cushion
        dollar_risky_gz = np.minimum(w_gz[:, t], m_multiplier * cushion)
        dollar_rf_gz = w_gz[:, t] - dollar_risky_gz
        w_next_gz = dollar_rf_gz * (1.0 + r_rf) + dollar_risky_gz * (1.0 + r_risky[:, t])
        w_gz[:, t + 1] = np.maximum(alpha * m_gz[:, t] * 0.9999, w_next_gz)
        m_gz[:, t + 1] = np.maximum(m_gz[:, t], w_gz[:, t + 1])

        # 2. Unconstrained Merton step
        dollar_risky_merton = f_merton * w_merton[:, t]
        dollar_rf_merton = (1.0 - f_merton) * w_merton[:, t]
        w_merton[:, t + 1] = dollar_rf_merton * (1.0 + r_rf) + dollar_risky_merton * (1.0 + r_risky[:, t])
        m_merton[:, t + 1] = np.maximum(m_merton[:, t], w_merton[:, t + 1])

    # Compute drawdowns D(t) = 1 - W(t)/M(t)
    dd_gz = (m_gz - w_gz) / m_gz
    mdd_gz = np.max(dd_gz, axis=1)
    min_ratio_gz = np.min(w_gz / m_gz, axis=1)

    dd_merton = (m_merton - w_merton) / m_merton
    mdd_merton = np.max(dd_merton, axis=1)
    min_ratio_merton = np.min(w_merton / m_merton, axis=1)

    results = {
        "Grossman-Zhou": {
            "mean_terminal": float(np.mean(w_gz[:, -1])),
            "median_terminal": float(np.median(w_gz[:, -1])),
            "max_mdd": float(np.max(mdd_gz)),
            "mean_mdd": float(np.mean(mdd_gz)),
            "floor_breach_rate": float(np.mean(min_ratio_gz < alpha - 1e-4)),
            "min_ratio": float(np.min(min_ratio_gz)),
        },
        "Unconstrained Merton": {
            "mean_terminal": float(np.mean(w_merton[:, -1])),
            "median_terminal": float(np.median(w_merton[:, -1])),
            "max_mdd": float(np.max(mdd_merton)),
            "mean_mdd": float(np.mean(mdd_merton)),
            "floor_breach_rate": float(np.mean(min_ratio_merton < alpha - 1e-4)),
            "min_ratio": float(np.min(min_ratio_merton)),
        },
    }

    return results


def main() -> None:
    alpha = 0.85
    sim = simulate_grossman_zhou_policy(alpha=alpha, seed=42)

    print(f"Grossman-Zhou Floor Protection vs Unconstrained Merton (Floor alpha={alpha:.2f}):")
    print("=" * 72)
    print(f"{'Policy':<22} {'Mean W_T':<12} {'Median W_T':<12} {'Max MDD':<10} {'Mean MDD':<10} {'Breach Rate':<12}")
    print("-" * 72)

    for policy, r in sim.items():
        print(
            f"{policy:<22} {r['mean_terminal']:<12.4f} {r['median_terminal']:<12.4f} "
            f"{r['max_mdd']:<10.4f} {r['mean_mdd']:<10.4f} {r['floor_breach_rate']:<12.4f}"
        )


main()
