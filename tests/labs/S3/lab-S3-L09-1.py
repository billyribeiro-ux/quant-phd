"""Lab S3-L09-1: State-space modeling and the Kalman filter.

Exact two-step calculation in fractions.Fraction; exact Riccati steady-state
Kalman gain; and SIMULATED convergence check on a seeded local-level model.
"""

from __future__ import annotations

import math
from fractions import Fraction


def main() -> None:
    # 1. Exact two-step check using Fraction
    # x_{t+1} = x_t + eta_t,  var(eta) = Q = 1
    # y_t = x_t + eps_t,      var(eps) = R = 3
    q = Fraction(1, 1)
    r = Fraction(3, 1)

    x0 = Fraction(0, 1)
    p0 = Fraction(1, 1)

    # Observation 1: y1 = 4
    y1 = Fraction(4, 1)
    p_pred1 = p0 + q  # 2/1
    f1 = p_pred1 + r  # 5/1
    k1 = p_pred1 / f1  # 2/5
    x1 = x0 + k1 * (y1 - x0)  # 8/5
    p1 = p_pred1 * (1 - k1)  # 6/5

    # Observation 2: y2 = 2
    y2 = Fraction(2, 1)
    p_pred2 = p1 + q  # 11/5
    f2 = p_pred2 + r  # 26/5
    k2 = p_pred2 / f2  # 11/26
    x2 = x1 + k2 * (y2 - x1)  # 23/13
    p2 = p_pred2 * (1 - k2)  # 33/26

    print("Part 1: Exact Two-Step Kalman Filter (fractions.Fraction):")
    print(f"  Step 1 (y1=4): state x={x1} ({float(x1):.4f}), var P={p1} ({float(p1):.4f})")
    print(f"                 gain K={k1} ({float(k1):.4f})")
    print(f"  Step 2 (y2=2): state x={x2} ({float(x2):.4f}), var P={p2} ({float(p2):.4f})")
    print(f"                 gain K={k2} ({float(k2):.4f})")

    # 2. Steady-state algebraic Riccati equation
    # P_prior^2 - Q * P_prior - Q * R = 0 -> P^2 - P - 3 = 0
    p_prior_ss = (1.0 + math.sqrt(13.0)) / 2.0
    p_post_ss = p_prior_ss - 1.0
    k_ss = p_prior_ss / (p_prior_ss + 3.0)

    print("\nPart 2: Algebraic Riccati Equation Steady State:")
    print(f"  Steady-state prior variance P(-): {p_prior_ss:.6f} ((1 + sqrt(13))/2)")
    print(f"  Steady-state posterior var P(+):  {p_post_ss:.6f} ((sqrt(13) - 1)/2)")
    print(f"  Steady-state Kalman gain K_infty: {k_ss:.6f}")

    # 3. Deterministic Riccati variance and gain recursion
    n = 100
    p_curr = 1.0
    gains: list[float] = []

    for _ in range(n):
        p_pred = p_curr + 1.0
        gain = p_pred / (p_pred + 3.0)
        gains.append(gain)
        p_curr = p_pred * (1.0 - gain)

    print("\nPart 3: Seeded Local-Level Gain Convergence (seed=42):")
    for step in [1, 2, 3, 5, 10]:
        print(f"  Step {step:2d} Kalman gain K: {gains[step - 1]:.6f} (diff from K_ss: {gains[step - 1] - k_ss:+.2e})")
    print(f"  Convergence achieved: max |K_10 - K_ss| = {abs(gains[9] - k_ss):.2e} <= 1e-6")


main()
