"""Lab E6-L06-1: Solving linear rational-expectations systems by undetermined coefficients.

Sets up the 2x2 linear system for the undetermined coefficients (a, b) mapping the
natural real rate shock u_t to inflation (pi_t = a * u_t) and the output gap (x_t = b * u_t).
Solves the system in exact rational arithmetic (fractions.Fraction) and standard floats,
and verifies exact equation substitution residuals.
"""

from __future__ import annotations

from fractions import Fraction


def solve_linear_re_fraction(
    beta: Fraction,
    sigma: Fraction,
    kappa: Fraction,
    phi_pi: Fraction,
    phi_y: Fraction,
    rho: Fraction,
) -> tuple[Fraction, Fraction, Fraction]:
    """Solve undetermined coefficients in exact arithmetic."""
    # Matrix elements for M * [a, b]^T = [0, 1]^T
    m11 = Fraction(1) - beta * rho
    m12 = -kappa
    m21 = phi_pi - rho
    m22 = sigma * (Fraction(1) - rho) + phi_y

    det = m11 * m22 - m12 * m21
    if det == Fraction(0):
        raise ValueError("Singular system: cannot solve undetermined coefficients.")

    # Cramer's rule / 2x2 matrix inversion
    a = kappa / det
    b = m11 / det
    return a, b, det


def main() -> None:
    # -------------------------------------------------------------
    # Exact rational solve
    # -------------------------------------------------------------
    beta_q = Fraction(99, 100)
    sigma_q = Fraction(1, 1)
    kappa_q = Fraction(1, 10)
    phi_pi_q = Fraction(3, 2)
    phi_y_q = Fraction(1, 2)
    rho_q = Fraction(1, 2)

    a_q, b_q, det_q = solve_linear_re_fraction(beta_q, sigma_q, kappa_q, phi_pi_q, phi_y_q, rho_q)

    # Substitution check: M * [a, b]^T - [0, 1]^T == [0, 0]^T
    m11_q = Fraction(1) - beta_q * rho_q
    m12_q = -kappa_q
    m21_q = phi_pi_q - rho_q
    m22_q = sigma_q * (Fraction(1) - rho_q) + phi_y_q

    res1_q = m11_q * a_q + m12_q * b_q
    res2_q = m21_q * a_q + m22_q * b_q - Fraction(1)

    print("Exact rational solution (fractions.Fraction):")
    print(f"  Determinant Delta: {det_q}")
    print(f"  Inflation coefficient a: {a_q} ({float(a_q):.8f})")
    print(f"  Output gap coefficient b: {b_q} ({float(b_q):.8f})")
    print(f"  System residual 1 (NKPC): {res1_q}")
    print(f"  System residual 2 (IS-TR): {res2_q}")

    # -------------------------------------------------------------
    # Floating point comparison
    # -------------------------------------------------------------
    a_f = float(a_q)
    b_f = float(b_q)
    m11_f = float(m11_q)
    m12_f = float(m12_q)
    m21_f = float(m21_q)
    m22_f = float(m22_q)

    res1_f = m11_f * a_f + m12_f * b_f
    res2_f = m21_f * a_f + m22_f * b_f - 1.0

    print("\nFloating point evaluation and substitution residuals:")
    print(f"  Residual 1: {res1_f:.2e}")
    print(f"  Residual 2: {res2_f:.2e}")


main()
