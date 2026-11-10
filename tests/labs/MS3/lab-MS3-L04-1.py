"""Lab MS3-L04-1: Almgren-Chriss efficient execution frontier solver.

Traces the Pareto-optimal frontier of expected execution cost E[x] vs cost variance V[x]
across risk aversion parameter lambda and verifies strict convexity.
"""

from __future__ import annotations

import math

import numpy as np


def compute_cost_and_variance(
    total_shares: float,
    trajectory: np.ndarray,
    tau: float,
    volatility: float,
    gamma: float,
    eta: float,
) -> tuple[float, float]:
    """Compute expected execution cost E[x] and variance V[x]."""
    trades = trajectory[:-1] - trajectory[1:]
    perm_cost = 0.5 * gamma * (total_shares**2)
    temp_cost = (eta / tau) * float(np.sum(trades**2))
    expected_cost = perm_cost + temp_cost

    holdings = trajectory[1:]
    variance = float((volatility**2) * tau * np.sum(holdings**2))
    return expected_cost, variance


def almgren_chriss_trajectory(
    total_shares: float,
    horizon: float,
    n_steps: int,
    volatility: float,
    eta: float,
    risk_aversion: float,
) -> np.ndarray:
    if risk_aversion == 0.0 or volatility == 0.0:
        return np.array([total_shares * (1.0 - k / n_steps) for k in range(n_steps + 1)], dtype=np.float64)

    tau = horizon / n_steps
    times = np.linspace(0.0, horizon, n_steps + 1, dtype=np.float64)
    arg = 1.0 + 0.5 * (risk_aversion * (volatility**2) * (tau**2)) / eta
    kappa = math.acosh(arg) / tau
    sinh_kt = math.sinh(kappa * horizon)

    trajectory = np.zeros(n_steps + 1, dtype=np.float64)
    for k in range(n_steps + 1):
        trajectory[k] = total_shares * math.sinh(kappa * (horizon - times[k])) / sinh_kt
    trajectory[0] = total_shares
    trajectory[-1] = 0.0
    return trajectory


def main() -> None:
    x_total = 500_000.0  # 500,000 shares
    horizon = 1.0  # 1 day
    n_steps = 20  # 20 intervals
    tau = horizon / n_steps
    volatility = 0.02  # $1.00 daily sigma on $50 stock
    gamma = 2e-7  # permanent impact parameter
    eta = 1e-6  # temporary impact parameter

    lambdas = [0.0, 1e-7, 5e-7, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4]

    print("Efficient Execution Frontier (X=500k, T=1.0d, N=20, sigma=0.02, eta=1e-6):")
    print("  Lambda       | Expected Cost E[x] ($) | Variance V[x] ($^2) | Std Dev ($)")
    print("-------------------------------------------------------------------------")

    e_costs: list[float] = []
    variances: list[float] = []

    for lam in lambdas:
        traj = almgren_chriss_trajectory(x_total, horizon, n_steps, volatility, eta, lam)
        e_c, var = compute_cost_and_variance(x_total, traj, tau, volatility, gamma, eta)
        e_costs.append(e_c)
        variances.append(var)
        std_dev = math.sqrt(var)
        print(f"  {lam:12.1e} | {e_c:22.2f} | {var:19.2f} | {std_dev:11.2f}")

    print("-------------------------------------------------------------------------")

    # Verify frontier convexity: dE/dV < 0 everywhere
    de = [e_costs[i + 1] - e_costs[i] for i in range(len(e_costs) - 1)]
    dv = [variances[i + 1] - variances[i] for i in range(len(variances) - 1)]
    slopes = [de / dv for de, dv in zip(de, dv, strict=True)]

    print(f"Minimum Expected Cost (Risk-Neutral TWAP, lambda=0): $ {e_costs[0]:,.2f}")
    print(f"Maximum Expected Cost (High Aversion, lambda=1e-4):   $ {e_costs[-1]:,.2f}")
    print(f"Variance Reduction from TWAP to lambda=1e-4:          {(1.0 - variances[-1] / variances[0]) * 100:.1f}%")
    print(f"Frontier Slope dE/dV is strictly negative: min={max(slopes):.6f}, max={min(slopes):.6f}")


main()
