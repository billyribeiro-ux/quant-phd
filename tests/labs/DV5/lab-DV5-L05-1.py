"""Lab 5 · The February 2018 Short-Volatility Blow-Up (Volmageddon).

This lab simulates the end-of-day rebalancing feedback loop of inverse-VIX
exchange-traded products (XIV, SVXY) on February 5, 2018 (SIMULATED),
demonstrating how one-way futures rebalancing demand in an illiquid market
caused a 115.6% VIX explosion and the terminal liquidation of short-vol ETPs.
"""

from __future__ import annotations


def simulate_volmageddon_rebalancing(
    initial_vix: float,
    vix_fut_price: float,
    inv_etp_aum: float,  # in millions USD
    lev_etp_aum: float,  # in millions USD
    market_depth_lambda: float,  # VIX points per 1,000 futures contracts
    initial_vix_shock: float,
) -> tuple[list[float], list[float], list[float], float]:
    """Iteratively simulate the market-close rebalancing feedback loop."""
    vix_path = [initial_vix]
    fut_path = [vix_fut_price]
    xiv_nav_path = [100.0]  # normalized to 100

    vix_current = initial_vix + initial_vix_shock
    fut_current = vix_fut_price + initial_vix_shock * 0.90
    vix_path.append(vix_current)
    fut_path.append(fut_current)

    # Initial NAV decline
    xiv_ret = -((fut_current - vix_fut_price) / vix_fut_price)
    xiv_nav = max(0.0, 100.0 * (1.0 + xiv_ret))
    xiv_nav_path.append(xiv_nav)

    # Feedback iterations into market close (4:00 PM to 4:15 PM)
    contract_size = 1000.0  # $1,000 per VIX point

    for _ in range(5):
        # 1. Inverse product (-1x): must BUY futures to reduce short exposure
        # Delta Contracts = (AUM / Fut_price) * (Fut_new - Fut_old) / Fut_new
        delta_inv_contracts = (inv_etp_aum * 1e6 / (fut_current * contract_size)) * (
            (fut_current - fut_path[-2]) / fut_path[-2]
        )

        # 2. Leveraged product (+2x): must BUY futures to increase long exposure
        delta_lev_contracts = (lev_etp_aum * 1e6 / (fut_current * contract_size)) * (
            (fut_current - fut_path[-2]) / fut_path[-2]
        )

        total_buy_contracts = delta_inv_contracts + delta_lev_contracts

        # 3. Market price impact
        fut_impact = (total_buy_contracts / 1000.0) * market_depth_lambda
        fut_new = fut_current + fut_impact
        vix_new = vix_current + fut_impact * 1.10

        # Update NAV
        cum_ret = -((fut_new - vix_fut_price) / vix_fut_price)
        xiv_nav = max(0.0, 100.0 * (1.0 + cum_ret))

        vix_path.append(vix_new)
        fut_path.append(fut_new)
        xiv_nav_path.append(xiv_nav)

        fut_current = fut_new
        vix_current = vix_new

        if xiv_nav <= 20.0:
            # 80% intraday loss threshold triggers accelerated termination
            break

    return vix_path, fut_path, xiv_nav_path, total_buy_contracts


def main() -> None:
    print("=== February 5, 2018 'Volmageddon' ETP Liquidation Simulation ===")
    v0 = 17.30
    fut0 = 15.80
    inv_aum = 2200.0  # $2.2B in inverse ETPs (XIV, SVXY)
    lev_aum = 1400.0  # $1.4B in 2x leveraged ETPs (UVXY, TVIX)
    lambda_impact = 0.45  # 0.45 VIX points per 1,000 contracts
    init_shock = 5.20  # initial afternoon market selloff

    print("Pre-Close Market State:")
    print(f"  VIX Baseline:       {v0:.2f}")
    print(f"  VIX Future (1M):    {fut0:.2f}")
    print(f"  Short-Vol ETP AUM:  {inv_aum:.1f} M USD")
    print(f"  2x Long ETP AUM:    {lev_aum:.1f} M USD")
    print(f"  Market Depth:       {lambda_impact:.2f} pts / 1k contracts")

    vix_p, fut_p, nav_p, final_order = simulate_volmageddon_rebalancing(
        v0, fut0, inv_aum, lev_aum, lambda_impact, init_shock
    )

    print("\nEnd-of-Day Feedback Cascade (4:00 PM - 4:15 PM ET):")
    print(" Step |   VIX Index |  VIX Future |   XIV NAV ($) | Drawdown (%) | Status ")
    print("--------------------------------------------------------------------------")
    for step in range(len(vix_p)):
        v = vix_p[step]
        f = fut_p[step]
        nav = nav_p[step]
        dd = 100.0 - nav
        status = "Normal" if nav > 50.0 else ("Severe Distress" if nav > 20.0 else "TERMINATION EVENT")
        print(f"   {step}  |      {v:6.2f} |      {f:6.2f} |        {nav:6.2f} |      {dd:6.2f}% | {status} ")

    print("\nFinal Terminal State:")
    print(f"  VIX Surge:          +{(vix_p[-1] - v0) / v0 * 100.0:.2f}% (from {v0:.2f} to {vix_p[-1]:.2f})")
    print(f"  XIV Terminal Loss:  -{(100.0 - nav_p[-1]):.2f}%")
    print(f"  Cumulative Demand:  {final_order:.0f} VIX futures contracts into the close")


main()
