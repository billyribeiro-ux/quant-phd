"""Lab FI4-project-2: Plumbing monitor completion problem (Rung 2).

Solution twin for the completion problem: implements reserve balance extraction
from central-bank assets and liabilities and computes the 10Y swap spread.
"""

from __future__ import annotations


def compute_reserves_and_spreads(
    total_assets: float,
    currency: float,
    on_rrp: float,
    tga: float,
    other_liab: float,
    swap_10y: float,
    treasury_10y: float,
) -> tuple[float, float]:
    """Compute bank reserves via the balance sheet identity and the 10Y swap spread."""
    # Blank 1 in completion problem: extract bank reserves from central-bank identity
    reserves = total_assets - (currency + on_rrp + tga + other_liab)

    # Blank 2 in completion problem: compute swap spread in basis points
    swap_spread_bps = (swap_10y - treasury_10y) * 100.0

    return reserves, swap_spread_bps


def main() -> None:
    # SIMULATED March 2020 stress snapshot (numbers in USD Billions)
    total_assets = 5_200.0
    currency = 1_850.0
    on_rrp = 250.0
    tga = 480.0
    other_liab = 120.0
    swap_10y = 0.85  # 0.85% SOFR/OIS swap rate
    treasury_10y = 1.15  # 1.15% 10-year Treasury yield

    reserves, swap_spread_bps = compute_reserves_and_spreads(
        total_assets, currency, on_rrp, tga, other_liab, swap_10y, treasury_10y
    )

    print("Completed Plumbing Analysis (SIMULATED Stress State):")
    print(f"  Central Bank Total Assets:    ${total_assets:,.1f}B")
    print(f"  Currency in Circulation:      ${currency:,.1f}B")
    print(f"  ON RRP Facility Balance:      ${on_rrp:,.1f}B")
    print(f"  Treasury General Account:     ${tga:,.1f}B")
    print(f"  Other Liabilities & Capital:  ${other_liab:,.1f}B")
    print(f"  Calculated Bank Reserves:     ${reserves:,.1f}B")
    print(f"  10Y Swap Rate:                {swap_10y:.2f}%")
    print(f"  10Y Treasury Yield:           {treasury_10y:.2f}%")
    print(f"  10Y Swap Spread:              {swap_spread_bps:+.1f} bps")


main()
