"""Lab QR5-L01-1: Bellman Optimality & Contraction Property in Inventory MDP.

Demonstrates:
1. Formulation of an optimal liquidation MDP with inventory and price state.
2. Numerical verification of the Bellman operator contraction mapping property:
   ||T(V1) - T(V2)||_inf <= gamma * ||V1 - V2||_inf.
3. Convergence of Value Iteration to the unique fixed-point value function V*.
"""

from __future__ import annotations

import numpy as np


def bellman_operator(
    v: np.ndarray,
    n_inventory: int,
    n_times: int,
    gamma: float,
    terminal_penalty: float = 1.5,
) -> tuple[np.ndarray, np.ndarray]:
    """Applies Bellman optimality operator T(V) to value function matrix V."""
    tv = np.zeros_like(v)
    policy = np.zeros_like(v, dtype=int)

    # Terminal stage t = n_times - 1: must liquidate all remaining inventory
    for q in range(n_inventory):
        # Penalty for unliquidated inventory at maturity
        tv[q, n_times - 1] = -terminal_penalty * (q**2)
        policy[q, n_times - 1] = q

    # Backward induction from t = n_times - 2 down to 0
    for t in range(n_times - 2, -1, -1):
        for q in range(n_inventory):
            best_val = -float("inf")
            best_a = 0
            # Action: number of units to sell, a in [0, q]
            for a in range(q + 1):
                # Immediate reward: revenue minus quadratic execution friction
                reward = a * 10.0 - 0.5 * (a**2)
                # Next inventory state is deterministic: q - a
                next_q = q - a
                val = reward + gamma * v[next_q, t + 1]
                if val > best_val:
                    best_val = val
                    best_a = a
            tv[q, t] = best_val
            policy[q, t] = best_a

    return tv, policy


def main() -> None:
    n_inventory = 5
    n_times = 4
    gamma = 0.95

    # 1. Verify Contraction Mapping Property
    rng = np.random.default_rng(42)
    v1 = rng.normal(0.0, 5.0, size=(n_inventory, n_times))
    v2 = rng.normal(0.0, 5.0, size=(n_inventory, n_times))

    tv1, _ = bellman_operator(v1, n_inventory, n_times, gamma)
    tv2, _ = bellman_operator(v2, n_inventory, n_times, gamma)

    dist_input = float(np.max(np.abs(v1 - v2)))
    dist_output = float(np.max(np.abs(tv1 - tv2)))
    empirical_ratio = dist_output / dist_input

    # 2. Value Iteration to Fixed Point
    v = np.zeros((n_inventory, n_times))
    tol = 1e-8
    diff = 1.0
    iterations = 0
    while diff > tol and iterations < 100:
        tv, pol = bellman_operator(v, n_inventory, n_times, gamma)
        diff = float(np.max(np.abs(tv - v)))
        v = tv
        iterations += 1

    print(f"Contraction property holds: {dist_output <= gamma * dist_input}")
    print(f"Empirical contraction ratio: {empirical_ratio:.6f} <= gamma={gamma:.2f}")
    print(f"Value iteration converged in: {iterations} iterations")
    print(f"Optimal V*(q=4, t=0): {v[4, 0]:.4f}")
    print(f"Optimal action a*(q=4, t=0): {pol[4, 0]}")


main()
