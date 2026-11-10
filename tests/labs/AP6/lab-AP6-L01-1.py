"""Lab AP6-L01-1: Performance-Based Arbitrage and Noise Trader Risk.

SIMULATED: Shleifer & Vishny (1997) limits-to-arbitrage model demonstrating that
unfavorable noise trader sentiment shocks trigger fund withdrawals, forcing the
arbitrageur to liquidate positions, thereby widening the mispricing.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    n_steps = 10
    v_fundamental = 100.0  # true fundamental liquidation value

    # State variables
    # Period 0: fundamental value is 100, price is depressed at 90 due to noise trader pessimism
    # Arbitrageur manages AUM F_t = E_t + D_t (equity + debt/client funds)
    p_path = np.zeros(n_steps)
    mispricing = np.zeros(n_steps)
    arb_aum = np.zeros(n_steps)
    arb_position = np.zeros(n_steps)  # number of shares long

    p_path[0] = 90.0
    mispricing[0] = v_fundamental - p_path[0]
    arb_aum[0] = 1000.0  # initial fund assets
    # Arbitrageur invests 100% of capital in underpriced asset: Q_0 = F_0 / P_0
    arb_position[0] = arb_aum[0] / p_path[0]

    # Withdrawal sensitivity parameter: clients withdraw fraction a * (R_fund - R_bench)
    withdrawal_sensitivity = 1.5

    # Simulate sentiment shocks at t = 1, 2 (widening noise trader pessimism), then recovery at t = 5..9
    noise_shock = np.array([0.0, -8.0, -6.0, 2.0, 4.0, 5.0, 5.0, 4.0, 3.0, 1.0])

    for t in range(1, n_steps):
        # Noise trader shock moves price away from fundamental
        # Base price without arbitrageur liquidation
        p_base = p_path[t - 1] + noise_shock[t]

        # Fund performance before client redemptions
        gross_return = p_base / p_path[t - 1]
        pre_redemption_aum = arb_position[t - 1] * p_base

        # Client flow: if fund lost money (gross_return < 1.0), redemptions occur
        flow_rate = withdrawal_sensitivity * min(gross_return - 1.0, 0.0)
        net_redemptions = abs(flow_rate) * pre_redemption_aum

        # Fire sale price impact: selling shares to meet redemptions further depresses price
        price_impact_lambda = 0.05
        shares_to_liquidate = min(net_redemptions / max(p_base, 1.0), arb_position[t - 1])
        realized_price = p_base - price_impact_lambda * shares_to_liquidate

        p_path[t] = max(realized_price, 20.0)
        mispricing[t] = v_fundamental - p_path[t]
        arb_aum[t] = max(pre_redemption_aum - net_redemptions, 50.0)
        arb_position[t] = max(arb_position[t - 1] - shares_to_liquidate, 0.5)

    max_mispricing = float(np.max(mispricing))
    t_peak = int(np.argmax(mispricing))
    min_aum = float(np.min(arb_aum))

    print("Shleifer-Vishny (1997) Performance-Based Arbitrage Dynamics")
    print(f"Fundamental asset value V:        ${v_fundamental:.2f}")
    print(f"Initial market price P_0:          ${p_path[0]:.2f}")
    print(f"Initial mispricing (V - P_0):      ${mispricing[0]:.2f}")
    print(f"Peak mispricing at t={t_peak}:             ${max_mispricing:.2f}")
    print(f"Trough price at t={t_peak}:               ${p_path[t_peak]:.2f}")
    print(f"Arbitrageur AUM trough:            ${min_aum:.2f} (from ${arb_aum[0]:.2f})")
    print(f"Final price at horizon t={n_steps - 1}:        ${p_path[-1]:.2f}")
    print(f"Mispricing widened during crisis:  {bool(max_mispricing > mispricing[0])}")


main()
