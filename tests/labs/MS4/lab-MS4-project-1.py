"""Lab MS4-project-1: Rung 1 worked example · Factor strategy capacity calibration.

Provides an end-to-end worked solution computing trade lists, square-root market impact,
portfolio friction kappa, capacity limits, and buffer mitigation on a calibrated universe.
SIMULATED: 5-asset portfolio with known ground-truth parameters.
"""

from __future__ import annotations

import math


def run_worked_example() -> None:
    prices = [25.0, 50.0, 75.0, 100.0, 125.0]
    adv = [10000000.0, 20000000.0, 15000000.0, 30000000.0, 25000000.0]
    sigma = [0.020, 0.018, 0.025, 0.015, 0.022]
    w_initial = [0.20, 0.20, 0.20, 0.20, 0.20]
    w_target = [0.35, 0.10, 0.05, 0.30, 0.20]
    aum = 10000000.0
    gross_alpha = 0.10
    prefactor_y = 0.50

    # Step 1: Compute trade lists
    n = len(w_initial)
    dollar_trades = [aum * (w_target[i] - w_initial[i]) for i in range(n)]
    share_trades = [dollar_trades[i] / prices[i] for i in range(n)]
    turnover_dollars = 0.5 * sum(abs(d) for d in dollar_trades)
    turnover_frac = turnover_dollars / aum

    print("Step 1 · Trade Allocation and Turnover:")
    print(f"  AUM:                   {aum:.2f}")
    for i in range(n):
        print(f"  Asset {i}: trade dollars = {dollar_trades[i]:.2f}, shares = {share_trades[i]:.2f}")
    print(f"  Turnover Dollars:      {turnover_dollars:.2f}")
    print(f"  Turnover Fraction:     {turnover_frac:.4f} ({turnover_frac * 100.0:.2f}%)")

    # Step 2: Estimate market impact costs
    total_cost = 0.0
    total_traded = sum(abs(d) for d in dollar_trades)
    for i in range(n):
        abs_d = abs(dollar_trades[i])
        if abs_d > 1e-9:
            impact = prefactor_y * sigma[i] * math.sqrt(abs_d / adv[i])
            cost_i = abs_d * impact
            total_cost += cost_i
    eff_bps = (total_cost / total_traded) * 10000.0 if total_traded > 0 else 0.0

    print("Step 2 · Square-Root Market Impact:")
    print(f"  Total Impact Cost:     {total_cost:.2f}")
    print(f"  Effective Spread:      {eff_bps:.2f} bps")

    # Step 3: Find capacity limits
    kappa = prefactor_y * sum(sigma[i] * (abs(w_target[i] - w_initial[i]) ** 1.5) / math.sqrt(adv[i]) for i in range(n))
    a_star = (gross_alpha / kappa) ** 2
    a_opt = (4.0 / 9.0) * a_star
    max_d_alpha = (4.0 / 27.0) * (gross_alpha**3) / (kappa**2)
    net_opt = gross_alpha / 3.0

    print("Step 3 · Strategy Capacity Limits:")
    print(f"  Portfolio Friction:    {kappa:.8e}")
    print(f"  Break-even AUM A*:     {a_star:.2f}")
    print(f"  Optimal AUM A_opt:     {a_opt:.2f}")
    print(f"  A_opt / A* Ratio:      {a_opt / a_star:.4f}")
    print(f"  Net Alpha at A_opt:    {net_opt * 100.0:.2f}% ({net_opt * 10000.0:.1f} bps)")
    print(f"  Max Dollar Alpha:      {max_d_alpha:.2f}")

    # Step 4: Cost mitigation via buffer zones
    ranks = [1.0, 5.0, 4.0, 2.0, 3.0]
    target_k = 3
    buffer_ratio = 1.5
    k_hold = math.floor(target_k * buffer_ratio)  # 4

    # Existing holdings: assets where w_initial > 1e-6 (all 5 held)
    is_held = [w > 1e-6 for w in w_initial]
    retained = [i for i in range(n) if is_held[i] and ranks[i] <= k_hold]
    retained.sort(key=lambda idx: ranks[idx])
    selected = retained[:target_k]

    w_mitigated = [0.0] * n
    for idx in selected:
        w_mitigated[idx] = 1.0 / target_k

    print("Step 4 · Cost Mitigation Weights:")
    for i in range(n):
        print(f"  Asset {i}: weight = {w_mitigated[i]:.4f}")
    print(f"  Weights Sum:           {sum(w_mitigated):.6f}")


def main() -> None:
    run_worked_example()


main()
