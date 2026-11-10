"""Lab AP6-L05-1: The Inelastic Markets Hypothesis and Aggregate Flow Multiplier.

SIMULATED: Calibrates the Gabaix & Koijen (2021) inelastic markets framework across
US institutional sectors. Calculates aggregate market demand elasticity zeta_m,
derives the aggregate flow multiplier M = 1 / zeta_m, and evaluates market-wide price impact.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # US equity market ownership shares and sectoral demand elasticities
    # Calibrated from Gabaix & Koijen (2021, Table 1 & Table 3)
    # Sectors: Mutual Funds, Pension Funds, Life Insurers, Foreign Investors, Households/Hedge Funds
    sectors = [
        "Mutual Funds",
        "Pension & Retirement Funds",
        "Life Insurers",
        "Foreign Investors",
        "Households & Hedge Funds",
    ]

    # Market shares of equity capitalization (summing to 1.0)
    ownership_shares = np.array([0.22, 0.20, 0.08, 0.16, 0.34])

    # Estimated demand elasticities zeta_i for each institutional sector
    # Institutions with strict mandates or benchmarks (pensions, passive index funds) have near-zero elasticity
    # Active hedge funds and direct households have higher elasticity
    sector_elasticities = np.array([0.25, 0.05, 0.08, 0.30, 0.45])

    # Aggregate market demand elasticity: zeta_m = sum_i (s_i * zeta_i)
    zeta_m = float(np.sum(ownership_shares * sector_elasticities))

    # Gabaix-Koijen aggregate flow multiplier: M = 1 / zeta_m
    flow_multiplier_m = 1.0 / zeta_m

    # Macro price impact of an exogenous institutional inflow:
    # Delta ln(P_market) = M * (Inflow / Total Market Capitalization)
    total_market_cap = 45000.0  # $45 Trillion US equity market
    inflow_amount = 450.0  # $450 Billion exogenous inflow (1% of market cap, e.g. retirement contribution)
    inflow_fraction = inflow_amount / total_market_cap

    delta_log_price = flow_multiplier_m * inflow_fraction
    dollar_wealth_increase = total_market_cap * (np.exp(delta_log_price) - 1.0)
    wealth_multiplier = dollar_wealth_increase / inflow_amount

    # Perfectly elastic baseline (classical finance with zeta -> infinity, M -> 0)

    min_sec = f"{sectors[np.argmin(sector_elasticities)]} ({np.min(sector_elasticities):.2f})"
    max_sec = f"{sectors[np.argmax(sector_elasticities)]} ({np.max(sector_elasticities):.2f})"

    print("Gabaix & Koijen (2021) Inelastic Markets Multiplier Calibration")
    print(f"Number of institutional sectors:   {len(sectors)}")
    print(f"Lowest elasticity sector:          {min_sec}")
    print(f"Highest elasticity sector:         {max_sec}")
    print(f"Aggregate market elasticity zeta:  {zeta_m:.4f}")
    print(f"Aggregate flow multiplier M:       {flow_multiplier_m:.2f}")
    print(f"Exogenous inflow:                  ${inflow_amount:.1f}B ({inflow_fraction * 100:.1f}% of market)")
    print(f"Equilibrium market price impact:   {delta_log_price * 100:.2f}%")
    print(f"Aggregate market value gain:       ${dollar_wealth_increase:.1f}B")
    print(f"Wealth gain per dollar invested:   ${wealth_multiplier:.2f}")
    print(f"Consistent with GK2021 range (3-8): {bool(3.0 <= flow_multiplier_m <= 8.0)}")


main()
