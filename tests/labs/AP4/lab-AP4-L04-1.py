"""Lab AP4-L04-1: Barro (2006) rare disaster pricing and resolution of asset pricing puzzles.

Evaluates the equity premium, precautionary risk-free rate, and price-dividend ratio
under compound Poisson macroeconomic disasters with international calibration parameters.
"""

from __future__ import annotations

import numpy as np

# International historical disaster calibration (Barro 2006 Table IV)
g = 0.025  # Normal per-capita GDP/consumption growth rate
sigma = 0.020  # Normal consumption growth standard deviation
p_disaster = 0.017  # Disaster probability per year (~1.7% per year)
b_mean = 0.29  # Average contraction in consumption during disaster (29%)
b_d = 0.435  # Average contraction in equity/dividends during disaster (43.5%)
delta = 0.970  # Subjective discount factor
gamma = 4.0  # Relative risk aversion

# 1. Expected pricing kernel for risk-free bond: E[M]
# Under log-normal normal growth + Bernoulli disaster jump:
# E[M] = delta * exp(-gamma * g + 0.5 * gamma^2 * sigma^2) * [(1 - p) + p * (1 - b)^(-gamma)]
base_disc = delta * np.exp(-gamma * g + 0.5 * gamma**2 * sigma**2)
precautionary_term = (1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma))
em = base_disc * precautionary_term
rf_gross = 1.0 / em
rf_net = float(rf_gross - 1.0)

# 2. Risk-free rate without disasters (standard Lucas CCAPM):
rf_no_disaster = float(1.0 / base_disc - 1.0)

# 3. Pricing kernel expectation for equity: E[M * (D'/D)]
base_equity = delta * np.exp((1.0 - gamma) * g + 0.5 * (1.0 - gamma) ** 2 * sigma**2)
equity_jump_term = (1.0 - p_disaster) + p_disaster * ((1.0 - b_mean) ** (-gamma)) * (1.0 - b_d)
alpha_d = base_equity * equity_jump_term
pd_ratio = float(alpha_d / (1.0 - alpha_d))

# 4. Expected equity return in calm (non-disaster) sample:
expected_calm_return = float(((pd_ratio + 1.0) / pd_ratio) * np.exp(g + 0.5 * (0.05**2)) - 1.0)
calm_equity_premium = expected_calm_return - rf_net

print(f"Risk Aversion gamma: {gamma:.1f}")
print(f"Annual Disaster Probability: {p_disaster * 100:.2f}%")
print(f"Disaster Contraction Size: Consumption = {b_mean * 100:.1f}%, Equity = {b_d * 100:.1f}%")
print(f"Risk-free rate without disasters: {rf_no_disaster * 100:.2f}%")
print(f"Precautionary savings factor: {precautionary_term:.4f}")
print(f"Equilibrium Risk-free rate with disasters r_f: {rf_net * 100:.2f}%")
print(f"Equilibrium Price-Dividend ratio P/D: {pd_ratio:.2f}")
print(f"Expected Equity Return (calm sample): {expected_calm_return * 100:.2f}%")
print(f"Observed Equity Premium (calm sample): {calm_equity_premium * 100:.2f}%")
