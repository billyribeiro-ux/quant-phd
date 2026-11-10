"""Lab GM3-project-3: Rung 3 Independent Project — End-to-End Monetary Policy & Drift Evaluation.

SIMULATED: Complete empirical pipeline: Kuttner futures scaling, Bernanke-Kuttner
equity sensitivity regression, in-sample vs out-of-sample drift decay testing,
and non-parametric placebo permutation audits on a synthetic multi-decade fixture.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(101)
    n_days = 7500
    n_events = 240
    n_is = 144
    n_oos = 96

    # Background daily equity returns (standard deviation 100 bps)
    daily_returns_bps = rng.normal(3.0, 100.0, size=n_days)

    # Event indices
    event_indices = np.array([25 + i * 31 for i in range(n_events)], dtype=int)
    is_events = event_indices[:n_is]
    oos_events = event_indices[n_is:]

    # Policy target surprises (bps)
    surprises_bps = rng.normal(0.0, 7.5, size=n_events)
    # Announcement day equity return response (Bernanke & Kuttner 2005: beta ~ -4.7)
    equity_responses_bps = -4.65 * (surprises_bps / 100.0) * 100.0 + rng.normal(0.0, 80.0, size=n_events)
    daily_returns_bps[event_indices] += equity_responses_bps

    # Pre-FOMC drift on day t-1
    # In-sample: mean ~ +49 bps; Out-of-sample: mean ~ +2 bps
    is_drift_draws = rng.normal(49.0, 25.0, size=n_is)
    oos_drift_draws = rng.normal(2.0, 25.0, size=n_oos)
    daily_returns_bps[is_events - 1] += is_drift_draws
    daily_returns_bps[oos_events - 1] += oos_drift_draws

    # 1. Equity sensitivity OLS regression
    x = surprises_bps
    y = daily_returns_bps[event_indices]
    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))
    ss_xx = float(np.sum((x - mean_x) ** 2))
    ss_xy = float(np.sum((x - mean_x) * (y - mean_y)))
    beta = ss_xy / ss_xx
    residuals = y - (mean_y + beta * (x - mean_x))
    se_beta = math.sqrt((float(np.sum(residuals**2)) / (n_events - 2)) / ss_xx)
    t_beta = beta / se_beta

    # 2. In-sample and out-of-sample drift stats
    is_drift = daily_returns_bps[is_events - 1]
    oos_drift = daily_returns_bps[oos_events - 1]

    mu_is = float(np.mean(is_drift))
    std_is = float(np.std(is_drift, ddof=1))
    sharpe_is = (mu_is / std_is) * math.sqrt(8.0)

    mu_oos = float(np.mean(oos_drift))
    std_oos = float(np.std(oos_drift, ddof=1))
    sharpe_oos = (mu_oos / std_oos) * math.sqrt(8.0)

    # 3. Placebo tests
    excluded = set()
    for idx in event_indices:
        for offset in range(-2, 3):
            excluded.add(idx + offset)
    valid_pool = np.array([t for t in range(2, n_days - 2) if t not in excluded], dtype=int)

    n_sims = 500
    is_placebos = np.zeros(n_sims)
    oos_placebos = np.zeros(n_sims)
    for s in range(n_sims):
        ch_is = rng.choice(valid_pool, size=n_is, replace=False)
        is_placebos[s] = float(np.mean(daily_returns_bps[ch_is - 1]))
        ch_oos = rng.choice(valid_pool, size=n_oos, replace=False)
        oos_placebos[s] = float(np.mean(daily_returns_bps[ch_oos - 1]))

    is_p_val = float(np.sum(np.abs(is_placebos) >= abs(mu_is))) / float(n_sims)
    oos_p_val = float(np.sum(np.abs(oos_placebos) >= abs(mu_oos))) / float(n_sims)

    # 4. Decay evaluation
    decay_ratio = mu_oos / mu_is if abs(mu_is) > 1e-12 else 0.0
    se_welch = math.sqrt((std_is**2) / n_is + (std_oos**2) / n_oos)
    welch_t = (mu_oos - mu_is) / se_welch

    se_oos = std_oos / math.sqrt(n_oos)
    t_oos = mu_oos / se_oos
    p_oos = math.erfc(abs(t_oos) / math.sqrt(2.0))
    survived = bool(mu_oos > 0 and p_oos < 0.05)

    print("Total FOMC Announcements:", n_events)
    print("Equity Sensitivity Beta:", round(beta, 4))
    print("Equity Sensitivity t-stat:", round(t_beta, 4))
    print("In-Sample Pre-FOMC Drift (bps):", round(mu_is, 4))
    print("In-Sample Sharpe Ratio:", round(sharpe_is, 4))
    print("In-Sample Placebo p-value:", round(is_p_val, 4))
    print("Out-of-Sample Pre-FOMC Drift (bps):", round(mu_oos, 4))
    print("Out-of-Sample Sharpe Ratio:", round(sharpe_oos, 4))
    print("Out-of-Sample Placebo p-value:", round(oos_p_val, 4))
    print("Decay Ratio (OOS / IS):", round(decay_ratio, 4))
    print("Welch Decay t-statistic:", round(welch_t, 4))
    print("Drift Out-of-Sample Survival:", survived)


main()
