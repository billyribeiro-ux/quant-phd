"""Lab E6-L04-1: Forward solution of the New Keynesian Phillips Curve.

Iterates the NKPC forward for an AR(1) output gap process.
Demonstrates that the forward-looking inflation rate converges to its closed form
pi_t = (kappa / (1 - beta * rho)) * x_t, with truncation error decaying at geometric rate (beta * rho)^H.
"""

from __future__ import annotations


def solve_nkpc_truncated(beta: float, kappa: float, rho: float, x_0: float, horizon: int) -> float:
    """Compute the finite-horizon truncated forward sum for inflation."""
    return float(kappa * sum(((beta * rho) ** k) * x_0 for k in range(horizon)))


def solve_nkpc_exact(beta: float, kappa: float, rho: float, x_0: float) -> float:
    """Compute the exact infinite-horizon forward inflation: kappa * x_0 / (1 - beta * rho)."""
    return float(kappa * x_0 / (1.0 - beta * rho))


def main() -> None:
    beta = 0.99  # Quarterly discount factor
    kappa = 0.1275  # Composite Phillips curve slope
    rho = 0.6  # Output gap persistence
    x_0 = 0.05  # 5% initial output gap deviation

    pi_exact = solve_nkpc_exact(beta, kappa, rho, x_0)

    print(f"NKPC forward solution parameters (beta={beta}, kappa={kappa}, rho={rho}, x_0={x_0}):")
    print(f"  Exact infinite-horizon inflation pi*: {pi_exact:.6f}")
    print("\nForward horizon truncation analysis:")

    horizons = [4, 8, 12, 16, 20]
    for h in horizons:
        pi_trunc = solve_nkpc_truncated(beta, kappa, rho, x_0, h)
        num_err = abs(pi_exact - pi_trunc)
        th_err = abs(kappa * (((beta * rho) ** h) * x_0) / (1.0 - beta * rho))
        diff = abs(num_err - th_err)

        print(
            f"  H = {h:2d}: pi_trunc = {pi_trunc:9.6f}, "
            f"error = {num_err:10.6e}, "
            f"theoretical = {th_err:10.6e}, "
            f"discrepancy = {diff:.2e}"
        )


main()
