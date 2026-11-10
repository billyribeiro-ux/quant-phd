"""QR1 Lesson 6 Inline Lab 1: Alternative-data due diligence and survivorship bias.

Demonstrates quantification of survivorship bias in historical cross-sectional panels
by comparing naive survivor-only backtest returns against the comprehensive,
point-in-time constituent panel including delistings and terminal resolution.
Data: SIMULATED corporate panel with performance-correlated distress attrition.
"""

from __future__ import annotations

import random
from typing import NamedTuple


class CompanyHistory(NamedTuple):
    symbol: str
    annual_returns: list[float]  # 5-year trajectory
    delisted_in_year: int | None  # 0 to 4 if delisted, None if survived full horizon
    delisting_return: float | None  # Terminal resolution return


def calculate_compound_annual_return(returns: list[float]) -> float:
    """Calculate geometric compound annual growth rate across the return vector."""
    if not returns:
        return 0.0
    wealth = 1.0
    for r in returns:
        wealth *= 1.0 + r
    return float((wealth ** (1.0 / len(returns))) - 1.0)


def main() -> None:
    rng = random.Random(777)
    n_companies = 40
    n_years = 5

    panel: list[CompanyHistory] = []
    for i in range(n_companies):
        sym = f"EQUITY_{i:02d}"
        returns: list[float] = []
        delisted_year: int | None = None
        delist_ret: float | None = None

        for year in range(n_years):
            # Performance draw with some cross-sectional dispersion
            base_ret = rng.gauss(0.08, 0.20)

            # Distress threshold: severe cumulative underperformance triggers delisting
            if base_ret < -0.30 and delisted_year is None and year >= 1:
                delisted_year = year
                delist_ret = rng.uniform(-0.60, -0.30)  # Severe terminal delisting penalty
                returns.append(delist_ret)
                break
            else:
                returns.append(base_ret)

        panel.append(CompanyHistory(sym, returns, delisted_year, delist_ret))

    survivors = [c for c in panel if c.delisted_in_year is None]
    delisted = [c for c in panel if c.delisted_in_year is not None]

    # 1. Survivor-only annualized portfolio return (naive backward-looking backtest)
    survivor_returns = [calculate_compound_annual_return(c.annual_returns) for c in survivors]
    survivor_mean = sum(survivor_returns) / len(survivor_returns)

    # 2. Survivorship-bias-free panel annualized portfolio return
    # Incorporates every firm for its active lifetime
    full_returns = [calculate_compound_annual_return(c.annual_returns) for c in panel]
    full_panel_mean = sum(full_returns) / len(full_returns)

    survivorship_gap = survivor_mean - full_panel_mean

    print(f"Total initial constituent universe: {len(panel)}")
    print(f"Survivors through year {n_years}: {len(survivors)} ({len(survivors) / len(panel):.1%})")
    print(f"Delisted / distressed firms: {len(delisted)} ({len(delisted) / len(panel):.1%})")

    print("\nEmpirical Return Comparison:")
    print(f"  Survivor-only mean annualized return:       {survivor_mean:+7.2%}")
    print(f"  Point-in-time full-panel mean return:     {full_panel_mean:+7.2%}")
    print(f"  Artificial survivorship alpha distortion: {survivorship_gap:+7.2%}")

    print("\nSample Delisted Entities (omitted from survivor-only backtests):")
    for d in delisted[:4]:
        cum_ret = calculate_compound_annual_return(d.annual_returns)
        term_str = f"{d.delisting_return:+.1%}" if d.delisting_return is not None else "N/A"
        print(f"  {d.symbol}: delisted year {d.delisted_in_year}, terminal ret={term_str}, annualized={cum_ret:+.1%}")

    assert survivorship_gap > 0.0, "Survivorship bias must inflate apparent returns"
    print("\nSurvivorship bias verification: confirmed positive distortion gap.")


main()
