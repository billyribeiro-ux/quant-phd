r"""Lab 1 · Martingale optimality property of the controlled value process.

Demonstrates that along the optimal state trajectory X_t*, the discounted value process
M_t* = e^(-rho t) V(X_t*) + \int_0^t e^(-rho s) f(X_s*, u_s*) ds is a true martingale
with E[M_t*] = V(X_0) for all t. For any suboptimal policy, the process is a supermartingale,
so E[M_t] <= V(X_0).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Model parameters (SIMULATED)
    seed = 42
    rng = random.Random(seed)

    rho = 0.05
    q = 2.0
    sigma = 0.30
    x0 = 1.0

    # Riccati solution for quadratic regulator: P^2 + rho P - q = 0
    p_param = (-rho + math.sqrt(rho**2 + 4.0 * q)) / 2.0
    k_param = (0.5 * p_param * (sigma**2)) / rho

    def value(x: float) -> float:
        # Negative cost function: reward maximization
        return -(0.5 * p_param * (x**2) + k_param)

    v0 = value(x0)

    n_paths = 10000
    n_steps = 50
    t_horiz = 1.0
    dt = t_horiz / n_steps
    sq_dt = math.sqrt(dt)

    paths_opt = [x0] * n_paths
    paths_sub = [x0] * n_paths

    cum_reward_opt = [0.0] * n_paths
    cum_reward_sub = [0.0] * n_paths

    for step in range(n_steps):
        t_curr = step * dt
        disc = math.exp(-rho * t_curr)

        for i in range(n_paths):
            # Optimal control: u*(x) = -P x
            x_opt = paths_opt[i]
            u_opt = -p_param * x_opt
            rew_opt = -(0.5 * (u_opt**2) + 0.5 * q * (x_opt**2))
            cum_reward_opt[i] += disc * rew_opt * dt

            # Suboptimal zero-control: u_sub(x) = 0
            x_sub = paths_sub[i]
            u_sub = 0.0
            rew_sub = -(0.5 * (u_sub**2) + 0.5 * q * (x_sub**2))
            cum_reward_sub[i] += disc * rew_sub * dt

            z = rng.gauss(0.0, 1.0)
            paths_opt[i] = x_opt + u_opt * dt + sigma * sq_dt * z
            paths_sub[i] = x_sub + u_sub * dt + sigma * sq_dt * z

    disc_t = math.exp(-rho * t_horiz)
    m_opt = [cum_reward_opt[i] + disc_t * value(paths_opt[i]) for i in range(n_paths)]
    m_sub = [cum_reward_sub[i] + disc_t * value(paths_sub[i]) for i in range(n_paths)]

    mean_opt = sum(m_opt) / n_paths
    mean_sub = sum(m_sub) / n_paths
    se_opt = math.sqrt(sum((x - mean_opt) ** 2 for x in m_opt) / (n_paths - 1) / n_paths)

    print(f"V(x0) exact: {v0:.4f}")
    print(f"E[M_T*] (optimal): {mean_opt:.4f} (se {se_opt:.4f})")
    print(f"E[M_T] (suboptimal): {mean_sub:.4f}")
    print(f"martingale preserved under optimal control: {abs(mean_opt - v0) <= 5.0 * se_opt}")
    print(f"supermartingale deficit under suboptimal control: {v0 - mean_sub:.4f}")


main()
