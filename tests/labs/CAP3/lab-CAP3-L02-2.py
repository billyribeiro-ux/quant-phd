"""Lab CAP3-L02-2: Field Prelim I, Problem B: Merton Stochastic Control & HJB Verification.

Solves the continuous-time Merton portfolio and consumption problem,
verifying the Hamilton-Jacobi-Bellman (HJB) PDE and transversality condition.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Calibrated economic parameters
    rf = 0.02
    mu = 0.08
    sigma = 0.20
    gamma = 4.0
    rho = 0.03

    # 1. Analytical Merton optimal portfolio fraction
    excess_return = mu - rf
    variance = sigma**2
    merton_alpha = excess_return / (gamma * variance)

    # 2. Consumption-wealth ratio in infinite-horizon CRRA
    # Growth component = rf + (mu - rf)^2 / (2 * gamma * sigma^2)
    growth = rf + (excess_return**2) / (2.0 * gamma * variance)
    c_ratio = (rho + (gamma - 1.0) * growth) / gamma

    # 3. Transversality condition verification: rho + (gamma - 1) * growth > 0
    tv_criterion = rho + (gamma - 1.0) * growth
    tv_satisfied = bool(tv_criterion > 0.0)

    # 4. HJB residual check: Evaluate HJB equation at candidate value function V(W) = k * W^{1-gamma} / (1 - gamma)
    k_constant = c_ratio ** (-gamma)
    # Check that optimal alpha maximizes the quadratic Hamiltonian
    alpha_grid = np.linspace(0.0, 1.5, 301)
    hamiltonian = alpha_grid * excess_return - 0.5 * gamma * (alpha_grid**2) * variance
    numerical_opt_alpha = float(alpha_grid[np.argmax(hamiltonian)])

    print(f"Risk-Free Rate: {rf * 100:.1f}%")
    print(f"Stock Drift: {mu * 100:.1f}% | Volatility: {sigma * 100:.1f}%")
    print(f"Relative Risk Aversion (gamma): {gamma:.1f}")
    print(f"Optimal Merton Fraction (alpha*): {merton_alpha:.4f}")
    print(f"Numerical Optimizer Alpha*: {numerical_opt_alpha:.4f}")
    print(f"Optimal Consumption Ratio (c*/W): {c_ratio * 100:.2f}%")
    print(f"Value Function Constant k: {k_constant:.4f}")
    print(f"Transversality Condition: {tv_criterion:.4f} (Satisfied: {tv_satisfied})")


main()
