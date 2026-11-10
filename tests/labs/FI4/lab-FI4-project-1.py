"""Lab FI4-project-1: Plumbing monitor worked example (Rung 1).

A fully worked implementation of the money-market plumbing monitor.
Tracks bank reserves, ON RRP balances, TGA cash, overnight repo spreads,
and 10Y swap spreads from simulated public series.
"""

from __future__ import annotations

from typing import Any, NamedTuple


class SnapshotInput(NamedTuple):
    date: str
    res: float
    rrp: float
    tga: float
    sofr: float
    iorb: float
    ust10: float
    sw10: float


def analyze_plumbing_snapshot(
    date: str,
    reserves_bil: float,
    on_rrp_bil: float,
    tga_bil: float,
    sofr_pct: float,
    iorb_pct: float,
    treasury_10y_pct: float,
    swap_10y_pct: float,
) -> dict[str, Any]:
    """Compute plumbing indicators and status flags for a single market date."""
    # Reserve adequacy indicator: Total liquidity cushion = Reserves + ON RRP
    total_liquidity_cushion = reserves_bil + on_rrp_bil

    # Repo corridor spread: SOFR - IORB (in basis points)
    # Positive spread indicates secured cash scarcity; negative indicates cash abundance
    repo_spread_bps = (sofr_pct - iorb_pct) * 100.0

    # 10Y Swap spread: Swap rate minus Treasury yield (in basis points)
    swap_spread_bps = (swap_10y_pct - treasury_10y_pct) * 100.0

    # Regime classification based on plumbing mechanics
    if repo_spread_bps > 10.0:
        regime = "Funding Stress (Repo Spike)"
    elif total_liquidity_cushion < 2500.0:
        regime = "Scarce Reserves Caution"
    elif swap_spread_bps < -25.0:
        regime = "Balance Sheet Dislocation (SLR Bound)"
    else:
        regime = "Abundant Reserves (Orderly)"

    return {
        "date": date,
        "reserves_bil": reserves_bil,
        "on_rrp_bil": on_rrp_bil,
        "tga_bil": tga_bil,
        "total_liquidity_cushion": total_liquidity_cushion,
        "repo_spread_bps": repo_spread_bps,
        "swap_spread_bps": swap_spread_bps,
        "regime": regime,
    }


def main() -> None:
    # 5-day simulated plumbing time series across an emerging stress episode
    data = [
        SnapshotInput(
            date="2026-03-02", res=3200.0, rrp=1100.0, tga=650.0, sofr=4.30, iorb=4.40, ust10=4.20, sw10=4.05
        ),
        SnapshotInput(date="2026-03-09", res=3050.0, rrp=950.0, tga=780.0, sofr=4.35, iorb=4.40, ust10=4.25, sw10=4.02),
        SnapshotInput(date="2026-03-16", res=2800.0, rrp=700.0, tga=920.0, sofr=4.48, iorb=4.40, ust10=4.35, sw10=3.95),
        SnapshotInput(date="2026-03-17", res=2650.0, rrp=450.0, tga=950.0, sofr=4.65, iorb=4.40, ust10=4.42, sw10=3.90),
        SnapshotInput(date="2026-03-18", res=2400.0, rrp=200.0, tga=980.0, sofr=5.10, iorb=4.40, ust10=4.50, sw10=3.80),
    ]

    print("Money-Market Plumbing Monitor — Time Series (SIMULATED):")
    print(
        f"{'Date':<11s} {'Reserves':<10s} {'ON RRP':<9s} {'TGA':<8s} "
        f"{'Liquidity':<11s} {'Repo Sprd':<11s} {'Swap Sprd':<11s} {'Plumbing Regime'}"
    )

    for row in data:
        snap = analyze_plumbing_snapshot(
            date=row.date,
            reserves_bil=row.res,
            on_rrp_bil=row.rrp,
            tga_bil=row.tga,
            sofr_pct=row.sofr,
            iorb_pct=row.iorb,
            treasury_10y_pct=row.ust10,
            swap_10y_pct=row.sw10,
        )
        print(
            f"{snap['date']} "
            f"${snap['reserves_bil']:>6.0f}B    "
            f"${snap['on_rrp_bil']:>5.0f}B  "
            f"${snap['tga_bil']:>5.0f}B  "
            f"${snap['total_liquidity_cushion']:>7.0f}B    "
            f"{snap['repo_spread_bps']:>+6.1f} bps   "
            f"{snap['swap_spread_bps']:>+6.1f} bps   "
            f"{snap['regime']}"
        )


main()
