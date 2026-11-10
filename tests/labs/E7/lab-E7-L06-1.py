"""Lab E7-L06-1: QE Transmission Channels: Portfolio Balance vs Signalling.

Decomposes Treasury and agency yields around quantitative easing announcements
into distinct transmission channels per Krishnamurthy & Vissing-Jorgensen (2011):
1. Signalling channel: captured by short-to-medium Fed funds futures and OIS rate declines
2. Portfolio-balance / duration risk channel: maturity-gradient yield declines
3. Safety / scarcity premium channel: CDS and Treasury-agency spread adjustments
"""

from __future__ import annotations


def decompose_qe_event_window(
    yield_change_10y_treasury_bps: float,  # Total 10-year Treasury yield change
    yield_change_2y_treasury_bps: float,  # 2-year yield change (proxy for policy expectations)
    yield_change_10y_agency_bps: float,  # 10-year Agency debt yield change
    term_premium_loading_ratio: float,  # Relative duration loading of 10y vs 2y (e.g. 10y duration / 2y duration)
) -> dict[str, float]:
    """Decompose total yield change into Signalling, Duration Risk, and Safety/Scarcity components."""
    # Under Krishnamurthy-Vissing-Jorgensen (2011):
    # 2y yield is predominantly driven by policy expectations / signalling:
    signalling_component = yield_change_2y_treasury_bps

    # The duration risk / portfolio balance component impacts 10y beyond 2y:
    duration_portfolio_balance = (yield_change_10y_treasury_bps - signalling_component) * (
        1.0 - (1.0 / term_premium_loading_ratio)
    )

    # Safety premium is reflected in the relative Treasury-Agency spread change:
    # Treasuries carry a unique safe-asset convenience yield that rises when Treasury supply shrinks
    safety_spread_change = yield_change_10y_treasury_bps - yield_change_10y_agency_bps

    residual_liquidity = yield_change_10y_treasury_bps - signalling_component - duration_portfolio_balance

    return {
        "total_change_bps": yield_change_10y_treasury_bps,
        "signalling_bps": signalling_component,
        "portfolio_balance_bps": duration_portfolio_balance,
        "safety_premium_bps": safety_spread_change,
        "residual_liquidity_bps": residual_liquidity,
    }


def main() -> None:
    # Representative calibration for QE1 announcement (November 2008 / March 2009)
    # Total 10y yield drop of ~100 bps
    dy_10y = -107.0
    dy_2y = -35.0
    dy_agency = -135.0
    duration_ratio = 4.5  # 10y duration ~ 8.5 vs 2y duration ~ 1.9

    decomp = decompose_qe_event_window(dy_10y, dy_2y, dy_agency, duration_ratio)

    print("QE Announcement Yield Decomposition (Krishnamurthy-Vissing-Jorgensen 2011):")
    print(f"  Total 10Y Treasury yield change: {decomp['total_change_bps']:.1f} bps")
    print("\nChannel Decomposition:")
    sig_share = decomp["signalling_bps"] / decomp["total_change_bps"]
    pb_share = decomp["portfolio_balance_bps"] / decomp["total_change_bps"]
    print(f"  1. Signalling channel:          {decomp['signalling_bps']:.1f} bps ({sig_share:.1%})")
    print(f"  2. Portfolio-balance (duration):{decomp['portfolio_balance_bps']:.1f} bps ({pb_share:.1%})")
    print(f"  3. Safety/Scarcity channel:     {decomp['safety_premium_bps']:.1f} bps (Agency spread expansion)")
    print(f"  4. Residual liquidity channel:  {decomp['residual_liquidity_bps']:.1f} bps")


main()
