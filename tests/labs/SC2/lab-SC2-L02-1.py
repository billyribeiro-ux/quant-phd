"""Lab 1 · Itô isometry and left-endpoint versus right-endpoint Riemann sums.

For the integrand H_s = B_s on [0, H], evaluating at the left endpoint t_k gives the Itô integral
sum_k B_{t_k} Delta B_k, whose expectation is identically zero. Evaluating at the right endpoint t_{k+1} is
anticipating: since B_{t_{k+1}} = B_{t_k} + Delta B_k, the product contains (Delta B_k)^2 whose expectation is
Delta t_k, so the sum has expectation H. This lab simulates 5,000 paths on a 50-step grid with H = 1.0 from seed 42
(SIMULATED), printing the sample means and standard errors for both sums alongside the theoretical values.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    horizon = 1.0
    n_steps = 50
    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    n_paths = 5000
    seed = 42

    rng = random.Random(seed)
    left_sums: list[float] = []
    right_sums: list[float] = []

    for _ in range(n_paths):
        b = 0.0
        s_left = 0.0
        s_right = 0.0
        for _ in range(n_steps):
            db = rng.gauss(0.0, sq_dt)
            b_next = b + db
            s_left += b * db
            s_right += b_next * db
            b = b_next
        left_sums.append(s_left)
        right_sums.append(s_right)

    mean_left = sum(left_sums) / n_paths
    var_left = sum((x - mean_left) ** 2 for x in left_sums) / (n_paths - 1)
    se_left = math.sqrt(var_left / n_paths)

    mean_right = sum(right_sums) / n_paths
    var_right = sum((x - mean_right) ** 2 for x in right_sums) / (n_paths - 1)
    se_right = math.sqrt(var_right / n_paths)

    print("theoretical mean (left endpoint, Itô): 0.000000")
    print(f"sample mean (left endpoint): {mean_left:.6f} (se {se_left:.6f})")
    print(f"theoretical mean (right endpoint, anticipating): {horizon:.6f}")
    print(f"sample mean (right endpoint): {mean_right:.6f} (se {se_right:.6f})")
    print("left mean within 5*se of 0:", abs(mean_left) <= 5.0 * se_left)
    print("right mean within 5*se of H:", abs(mean_right - horizon) <= 5.0 * se_right)


main()
