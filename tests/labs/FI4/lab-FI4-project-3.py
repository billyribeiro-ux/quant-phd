"""Lab FI4-project-3: Rung 3 independent project verification check.

Validates the plumbing monitor against two stylized historical stress episodes:
the September 2019 repo spike and the March 2020 dash for cash.
"""

from __future__ import annotations

from typing import Any


def evaluate_stress_episode(
    episode_name: str,
    reserves_bil: float,
    on_rrp_bil: float,
    tga_bil: float,
    sofr_pct: float,
    iorb_pct: float,
    treasury_10y_pct: float,
    swap_10y_pct: float,
    dealer_equity_bil: float,
    dealer_tle_bil: float,
) -> dict[str, Any]:
    """Evaluate full plumbing metrics for a stress episode."""
    total_liquidity = reserves_bil + on_rrp_bil
    repo_spread_bps = (sofr_pct - iorb_pct) * 100.0
    swap_spread_bps = (swap_10y_pct - treasury_10y_pct) * 100.0
    slr = dealer_equity_bil / dealer_tle_bil if dealer_tle_bil > 0 else float("inf")
    slr_surplus_bil = dealer_equity_bil - 0.05 * dealer_tle_bil

    # Identify primary mechanism driver
    if repo_spread_bps > 50.0 and total_liquidity < 1600.0:
        driver = "Reserve Scarcity & Frictional Bottleneck"
    elif swap_spread_bps < -20.0 and slr < 0.052:
        driver = "Dealer SLR Capacity Exhaustion"
    else:
        driver = "Orderly Liquidity Distribution"

    return {
        "episode": episode_name,
        "total_liquidity": total_liquidity,
        "repo_spread_bps": repo_spread_bps,
        "swap_spread_bps": swap_spread_bps,
        "slr": slr,
        "slr_surplus_bil": slr_surplus_bil,
        "primary_mechanism": driver,
    }


def main() -> None:
    # Episode 1: September 2019 Repo Spike (SIMULATED stylized figures)
    ep1 = evaluate_stress_episode(
        episode_name="September 2019 Repo Spike",
        reserves_bil=1450.0,
        on_rrp_bil=5.0,
        tga_bil=380.0,
        sofr_pct=5.25,
        iorb_pct=2.10,
        treasury_10y_pct=1.80,
        swap_10y_pct=1.75,
        dealer_equity_bil=15.0,
        dealer_tle_bil=260.0,
    )

    # Episode 2: March 2020 Dash for Cash (SIMULATED stylized figures)
    ep2 = evaluate_stress_episode(
        episode_name="March 2020 Dash for Cash",
        reserves_bil=1700.0,
        on_rrp_bil=15.0,
        tga_bil=420.0,
        sofr_pct=1.20,
        iorb_pct=1.10,
        treasury_10y_pct=1.15,
        swap_10y_pct=0.75,
        dealer_equity_bil=15.0,
        dealer_tle_bil=298.0,
    )

    print("Plumbing Monitor Stress Episode Verification (SIMULATED):")
    print("=" * 80)
    for ep in [ep1, ep2]:
        print(f"Episode: {ep['episode']}")
        print(f"  Total Liquidity Cushion (Reserves + RRP): ${ep['total_liquidity']:,.0f}B")
        print(f"  Overnight Repo Spread (SOFR - IORB):      {ep['repo_spread_bps']:+.1f} bps")
        print(f"  10Y Swap Spread (Swap - Treasury):        {ep['swap_spread_bps']:+.1f} bps")
        print(f"  Dealer Supplementary Leverage Ratio (SLR):{ep['slr']:.2%}")
        print(f"  Dealer Capital Surplus over 5% SLR:       ${ep['slr_surplus_bil']:+,.2f}B")
        print(f"  Diagnosed Primary Mechanism:              {ep['primary_mechanism']}")
        print("-" * 80)


main()
