"""Lab QR5-L04-1: Tabular RL Execution vs. Analytical Almgren-Chriss Benchmark.

Demonstrates:
1. Formulation of optimal liquidation under temporary and permanent price impact.
2. Derivation of the analytical Almgren-Chriss hyperbolic inventory trajectory.
3. Training of an execution policy to minimize risk-adjusted execution shortfall.
4. Trajectory tracking comparison between RL execution policy and closed-form AC solution.
"""

from __future__ import annotations

import math

import numpy as np


def almgren_chriss_trajectory(
    total_shares: float,
    n_steps: int,
    t_total: float,
    sigma: float,
    eta: float,
    risk_aversion: float,
) -> np.ndarray:
    """Compute analytical discrete Almgren-Chriss optimal inventory trajectory.

    kappa approx sqrt(lambda * sigma^2 / eta).
    x_j = X_0 * sinh(kappa * (T - t_j)) / sinh(kappa * T).
    """
    kappa = math.sqrt((risk_aversion * (sigma**2)) / eta)
    times = np.linspace(0.0, t_total, n_steps + 1)

    traj = np.zeros(n_steps + 1)
    sinh_total = math.sinh(kappa * t_total)
    for j in range(n_steps + 1):
        rem_time = t_total - times[j]
        traj[j] = total_shares * (math.sinh(kappa * rem_time) / sinh_total)
    traj[-1] = 0.0
    return traj


def main() -> None:
    x0 = 100.0  # 100 shares / lots
    n_steps = 5
    t_total = 1.0  # 1 day / period
    sigma = 0.20
    eta = 0.10  # temporary impact coefficient
    gamma_p = 0.05  # permanent impact coefficient
    risk_aversion = 0.50

    ac_traj = almgren_chriss_trajectory(x0, n_steps, t_total, sigma, eta, risk_aversion)

    # Dynamic Programming / Backward Induction RL on discrete execution grid
    # Inventory states: 0 to 100 in steps of 5
    inv_grid = np.linspace(0, x0, 21)
    v_table = np.zeros((len(inv_grid), n_steps + 1))
    best_action = np.zeros((len(inv_grid), n_steps), dtype=int)

    # Terminal stage t = n_steps: penalty for leftover inventory
    v_table[:, n_steps] = 1e6 * (inv_grid > 0)

    dt = t_total / n_steps

    for t in range(n_steps - 1, -1, -1):
        for i_idx, q in enumerate(inv_grid):
            min_cost = float("inf")
            best_a_idx = 0
            # Candidate actions: sell delta_q in [0, q]
            for a_idx, next_q in enumerate(inv_grid):
                if next_q <= q:
                    sold = q - next_q
                    trading_rate = sold / dt
                    # Temporary impact cost + permanent impact + variance penalty
                    temp_cost = eta * (trading_rate**2) * dt
                    perm_cost = 0.5 * gamma_p * (sold**2)
                    var_penalty = 0.5 * risk_aversion * (sigma**2) * (q**2) * dt
                    step_cost = temp_cost + perm_cost + var_penalty + v_table[a_idx, t + 1]

                    if step_cost < min_cost:
                        min_cost = step_cost
                        best_a_idx = a_idx

            v_table[i_idx, t] = min_cost
            best_action[i_idx, t] = best_a_idx

    # Forward rollout of optimal RL execution trajectory starting from x0
    rl_traj = np.zeros(n_steps + 1)
    rl_traj[0] = x0
    curr_idx = len(inv_grid) - 1

    for t in range(n_steps):
        next_idx = best_action[curr_idx, t]
        rl_traj[t + 1] = inv_grid[next_idx]
        curr_idx = next_idx

    rmse = float(np.sqrt(np.mean((rl_traj - ac_traj) ** 2)))
    max_dev = float(np.max(np.abs(rl_traj - ac_traj)))

    print("Step | AC Trajectory | RL Policy Trajectory")
    for step in range(n_steps + 1):
        print(f"{step:4d} | {ac_traj[step]:13.2f} | {rl_traj[step]:20.2f}")

    print(f"\nTrajectory RMSE vs. Almgren-Chriss: {rmse:.4f}")
    print(f"Maximum absolute deviation: {max_dev:.4f}")
    print(f"Terminal inventory under RL: {rl_traj[-1]:.2f}")


main()
