"""Lab AP4-L01-1: Hansen-Jagannathan bound diagnostics for standard CRRA CCAPM.

Evaluates whether time-separable CRRA power utility can satisfy the nonparametric
Hansen-Jagannathan volatility bound using historical US equity and Treasury return moments.
"""

from __future__ import annotations

import numpy as np

# Historical US annual moments (1889-1978, Mehra & Prescott 1985; Campbell 2003)
mean_rf = 0.0080
mean_re = 0.0618
vol_re = 0.1654
mean_gc = 0.0183
vol_gc = 0.0357

# Empirical Sharpe ratio: lower bound on sigma(M) / E[M]
sharpe = mean_re / vol_re
e_m = 1.0 / (1.0 + mean_rf)
hj_lower_bound = sharpe * e_m

print(f"Historical Consumption Growth: {mean_gc * 100:.2f}% (vol = {vol_gc * 100:.2f}%)")
print(f"Historical Equity Premium: {mean_re * 100:.2f}%")
print(f"Historical Excess Volatility: {vol_re * 100:.2f}%")
print(f"Historical Sharpe Ratio: {sharpe:.4f}")
print(f"Hansen-Jagannathan Minimum Volatility sigma(M) >= {hj_lower_bound:.4f}")
print("--- CRRA Model Comparison ---")

gammas = [1.0, 2.0, 5.0, 10.0, 20.0, 30.0]
for g in gammas:
    # For lognormal consumption growth: M = beta * exp(-gamma * Delta c)
    # Var(ln M) = gamma^2 * vol_gc^2 => sigma(M)/E[M] approx gamma * vol_gc
    model_vol_ratio = np.sqrt(np.exp(g**2 * vol_gc**2) - 1.0)
    satisfied = model_vol_ratio >= sharpe
    print(f"gamma = {g:4.1f}: sigma(M)/E[M] = {model_vol_ratio:.4f} | HJ Bound Satisfied: {satisfied}")
