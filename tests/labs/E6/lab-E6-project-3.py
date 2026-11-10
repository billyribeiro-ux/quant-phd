"""Lab E6-project-3: Rung 3 reference verification check on seed 0.

Evaluates the canonical New Keynesian model solver on the seed 0 instance parameters:
beta=0.9725, sigma=1.27, kappa=0.319, phi_pi=1.861, phi_y=0.338, rho=-0.313.
Prints the determinacy certificate, impact coefficients, and the five-period impulse response table
that an independent implementation must match.
Model output, no data.
"""

from __future__ import annotations


def solve_undetermined_coefficients(
    beta: float, sigma: float, kappa: float, phi_pi: float, phi_y: float, rho: float
) -> tuple[bool, float, float, float, float]:
    det_metric = kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y
    is_det = det_metric > 0.0

    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    b_demand = (1.0 - beta * rho) / delta
    a_demand = kappa / delta

    b_policy = -(1.0 - beta * rho) / delta
    a_policy = -kappa / delta

    return is_det, b_demand, a_demand, b_policy, a_policy


def main() -> None:
    # Seed 0 instance parameters
    beta = 0.9725
    sigma = 1.27
    kappa = 0.319
    phi_pi = 1.861
    phi_y = 0.338
    rho = -0.313
    horizon = 4

    is_det, b_d, a_d, b_v, a_v = solve_undetermined_coefficients(beta, sigma, kappa, phi_pi, phi_y, rho)

    print("Rung 3 Solver Verification (Seed 0 Parameter Set):")
    print(f"  beta={beta}, sigma={sigma}, kappa={kappa}, phi_pi={phi_pi}, phi_y={phi_y}, rho={rho}")
    print(f"  Equilibrium determinacy: {is_det}")
    print(f"  Demand coefficients: b_d = {b_d:.6f}, a_d = {a_d:.6f}")
    print(f"  Policy coefficients: b_v = {b_v:.6f}, a_v = {a_v:.6f}")

    print("\nImpulse Response Trajectory (dates 0 to 4):")
    print("  Date | Demand: x_t    pi_t     i_t    | Policy: x_t    pi_t     i_t")
    print("  -----+--------------------------------+-------------------------------")

    for t in range(horizon + 1):
        u_t = rho**t
        xd = b_d * u_t
        pid = a_d * u_t
        id_val = phi_pi * pid + phi_y * xd

        xv = b_v * u_t
        piv = a_v * u_t
        iv_val = phi_pi * piv + phi_y * xv + u_t

        print(f"  {t:4d} |        {xd:7.4f}  {pid:7.4f}  {id_val:7.4f} |        {xv:7.4f}  {piv:7.4f}  {iv_val:7.4f}")


main()
