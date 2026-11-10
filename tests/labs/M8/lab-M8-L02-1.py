"""Lab M8-L02-1: Conditioning and stability of a linear system.

Exact arithmetic using fractions.Fraction. Computes the exact condition number
and compares the theoretical error bound to the observed solution error under perturbation.
"""

from __future__ import annotations

from fractions import Fraction


def inf_norm_matrix(a11: Fraction, a12: Fraction, a21: Fraction, a22: Fraction) -> Fraction:
    """Maximum row sum norm."""
    r1 = abs(a11) + abs(a12)
    r2 = abs(a21) + abs(a22)
    return max(r1, r2)


def inf_norm_vector(v1: Fraction, v2: Fraction) -> Fraction:
    """Maximum absolute entry norm."""
    return max(abs(v1), abs(v2))


def solve_2x2(
    a11: Fraction, a12: Fraction, a21: Fraction, a22: Fraction, b1: Fraction, b2: Fraction
) -> tuple[Fraction, Fraction]:
    """Solve 2x2 linear system via Cramer's rule in exact arithmetic."""
    det = a11 * a22 - a12 * a21
    if det == 0:
        raise ValueError("Matrix is singular")
    x1 = (b1 * a22 - a12 * b2) / det
    x2 = (a11 * b2 - b1 * a21) / det
    return x1, x2


def invert_2x2(
    a11: Fraction, a12: Fraction, a21: Fraction, a22: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Inverse of 2x2 matrix."""
    det = a11 * a22 - a12 * a21
    if det == 0:
        raise ValueError("Matrix is singular")
    return a22 / det, -a12 / det, -a21 / det, a11 / det


def main() -> None:
    # A = [[1, 1], [1, 1 - eps]] with eps = 1/10000
    eps = Fraction(1, 10_000)
    a11, a12 = Fraction(1, 1), Fraction(1, 1)
    a21, a22 = Fraction(1, 1), Fraction(1, 1) - eps

    # b = [2, 2 - eps], exact solution x = [1, 1]
    b1, b2 = Fraction(2, 1), Fraction(2, 1) - eps
    x1, x2 = solve_2x2(a11, a12, a21, a22, b1, b2)

    # Invert A
    inv11, inv12, inv21, inv22 = invert_2x2(a11, a12, a21, a22)

    norm_a = inf_norm_matrix(a11, a12, a21, a22)
    norm_inv = inf_norm_matrix(inv11, inv12, inv21, inv22)
    kappa_inf = norm_a * norm_inv

    print(f"Matrix A: [[{a11}, {a12}], [{a21}, {a22}]]")
    print(f"Right-hand side b: [{b1}, {b2}]")
    print(f"Exact unperturbed solution x: [{x1}, {x2}]")
    print(f"||A||_inf: {norm_a}")
    print(f"||A^-1||_inf: {norm_inv}")
    print(f"Exact condition number kappa_inf(A): {kappa_inf} (decimal: {float(kappa_inf):.1f})")

    # Perturb b by delta_b = [0, 1/100000]
    delta_b1, delta_b2 = Fraction(0, 1), Fraction(1, 100_000)
    b1_pert = b1 + delta_b1
    b2_pert = b2 + delta_b2

    x1_pert, x2_pert = solve_2x2(a11, a12, a21, a22, b1_pert, b2_pert)
    delta_x1 = x1_pert - x1
    delta_x2 = x2_pert - x2

    norm_b = inf_norm_vector(b1, b2)
    norm_delta_b = inf_norm_vector(delta_b1, delta_b2)
    norm_x = inf_norm_vector(x1, x2)
    norm_delta_x = inf_norm_vector(delta_x1, delta_x2)

    rel_b = norm_delta_b / norm_b
    rel_x = norm_delta_x / norm_x
    bound = kappa_inf * rel_b

    print(f"\nPerturbation delta_b: [{delta_b1}, {delta_b2}]")
    print(f"Perturbed solution x_pert: [{x1_pert}, {x2_pert}]")
    print(f"Solution error delta_x: [{delta_x1}, {delta_x2}]")
    print(f"Relative rhs change ||delta_b|| / ||b||: {rel_b} (decimal: {float(rel_b):.2e})")
    print(f"Relative solution change ||delta_x|| / ||x||: {rel_x} (decimal: {float(rel_x):.2e})")
    print(f"Condition bound kappa_inf * (||delta_b|| / ||b||): {bound} (decimal: {float(bound):.2e})")
    print(f"Theoretical bound holds: {rel_x <= bound}")


main()
