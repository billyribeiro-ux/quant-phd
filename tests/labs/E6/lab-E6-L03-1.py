"""Lab E6-L03-1: Forward recursion and truncation error of the dynamic IS curve.

Solves the dynamic IS equation forward under an AR(1) real interest rate gap process.
Compares finite forward truncations at horizons H in {4, 8, 16, 32} against the exact
infinite-horizon closed form, demonstrating that truncation error decays geometrically as rho^H.
"""

from __future__ import annotations


def solve_dynamic_is_truncated(sigma: float, rho: float, r_gap_0: float, horizon: int) -> float:
    """Compute the finite-horizon truncated forward sum for the output gap."""
    return float(-(1.0 / sigma) * sum((rho**j) * r_gap_0 for j in range(horizon)))


def solve_dynamic_is_exact(sigma: float, rho: float, r_gap_0: float) -> float:
    """Compute the exact infinite-horizon closed-form output gap: -r_gap_0 / (sigma * (1 - rho))."""
    return float(-r_gap_0 / (sigma * (1.0 - rho)))


def main() -> None:
    sigma = 1.0  # Log utility / unit intertemporal elasticity of substitution
    rho = 0.7  # Real interest rate gap persistence
    r_gap_0 = 0.02  # Initial 200 basis point ex-ante real interest rate tightening

    x_exact = solve_dynamic_is_exact(sigma, rho, r_gap_0)

    print(f"Dynamic IS forward solution parameters (sigma={sigma}, rho={rho}, r_gap={r_gap_0}):")
    print(f"  Exact infinite-horizon output gap x*: {x_exact:.6f}")
    print("\nForward horizon truncation analysis:")

    horizons = [4, 8, 16, 32]
    for h in horizons:
        x_trunc = solve_dynamic_is_truncated(sigma, rho, r_gap_0, h)
        num_error = abs(x_exact - x_trunc)
        th_error = abs((rho**h) * r_gap_0 / (sigma * (1.0 - rho)))
        diff = abs(num_error - th_error)

        print(
            f"  H = {h:2d}: x_trunc = {x_trunc:9.6f}, "
            f"error = {num_error:10.6e}, "
            f"theoretical = {th_error:10.6e}, "
            f"discrepancy = {diff:.2e}"
        )


main()
