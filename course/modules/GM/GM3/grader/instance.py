"""Instance generator for GM3 project grader.

Generates deterministic, per-seed synthetic macroeconomic panels and asset returns
for high-frequency FOMC event studies and pre-FOMC drift out-of-sample testing.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic synthetic event study instance for seed.

    Parameters
    ----------
    seed : int
        RNG seed derived from learner workspace.

    Returns
    -------
    dict[str, Any]
        Instance dictionary containing daily return series, event dates and indices,
        futures price jumps, calendar scaling parameters, and period splits.
    """
    rng = np.random.default_rng(seed)

    # 30 years of daily trading data: 252 days/yr * 30 = 7,560 days (1994 to 2023)
    n_days = 7560
    base_vol = 0.010  # 1.0% daily volatility (16% annualized)

    # Background daily equity returns with student-t innovations
    df_t = 6
    daily_returns = rng.standard_t(df=df_t, size=n_days) * (base_vol / np.sqrt(df_t / (df_t - 2)))

    # Generate 8 scheduled FOMC meetings per year across 30 years = 240 meetings
    # Spaced approximately every 31 trading days (approx 6 weeks)
    event_indices_list: list[int] = []
    current_idx = 20 + int(rng.integers(5, 15))
    while current_idx < n_days - 20:
        event_indices_list.append(current_idx)
        current_idx += int(rng.integers(28, 35))

    event_indices = np.array(event_indices_list, dtype=int)
    n_events = len(event_indices)

    # Split sample at year 2011 (event ~ 144 out of 240, approx index 4500)
    split_event_idx = 144
    split_day_idx = int(event_indices[split_event_idx])

    # Calendar metadata for Kuttner scaling formula
    days_in_month = rng.choice([28, 30, 31], size=n_events, p=[0.08, 0.35, 0.57])
    # Announcement day of the month d (between 1 and M-2 to avoid pure month-end singularities)
    announcement_days = np.array([int(rng.integers(2, int(m) - 2)) for m in days_in_month], dtype=int)

    # Discrete target surprises Delta i_u in basis points (mean 0, std ~ 8 bps)
    true_surprises_bps = rng.normal(0.0, 8.0, size=n_events)

    # Implied pre-announcement futures rate (%)
    base_funds_rate = 3.5 + rng.normal(0.0, 1.5)
    base_funds_rate = max(0.25, base_funds_rate)
    pre_rates = base_funds_rate + np.cumsum(rng.normal(0.0, 0.05, size=n_events))
    pre_rates = np.maximum(0.10, pre_rates)

    # Derive post-announcement futures rate using inverted Kuttner formula:
    # Delta f = ((M - d) / M) * Delta i_u
    # post_rates = pre_rates + Delta f / 100
    kuttner_factors = days_in_month / (days_in_month - announcement_days)
    futures_jumps_bps = true_surprises_bps / kuttner_factors
    post_rates = pre_rates + (futures_jumps_bps / 100.0)

    # Bernanke & Kuttner (2005) equity sensitivity: beta ~ -4.7 (% return per 100 bps surprise)
    # Since 1% = 100 bps, a -4.7% return = -470 bps. -470 bps / 100 bps = -4.7 bps return per 1 bps surprise.
    beta_equity_bps = -4.7
    equity_event_jumps_bps = beta_equity_bps * true_surprises_bps + rng.normal(0.0, 15.0, size=n_events)

    # In-sample pre-FOMC drift (Lucca & Moench 2015): ~ +49 bps over the 24h prior to announcement
    # Pre-announcement day is t-1
    # Out-of-sample drift: decayed to near zero (~ +4 bps, not statistically significant)
    in_sample_drift_mean_bps = 48.5 + rng.normal(0.0, 3.0)
    out_of_sample_drift_mean_bps = 4.2 + rng.normal(0.0, 2.5)

    for i, idx in enumerate(event_indices):
        is_in_sample = i < split_event_idx
        drift_mean = in_sample_drift_mean_bps if is_in_sample else out_of_sample_drift_mean_bps
        # Inject pre-FOMC drift on day t-1 (in basis points -> fraction)
        drift_return = (drift_mean + rng.normal(0.0, 25.0)) / 10000.0
        daily_returns[idx - 1] = drift_return
        # Inject event response on announcement day t
        daily_returns[idx] += equity_event_jumps_bps[i] / 10000.0

    in_sample_events = event_indices[event_indices < split_day_idx]
    out_of_sample_events = event_indices[event_indices >= split_day_idx]

    return {
        "seed": seed,
        "n_days": n_days,
        "daily_returns": daily_returns,
        "event_indices": event_indices,
        "split_day_idx": split_day_idx,
        "in_sample_events": in_sample_events,
        "out_of_sample_events": out_of_sample_events,
        "pre_rates": pre_rates,
        "post_rates": post_rates,
        "days_in_month": days_in_month,
        "announcement_days": announcement_days,
        "true_surprises_bps": true_surprises_bps,
        "expected_is_drift_bps": float(in_sample_drift_mean_bps),
        "expected_oos_drift_bps": float(out_of_sample_drift_mean_bps),
    }
