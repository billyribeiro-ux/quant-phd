"""Lab F1-L01-1: CRSP & Compustat Point-in-Time Merging Simulator.

Demonstrates point-in-time linking discipline and Fama-French June portfolio
formation rules to prevent look-ahead bias in cross-sectional asset pricing.
"""

from __future__ import annotations

import numpy as np


def simulate_point_in_time_merge(seed: int = 42) -> dict[str, float | int]:
    """Simulate point-in-time matching of accounting data with market prices.

    Fama-French (1992, 1993) convention:
    - Fiscal year t-1 ends in Dec (or any month of calendar year t-1).
    - SEC 10-K filing deadline historically was 90 days after fiscal year-end.
    - Portfolio formation occurs at the end of June of year t.
    - Book Equity (BE) from fiscal year t-1 is matched with Market Equity (ME)
      from December of calendar year t-1 to compute Book-to-Market (BE/ME).
    - Portfolio weights use Market Equity from June of year t.
    """
    rng = np.random.default_rng(seed)
    n_firms = 50

    # Simulate true fundamentals for fiscal year t-1 (Dec 31, t-1)
    true_book_equity = rng.lognormal(mean=5.0, sigma=0.8, size=n_firms)
    dec_market_equity = true_book_equity * np.exp(rng.normal(0.0, 0.4, size=n_firms))

    # Filing lag: number of days between fiscal year end and public filing
    # Historical median ~75-80 days; some late filers take 120-150 days
    filing_lags_days = rng.integers(low=45, high=160, size=n_firms)

    # In June of year t (~180 days after Dec 31):
    # Stocks with filing lag <= 180 days have known accounting data by June
    available_in_june = filing_lags_days <= 181
    pct_available_june = float(np.mean(available_in_june) * 100.0)

    # Stocks with filing lag <= 31 days (if formed in January, lookahead bias!)
    available_in_jan = filing_lags_days <= 31
    pct_available_jan = float(np.mean(available_in_jan) * 100.0)

    # Calculate Book-to-Market ratio using December t-1 Market Equity
    bm_ratio = true_book_equity / dec_market_equity
    median_bm = float(np.median(bm_ratio))

    # Market Equity growth from Dec t-1 to June t
    growth = np.exp(rng.normal(0.04, 0.12, size=n_firms))
    june_market_equity = dec_market_equity * growth

    return {
        "n_firms": n_firms,
        "pct_available_jan": pct_available_jan,
        "pct_available_june": pct_available_june,
        "median_bm": round(median_bm, 4),
        "mean_me_dec": round(float(np.mean(dec_market_equity)), 2),
        "mean_me_june": round(float(np.mean(june_market_equity)), 2),
    }


def main() -> None:
    print("Lab F1-L01-1 | CRSP & Compustat Point-in-Time Merging Simulator")
    print("----------------------------------------------------------------")
    res = simulate_point_in_time_merge(seed=42)
    print(f"Total simulated firms:                  {res['n_firms']}")
    print(f"Filing availability in January (Day 31): {res['pct_available_jan']:.1f}%")
    print(f"Filing availability in June (Day 181):    {res['pct_available_june']:.1f}%")
    print(f"Sample median Book-to-Market ratio:     {res['median_bm']:.4f}")
    print(f"Mean Market Equity at Dec t-1 ($M):     {res['mean_me_dec']:.2f}")
    print(f"Mean Market Equity at June t ($M):      {res['mean_me_june']:.2f}")


main()
