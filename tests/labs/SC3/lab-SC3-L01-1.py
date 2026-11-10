"""Lab 1 · Numerical verification of Girsanov's theorem and drift shifting.

Under the physical measure P, standard Brownian motion B_t has mean zero and variance t.
For a constant drift shift theta and horizon H, the process B_tilde_t = B_t + theta * t has
physical expectation E^P[B_tilde_H] = theta * H.
Weighting paths by the Doléans-Dade exponential martingale:
    Z_H = exp(-theta * B_H - (1/2) * theta^2 * H)
defines an equivalent measure Q under which B_tilde_t is a standard Brownian motion.
This lab verifies that E^P[Z_H] = 1, E^Q[B_tilde_H] = 0, and Var^Q(B_tilde_H) = H within
sampling error using 10,000 simulated paths (SIMULATED).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    seed = 42
    rng = random.Random(seed)
    n_paths = 10000
    horizon = 1.0
    theta = 0.75

    sq_h = math.sqrt(horizon)

    z_vals: list[float] = []
    b_tilde_vals: list[float] = []
    weighted_b_tilde: list[float] = []
    weighted_b_tilde_sq: list[float] = []

    for _ in range(n_paths):
        b_h = sq_h * rng.gauss(0.0, 1.0)
        b_tilde = b_h + theta * horizon
        # Radon-Nikodym derivative Z = exp(-theta * B_H - 0.5 * theta^2 * H)
        z = math.exp(-theta * b_h - 0.5 * (theta**2) * horizon)

        z_vals.append(z)
        b_tilde_vals.append(b_tilde)
        weighted_b_tilde.append(z * b_tilde)
        weighted_b_tilde_sq.append(z * (b_tilde**2))

    # Mean of Z under P (should equal 1)
    mean_z = sum(z_vals) / n_paths
    var_z = sum((x - mean_z) ** 2 for x in z_vals) / (n_paths - 1)
    se_z = math.sqrt(var_z / n_paths)

    # Physical expectation E^P[B_tilde_H] (should equal theta * H = 0.75)
    mean_p_btilde = sum(b_tilde_vals) / n_paths
    expected_p = theta * horizon

    # Measure Q expectation E^Q[B_tilde_H] = E^P[Z * B_tilde_H] (should equal 0)
    mean_q_btilde = sum(weighted_b_tilde) / n_paths
    var_q_btilde = sum((x - mean_q_btilde) ** 2 for x in weighted_b_tilde) / (n_paths - 1)
    se_q_btilde = math.sqrt(var_q_btilde / n_paths)

    # Measure Q second moment E^Q[B_tilde_H^2] = E^P[Z * B_tilde_H^2] (should equal H = 1.0)
    mean_q_sq = sum(weighted_b_tilde_sq) / n_paths

    print(f"horizon H: {horizon:.2f}, drift shift theta: {theta:.2f}")
    print(f"E^P[Z_H]: {mean_z:.6f} (se {se_z:.6f})")
    print(f"E^P[B_tilde_H]: {mean_p_btilde:.6f} (target {expected_p:.6f})")
    print(f"E^Q[B_tilde_H]: {mean_q_btilde:.6f} (se {se_q_btilde:.6f})")
    print(f"E^Q[B_tilde_H^2]: {mean_q_sq:.6f} (target {horizon:.6f})")
    print("Z martingale property |E[Z] - 1| <= 3*se:", abs(mean_z - 1.0) <= 3.0 * se_z)
    print("Q-Brownian zero drift |E^Q[B_tilde]| <= 3*se:", abs(mean_q_btilde) <= 3.0 * se_q_btilde)


main()
