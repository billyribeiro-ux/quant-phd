"""Lab 1 · Picard iteration for the Ornstein-Uhlenbeck SDE on a fixed Brownian path.

Under global Lipschitz and linear growth conditions, the Picard iteration X^{(0)}_t = x0, X^{(n+1)}_t = x0 +
int_0^t b(s, X^{(n)}_s) ds + int_0^t sigma(s, X^{(n)}_s) dB_s converges uniformly on compact intervals to the unique
solution. For the OU equation dX_t = kappa(theta - X_t) dt + sigma dB_t, the Picard map contracts geometrically. This
lab generates one fixed Brownian path with N = 100 steps over [0, 1] from seed 42 (SIMULATED), computes successive
Picard iterates n = 1 through 6, and prints the supremum norm error sup_{t in [0, 1]} |X^{(n)}_t - X^{exact}_t| against
the reference path, demonstrating geometric contraction.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    x0 = 0.5
    kappa = 2.0
    theta = 1.0
    sigma = 0.30
    horizon = 1.0
    n_steps = 100
    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    seed = 42

    rng = random.Random(seed)
    b_path = [0.0]
    for _ in range(n_steps):
        b_path.append(b_path[-1] + rng.gauss(0.0, sq_dt))

    # Reference exact path
    x_exact = [x0]
    for k in range(n_steps):
        db = b_path[k + 1] - b_path[k]
        x_val = x_exact[-1] + kappa * (theta - x_exact[-1]) * dt + sigma * db
        x_exact.append(x_val)

    # Picard iterates: X^{(0)}_k = x0
    x_n = [x0] * (n_steps + 1)
    print("Picard iterate supremum errors on [0, 1]:")
    for it in range(1, 7):
        x_iter_path = [x0]
        for k in range(1, n_steps + 1):
            int_x = sum(x_n[j] for j in range(k)) * dt
            val = x0 + kappa * theta * (k * dt) - kappa * int_x + sigma * b_path[k]
            x_iter_path.append(val)
        sup_err = max(abs(x_iter_path[k] - x_exact[k]) for k in range(n_steps + 1))
        print(f"iterate {it}: sup-error = {sup_err:.6e}")
        x_n = x_iter_path


main()
