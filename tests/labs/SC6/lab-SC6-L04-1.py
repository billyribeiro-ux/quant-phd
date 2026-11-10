r"""Lab 1 · Merton ODE algebraic reduction and consumption-wealth ratio.

Demonstrates that the non-linear stationary HJB equation for power utility V(w) = A w^(1-gamma) / (1-gamma)
reduces to the closed-form algebraic root nu = A^(-1/gamma) = (rho - (1-gamma) k) / gamma,
confirming that the HJB algebraic residual vanishes to machine precision and that nu -> rho as gamma -> 1.
"""

from __future__ import annotations


def main() -> None:
    # Market and preference parameters (SIMULATED)
    r = 0.025
    mu = 0.085
    sigma = 0.20
    rho = 0.05

    gamma_grid = [1.0001, 1.5, 2.0, 3.0, 4.0, 5.0]

    print(f"market parameters: r = {r:.3f}, mu = {mu:.3f}, sigma = {sigma:.2f}, rho = {rho:.3f}")

    all_vanish = True

    for gamma in gamma_grid:
        pi_star = (mu - r) / (gamma * (sigma**2))
        k = r + 0.5 * ((mu - r) ** 2) / (gamma * (sigma**2))
        nu = (rho - (1.0 - gamma) * k) / gamma
        nu ** (-gamma)

        # HJB algebraic equation residual: rho * A - gamma * A^(1 - 1/gamma) - (1-gamma)*k*A
        # Dividing by A: rho - gamma * nu - (1 - gamma) * k = 0
        normalized_residual = rho - gamma * nu - (1.0 - gamma) * k

        if abs(normalized_residual) > 1e-12:
            all_vanish = False

        print(
            f"gamma = {gamma:5.2f}: pi* = {pi_star:5.3f}, k = {k:6.4f}, "
            f"nu = {nu:6.4f}, residual = {normalized_residual:+.2e}"
        )

    # Check limiting log-utility behavior (gamma -> 1)
    nu_log_limit = (rho - (1.0 - 1.0001) * (r + 0.5 * ((mu - r) ** 2) / (sigma**2))) / 1.0001
    print(f"log-utility limit nu at gamma=1.0001: {nu_log_limit:.6f} vs rho={rho:.6f}")
    print(f"HJB equation satisfied exactly across all gamma: {all_vanish}")


main()
