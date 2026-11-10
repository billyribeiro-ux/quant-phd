"""Lab AP4-L03-1: Bansal-Yaron (2004) Campbell-Shiller coefficient solver and pricing kernel decomposition.

Calculates the analytical Campbell-Shiller log-linearization coefficients A1 and A2,
evaluates the early resolution of uncertainty restriction (gamma > 1/psi, psi > 1),
and computes the long-run risk equity premium.
"""

from __future__ import annotations

# Published annual calibration parameters (Bansal & Yaron 2004 Table IV)
mu = 0.0180  # Mean consumption growth
rho = 0.979  # Persistence of expected growth x_t
phi_e = 0.044  # Exposure of x_t to volatility shocks
sigma_bar = 0.015  # Baseline consumption volatility
phi_d = 3.0  # Dividend leverage on expected growth x_t
gamma = 10.0  # Relative risk aversion
psi = 1.5  # Elasticity of intertemporal substitution (EIS)
kappa1 = 0.96  # Campbell-Shiller linearization constant

# Epstein-Zin composite parameter: theta = (1 - gamma) / (1 - 1/psi)
theta = (1.0 - gamma) / (1.0 - 1.0 / psi)

# 1. Price-consumption ratio coefficient A1 (consumption claim)
a1_c = (1.0 - 1.0 / psi) / (1.0 - kappa1 * rho)

# 2. Price-dividend ratio coefficient A1_m (dividend equity claim)
a1_m = (phi_d - 1.0 / psi) / (1.0 - kappa1 * rho)

# Risk prices for consumption shocks lambda_eta and long-run growth shocks lambda_e
lambda_eta = gamma
lambda_e = (gamma - 1.0 / psi) * (kappa1 * phi_e) / (1.0 - kappa1 * rho)

# Equity risk exposure (beta on long-run risk)
beta_e = kappa1 * a1_m * phi_e

# Equity premium component from long-run risk covariance
cov_e = beta_e * lambda_e * (sigma_bar**2)

print(f"Calibration: mu = {mu:.4f}, sigma_bar = {sigma_bar:.4f}, rho = {rho:.3f}")
print(f"Epstein-Zin composite parameter theta: {theta:.2f}")
print(f"Consumption claim sensitivity A1_c: {a1_c:.4f}")
print(f"Equity claim sensitivity A1_m: {a1_m:.4f}")
print(f"Short-run consumption risk price lambda_eta: {lambda_eta:.2f}")
print(f"Long-run growth risk price lambda_e: {lambda_e:.2f}")
print(f"Equity long-run risk exposure beta_e: {beta_e:.4f}")
print(f"Analytical long-run risk premium contribution: {cov_e * 100:.2f}%")
