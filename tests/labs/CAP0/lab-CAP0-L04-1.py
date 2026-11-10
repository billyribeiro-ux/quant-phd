"""Lab L04-1: Capital structure trade-off curve and corporate hedging program."""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    # 1. Capital Structure Trade-off Optimization
    ebit = 220.0
    tax_rate = 0.25
    r_u = 0.088
    v_u = (ebit * (1.0 - tax_rate)) / r_u
    distress_cost_frac = 0.25
    k = 12.0
    d0 = 0.55

    leverage_ratios = np.linspace(0.0, 0.8, 9)
    print("Leverage (D/V) | Distress Prob | Tax Shield ($M) | Distress Cost ($M) | Levered Value ($M)")
    print("-" * 80)

    best_vl = 0.0
    best_d = 0.0

    for d in leverage_ratios:
        pi = 1.0 / (1.0 + math.exp(-k * (d - d0)))
        tax_shield = tax_rate * d * v_u
        distress_cost = pi * distress_cost_frac * v_u
        v_l = v_u + tax_shield - distress_cost

        if v_l > best_vl:
            best_vl = v_l
            best_d = d

        print(f"{d:14.2f} | {pi:13.4f} | {tax_shield:15.2f} | {distress_cost:18.2f} | {v_l:18.2f}")

    print(f"\nOptimal Leverage Ratio: {best_d:.2f} (Max Firm Value: ${best_vl:,.2f}M)")

    # 2. Minimum-Variance Hedging Regression
    np.random.seed(42)
    t_obs = 36
    r_f = np.random.normal(0.002, 0.045, size=t_obs)
    # Spot return with high correlation and basis noise
    r_s = 1.05 * r_f + np.random.normal(0.0, 0.015, size=t_obs)

    cov_sf = float(np.cov(r_s, r_f)[0, 1])
    var_f = float(np.var(r_f, ddof=1))
    var_s = float(np.var(r_s, ddof=1))
    h_star = cov_sf / var_f

    slope, intercept = np.polyfit(r_f, r_s, deg=1)
    y_pred = intercept + slope * r_f
    ss_tot = float(np.sum((r_s - np.mean(r_s)) ** 2))
    ss_res = float(np.sum((r_s - y_pred) ** 2))
    r_squared = 1.0 - (ss_res / ss_tot)

    r_hedged = r_s - h_star * r_f
    var_hedged = float(np.var(r_hedged, ddof=1))
    var_reduction = 1.0 - (var_hedged / var_s)

    print("\nHedging Effectiveness Analysis:")
    print(f"  Optimal Hedge Ratio h*: {h_star:.4f}")
    print(f"  Regression Slope beta:   {slope:.4f}")
    print(f"  R-Squared:               {r_squared:.4f}")
    print(f"  Variance Reduction:      {var_reduction * 100:.2f}%")
    print(f"  ASC 815 Qualifying:      {(0.80 <= slope <= 1.25) and (r_squared >= 0.80)}")


main()
