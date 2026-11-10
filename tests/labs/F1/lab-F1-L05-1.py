"""Lab F1-L05-1: NYSE Breakpoints & The Microcap Problem.

Demonstrates that calculating breakpoints on all exchange-listed stocks
causes NASDAQ microcaps to dominate bottom bins, while NYSE breakpoints
preserve cross-sectional stability and prevent microcap contamination.
"""

from __future__ import annotations

import numpy as np


def simulate_nyse_breakpoints(seed: int = 88) -> dict[str, float | int]:
    """Compare all-stock breakpoints versus NYSE breakpoints across exchanges."""
    rng = np.random.default_rng(seed)

    # 1. Simulate cross-section: 100 NYSE firms (large) and 200 NASDAQ firms (skewed microcaps)
    n_nyse = 100
    n_nasdaq = 200
    n_total = n_nyse + n_nasdaq

    nyse_caps = rng.lognormal(mean=8.0, sigma=1.2, size=n_nyse)  # Large cap median ~$3000M
    nasdaq_caps = rng.lognormal(mean=4.2, sigma=1.1, size=n_nasdaq)  # Micro/small cap median ~$65M

    all_caps = np.concatenate([nyse_caps, nasdaq_caps])
    ex_codes = np.concatenate([np.ones(n_nyse, dtype=np.int32), np.full(n_nasdaq, 3, dtype=np.int32)])

    total_market_cap = float(np.sum(all_caps))
    microcap_threshold = float(np.percentile(nyse_caps, 20.0))  # 20th percentile of NYSE ME

    # Aggregate share of microcaps
    microcap_mask = all_caps <= microcap_threshold
    microcap_firm_share = float(np.mean(microcap_mask) * 100.0)
    microcap_cap_share = float((np.sum(all_caps[microcap_mask]) / total_market_cap) * 100.0)

    # 2. Quintile sorting on size using all-stock breakpoints vs NYSE breakpoints
    cuts_all = np.percentile(all_caps, [20.0, 40.0, 60.0, 80.0])
    cuts_nyse = np.percentile(nyse_caps, [20.0, 40.0, 60.0, 80.0])

    q_all = np.digitize(all_caps, cuts_all)
    q_nyse = np.digitize(all_caps, cuts_nyse)

    # Count NASDAQ stocks in the bottom quintile (Q1) under both schemes
    nasdaq_in_q1_all = int(np.sum((q_all == 0) & (ex_codes == 3)))
    nasdaq_in_q1_nyse = int(np.sum((q_nyse == 0) & (ex_codes == 3)))

    total_in_q1_all = int(np.sum(q_all == 0))
    total_in_q1_nyse = int(np.sum(q_nyse == 0))

    pct_nasdaq_q1_all = float(nasdaq_in_q1_all / total_in_q1_all * 100.0)
    pct_nasdaq_q1_nyse = float(nasdaq_in_q1_nyse / total_in_q1_nyse * 100.0)

    return {
        "n_total": n_total,
        "microcap_firm_share_pct": round(microcap_firm_share, 1),
        "microcap_cap_share_pct": round(microcap_cap_share, 2),
        "cut1_all_m": round(float(cuts_all[0]), 1),
        "cut1_nyse_m": round(float(cuts_nyse[0]), 1),
        "pct_nasdaq_q1_all": round(pct_nasdaq_q1_all, 1),
        "pct_nasdaq_q1_nyse": round(pct_nasdaq_q1_nyse, 1),
        "total_in_q1_nyse": total_in_q1_nyse,
    }


def main() -> None:
    print("Lab F1-L05-1 | NYSE Breakpoints & Microcap Problem Simulator")
    print("-------------------------------------------------------------")
    res = simulate_nyse_breakpoints(seed=88)
    print(f"Total listed universe:                  {res['n_total']} firms")
    print(f"Microcaps (<20th pct NYSE) share of firms: {res['microcap_firm_share_pct']:.1f}%")
    print(f"Microcaps share of total market cap:    {res['microcap_cap_share_pct']:.2f}%")
    print(f"Size Q1 breakpoint (All Stocks):        ${res['cut1_all_m']:.1f}M")
    print(f"Size Q1 breakpoint (NYSE Only):         ${res['cut1_nyse_m']:.1f}M")
    print(f"NASDAQ concentration in Q1 (All Cuts):  {res['pct_nasdaq_q1_all']:.1f}%")
    print(f"NASDAQ concentration in Q1 (NYSE Cuts): {res['pct_nasdaq_q1_nyse']:.1f}%")
    print(f"Total firms allocated to Q1 (NYSE):     {res['total_in_q1_nyse']} firms")


main()
