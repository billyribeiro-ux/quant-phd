"""Lab SR4-project-1: Project Rung 1 Worked Example.

SIMULATED. Quantitative dealer balance-sheet intermediation cost under the
Supplementary Leverage Ratio (SLR). Computes maximum total leverage exposure,
portfolio allocation, hurdle rate on zero-risk Treasuries, and break-even
market-making bid-ask spreads.
"""

from __future__ import annotations


def calculate_dealer_intermediation(
    equity: float,
    slr_ratio: float,
    non_treasury_assets: float,
    equity_cost_pct: float,
    annual_turnover: float,
) -> dict[str, float]:
    """Calculate dealer Treasury capacity and market-making bid-ask spread requirements."""
    if equity <= 0 or slr_ratio <= 0:
        raise ValueError("equity and SLR ratio must be positive")
    if non_treasury_assets < 0:
        raise ValueError("non-treasury assets cannot be negative")

    # 1. Total Leverage Exposure (TLE) Capacity
    total_capacity = equity / slr_ratio

    # 2. Maximum Treasury Intermediation Capacity
    treasury_capacity = max(0.0, total_capacity - non_treasury_assets)

    # 3. Hurdle rate on balance-sheet expansion:
    # Each $1 of Treasuries requires $slr_ratio of equity.
    # At cost of equity r_e, the required return per dollar of assets is:
    hurdle_rate_bps = slr_ratio * equity_cost_pct * 10000.0  # in basis points (1 bp = 0.0001)

    # 4. Break-even bid-ask spread in market making:
    # If inventory turns over 'annual_turnover' times per year,
    # the required half-spread per turn is hurdle_rate / annual_turnover,
    # so the full round-trip bid-ask spread is 2 * (hurdle_rate / annual_turnover).
    breakeven_spread_bps = (2.0 * hurdle_rate_bps) / annual_turnover if annual_turnover > 0 else 0.0

    return {
        "equity": equity,
        "total_capacity": total_capacity,
        "treasury_capacity": treasury_capacity,
        "hurdle_rate_bps": hurdle_rate_bps,
        "breakeven_spread_bps": breakeven_spread_bps,
    }


def main() -> None:
    # Representative primary dealer instance (SIMULATED)
    equity = 50.0  # $50 billion Tier 1 capital
    slr_ratio = 0.05  # 5.0% enhanced SLR requirement
    non_treasury = 650.0  # $650 billion existing credit and mortgage loans
    equity_cost = 0.12  # 12.0% annual required return on equity
    turnover = 24.0  # 24x annual inventory turnover (holding period ~15 days)

    print("=== PROJECT RUNG 1: WORKED EXAMPLE (SIMULATED) ===")
    print(f"Inputs: Equity = ${equity:.1f}B, SLR = {slr_ratio * 100:.1f}%, Non-Treasury Assets = ${non_treasury:.1f}B")

    res = calculate_dealer_intermediation(
        equity=equity,
        slr_ratio=slr_ratio,
        non_treasury_assets=non_treasury,
        equity_cost_pct=equity_cost,
        annual_turnover=turnover,
    )

    print(f"Step 1: Total Balance-Sheet Capacity (TLE): ${res['total_capacity']:.1f}B")
    print(f"Step 2: Available Treasury Intermediation Capacity: ${res['treasury_capacity']:.1f}B")
    print(f"Step 3: Equity Hurdle Rate on Zero-Risk Treasuries: {res['hurdle_rate_bps']:.2f} bps")
    print(f"Step 4: Break-Even Market-Making Bid-Ask Spread: {res['breakeven_spread_bps']:.3f} bps")


main()
