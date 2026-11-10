"""Lab GM3-project-1: Rung 1 Worked Example — In-Sample Pre-FOMC Drift Estimation.

SIMULATED: Calculates in-sample (1994-2011) pre-FOMC equity drift, Sharpe ratio,
and non-parametric placebo permutation distribution on a deterministic fixture.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_days = 4500  # 18 in-sample years
    n_events = 144

    # Background daily equity returns (standard deviation 100 bps)
    daily_returns_bps = rng.normal(3.0, 100.0, size=n_days)

    # Event indices approximately every 31 days
    event_indices = np.array([25 + i * 31 for i in range(n_events)], dtype=int)

    # Inject Lucca & Moench (2015) pre-FOMC drift on day t-1: mean ~ +50 bps
    drift_draws = rng.normal(50.5, 25.0, size=n_events)
    daily_returns_bps[event_indices - 1] += drift_draws

    # Pre-FOMC drift on day t-1
    drift_returns = daily_returns_bps[event_indices - 1]

    mean_drift = float(np.mean(drift_returns))
    std_drift = float(np.std(drift_returns, ddof=1))
    t_stat = mean_drift / (std_drift / math.sqrt(n_events))
    sharpe = (mean_drift / std_drift) * math.sqrt(8.0)
    win_rate = float(np.mean(drift_returns > 0.0))

    # Placebo permutation test
    excluded = set()
    for idx in event_indices:
        for offset in range(-2, 3):
            excluded.add(idx + offset)

    valid_pool = np.array([t for t in range(2, n_days - 2) if t not in excluded], dtype=int)
    n_sims = 1000
    placebo_means = np.zeros(n_sims)
    for s in range(n_sims):
        chosen = rng.choice(valid_pool, size=n_events, replace=False)
        placebo_means[s] = float(np.mean(daily_returns_bps[chosen - 1]))

    p_val_placebo = float(np.sum(np.abs(placebo_means) >= abs(mean_drift))) / float(n_sims)

    print("In-Sample FOMC Announcements:", n_events)
    print("Mean Pre-FOMC Drift (bps):", round(mean_drift, 4))
    print("Pre-FOMC Std Deviation (bps):", round(std_drift, 4))
    print("Pre-FOMC t-statistic:", round(t_stat, 4))
    print("Annualized Strategy Sharpe:", round(sharpe, 4))
    print("Win Rate (%):", round(win_rate * 100.0, 4))
    print("Placebo Permutation p-value:", round(p_val_placebo, 4))


main()
