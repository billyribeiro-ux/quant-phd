"""Lab E6-L05-1: Three-equation New Keynesian model: residual verification along a shock path.

Computes the equilibrium trajectory of the output gap, inflation, and policy rate
under an AR(1) natural real rate disturbance. Verifies that the dynamic IS curve,
the New Keynesian Phillips curve, and the contemporaneous Taylor rule hold with
zero residual at every date.
"""

from __future__ import annotations


def solve_undetermined_coefficients(
    beta: float, sigma: float, kappa: float, phi_pi: float, phi_y: float, rho: float
) -> tuple[float, float]:
    """Analytical undetermined coefficients for AR(1) natural rate shock."""
    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    b = (1.0 - beta * rho) / delta
    a = kappa / delta
    return b, a


def main() -> None:
    beta = 0.99
    sigma = 1.0
    kappa = 0.1
    phi_pi = 1.5
    phi_y = 0.5
    rho = 0.5
    r_n_0 = 1.0

    b, a = solve_undetermined_coefficients(beta, sigma, kappa, phi_pi, phi_y, rho)
    print("Three-equation NK model calibration:")
    print(f"  beta={beta}, sigma={sigma}, kappa={kappa}, phi_pi={phi_pi}, phi_y={phi_y}, rho={rho}")
    print(f"  Coefficients: b (output gap) = {b:.6f}, a (inflation) = {a:.6f}")
    print("\nTrajectory and equation residuals along shock path:")

    max_res = 0.0
    for t in range(6):
        rn_t = r_n_0 * (rho**t)
        rn_next = r_n_0 * (rho ** (t + 1))

        xt = b * rn_t
        pit = a * rn_t
        it = phi_pi * pit + phi_y * xt

        xt_next = b * rn_next
        pit_next = a * rn_next

        # Equation residuals
        res_is = xt - xt_next + (1.0 / sigma) * (it - pit_next - rn_t)
        res_nk = pit - beta * pit_next - kappa * xt
        res_tr = it - (phi_pi * pit + phi_y * xt)

        current_max = max(abs(res_is), abs(res_nk), abs(res_tr))
        if current_max > max_res:
            max_res = current_max

        print(
            f"  t={t}: r^n={rn_t:6.4f}, x={xt:6.4f}, pi={pit:6.4f}, i={it:6.4f} | "
            f"residuals: IS={res_is:9.2e}, NKPC={res_nk:9.2e}, TR={res_tr:9.2e}"
        )

    print(f"\nMaximum absolute residual across all dates: {max_res:.2e}")


main()
