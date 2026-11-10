"""Lab GM5-L03-1: Currency Peg Abandonment & Speculative Attack Dynamics.

Simulates the Krugman (1979) and Obstfeld (1996) speculative attack framework,
modeling reserve depletion, shadow exchange rates, and post-abandonment jumps.
"""

from __future__ import annotations

import math
from typing import Any


def simulate_speculative_attack(
    peg_rate: float,
    initial_reserves: float,
    domestic_credit_growth: float,
    money_demand_semi_elasticity: float,
    speculative_capital_flow_rate: float,
    n_days: int = 60,
) -> dict[str, Any]:
    """Simulate central bank reserve depletion and shadow exchange rate dynamics.

    Parameters
    ----------
    peg_rate : float
        Fixed exchange rate parity (e.g. 1.20 CHF per EUR or GBP parity).
    initial_reserves : float
        Foreign exchange reserves in billions USD.
    domestic_credit_growth : float
        Daily domestic credit expansion rate (driving fundamental divergence).
    money_demand_semi_elasticity : float
        Interest rate semi-elasticity of money demand (eta).
    speculative_capital_flow_rate : float
        Sensitivity of speculative outflows to shadow exchange rate premium.
    n_days : int
        Simulation horizon in days.

    Returns
    -------
    dict[str, float | int | list[float]]
        Trajectory of reserves, shadow rates, attack day, and de-peg devaluation jump.
    """
    reserves = [initial_reserves]
    shadow_rates = [peg_rate * 0.95]
    realized_rates = [peg_rate]
    attack_day = -1
    peg_intact = True

    current_r = initial_reserves
    domestic_credit = 100.0

    for day in range(1, n_days + 1):
        domestic_credit += domestic_credit_growth

        # Shadow floating rate s_tilde_t = m_t + eta * mu (Krugman 1979)
        # where shadow rate rises as domestic credit expands
        shadow_s = peg_rate * (1.0 + (domestic_credit - 100.0) / 200.0)
        shadow_rates.append(shadow_s)

        if peg_intact:
            # Baseline reserve drain from trade/macro imbalance
            baseline_drain = domestic_credit_growth * 0.40

            # Speculative attack intensity escalates when shadow rate approaches or exceeds peg
            premium = max(0.0, (shadow_s - peg_rate) / peg_rate)
            speculative_drain = speculative_capital_flow_rate * (math.exp(premium * 25.0) - 1.0)
            total_drain = baseline_drain + speculative_drain

            current_r = max(0.0, current_r - total_drain)
            reserves.append(current_r)

            # Central bank abandons peg when reserves breach minimum threshold or speculative flow overwhelms
            if current_r <= 5.0 or total_drain > 15.0:
                peg_intact = False
                attack_day = day
                realized_rates.append(shadow_s)
            else:
                realized_rates.append(peg_rate)
        else:
            # Post-abandonment floating exchange rate tracks shadow rate
            reserves.append(current_r)
            realized_rates.append(shadow_s)

    devaluation_jump_pct = ((realized_rates[attack_day] - peg_rate) / peg_rate) * 100.0 if attack_day > 0 else 0.0

    return {
        "attack_day": attack_day,
        "terminal_reserves": reserves[-1],
        "terminal_exchange_rate": realized_rates[-1],
        "devaluation_jump_pct": devaluation_jump_pct,
        "reserves_trajectory": reserves,
        "realized_rates": realized_rates,
    }


def main() -> None:
    peg = 1.20  # e.g., CHF minimum exchange rate (1.20 per EUR)
    r0 = 100.0  # 100 billion foreign reserves

    results = simulate_speculative_attack(
        peg_rate=peg,
        initial_reserves=r0,
        domestic_credit_growth=0.80,
        money_demand_semi_elasticity=2.5,
        speculative_capital_flow_rate=0.50,
        n_days=45,
    )

    print("Peg Exchange Rate:", round(peg, 4))
    print("Initial Reserves ($B):", round(r0, 1))
    print("Speculative Attack Day:", results["attack_day"])
    print("Terminal Reserves ($B):", round(float(results["terminal_reserves"]), 2))
    print("Terminal Exchange Rate:", round(float(results["terminal_exchange_rate"]), 4))
    print("Devaluation Jump (%):", round(float(results["devaluation_jump_pct"]), 2))


main()
