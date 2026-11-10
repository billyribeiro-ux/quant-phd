"""Lab 8: Macro and Historical Scenario Stress Testing with Reverse Stress Analysis.

Demonstrates multi-asset crisis scenario stress testing (1987, 1998, 2008, 2020)
and implements reverse stress testing to identify minimum insolvency thresholds.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 4-Asset Multi-Strategy Portfolio: US Equities, Corporate Credit, Treasuries, Commodities
    assets = ["US Equities", "Credit", "Treasuries", "Commodities"]
    weights = np.array([0.40, 0.25, 0.25, 0.10], dtype=np.float64)
    portfolio_value = 10_000_000.0  # $10M baseline equity

    # Historical Macro Shock Vectors (fractional returns)
    scenarios: dict[str, np.ndarray] = {
        "1987 Black Monday": np.array([-0.226, -0.050, 0.030, -0.080]),
        "1998 Russian/LTCM Crisis": np.array([-0.150, -0.120, 0.050, -0.100]),
        "2008 Lehman Bankruptcy": np.array([-0.200, -0.150, 0.080, -0.250]),
        "2020 COVID Liquidity Shock": np.array([-0.250, -0.100, 0.040, -0.350]),
    }

    alloc_dict = {a: f"{w * 100:.1f}%" for a, w in zip(assets, weights, strict=True)}
    print(f"Base Portfolio Value: ${portfolio_value:,.2f}")
    print(f"Asset Allocations: {alloc_dict}")
    print("=" * 70)
    print(f"{'Crisis Scenario':<28} | {'Dollar P&L ($)':<16} | {'Portfolio Return':<16}")
    print("-" * 70)

    for name, shocks in scenarios.items():
        dollar_pnl = float(portfolio_value * np.dot(weights, shocks))
        return_pct = (dollar_pnl / portfolio_value) * 100.0
        print(f"{name:<28} | ${dollar_pnl:14,.2f} | {return_pct:+14.2f}%")

    # Reverse Stress Testing:
    # Find scaling factor k on the 2008 Lehman shock vector that causes a $2,500,000 drawdown
    loss_threshold = 2_500_000.0
    base_lehman_loss = -float(portfolio_value * np.dot(weights, scenarios["2008 Lehman Bankruptcy"]))
    k_star = loss_threshold / base_lehman_loss

    print("=" * 70)
    print(f"Reverse Stress Test Capital Threshold: ${loss_threshold:,.2f}")
    print(f"Base 2008 Lehman Loss:                  ${base_lehman_loss:,.2f}")
    print(f"Required Macro Severity Multiplier k*:  {k_star:.4f}x")
    crit_shocks = {
        a: f"{s * k_star * 100:+.2f}%" for a, s in zip(assets, scenarios["2008 Lehman Bankruptcy"], strict=True)
    }
    print(f"Critical Asset Shock Vector under k*:   {crit_shocks}")


main()
