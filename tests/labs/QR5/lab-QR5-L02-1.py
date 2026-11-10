"""Lab QR5-L02-1: Tabular Q-Learning Convergence vs. Exact Bellman Optimality.

Demonstrates:
1. Implementation of Temporal Difference Q-learning on a trade execution MDP.
2. Decay of TD root-mean-squared error over training episodes.
3. Convergence of empirical Q-table to the analytical Bellman fixed-point Q*(s, a).
"""

from __future__ import annotations

import numpy as np


def compute_exact_q_values(
    n_inventory: int,
    n_times: int,
    gamma: float,
    terminal_penalty: float = 1.5,
) -> np.ndarray:
    """Compute exact analytical Q*(s, a) via backward dynamic programming."""
    v = np.zeros((n_inventory, n_times))
    q_table = np.full((n_inventory, n_times, n_inventory), -1e9)

    # Terminal stage
    for q in range(n_inventory):
        v[q, n_times - 1] = -terminal_penalty * (q**2)
        q_table[q, n_times - 1, q] = -terminal_penalty * (q**2)

    for t in range(n_times - 2, -1, -1):
        for q in range(n_inventory):
            for a in range(q + 1):
                reward = a * 10.0 - 0.5 * (a**2)
                next_q = q - a
                q_val = reward + gamma * v[next_q, t + 1]
                q_table[q, t, a] = q_val
            valid_vals = [q_table[q, t, a] for a in range(q + 1)]
            v[q, t] = max(valid_vals)

    return q_table


def main() -> None:
    n_inventory = 4
    n_times = 3
    gamma = 0.90
    q_exact = compute_exact_q_values(n_inventory, n_times, gamma)

    # Tabular Q-learning
    q_learned = np.zeros((n_inventory, n_times, n_inventory))
    rng = np.random.default_rng(42)

    n_episodes = 25000
    alpha_0 = 0.2
    epsilon_0 = 0.5

    td_errors: list[float] = []

    for ep in range(n_episodes):
        alpha = alpha_0 / (1.0 + 0.0001 * ep)
        eps = epsilon_0 / (1.0 + 0.0002 * ep)

        # Start from random inventory and t=0
        q = int(rng.integers(1, n_inventory))
        t = 0

        while t < n_times - 1 and q > 0:
            # Epsilon-greedy action
            a = int(rng.integers(0, q + 1)) if rng.uniform() < eps else int(np.argmax(q_learned[q, t, : q + 1]))

            reward = a * 10.0 - 0.5 * (a**2)
            next_q = q - a
            next_t = t + 1

            if next_t == n_times - 1:
                target = reward + gamma * (-1.5 * (next_q**2))
            else:
                next_best = float(np.max(q_learned[next_q, next_t, : next_q + 1]))
                target = reward + gamma * next_best

            td_err = target - q_learned[q, t, a]
            q_learned[q, t, a] += alpha * td_err
            td_errors.append(abs(td_err))

            q = next_q
            t = next_t

    # Compare learned Q-values with exact values on reachable states
    errors = []
    for t in range(n_times - 1):
        for q in range(1, n_inventory):
            for a in range(q + 1):
                err = abs(q_learned[q, t, a] - q_exact[q, t, a])
                errors.append(err)

    mean_abs_err = float(np.mean(errors))
    max_abs_err = float(np.max(errors))
    mean_late_td = float(np.mean(td_errors[-1000:]))

    print(f"Mean absolute error vs. Bellman exact: {mean_abs_err:.4f}")
    print(f"Max absolute error: {max_abs_err:.4f}")
    print(f"Late training mean TD error: {mean_late_td:.4f}")
    print(f"Learned optimal action a*(q=3, t=0): {int(np.argmax(q_learned[3, 0, :4]))}")
    print(f"Exact optimal action a*(q=3, t=0): {int(np.argmax(q_exact[3, 0, :4]))}")


main()
