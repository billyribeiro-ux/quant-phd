"""CF9 project lab 2 (rung 2, completion solution): Core Hedging and Risk Calculations.

SIMULATED: Completion exercise implementing core treasury hedging formulas:
1. Net contractual transaction exposure calculation.
2. Minimum-variance hedge ratio derivation: h* = Cov(Delta CF, Delta F) / Var(Delta F).
3. Multi-currency portfolio cash flow variance with full covariance matrix.
4. Analytical 95% Cash-Flow-at-Risk (CFaR) and shortfall probability.
5. Retrospective dollar-offset ratio for ASC 815 / IFRS 9 hedge accounting.
Standard library only; deterministic execution.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def main() -> None:
    # 3 Sample Currencies
    receivables = {"EUR": 25.0, "JPY": 3000.0, "GBP": 15.0}
    payables = {"EUR": 10.0, "JPY": 1000.0, "GBP": 5.0}
    spots = {"EUR": 1.1000, "JPY": 0.007000, "GBP": 1.3000}

    # Completed Line 1: Net foreign currency exposure
    net_exposure = {c: receivables[c] - payables[c] for c in receivables}

    # Completed Line 2: USD translated cash flows
    usd_exposures = [net_exposure[c] * spots[c] for c in ["EUR", "JPY", "GBP"]]

    # Completed Line 3: Minimum-variance hedge ratio
    cov_eur = 0.0095
    var_eur_f = 0.0121
    h_star_eur = cov_eur / var_eur_f

    # Completed Line 4: Portfolio cash flow variance
    cov_matrix = [
        [0.0100, 0.0042, 0.0065],
        [0.0042, 0.0144, 0.0036],
        [0.0065, 0.0036, 0.0081],
    ]
    total_var = sum(usd_exposures[i] * usd_exposures[j] * cov_matrix[i][j] for i in range(3) for j in range(3))
    total_std = math.sqrt(total_var)

    # Completed Line 5: 95% Cash-Flow-at-Risk (CFaR)
    mean_cf = sum(usd_exposures) - 10.0  # $10M domestic operating costs
    dist = NormalDist()
    z_95 = dist.inv_cdf(0.95)
    cfar_95 = z_95 * total_std
    worst_case_cf = mean_cf - cfar_95

    # Shortfall probability below hurdle $30M
    hurdle = 30.0
    z_hurdle = (hurdle - mean_cf) / total_std
    prob_shortfall = dist.cdf(z_hurdle)

    # Completed Line 6: ASC 815 / IFRS 9 Dollar-Offset Ratio
    delta_deriv = 8.50
    delta_exposure = -9.20
    offset_ratio = abs(delta_deriv) / abs(delta_exposure)
    qualified = 0.80 <= offset_ratio <= 1.25

    print("CF9 Project Rung 2: Completion Lab Results")
    print(f"Net FC Exposures:            {net_exposure}")
    print(f"USD Exposures:               {[round(x, 2) for x in usd_exposures]}")
    print(f"Optimal EUR Hedge Ratio h*:  {h_star_eur:.4f}")
    print(f"Portfolio CF Variance:       {total_var:.4f}")
    print(f"Portfolio CF Std Dev:        ${total_std:.2f}M")
    print(f"Expected Operating CF:       ${mean_cf:.2f}M")
    print(f"95% CFaR Shortfall:          ${cfar_95:.2f}M")
    print(f"Worst-Case 5% Cash Flow:     ${worst_case_cf:.2f}M")
    print(f"Hurdle Shortfall Risk:       {prob_shortfall:.2%}")
    print(f"Hedge Dollar-Offset Ratio:   {offset_ratio:.2%}")
    print(f"Hedge Accounting Qualified:  {qualified}")


main()
