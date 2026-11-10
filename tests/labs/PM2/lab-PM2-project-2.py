"""PM2 project lab 2 (rung 2, completion): Anti-dilution formula and residual allocation.

SIMULATED: A Series B down-round anti-dilution calculation and residual waterfall allocation.
Standard library, NumPy, and SciPy only; fully deterministic.
"""

from __future__ import annotations


def main() -> None:
    # 1. Broad-Based Weighted Average Anti-Dilution
    old_conv_price = 2.00
    down_issue_price = 1.00
    investment_b = 6_000_000.0
    fd_pre = 12_000_000.0  # Common + options + Series A pre-round

    new_shares = investment_b / down_issue_price
    hypothetical_shares = investment_b / old_conv_price
    adjusted_conv_price = old_conv_price * (fd_pre + hypothetical_shares) / (fd_pre + new_shares)
    conversion_ratio = old_conv_price / adjusted_conv_price

    print(f"Adjusted Conversion Price: ${adjusted_conv_price:.4f}")
    print(f"Adjusted Conversion Ratio: {conversion_ratio:.4f}")

    # 2. Exit Waterfall Residual Allocation
    # Exit value = $60.0M. Total liquidation preference paid = $20.0M. Residual = $40.0M.
    # Series A converts to common; Series B is non-participating and takes $10.0M preference.
    residual_proceeds = 40_000_000.0
    founders_shares = 8_000_000.0
    options_shares = 2_000_000.0
    series_a_shares = 2_500_000.0 * conversion_ratio

    total_common_pool = founders_shares + options_shares + series_a_shares
    payout_founders = residual_proceeds * (founders_shares / total_common_pool)
    payout_series_a = residual_proceeds * (series_a_shares / total_common_pool)

    print(f"Founders Payout: ${payout_founders / 1e6:.2f}M")
    print(f"Series A Payout (Converted): ${payout_series_a / 1e6:.2f}M")


main()
