"""Lab F1-L02-1: Survivorship Bias & Database Inclusion Rules Simulator.

Quantifies the phantom alpha induced by backtesting strategies on surviving-only
firm panels versus complete survivor-unbiased universes with default events.
"""

from __future__ import annotations

import numpy as np


def simulate_survivorship_bias(
    n_firms: int = 400,
    n_years: int = 10,
    seed: int = 101,
) -> dict[str, float]:
    """Simulate equity return dynamics with default hazard and measure survivorship bias."""
    rng = np.random.default_rng(seed)

    # Base annual parameters
    mu_healthy = 0.09
    sigma_healthy = 0.20
    hazard_base = 0.035  # ~3.5% baseline annual distress default hazard

    # Track returns across all firms and surviving firms
    # Each row is a firm, columns are years 1..T
    returns = np.zeros((n_firms, n_years), dtype=np.float64)
    active = np.ones(n_firms, dtype=bool)
    survived_full_sample = np.ones(n_firms, dtype=bool)

    for y in range(n_years):
        # Draw healthy returns
        r_draws = rng.normal(mu_healthy, sigma_healthy, size=n_firms)

        # Draw default shocks for active firms
        # Under distress (large negative return), default hazard spikes
        hazard_prob = np.where(r_draws < -0.20, hazard_base * 4.0, hazard_base)
        defaults = (rng.uniform(size=n_firms) < hazard_prob) & active

        for i in range(n_firms):
            if not active[i]:
                # Firm already defunct
                returns[i, y] = np.nan
            elif defaults[i]:
                # Terminal bankruptcy return (severe wipeout, -80%)
                returns[i, y] = -0.80
                active[i] = False
                survived_full_sample[i] = False
            else:
                returns[i, y] = r_draws[i]

    # Universe 1: Complete unbiased sample (all firm-year observations when active)
    valid_mask = np.isfinite(returns)
    unbiased_mean = float(np.mean(returns[valid_mask]))
    unbiased_vol = float(np.std(returns[valid_mask], ddof=1))
    unbiased_sr = unbiased_mean / unbiased_vol if unbiased_vol > 0 else 0.0

    # Universe 2: Survivorship-biased sample (only firms that survived all T years)
    survivors_returns = returns[survived_full_sample]
    biased_mean = float(np.mean(survivors_returns))
    biased_vol = float(np.std(survivors_returns, ddof=1))
    biased_sr = biased_mean / biased_vol if biased_vol > 0 else 0.0

    phantom_alpha = biased_mean - unbiased_mean
    survival_rate = float(np.mean(survived_full_sample) * 100.0)

    return {
        "survival_rate_pct": round(survival_rate, 2),
        "unbiased_mean_pct": round(unbiased_mean * 100.0, 2),
        "biased_mean_pct": round(biased_mean * 100.0, 2),
        "phantom_alpha_pct": round(phantom_alpha * 100.0, 2),
        "unbiased_sr": round(unbiased_sr, 4),
        "biased_sr": round(biased_sr, 4),
    }


def main() -> None:
    print("Lab F1-L02-1 | Survivorship Bias & Database Inclusion Simulator")
    print("----------------------------------------------------------------")
    res = simulate_survivorship_bias(n_firms=400, n_years=10, seed=101)
    print(f"Ten-year firm survival rate:            {res['survival_rate_pct']:.2f}%")
    print(f"Unbiased full-universe mean return:     {res['unbiased_mean_pct']:.2f}% p.a.")
    print(f"Survivorship-biased mean return:        {res['biased_mean_pct']:.2f}% p.a.")
    print(f"Phantom alpha (survivorship wedge):     +{res['phantom_alpha_pct']:.2f}% p.a.")
    print(f"Unbiased Sharpe ratio:                  {res['unbiased_sr']:.4f}")
    print(f"Biased Sharpe ratio:                    {res['biased_sr']:.4f}")


main()
