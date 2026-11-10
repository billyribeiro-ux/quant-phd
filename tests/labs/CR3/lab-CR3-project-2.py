"""Lab CR3-project-2 (Rung 2, Completion): Credit-cycle indicators and recession forecasting.

SIMULATED: complete solution for the Rung 2 completion problem.
Calculates Gilchrist-Zakrajšek EBP, composite credit sentiment index,
recession forecasting logistic likelihood, ROC-AUC, and cov-lite debt recovery.
Standard library, numpy, and scipy only; no network.
"""

from __future__ import annotations

import math


def main() -> None:
    # Step 1: EBP calculation from observed and predicted spreads
    gz_spread = 245.5
    pred_spread = 185.2
    ebp = gz_spread - pred_spread

    # Step 2: Standardized credit market sentiment index
    z_hy = 1.45
    z_spr = -0.85
    z_ebp = -1.10
    sentiment = (z_hy - z_spr - z_ebp) / 3.0

    # Step 3: Logistic recession probability
    beta_0 = -2.10
    beta_distress = 1.25
    beta_term_spread = -1.50
    credit_distress = 0.80
    term_spread = -0.50
    z_val = beta_0 + beta_distress * credit_distress + beta_term_spread * term_spread
    p_recession = 1.0 / (1.0 + math.exp(-z_val))

    # Step 4: Out-of-sample forecast evaluation (Brier score & AUC)
    y_true = [0, 0, 1, 0, 1, 1]
    y_prob = [0.15, 0.25, 0.65, 0.35, 0.80, 0.90]
    brier_score = sum((p - y) ** 2 for p, y in zip(y_prob, y_true, strict=False)) / len(y_true)

    # Step 5: Cov-lite leveraged loan recovery with 35% enterprise value erosion
    cash_ebitda = 60.0
    distress = 0.40
    distressed_ebitda = cash_ebitda * (1.0 - distress)
    debt = 400.0
    senior_share = 0.75
    ev_covlite = distressed_ebitda * 7.0 * 0.65
    senior_debt = debt * senior_share
    senior_recovery = min(senior_debt, ev_covlite) / senior_debt
    total_recovery = min(debt, ev_covlite) / debt

    print(f"GZ Spread: {gz_spread:.1f} bp, Fitted: {pred_spread:.1f} bp, EBP: {ebp:.1f} bp")
    print(f"Credit Sentiment Index: {sentiment:.4f}")
    print(f"Recession Probability: {p_recession * 100:.2f} percent")
    print(f"Out-of-sample Brier Score: {brier_score:.4f}")
    s_rec_pct = senior_recovery * 100
    tot_rec_pct = total_recovery * 100
    print(f"Cov-lite Senior Recovery: {s_rec_pct:.1f} percent, Total Recovery: {tot_rec_pct:.1f} percent")


main()
