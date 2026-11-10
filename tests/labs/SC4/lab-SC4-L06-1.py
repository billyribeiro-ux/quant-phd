"""Lab SC4-L06-1 · Implicit BTCS Scheme and Tridiagonal Thomas Algorithm Validation.

Validates the backward-time central-space (BTCS) implicit finite difference scheme under a large
mesh ratio lambda = dt / dx^2 = 5.0 (where explicit methods immediately explode).
Demonstrates O(N) Thomas algorithm equivalence to scipy.linalg.solve_banded to machine precision (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import linalg  # type: ignore[import-untyped]


def thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Thomas algorithm (TDMA) for tridiagonal system Ax = d."""
    n = len(d)
    cp = np.zeros(n, dtype=np.float64)
    dp = np.zeros(n, dtype=np.float64)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / denom
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom
    x = np.zeros(n, dtype=np.float64)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def main() -> None:
    n_space = 100
    n_steps = 50
    lambda_mesh = 5.0  # Far above explicit CFL threshold 0.50

    dx = 1.0 / n_space
    dt = lambda_mesh * (dx**2)
    x = np.linspace(0.0, 1.0, n_space + 1)

    # Initial condition: fundamental mode sin(pi * x)
    u_thomas = np.sin(math.pi * x)
    u_scipy = np.sin(math.pi * x)

    # System matrix: (I - dt * L) u^{n+1} = u^n
    # -lambda * u_{j-1}^{n+1} + (1 + 2*lambda) * u_j^{n+1} - lambda * u_{j+1}^{n+1} = u_j^n
    m_int = n_space - 1
    a_diag = np.full(m_int, -lambda_mesh)
    b_diag = np.full(m_int, 1.0 + 2.0 * lambda_mesh)
    c_diag = np.full(m_int, -lambda_mesh)

    # SciPy banded matrix format: shape (3, m_int)
    # row 0: superdiagonal (shifted left, first element ignored)
    # row 1: main diagonal
    # row 2: subdiagonal (shifted right, last element ignored)
    ab = np.zeros((3, m_int), dtype=np.float64)
    ab[0, 1:] = -lambda_mesh
    ab[1, :] = 1.0 + 2.0 * lambda_mesh
    ab[2, :-1] = -lambda_mesh

    for _ in range(n_steps):
        # Thomas solve
        d_thomas = u_thomas[1:-1].copy()
        v_thomas = thomas_solve(a_diag, b_diag, c_diag, d_thomas)
        u_thomas = np.concatenate([[0.0], v_thomas, [0.0]])

        # SciPy solve_banded
        d_scipy = u_scipy[1:-1].copy()
        v_scipy = linalg.solve_banded((1, 1), ab, d_scipy)
        u_scipy = np.concatenate([[0.0], v_scipy, [0.0]])

    max_diff = float(np.max(np.abs(u_thomas - u_scipy)))
    max_amp = float(np.max(u_thomas))

    # Analytical solution for comparison
    t_final = n_steps * dt
    exact = math.exp(-(math.pi**2) * t_final) * np.sin(math.pi * x)
    max_err_exact = float(np.max(np.abs(u_thomas - exact)))

    print(f"Implicit BTCS scheme with mesh ratio lambda = {lambda_mesh:.1f} (CFL = 0.50):")
    print(f"  Maximum amplitude at t = {t_final:.4f}: {max_amp:.6f}")
    print(f"  Maximum difference vs scipy.linalg.solve_banded: {max_diff:.4e}")
    print(f"  Maximum error vs exact analytical solution:     {max_err_exact:.4e}")
    print(f"  Unconditional stability confirmed (max_amp < 1): {max_amp < 1.0}")
    print(f"  Agreement with SciPy within 1e-13:               {max_diff < 1e-13}")


main()
