"""Lab 1 · Discrete algebraic identity backing Itô's lemma for B_t^2.

For any discrete path, the telescoping identity B_H^2 - B_0^2 = sum_k (B_{t_{k+1}}^2 - B_{t_k}^2) factors algebraically
as 2 sum_k B_{t_k} Delta B_k + sum_k (Delta B_k)^2. This identity holds pathwise without limits. In the continuous
limit, the second term converges in L^2 to the quadratic variation [B, B]_H = H, establishing
d(B_t^2) = 2 B_t dB_t + dt. This lab simulates one Brownian path with N = 1,000 steps over [0, 1] from seed 42
(SIMULATED), evaluates the discrete sums, prints the exact algebraic residual to machine precision, and compares the sum
of squared increments to H.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    horizon = 1.0
    n_steps = 1000
    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    seed = 42

    rng = random.Random(seed)
    b = 0.0
    cross_sum = 0.0
    quad_var = 0.0

    for _ in range(n_steps):
        db = rng.gauss(0.0, sq_dt)
        cross_sum += b * db
        quad_var += db * db
        b += db

    b_sq = b * b
    identity_rhs = 2.0 * cross_sum + quad_var
    residual = abs(b_sq - identity_rhs)

    print(f"terminal B_H: {b:.6f}, B_H^2: {b_sq:.6f}")
    print(f"cross term 2 * sum(B_k * dB_k): {2.0 * cross_sum:.6f}")
    print(f"sum of squared increments sum(dB_k^2): {quad_var:.6f}")
    print(f"exact pathwise residual: {residual:.2e}")
    print(f"difference |sum(dB_k^2) - H|: {abs(quad_var - horizon):.6f}")
    print("residual within 1e-12:", residual < 1e-12)


main()
