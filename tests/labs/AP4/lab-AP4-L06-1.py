"""Lab AP4-L06-1: Beeler & Campbell (2012) 12-moment scorecard evaluation.

Computes the 12 canonical macro-finance moments on benchmark simulation data
and calculates relative error distance against historical US target moments.
"""

from __future__ import annotations

import numpy as np

# 12 Target moments from US historical annual data (1930-2008 / Beeler & Campbell 2012)
targets = {
    "mean_consumption_growth": 0.0189,
    "vol_consumption_growth": 0.0325,
    "ac1_consumption_growth": 0.4500,
    "mean_equity_premium": 0.0620,
    "vol_equity_return": 0.1940,
    "sharpe_ratio": 0.3200,
    "mean_risk_free_rate": 0.0080,
    "vol_risk_free_rate": 0.0540,
    "mean_log_pd": 3.3800,
    "vol_log_pd": 0.4000,
    "ac1_log_pd": 0.8700,
    "predictability_slope_1y": -0.1500,
}

# Mock simulated moments from candidate macro-finance model
candidate_sim = {
    "mean_consumption_growth": 0.0195,
    "vol_consumption_growth": 0.0280,
    "ac1_consumption_growth": 0.3800,
    "mean_equity_premium": 0.0580,
    "vol_equity_return": 0.1850,
    "sharpe_ratio": 0.3135,
    "mean_risk_free_rate": 0.0110,
    "vol_risk_free_rate": 0.0120,
    "mean_log_pd": 3.4200,
    "vol_log_pd": 0.3500,
    "ac1_log_pd": 0.8200,
    "predictability_slope_1y": -0.1100,
}

print(f"{'Moment':<26} | {'Target':<8} | {'Simulated':<9} | {'Rel Error':<9}")
print("-" * 62)

rel_errors = []
for k in targets:
    tgt = targets[k]
    sim = candidate_sim[k]
    rel_err = abs(sim - tgt) / (abs(tgt) if abs(tgt) > 1e-4 else 1e-4)
    rel_errors.append(rel_err)
    print(f"{k:<26} | {tgt:8.4f} | {sim:9.4f} | {rel_err * 100:8.2f}%")

mape = float(np.mean(rel_errors))
matched_50pct = sum(1 for e in rel_errors if e <= 0.50)
print("-" * 62)
print(f"Mean Absolute Percentage Error (MAPE): {mape * 100:.2f}%")
print(f"Moments Matched within 50% tolerance: {matched_50pct} / {len(targets)}")
