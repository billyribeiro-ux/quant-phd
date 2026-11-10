"""Lab FC3-L02-1: Sharpe's arithmetic of active management, simulated.

SIMULATED exact Fraction arithmetic on a market universe verifying that
before costs the active group matches the passive group, and after costs
underperforms by exactly the expense gap.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    """Demonstrate Sharpe (1991) arithmetic of active management exactly."""
    # SIMULATED: Market of 4 assets with market capitalizations ($M)
    caps = [Fraction(150), Fraction(250), Fraction(350), Fraction(250)]
    total_wealth = sum(caps)  # 1000
    market_weights = [c / total_wealth for c in caps]

    # Gross asset returns for the period
    asset_returns = [Fraction(14, 100), Fraction(9, 100), Fraction(4, 100), Fraction(-3, 100)]

    # Market portfolio return
    r_market = sum(w * r for w, r in zip(market_weights, asset_returns, strict=True))

    # Passive investors hold 35% of total wealth in index proportions
    theta = Fraction(35, 100)
    passive_wealth = theta * total_wealth
    active_wealth = (1 - theta) * total_wealth

    # Passive holdings: exactly market weights
    passive_holdings = [theta * c for c in caps]
    r_passive_gross = sum(h * r for h, r in zip(passive_holdings, asset_returns, strict=True)) / passive_wealth

    # Active holdings: market clearing implies Active = Total - Passive = (1 - theta) * Total
    active_holdings = [caps[j] - passive_holdings[j] for j in range(len(caps))]
    r_active_gross = sum(h * r for h, r in zip(active_holdings, asset_returns, strict=True)) / active_wealth

    # Cost schedules: passive 10 bps (0.10%), active 120 bps (1.20%)
    cost_passive = Fraction(1, 1000)
    cost_active = Fraction(12, 1000)

    r_passive_net = r_passive_gross - cost_passive
    r_active_net = r_active_gross - cost_active
    net_shortfall = r_passive_net - r_active_net
    cost_diff = cost_active - cost_passive

    print(f"Market return: {float(r_market):.6f} ({r_market})")
    print(f"Passive gross return: {float(r_passive_gross):.6f} ({r_passive_gross})")
    print(f"Active gross return: {float(r_active_gross):.6f} ({r_active_gross})")
    print(f"Gross difference (active - passive): {float(r_active_gross - r_passive_gross):.6f}")
    print(f"Passive net return: {float(r_passive_net):.6f} ({r_passive_net})")
    print(f"Active net return: {float(r_active_net):.6f} ({r_active_net})")
    print(f"Net shortfall (passive - active): {float(net_shortfall):.6f} ({net_shortfall})")
    print(f"Cost difference (c_act - c_pass): {float(cost_diff):.6f} ({cost_diff})")
    print(f"Arithmetic identity verified: {net_shortfall == cost_diff}")


main()
