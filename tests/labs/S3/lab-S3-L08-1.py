"""Lab S3-L08-1: Structural VAR identification via Cholesky decomposition.

Exact check: verifies Cholesky factorization of reduced-form covariance matrix
and shows the sensitivity of contemporaneous structural impacts to variable ordering.
"""

from __future__ import annotations

import math


def main() -> None:
    # Reduced-form residual covariance matrix: Sigma_u = [[4.0, 2.0], [2.0, 5.0]]
    s11, s12, s22 = 4.0, 2.0, 5.0

    print("Reduced-form Covariance Matrix Sigma_u:")
    print(f"  [[{s11:.4f}, {s12:.4f}], [{s12:.4f}, {s22:.4f}]]")

    # Ordering 1: y1 precedes y2 (P1 lower triangular)
    p11 = math.sqrt(s11)
    p21 = s12 / p11
    p22 = math.sqrt(s22 - p21**2)

    # Verification: P1 * P1^T == Sigma_u
    rec1_11 = p11 * p11
    rec1_12 = p11 * p21
    rec1_22 = p21 * p21 + p22 * p22
    err_p1 = max(abs(rec1_11 - s11), abs(rec1_12 - s12), abs(rec1_22 - s22))

    print("\nOrdering 1 (y1 -> y2):")
    print(f"  Cholesky factor P1: [[{p11:.4f}, {0.0:.4f}], [{p21:.4f}, {p22:.4f}]]")
    print(f"  Factorization error max|P1 P1^T - Sigma_u|: {err_p1:.2e}")
    print("  Contemporaneous shock response of (y1, y2):")
    print(f"    Shock 1 -> y1: {p11:.4f}, y2: {p21:.4f}")
    print(f"    Shock 2 -> y1: {0.0:.4f}, y2: {p22:.4f}")

    # Ordering 2: y2 precedes y1 (P2 lower triangular on permuted variables)
    q11 = math.sqrt(s22)
    q21 = s12 / q11
    q22 = math.sqrt(s11 - q21**2)

    rec2_11 = q11 * q11
    rec2_12 = q11 * q21
    rec2_22 = q21 * q21 + q22 * q22
    err_p2 = max(abs(rec2_11 - s22), abs(rec2_12 - s12), abs(rec2_22 - s11))

    print("\nOrdering 2 (y2 -> y1):")
    print(f"  Cholesky factor P2: [[{q11:.4f}, {0.0:.4f}], [{q21:.4f}, {q22:.4f}]]")
    print(f"  Factorization error max|P2 P2^T - Sigma_permuted|: {err_p2:.2e}")
    print("  Contemporaneous shock response of (y1, y2):")
    print(f"    Shock 1 (y2-ordered) -> y1: {q21:.4f}, y2: {q11:.4f}")
    print(f"    Shock 2 (y1-residual) -> y1: {q22:.4f}, y2: {0.0:.4f}")

    print("\nEconomic Interpretation:")
    print(f"  Under Ordering 1, immediate impact of Shock 1 on y2 is {p21:.4f}.")
    print(f"  Under Ordering 2, immediate impact of Shock 1 on y1 is {q21:.4f}.")
    print("  Structural identification depends strictly on the non-testable ordering assumption.")


main()
