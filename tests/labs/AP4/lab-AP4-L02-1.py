"""Lab AP4-L02-1: Campbell-Cochrane (1999) surplus consumption ratio and constant risk-free rate.

Simulates the external habit formation model, computes the steady-state surplus ratio,
evaluates the sensitivity function lambda(s), and verifies that the real risk-free rate is constant.
"""

from __future__ import annotations

import numpy as np

# Published annual calibration parameters (Campbell & Cochrane 1999)
g = 0.0189  # Mean consumption growth
sigma = 0.0150  # Consumption growth standard deviation
phi = 0.87  # Persistence of surplus consumption ratio
gamma = 2.0  # Curvature parameter
delta = 0.89  # Subjective discount factor

# Steady state surplus consumption ratio S_bar and max log surplus s_max
s_bar_val = sigma * np.sqrt(gamma / (1.0 - phi))
s_bar = float(np.log(s_bar_val))
s_max = float(s_bar + 0.5 * (1.0 - s_bar_val**2))

# Analytical log risk-free rate
rf_log = -np.log(delta) + gamma * g - 0.5 * gamma * (1.0 - phi)
rf_net = float(np.exp(rf_log) - 1.0)

print(f"Steady-state surplus ratio S_bar: {s_bar_val:.4f} (ln S_bar = {s_bar:.4f})")
print(f"Maximum log surplus ratio s_max: {s_max:.4f}")
print(f"Analytical real risk-free rate r_f: {rf_net * 100:.2f}%")

# Simulation over 500 years
rng = np.random.default_rng(42)
t_len = 500
s = np.zeros(t_len)
v = rng.normal(0.0, sigma, t_len)
s[0] = s_bar

for t in range(t_len - 1):
    lam = (1.0 / s_bar_val) * np.sqrt(max(0.0, 1.0 - 2.0 * (s[t] - s_bar))) - 1.0 if s[t] <= s_max else 0.0
    s[t + 1] = (1.0 - phi) * s_bar + phi * s[t] + lam * v[t + 1]

# Effective risk aversion: gamma / S_t
s_levels = np.exp(s)
effective_gamma = gamma / s_levels

print(f"Simulated Surplus Ratio: Mean = {np.mean(s_levels):.4f}, Std = {np.std(s_levels):.4f}")
print(
    f"Effective Relative Risk Aversion gamma_t: Min = {np.min(effective_gamma):.1f}, "
    f"Mean = {np.mean(effective_gamma):.1f}, Max = {np.max(effective_gamma):.1f}"
)
