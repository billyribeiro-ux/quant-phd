"""Lab GM3-L02-1: The Pre-FOMC Announcement Drift.

Replicates the Lucca & Moench (2015) empirical event study measuring equity
excess returns in the 24 hours prior to scheduled FOMC announcements,
and executes non-parametric placebo permutation testing.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(101)
    n_days = 4000  # ~16 years (1994 to 2010)
    daily_vol = 0.010  # 1.0% daily standard deviation

    # Background daily equity returns (standard normal innovations)
    daily_returns_pct = rng.normal(0.03, daily_vol * 100.0, size=n_days)

    # 136 scheduled FOMC meetings across 17 years (8 meetings/year)
    meeting_indices_list: list[int] = []
    curr = 25
    while curr < n_days - 10 and len(meeting_indices_list) < 136:
        meeting_indices_list.append(curr)
        curr += int(rng.integers(28, 35))

    meeting_indices = np.array(meeting_indices_list, dtype=int)
    n_events = len(meeting_indices)

    # Inject Lucca & Moench (2015) pre-FOMC drift on day t-1: mean ~ +49 bps (+0.49%)
    drift_draws_pct = rng.normal(0.49, 0.85, size=n_events)
    daily_returns_pct[meeting_indices - 1] += drift_draws_pct

    # Extract observed pre-FOMC returns on day t-1
    fomc_drift_returns_bps = daily_returns_pct[meeting_indices - 1] * 100.0
    mean_drift_bps = float(np.mean(fomc_drift_returns_bps))
    std_drift_bps = float(np.std(fomc_drift_returns_bps, ddof=1))
    se_drift = std_drift_bps / math.sqrt(n_events)
    t_stat_drift = mean_drift_bps / se_drift
    sharpe_annualized = (mean_drift_bps / std_drift_bps) * math.sqrt(8.0)

    # Placebo permutation test: 1,000 simulations
    # Exclude true FOMC days and immediate 2-day buffers
    excluded = set()
    for idx in meeting_indices:
        for offset in range(-2, 3):
            excluded.add(idx + offset)

    valid_placebo_days = np.array([t for t in range(2, n_days - 2) if t not in excluded], dtype=int)
    n_sims = 1000
    placebo_means_bps = np.zeros(n_sims, dtype=np.float64)

    for s in range(n_sims):
        sample_days = rng.choice(valid_placebo_days, size=n_events, replace=False)
        placebo_means_bps[s] = float(np.mean(daily_returns_pct[sample_days - 1] * 100.0))

    p_value_placebo = float(np.sum(np.abs(placebo_means_bps) >= abs(mean_drift_bps))) / float(n_sims)

    print("Scheduled FOMC Meetings Analyzed:", n_events)
    print("Pre-FOMC Mean Drift (bps):", round(mean_drift_bps, 4))
    print("Pre-FOMC Std Deviation (bps):", round(std_drift_bps, 4))
    print("Pre-FOMC t-statistic:", round(t_stat_drift, 4))
    print("Annualized Strategy Sharpe:", round(sharpe_annualized, 4))
    print("Placebo Null Mean (bps):", round(float(np.mean(placebo_means_bps)), 4))
    print("Placebo Empirical p-value:", round(p_value_placebo, 4))


main()
