r"""Lab 1 · Upwind vs. central finite difference stability and M-matrix monotonicity.

Demonstrates that central differencing of the drift term in the HJB equation violates the M-matrix
property when the mesh Peclet number exceeds 1, generating negative entries in (rho I - A)^(-1) and
violating the discrete maximum principle, whereas the upwind scheme guarantees non-negative off-diagonals
and an inverse with strictly non-negative entries for all mesh sizes.
"""

from __future__ import annotations


def solve_tridiagonal(sub: list[float], diag: list[float], sup: list[float], rhs: list[float]) -> list[float]:
    n = len(diag)
    c_prime = [0.0] * n
    d_prime = [0.0] * n
    c_prime[0] = sup[0] / diag[0]
    d_prime[0] = rhs[0] / diag[0]
    for i in range(1, n):
        denom = diag[i] - sub[i] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = sup[i] / denom
        d_prime[i] = (rhs[i] - sub[i] * d_prime[i - 1]) / denom
    x = [0.0] * n
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


def invert_tridiagonal(sub: list[float], diag: list[float], sup: list[float]) -> list[list[float]]:
    n = len(diag)
    cols: list[list[float]] = []
    for j in range(n):
        e_j = [1.0 if i == j else 0.0 for i in range(n)]
        col_j = solve_tridiagonal(sub, diag, sup, e_j)
        cols.append(col_j)
    # Transpose cols to get rows
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def main() -> None:
    # Wealth grid with mesh spacing dw
    n = 21
    w_min = 1.0
    w_max = 5.0
    dw = (w_max - w_min) / (n - 1)
    rho = 0.05

    # Convection-diffusion parameters where drift dominates diffusion (SIMULATED)
    # Drift b(w) = 0.5 w, diffusion coefficient d(w) = 0.02 w^2
    w_nodes = [w_min + i * dw for i in range(n)]
    b = [0.5 * x for x in w_nodes]
    diff = [0.02 * (x**2) for x in w_nodes]

    # Calculate local Peclet numbers: Pe_i = b_i * dw / diff_i
    peclet_numbers = [(b[i] * dw) / diff[i] for i in range(1, n - 1)]
    max_pe = max(peclet_numbers)
    print(f"grid nodes n = {n}, mesh spacing dw = {dw:.2f}")
    print(f"maximum mesh Peclet number: {max_pe:.2f} (convection dominates diffusion, Pe > 1)")

    # 1. Central difference system (rho I - A_central)
    sub_c = [0.0] * n
    diag_c = [0.0] * n
    sup_c = [0.0] * n
    diag_c[0] = 1.0
    diag_c[-1] = 1.0

    for i in range(1, n - 1):
        alpha = diff[i] / (dw**2) - b[i] / (2.0 * dw)
        beta = rho + 2.0 * diff[i] / (dw**2)
        gamma = diff[i] / (dw**2) + b[i] / (2.0 * dw)
        sub_c[i] = -alpha
        diag_c[i] = beta
        sup_c[i] = -gamma

    # 2. Upwind difference system (rho I - A_upwind)
    sub_u = [0.0] * n
    diag_u = [0.0] * n
    sup_u = [0.0] * n
    diag_u[0] = 1.0
    diag_u[-1] = 1.0

    for i in range(1, n - 1):
        alpha = diff[i] / (dw**2)
        beta = rho + 2.0 * diff[i] / (dw**2) + b[i] / dw
        gamma = diff[i] / (dw**2) + b[i] / dw
        sub_u[i] = -alpha
        diag_u[i] = beta
        sup_u[i] = -gamma

    # Off-diagonal sign check: in an M-matrix, off-diagonals of (rho I - A) must be <= 0
    # That means -alpha <= 0 and -gamma <= 0, so alpha >= 0 and gamma >= 0.
    min_alpha_c = min(-sub_c[i] for i in range(1, n - 1))
    min_alpha_u = min(-sub_u[i] for i in range(1, n - 1))

    print(f"central difference min alpha (lower off-diagonal): {min_alpha_c:.4f} (negative!)")
    print(f"upwind difference min alpha (lower off-diagonal): {min_alpha_u:.4f} (non-negative)")

    # Invert both matrices to test inverse positivity
    inv_c = invert_tridiagonal(sub_c, diag_c, sup_c)
    inv_u = invert_tridiagonal(sub_u, diag_u, sup_u)

    min_inv_c = min(min(row) for row in inv_c)
    min_inv_u = min(min(row) for row in inv_u)

    print(f"central scheme inverse min element: {min_inv_c:.4f} (violates positivity)")
    print(f"upwind scheme inverse min element: {min_inv_u:.4f} (preserves positivity)")
    print(f"upwind scheme guarantees M-matrix property: {min_inv_u >= -1e-12}")


main()
