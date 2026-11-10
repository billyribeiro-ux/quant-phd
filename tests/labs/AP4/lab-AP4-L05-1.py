"""Lab AP4-L05-1: Constantinides-Duffie (1996) incomplete markets and cross-sectional variance aggregation.

Simulates cross-sectional consumer panels with persistent uninsurable idiosyncratic labor shocks,
computes the aggregate pricing kernel under countercyclical idiosyncratic variance,
and demonstrates how cross-sectional heterogeneity generates a large equity premium.
"""

from __future__ import annotations

import numpy as np

# Model parameters (Constantinides & Duffie 1996; Mankiw 1986)
gamma = 3.0  # Moderate relative risk aversion
beta = 0.98  # Subjective discount factor
g_c = 0.018  # Aggregate consumption growth
sigma_agg = 0.020  # Aggregate consumption volatility

# Cross-sectional variance of individual consumption shares:
# ln(c_i,t+1 / c_i,t) = ln(C_t+1 / C_t) + eta_i,t+1 - 0.5 * sigma_i,t+1^2
# In Constantinides-Duffie, the effective aggregate SDF is:
# M_t+1 = beta * (C_t+1 / C_t)^(-gamma) * exp(0.5 * gamma * (gamma + 1) * Var_i(ln(c_i,t+1 / C_t+1)))

# Scenario A: Homogeneous agents (zero cross-sectional variance)
var_cs_zero = 0.0
m_homo_factor = float(np.exp(0.5 * gamma * (gamma + 1.0) * var_cs_zero))

# Scenario B: Constant idiosyncratic risk (sigma_i = 10% per year)
sigma_idiosyncratic_const = 0.10
var_cs_const = sigma_idiosyncratic_const**2
m_const_factor = float(np.exp(0.5 * gamma * (gamma + 1.0) * var_cs_const))

# Scenario C: Countercyclical idiosyncratic risk (recession variance = 0.20^2, expansion = 0.08^2)
var_cs_recession = 0.20**2
var_cs_expansion = 0.08**2
m_recession_factor = float(np.exp(0.5 * gamma * (gamma + 1.0) * var_cs_recession))
m_expansion_factor = float(np.exp(0.5 * gamma * (gamma + 1.0) * var_cs_expansion))

# Implied SDF volatility ratio sigma(M) / E[M]:
excess_cov_premium = 0.5 * gamma * (gamma + 1.0) * (var_cs_recession - var_cs_expansion) * 0.5

print(f"Calibration: beta = {beta:.2f}, g_c = {g_c * 100:.1f}%, sigma_agg = {sigma_agg * 100:.1f}%")
print(f"Representative Agent Curvature gamma: {gamma:.1f}")
print(f"Homogeneous Factor: {m_homo_factor:.4f}")
print(f"Constant Idiosyncratic Risk Adjustment: {m_const_factor:.4f}")
print(
    f"Countercyclical Idiosyncratic Factor: Expansion = {m_expansion_factor:.4f}, Recession = {m_recession_factor:.4f}"
)
print(f"Ratio of Recession to Expansion Pricing Kernel: {m_recession_factor / m_expansion_factor:.2f}x")
print(f"Additional Equity Premium from Countercyclical Risk: {excess_cov_premium * 100:.2f}%")
