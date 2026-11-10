"""CF9 project lab 1 (rung 1, worked example): Corporate Hedging Program & CFaR Simulation.

SIMULATED: Meridian Global Industries multi-currency exposure and hedging pipeline.
Demonstrates the full corporate hedging workflow:
1. Extraction of net transaction exposure across EUR, JPY, and GBP.
2. Translation to USD base currency and portfolio covariance aggregation.
3. Minimum-variance hedge ratio determination and residual risk calculation.
4. Analytical 95% Cash-Flow-at-Risk (CFaR) and shortfall probability below capex hurdle.
5. ASC 815 / IFRS 9 retrospective dollar-offset hedge accounting compliance.
6. Cross-border capital budgeting valuation equivalence.
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def main() -> None:
    print("CF9 Project Lab 1: Corporate Hedging Program (Worked Example)")
    print("===========================================================")

    # 1. Foreign Currency Exposures (Millions)
    receivables = {"EUR": 30.0, "JPY": 3500.0, "GBP": 18.0}
    payables = {"EUR": 10.0, "JPY": 1200.0, "GBP": 6.0}
    spot_rates = {"EUR": 1.1000, "JPY": 0.007000, "GBP": 1.2800}

    currencies = ["EUR", "JPY", "GBP"]
    net_fc = {c: receivables[c] - payables[c] for c in currencies}
    usd_exp = [net_fc[c] * spot_rates[c] for c in currencies]

    print("1. Net Contractual Transaction Exposure:")
    for i, c in enumerate(currencies):
        print(
            f"   {c}: Receivables = {receivables[c]:,.1f}M, Payables = {payables[c]:,.1f}M -> "
            f"Net = {net_fc[c]:,.1f}M (USD ${usd_exp[i]:,.2f}M)"
        )
    total_gross_usd = sum(usd_exp)
    domestic_costs = 5.0
    expected_cf = total_gross_usd - domestic_costs
    print(f"   Total Gross Foreign Cash Flow:   ${total_gross_usd:,.2f}M")
    print(f"   Domestic USD Operating Costs:    ${domestic_costs:,.2f}M")
    print(f"   Net Expected Operating Cash Flow:${expected_cf:,.2f}M")

    # 2. Covariance Matrix (Annualized FX returns)
    vols = [0.10, 0.12, 0.09]
    corr = [
        [1.0, 0.35, 0.65],
        [0.35, 1.0, 0.30],
        [0.65, 0.30, 1.0],
    ]
    cov_matrix = [[corr[i][j] * vols[i] * vols[j] for j in range(3)] for i in range(3)]

    # Unhedged portfolio variance: Var(CF) = w^T * Sigma * w
    var_unhedged = sum(usd_exp[i] * usd_exp[j] * cov_matrix[i][j] for i in range(3) for j in range(3))
    std_unhedged = math.sqrt(var_unhedged)

    print("\n2. Portfolio Cash Flow Risk (Unhedged):")
    print(f"   Cash Flow Variance:              {var_unhedged:.4f} ($M^2)")
    print(f"   Cash Flow Standard Deviation:    ${std_unhedged:.2f}M")

    # 3. Minimum-Variance Hedging Program
    # Forward cover on EUR (85%), JPY (80%), GBP (90%)
    hedge_ratios = [0.85, 0.80, 0.90]
    residual_weights = [usd_exp[i] * (1.0 - hedge_ratios[i]) for i in range(3)]
    var_hedged = sum(residual_weights[i] * residual_weights[j] * cov_matrix[i][j] for i in range(3) for j in range(3))
    std_hedged = math.sqrt(var_hedged)
    hedge_eff = 1.0 - (var_hedged / var_unhedged)

    print("\n3. Hedged Portfolio Risk (Minimum-Variance Cover):")
    print(f"   Hedged Cash Flow Variance:       {var_hedged:.4f} ($M^2)")
    print(f"   Hedged Cash Flow Std Dev:        ${std_hedged:.2f}M")
    print(f"   Hedge Effectiveness (R^2):       {hedge_eff:.2%}")

    # 4. Cash-Flow-at-Risk (CFaR 95%) and Shortfall Below Hurdle K
    hurdle_k = 42.0  # Debt service $22M + critical capex $20M
    dist = NormalDist()
    z_95 = dist.inv_cdf(0.95)

    cfar_unhedged = z_95 * std_unhedged
    worst_cf_unhedged = expected_cf - cfar_unhedged
    prob_shortfall_unhedged = dist.cdf((hurdle_k - expected_cf) / std_unhedged)

    cfar_hedged = z_95 * std_hedged
    worst_cf_hedged = expected_cf - cfar_hedged
    prob_shortfall_hedged = dist.cdf((hurdle_k - expected_cf) / std_hedged)

    print("\n4. Cash-Flow-at-Risk Analysis (95% Confidence, Hurdle = $42.00M):")
    print(f"   Unhedged 95% CFaR Shortfall:     ${cfar_unhedged:.2f}M")
    worst_str_un = f"${worst_cf_unhedged:.2f}M"
    print(f"   Unhedged Worst-Case 5% Cash Flow:{worst_str_un} (Shortfall Risk = {prob_shortfall_unhedged:.2%})")
    worst_str_hd = f"${worst_cf_hedged:.2f}M"
    print(f"   Hedged 95% CFaR Shortfall:       ${cfar_hedged:.2f}M")
    print(f"   Hedged Worst-Case 5% Cash Flow:  {worst_str_hd} (Shortfall Risk = {prob_shortfall_hedged:.4%})")

    # 5. Hedge Accounting Compliance (ASC 815 / IFRS 9)
    delta_deriv = 9.80  # Derivative fair value gain
    delta_item = -10.50  # Hedged item foreign revenue drop
    offset_ratio = abs(delta_deriv) / abs(delta_item)
    qualified = 0.80 <= offset_ratio <= 1.25

    print("\n5. Hedge Accounting Qualification (80%-125% Corridor):")
    print(f"   Derivative Delta:                +${delta_deriv:.2f}M")
    print(f"   Hedged Item Delta:               ${delta_item:.2f}M")
    print(f"   Retrospective Dollar-Offset:     {offset_ratio:.2%}")
    print(f"   Cash Flow Hedge Qualified:       {qualified}")

    # 6. Cross-Border Project Valuation Parity
    initial_eur = 50.0
    cfs_eur = [14.0, 18.0, 22.0, 20.0]
    r_usd = 0.05
    r_eur = 0.03
    wacc_usd = 0.10
    wacc_eur = ((1.0 + wacc_usd) * (1.0 + r_eur) / (1.0 + r_usd)) - 1.0

    pv_eur = sum(cf / ((1.0 + wacc_eur) ** (t + 1)) for t, cf in enumerate(cfs_eur))
    npv_foreign_usd = (-initial_eur + pv_eur) * spot_rates["EUR"]

    forward_rates = [spot_rates["EUR"] * (((1.0 + r_usd) / (1.0 + r_eur)) ** (t + 1)) for t in range(4)]
    cfs_usd = [cf * fwd for cf, fwd in zip(cfs_eur, forward_rates, strict=True)]
    pv_usd = sum(cf / ((1.0 + wacc_usd) ** (t + 1)) for t, cf in enumerate(cfs_usd))
    npv_home_usd = (-initial_eur * spot_rates["EUR"]) + pv_usd

    print("\n6. Cross-Border Capital Budgeting Valuation:")
    print(f"   Foreign Currency Method NPV:     ${npv_foreign_usd:,.2f}M")
    print(f"   Home Currency Method NPV:        ${npv_home_usd:,.2f}M")
    print(f"   Parity Equivalence Confirmed:    {abs(npv_foreign_usd - npv_home_usd) < 1e-4}")


main()
