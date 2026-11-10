r"""Lab 1 · Verification inequality: candidate value function dominates arbitrary controls.

Demonstrates the verification inequality: for a C^{1,2} solution v(t, w) of the HJB equation
with terminal condition v(T, w) = g(w), v(0, w_0) >= J(0, w_0; pi) for all admissible control
processes, with equality achieved if and only if pi matches the optimal feedback policy pi*.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Model parameters (SIMULATED)
    seed = 42
    rng = random.Random(seed)

    r = 0.02
    mu = 0.08
    sigma = 0.20
    gamma = 2.0
    t_horiz = 1.0
    w0 = 1.0

    # Unconstrained optimal Merton fraction and growth rate
    pi_star = (mu - r) / (gamma * (sigma**2))
    k_star = r + 0.5 * ((mu - r) ** 2) / (gamma * (sigma**2))

    # Analytical value function at t=0: V(0, w0) = exp((1 - gamma) * k_star * T) * w0^(1 - gamma) / (1 - gamma)
    v0_exact = math.exp((1.0 - gamma) * k_star * t_horiz) * (w0 ** (1.0 - gamma)) / (1.0 - gamma)

    n_paths = 15000
    z_draws = [rng.gauss(0.0, 1.0) for _ in range(n_paths)]

    pi_candidates = [0.0, 0.35, pi_star, 1.0, 1.25]

    print(f"V(0, w0) candidate exact: {v0_exact:.5f}")
    print(f"theoretical optimal fraction pi*: {pi_star:.4f}")

    all_dominated = True
    opt_matched = False

    for pi in pi_candidates:
        drift = (r + pi * (mu - r) - 0.5 * (pi * sigma) ** 2) * t_horiz
        vol = pi * sigma * math.sqrt(t_horiz)
        payoffs = [(w0 * math.exp(drift + vol * z)) ** (1.0 - gamma) / (1.0 - gamma) for z in z_draws]
        mean_j = sum(payoffs) / n_paths
        se_j = math.sqrt(sum((x - mean_j) ** 2 for x in payoffs) / (n_paths - 1) / n_paths)

        diff = v0_exact - mean_j  # For gamma > 1, higher reward means less negative, so v0 >= J => v0 - J >= 0
        is_close = abs(diff) <= 2.5 * se_j

        if pi == pi_star:
            opt_matched = is_close
        else:
            if diff < -2.0 * se_j:
                all_dominated = False

        print(f"pi = {pi:5.3f}: J = {mean_j:.5f} (se {se_j:.5f}), deficit = {diff:+.5f}")

    print(f"candidate value function weakly dominates all controls: {all_dominated}")
    print(f"candidate value matches optimal expected payoff within sampling error: {opt_matched}")


main()
