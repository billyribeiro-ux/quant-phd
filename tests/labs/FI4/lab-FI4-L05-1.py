"""Lab FI4-L05-1: Swap spread mechanics and balance-sheet funded arbitrage limits.

Calculates term swap spreads and models why negative swap spreads persist when
holding cash Treasuries incurs binding Supplementary Leverage Ratio equity costs.
"""

from __future__ import annotations

from typing import NamedTuple


class TermPoint(NamedTuple):
    tenor_years: int
    treasury_yield_pct: float
    swap_rate_pct: float

    @property
    def swap_spread_bps(self) -> float:
        """Swap spread in basis points: (Swap Rate - Treasury Yield) * 10,000."""
        return (self.swap_rate_pct - self.treasury_yield_pct) * 100.0


def main() -> None:
    # SIMULATED term structure of Treasury par yields and SOFR fixed swap rates
    curve = [
        TermPoint(tenor_years=2, treasury_yield_pct=4.60, swap_rate_pct=4.52),
        TermPoint(tenor_years=5, treasury_yield_pct=4.30, swap_rate_pct=4.15),
        TermPoint(tenor_years=10, treasury_yield_pct=4.25, swap_rate_pct=4.02),
        TermPoint(tenor_years=30, treasury_yield_pct=4.55, swap_rate_pct=4.10),
    ]

    print("Term Structure of Swap Spreads (SIMULATED):")
    print(f"  {'Tenor':<8s} {'Treasury Yield':<16s} {'SOFR Swap Rate':<16s} {'Swap Spread':<15s}")
    for pt in curve:
        print(
            f"  {pt.tenor_years:>2d}Y     {pt.treasury_yield_pct:>6.2f}%          "
            f"{pt.swap_rate_pct:>6.2f}%          {pt.swap_spread_bps:>+6.1f} bps"
        )

    # Focus on 30-Year Negative Swap Spread: -45.0 bps
    pt30 = curve[3]
    pt30.treasury_yield_pct - pt30.swap_rate_pct  # +0.45% = +45 bps
    trade_notional_usd = 100_000_000  # $100M notional

    print("\nClassical 'Arbitrage' Trade on 30Y Spread (Receive Treasury, Pay Swap):")
    print(f"  Long $100M 30Y Treasury:   Receive {pt30.treasury_yield_pct:.2f}% fixed")
    print(f"  Pay Fixed 30Y SOFR Swap:   Pay     {pt30.swap_rate_pct:.2f}% fixed, Receive SOFR")
    print(f"  Finance Treasury via Repo: Pay     SOFR + 10 bps ({0.10:.2f}%) overnight repo")
    net_carry_bps = (pt30.treasury_yield_pct - pt30.swap_rate_pct) * 100.0 - 10.0
    gross_annual_pnl = trade_notional_usd * (net_carry_bps / 10_000.0)
    print(f"  Net Annual Carry Spread:   {net_carry_bps:+.1f} bps")
    print(f"  Gross Annual Cash PnL:     ${gross_annual_pnl:,.2f}")

    # Balance Sheet Capital Cost under Supplementary Leverage Ratio (SLR)
    slr_equity_weight = 0.05  # 5% Tier 1 capital allocated against $100M Treasury asset
    allocated_equity = trade_notional_usd * slr_equity_weight  # $5,000,000 equity
    cost_of_equity = 0.12  # 12.0% required return on bank capital
    annual_capital_hurdle = allocated_equity * cost_of_equity

    economic_profit = gross_annual_pnl - annual_capital_hurdle
    roe = gross_annual_pnl / allocated_equity

    print("\nRegulatory Capital Friction (SLR Impact):")
    print(f"  Treasury On-Balance-Sheet Asset: ${trade_notional_usd:,.0f}")
    print(f"  Tier 1 Equity Allocated (5% SLR): ${allocated_equity:,.0f}")
    print(f"  Annual Cost of Capital (12% ROE): ${annual_capital_hurdle:,.2f}")
    print(f"  Return on Allocated Equity (ROE): {roe:.2%}")
    print(f"  Net Economic Profit (EVA):        ${economic_profit:,.2f}")
    viability_str = (
        "Profitable" if economic_profit > 0 else "Unviable (Negative spread persists due to SLR balance sheet cost)"
    )
    print(f"  Arbitrage Viability:              {viability_str}")


main()
