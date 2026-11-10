"""Lab FI4-L02-1: Secured Overnight Financing Rate (SOFR) calculation methodology.

Implements the New York Fed volume-weighted median algorithm across simulated
tri-party, GCF, and bilateral cleared Treasury repo transactions.
"""

from __future__ import annotations

import random
from typing import NamedTuple


class RepoTrade(NamedTuple):
    rate_pct: float
    volume_millions: float
    segment: str


def compute_volume_weighted_percentiles(trades: list[RepoTrade], percentiles: list[float]) -> dict[float, float]:
    """Compute volume-weighted percentiles (including 50th for SOFR).

    Sorts trades by rate in ascending order, calculates cumulative volume,
    and returns the interest rate where cumulative volume crosses each percentile.
    """
    sorted_trades = sorted(trades, key=lambda t: t.rate_pct)
    total_volume = sum(t.volume_millions for t in sorted_trades)

    results: dict[float, float] = {}
    for p in percentiles:
        threshold = total_volume * (p / 100.0)
        cum_vol = 0.0
        selected_rate = sorted_trades[-1].rate_pct
        for t in sorted_trades:
            cum_vol += t.volume_millions
            if cum_vol >= threshold:
                selected_rate = t.rate_pct
                break
        results[p] = selected_rate
    return results


def main() -> None:
    # SIMULATED transaction dataset representing one business day across three repo segments
    rng = random.Random(42)

    segments = ["Tri-party", "GCF Repo", "FICC DVP Bilateral"]
    trades: list[RepoTrade] = []

    # Generate 15 representative transaction clusters
    base_rates = [4.30, 4.31, 4.32, 4.33, 4.33, 4.34, 4.34, 4.35, 4.35, 4.36, 4.37, 4.38, 4.40, 4.45, 4.50]
    for rate in base_rates:
        vol = round(rng.uniform(25_000, 120_000), 2)  # $25B to $120B per bucket
        seg = rng.choice(segments)
        trades.append(RepoTrade(rate_pct=rate, volume_millions=vol, segment=seg))

    total_volume = sum(t.volume_millions for t in trades)
    vw_mean = sum(t.rate_pct * t.volume_millions for t in trades) / total_volume

    percentiles = compute_volume_weighted_percentiles(trades, [25.0, 50.0, 75.0])
    sofr_rate = percentiles[50.0]
    p25_rate = percentiles[25.0]
    p75_rate = percentiles[75.0]

    print("SOFR Daily Calculation Summary (SIMULATED Market Day):")
    print(f"  Total Eligible Volume: ${total_volume:,.2f} million (${total_volume / 1_000:,.2f} billion)")
    print(f"  Total Transaction Count: {len(trades)} trade clusters")
    print("\nBenchmark Rates:")
    print(f"  Volume-Weighted Median (SOFR): {sofr_rate:.3f}%")
    print(f"  25th Percentile: {p25_rate:.3f}%")
    print(f"  75th Percentile: {p75_rate:.3f}%")
    print(f"  Interquartile Range: {p75_rate - p25_rate:.3f}% ({(p75_rate - p25_rate) * 100:.1f} bps)")
    print(f"  Volume-Weighted Mean: {vw_mean:.4f}%")

    print("\nVolume Breakdown by Segment:")
    for seg in segments:
        seg_vol = sum(t.volume_millions for t in trades if t.segment == seg)
        seg_share = seg_vol / total_volume
        print(f"  {seg:20s}: ${seg_vol:,.2f}M ({seg_share:.1%})")


main()
