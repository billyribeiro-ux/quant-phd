"""Lab GM3-L05-1: Cross-Asset Execution and Post-FOMC Volatility Crush.

Simulates options volatility surface dynamics around FOMC announcements,
quantifying the pre-announcement volatility premium, the post-announcement
volatility crush, and intraday execution slippage across the 30-minute event window.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    rng = np.random.default_rng(777)
    n_events = 80

    # Underlying S&P 500 index level S0 = 4,000
    s0 = 4000.0

    # Pre-FOMC event implied volatility reflects priced event jump:
    # IV rises from baseline 16% to ~22% annualized ahead of announcement
    iv_pre = rng.normal(0.22, 0.02, size=n_events)
    # Post-announcement IV collapses back to baseline: "volatility crush"
    iv_post = rng.normal(0.155, 0.015, size=n_events)

    # Days to option expiry tau (e.g. 5 trading days = 5/252)
    tau_pre = 5.0 / 252.0
    tau_post = 4.8 / 252.0  # after announcement (intra-day decay)

    # At-the-money (ATM) straddle price approximation (Brenner-Subrahmanyam formula):
    # Straddle ~ S0 * sigma * sqrt(2 * tau / pi) ~ 0.7979 * S0 * sigma * sqrt(tau)
    factor = math.sqrt(2.0 / math.pi)

    straddle_pre = s0 * iv_pre * math.sqrt(tau_pre) * factor
    straddle_post_priced = s0 * iv_post * math.sqrt(tau_post) * factor

    # Actual realized index jump |Delta S| on announcement day
    # Jump drawn from normal with std 1.2% (~48 index points)
    realized_jump = np.abs(rng.normal(0.0, s0 * 0.012, size=n_events))
    mean_realized_move_pct = float(np.mean(realized_jump / s0 * 100.0))

    # Short Straddle PnL (in index points):
    # Premium collected = straddle_pre
    # Terminal value or closeout value after event:
    # If closed immediately post-announcement: PnL = straddle_pre - (straddle_post_priced + slippage)
    # Execution slippage: bid-ask spread widens from normal 0.50 pts to 3.5 pts during announcement
    slippage_pts = rng.uniform(2.5, 4.5, size=n_events)
    short_straddle_pnl = straddle_pre - straddle_post_priced - slippage_pts

    # Statistics
    mean_iv_drop_pct = float(np.mean((iv_pre - iv_post) * 100.0))
    mean_pnl_pts = float(np.mean(short_straddle_pnl))
    win_rate = float(np.mean(short_straddle_pnl > 0.0))
    sharpe_event = (mean_pnl_pts / float(np.std(short_straddle_pnl, ddof=1))) * math.sqrt(8.0)

    # Breakeven move: straddle_pre / S0 in percent
    mean_breakeven_pct = float(np.mean(straddle_pre / s0 * 100.0))

    print("FOMC Option Events Simulated:", n_events)
    print("Mean Pre-FOMC Implied Volatility (%):", round(float(np.mean(iv_pre * 100.0)), 4))
    print("Mean Post-FOMC Implied Volatility (%):", round(float(np.mean(iv_post * 100.0)), 4))
    print("Average Volatility Crush (pct pts):", round(mean_iv_drop_pct, 4))
    print("Average Priced Breakeven Move (%):", round(mean_breakeven_pct, 4))
    print("Average Realized Move (%):", round(mean_realized_move_pct, 4))
    print("Mean Short Straddle PnL (pts):", round(mean_pnl_pts, 4))
    print("Short Straddle Win Rate (%):", round(win_rate * 100.0, 4))
    print("Annualized Strategy Sharpe:", round(sharpe_event, 4))


main()
