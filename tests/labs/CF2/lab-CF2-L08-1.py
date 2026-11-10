"""CF2 lab L08-1: Market timing in capital structure.

SIMULATED: Market-to-book ratios and operating requirements are generated
from a seeded stochastic process. No real company data is used.
Demonstrates the Baker & Wurgler (2002) mechanism:
  Firms issue equity when market valuations (M/B) are high, and debt when M/B is low.
  Shows that historical timing shocks produce persistent divergences in capital structure.
"""

from __future__ import annotations

import random

SEED = 20261110


def main() -> None:
    print("CF2 Lab L08-1: Market Timing and Leverage Persistence (SIMULATED)")
    print("----------------------------------------------------------------")

    rng = random.Random(SEED)
    n_years = 10
    mb_threshold = 1.35

    # Initial book values
    init_debt = 50.0  # $50M
    init_equity = 50.0  # $50M

    # Generate synthetic M/B path with swings
    mb_ratios: list[float] = []
    mb_current = 1.40
    for _ in range(n_years):
        shock = rng.gauss(0.0, 0.35)
        # AR(1) process around mean 1.50
        mb_current = 0.60 * mb_current + 0.40 * 1.50 + shock
        mb_ratios.append(round(max(0.80, mb_current), 2))

    # Annual funding need
    annual_funding = 15.0  # $15M external capital needed each year

    # Strategy A: Market-timing policy
    debt_timing = init_debt
    equity_timing = init_equity
    lev_timing: list[float] = []

    # Strategy B: Benchmark constant-mix policy (50% debt, 50% equity)
    debt_bench = init_debt
    equity_bench = init_equity
    lev_bench: list[float] = []

    print(f"Initial capital: Debt = ${init_debt:.1f}M, Equity = ${init_equity:.1f}M (Leverage = 50.0%)")
    print(f"Market-timing rule: Issue equity if M/B > {mb_threshold:.2f}, else issue debt.")
    print("\nYearly Simulation:")
    hdr = (
        f"{'Yr':>3} | {'M/B':>5} | {'Decision':>12} | {'Timing Lev (%)':>15} | "
        f"{'Benchmark Lev (%)':>18} | {'Gap (%)':>8}"
    )
    print(hdr)
    print("-" * 72)

    for t in range(n_years):
        mb = mb_ratios[t]

        # Timing strategy
        if mb > mb_threshold:
            # Issue equity
            equity_timing += annual_funding
            action = "Issued Equity"
        else:
            # Issue debt
            debt_timing += annual_funding
            action = "Issued Debt"

        # Benchmark strategy
        debt_bench += 0.50 * annual_funding
        equity_bench += 0.50 * annual_funding

        curr_lev_timing = debt_timing / (debt_timing + equity_timing)
        curr_lev_bench = debt_bench / (debt_bench + equity_bench)

        lev_timing.append(curr_lev_timing)
        lev_bench.append(curr_lev_bench)

        gap = curr_lev_timing - curr_lev_bench
        print(
            f"{t + 1:3d} | {mb:5.2f} | {action:>12} | {curr_lev_timing * 100:14.2f}% | "
            f"{curr_lev_bench * 100:17.2f}% | {gap * 100:7.2f}%"
        )

    print("-" * 72)
    print("Year 10 Capital Structures:")
    print(
        f"  Market Timer: Debt = ${debt_timing:.1f}M, Equity = ${equity_timing:.1f}M, Leverage = {lev_timing[-1]:.2%}"
    )
    print(f"  Benchmark:    Debt = ${debt_bench:.1f}M, Equity = ${equity_bench:.1f}M, Leverage = {lev_bench[-1]:.2%}")
    shift_pct = abs(lev_timing[-1] - lev_bench[-1])
    print(
        f"Demonstration: Market timing during high-valuation years shifts Year 10 leverage by "
        f"{shift_pct:.2%} (from 50.00% to {lev_timing[-1]:.2%})."
    )


main()
