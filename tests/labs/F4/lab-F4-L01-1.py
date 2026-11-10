"""Lab F4-L01-1: Asymmetric Optionality and Momentum Crash Betas.

Demonstrates the Daniel & Moskowitz (2016) optionality model: past losers
exhibit dramatic beta surges during market rebounds following bear market states,
driving negative momentum beta asymmetry and catastrophic tail drawdowns.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    n_months = 240
    dt = 1.0 / 12.0

    # Simulate market returns with normal periods and one severe panic rebound
    mkt = rng.normal(0.08 * dt, 0.15 * np.sqrt(dt), size=n_months)
    # Month 100 to 118: Bear market (2-year cumulative drop)
    mkt[100:119] = -0.04 + rng.normal(0.0, 0.03, size=19)
    # Month 119: Violent rebound (+15% market surge)
    mkt[119] = 0.15

    # Trailing 24-month cumulative market return to identify bear market states
    cum_mkt_24m = np.zeros(n_months)
    for t in range(24, n_months):
        cum_mkt_24m[t] = np.sum(mkt[t - 24 : t])

    # Winners and Losers beta dynamics
    # In normal states: beta_W ~ 1.05, beta_L ~ 1.15
    # In panic rebound (cum_24m < 0 and mkt > 0): beta_W ~ 0.88, beta_L ~ 3.25 (call optionality)
    beta_winner = np.full(n_months, 1.05)
    beta_loser = np.full(n_months, 1.15)

    is_bear = cum_mkt_24m < 0.0
    is_up_mkt = mkt > 0.0
    is_panic_rebound = is_bear & is_up_mkt

    beta_winner[is_panic_rebound] = 0.88
    beta_loser[is_panic_rebound] = 3.25

    ret_winner = beta_winner * mkt + rng.normal(0.005, 0.02, size=n_months)
    ret_loser = beta_loser * mkt + rng.normal(-0.005, 0.03, size=n_months)
    ret_wml = ret_winner - ret_loser

    # Compute empirical betas across market regimes
    # 1. Bull / Normal Up-market days
    norm_up = (~is_bear) & is_up_mkt
    cov_w_norm = np.cov(ret_winner[norm_up], mkt[norm_up])[0, 1] / np.var(mkt[norm_up])
    cov_l_norm = np.cov(ret_loser[norm_up], mkt[norm_up])[0, 1] / np.var(mkt[norm_up])
    cov_wml_norm = cov_w_norm - cov_l_norm

    # 2. Panic Rebound days (Bear market up-turns)
    cov_w_panic = np.cov(ret_winner[is_panic_rebound], mkt[is_panic_rebound])[0, 1] / np.var(mkt[is_panic_rebound])
    cov_l_panic = np.cov(ret_loser[is_panic_rebound], mkt[is_panic_rebound])[0, 1] / np.var(mkt[is_panic_rebound])
    cov_wml_panic = cov_w_panic - cov_l_panic

    # Crash month 119 specifics
    crash_ret_w = ret_winner[119]
    crash_ret_l = ret_loser[119]
    crash_ret_wml = ret_wml[119]

    print("=== DANIEL & MOSKOWITZ (2016) ASYMMETRIC BETA REGRESSION ===")
    print(f"Normal Up-Market Beta:  Winner={cov_w_norm:.2f}, Loser={cov_l_norm:.2f}, WML={cov_wml_norm:.2f}")
    print(f"Panic Rebound Beta:     Winner={cov_w_panic:.2f}, Loser={cov_l_panic:.2f}, WML={cov_wml_panic:.2f}")
    print("--- Crash Episode (Month 119 Rebound: Market +15.0%) ---")
    print(f"Past Winners Return:    {crash_ret_w:+.2%}")
    print(f"Past Losers Return:     {crash_ret_l:+.2%}")
    print(f"Momentum (WML) Return:  {crash_ret_wml:+.2%}")


main()
