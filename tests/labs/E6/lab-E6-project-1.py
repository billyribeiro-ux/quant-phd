"""Lab E6-project-1: Project Rung 1 worked example for the New Keynesian model solver.

Step-by-step fully annotated walkthrough solving:
1. Equilibrium determinacy via the generalized Taylor principle.
2. Undetermined coefficients for demand and policy disturbances.
3. Impulse response functions over horizon H = 3.
Model output, no data.
"""

from __future__ import annotations


def main() -> None:
    # Model parameters
    beta = 0.99
    sigma = 1.0
    kappa = 0.1
    phi_pi = 1.5
    phi_y = 0.5
    rho = 0.5
    horizon = 3

    print("Rung 1: Worked Example - Solving the Canonical New Keynesian Model")
    print("Parameters: beta=0.99, sigma=1.0, kappa=0.1, phi_pi=1.5, phi_y=0.5, rho=0.5")

    # Step 1: Check equilibrium determinacy
    # Why: In a forward-looking model, determinacy requires that nominal rate policy raises
    # the real interest rate in response to inflation, eliminating self-fulfilling sunspot fluctuations.
    taylor_metric = kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y
    is_determinate = taylor_metric > 0.0
    print(f"\nStep 1: Determinacy check: metric = {taylor_metric:.4f} > 0 -> {is_determinate}")

    # Step 2: Undetermined coefficients
    # Why: Substituting linear guesses x_t = b * u_t and pi_t = a * u_t into the dynamic IS and NKPC
    # gives a 2x2 linear system with determinant Delta.
    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    b_demand = (1.0 - beta * rho) / delta
    a_demand = kappa / delta

    b_policy = -(1.0 - beta * rho) / delta
    a_policy = -kappa / delta

    print(f"Step 2: Denominator Delta = {delta:.6f}")
    print(f"  Demand shock coefficients: b_d = {b_demand:.6f}, a_d = {a_demand:.6f}")
    print(f"  Policy shock coefficients: b_v = {b_policy:.6f}, a_v = {a_policy:.6f}")

    # Step 3: Compute impulse response paths
    # Why: For an AR(1) shock u_t = rho^t, variables decay along geometric paths.
    print(f"\nStep 3: Impulse response paths for horizon H = {horizon}:")
    print("  Date | Demand: x_t    pi_t     i_t    | Policy: x_t    pi_t     i_t")
    print("  -----+--------------------------------+-------------------------------")
    for t in range(horizon + 1):
        u_t = rho**t
        # Demand shock
        xd = b_demand * u_t
        pid = a_demand * u_t
        id_val = phi_pi * pid + phi_y * xd
        # Policy shock
        xv = b_policy * u_t
        piv = a_policy * u_t
        iv_val = phi_pi * piv + phi_y * xv + u_t

        print(f"  {t:4d} |        {xd:7.4f}  {pid:7.4f}  {id_val:7.4f} |        {xv:7.4f}  {piv:7.4f}  {iv_val:7.4f}")


main()
