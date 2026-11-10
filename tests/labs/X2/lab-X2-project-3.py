"""Lab X2-project-3: Rung 4 Stretch: Transaction Costs & Breakeven FX Spreads.

Simulates turnover, rebalancing friction, and bid-ask spreads on HML-FX carry,
and solves for breakeven execution costs (Burnside et al. 2011, Menkhoff et al. 2012).
"""

from __future__ import annotations

import math
import random
from typing import Any


def evaluate_transaction_costs(
    n_months: int = 120,
    seed: int = 42,
) -> dict[str, Any]:
    """Evaluate gross vs net HML-FX carry returns across transaction cost tiers."""
    rng = random.Random(seed)
    n_cur = 10

    base_spreads = [-0.035, -0.020, -0.010, -0.005, 0.005, 0.010, 0.018, 0.025, 0.035, 0.055]
    cur_spreads = list(base_spreads)

    gross_hml: list[float] = []
    turnover_series: list[float] = []

    prev_p1: set[int] = set()
    prev_p5: set[int] = set()

    for _ in range(n_months):
        # Update interest spreads with noise causing occasional rank changes
        for j in range(n_cur):
            cur_spreads[j] = 0.95 * cur_spreads[j] + 0.05 * base_spreads[j] + rng.gauss(0.0, 0.003)

        # Forward discounts
        fds = [-s / 12.0 for s in cur_spreads]
        ranked = sorted(range(n_cur), key=lambda j: fds[j], reverse=True)

        cur_p1 = set(ranked[:2])  # 2 lowest rate currencies (funding)
        cur_p5 = set(ranked[-2:])  # 2 highest rate currencies (target)

        # Calculate monthly turnover fraction in long and short legs
        if prev_p1:
            turnover_long = len(cur_p5 - prev_p5) / 2.0
            turnover_short = len(cur_p1 - prev_p1) / 2.0
            # Total portfolio two-way turnover fraction
            turnover = 0.5 * (turnover_long + turnover_short)
        else:
            turnover = 1.0
        turnover_series.append(turnover)
        prev_p1 = cur_p1
        prev_p5 = cur_p5

        # Monthly return
        r_p5 = (sum(cur_spreads[j] for j in cur_p5) / 2.0) / 12.0 + rng.gauss(0.0, 0.02)
        r_p1 = (sum(cur_spreads[j] for j in cur_p1) / 2.0) / 12.0 + rng.gauss(0.0, 0.018)
        gross_hml.append(r_p5 - r_p1)

    t_obs = len(gross_hml)
    m_gross = sum(gross_hml) / t_obs
    s_gross = math.sqrt(sum((r - m_gross) ** 2 for r in gross_hml) / (t_obs - 1))
    sr_gross = (m_gross * 12.0) / (s_gross * math.sqrt(12.0))

    avg_monthly_turnover = sum(turnover_series) / t_obs
    ann_turnover = avg_monthly_turnover * 12.0

    # Net returns for various half-spread costs (in basis points: 1 bp = 0.0001)
    cost_tiers_bps = [2.0, 5.0, 10.0, 15.0, 20.0]
    tier_results: list[dict[str, float]] = []

    for c_bp in cost_tiers_bps:
        # Effective cost per rebalance = turnover * (c_bp * 1e-4 * 2 legs)
        cost_rate = c_bp * 0.0001 * 2.0
        net_hml = [r - turnover_series[t] * cost_rate for t, r in enumerate(gross_hml)]
        m_net = sum(net_hml) / t_obs
        s_net = math.sqrt(sum((r - m_net) ** 2 for r in net_hml) / (t_obs - 1))
        sr_net = (m_net * 12.0) / (s_net * math.sqrt(12.0))
        tier_results.append(
            {
                "half_spread_bps": c_bp,
                "ann_cost_pct": round(ann_turnover * cost_rate * 100, 2),
                "net_mean_pct": round(m_net * 12.0 * 100, 2),
                "net_sharpe": round(sr_net, 3),
            }
        )

    # Breakeven half-spread: solves m_gross - avg_turnover * (c * 2) = 0
    # c_breakeven = m_gross / (2 * avg_turnover)
    be_half_spread_bps = (m_gross / (2.0 * avg_monthly_turnover)) * 10000.0

    return {
        "n_months": t_obs,
        "gross_mean_ann": round(m_gross * 12.0 * 100, 2),
        "gross_vol_ann": round(s_gross * math.sqrt(12.0) * 100, 2),
        "gross_sharpe": round(sr_gross, 3),
        "ann_turnover": round(ann_turnover, 2),
        "breakeven_half_spread_bps": round(be_half_spread_bps, 1),
        "tier_results": tier_results,
    }


def main() -> None:
    res = evaluate_transaction_costs(n_months=120, seed=42)
    print("=== Rung 4 Stretch: Transaction Costs & Breakeven Spreads ===")
    mean_s = f"{res['gross_mean_ann']}%"
    vol_s = f"{res['gross_vol_ann']}%"
    print(f"Sample: {res['n_months']} months | Gross Annualized Mean: {mean_s} | Vol: {vol_s}")
    print(f"Gross Sharpe Ratio: {res['gross_sharpe']:.3f} | Annualized Turnover: {res['ann_turnover']:.2f}x")
    print("-------------------------------------------------------------------")
    print("Half-Spread | Annual Cost | Net Return (ann) | Net Sharpe Ratio")
    print("-------------------------------------------------------------------")
    for tr in res["tier_results"]:
        hs_s = f"{tr['half_spread_bps']:>4.1f} bps"
        ac_s = f"{tr['ann_cost_pct']:>5.2f}%"
        nm_s = f"{tr['net_mean_pct']:>6.2f}%"
        ns_s = f"{tr['net_sharpe']:>5.3f}"
        print(f"  {hs_s}  |   {ac_s}   |     {nm_s}    |      {ns_s}")
    print("-------------------------------------------------------------------")
    print(f"Breakeven Round-Trip / Half-Spread: {res['breakeven_half_spread_bps']:.1f} bps")


main()
