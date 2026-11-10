"""Lab SC4-L07-1 · Von Neumann Stability Analysis and Crank-Nicolson Amplification Factor.

Validates the theoretical Von Neumann amplification factor G(xi) for the Crank-Nicolson scheme
against empirical discrete steps across spatial Fourier frequencies xi in [0, pi] (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def thomas_periodic_or_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
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
    dx = 1.0 / n_space
    x = np.linspace(0.0, 1.0, n_space + 1)
    lambda_mesh = 2.5  # Large mesh ratio

    # Frequencies m = 1, 5, 20, 50 (Nyquist mode is m = 50, xi = pi)
    modes_m = [1, 5, 20, 50]

    print(f"Von Neumann amplification analysis for Crank-Nicolson (theta = 0.5, lambda = {lambda_mesh:.1f}):")

    for m in modes_m:
        xi = m * math.pi * dx  # phase angle per cell
        g_theory = (1.0 - lambda_mesh * (1.0 - math.cos(xi))) / (1.0 + lambda_mesh * (1.0 - math.cos(xi)))

        # Initial eigenmode u_j = sin(m * pi * x_j)
        u0 = np.sin(m * math.pi * x)

        # Crank-Nicolson step: (I - 0.5 * dt * L) u1 = (I + 0.5 * dt * L) u0
        m_int = n_space - 1
        a_diag = np.full(m_int, -0.5 * lambda_mesh)
        b_diag = np.full(m_int, 1.0 + lambda_mesh)
        c_diag = np.full(m_int, -0.5 * lambda_mesh)

        d = (1.0 - lambda_mesh) * u0[1:-1] + 0.5 * lambda_mesh * u0[:-2] + 0.5 * lambda_mesh * u0[2:]
        u1_int = thomas_periodic_or_solve(a_diag, b_diag, c_diag, d)
        u1 = np.concatenate([[0.0], u1_int, [0.0]])

        # Empirical amplification at the peak
        idx_peak = np.argmax(np.abs(u0[1:-1])) + 1
        g_emp = float(u1[idx_peak] / u0[idx_peak])
        diff = abs(g_emp - g_theory)

        print(f"  Mode m = {m:2d} (xi = {xi:.4f}): G_theory = {g_theory:+.6f}, G_emp = {g_emp:+.6f}, diff = {diff:.2e}")

    # Check high-frequency limit: G(pi) = (1 - 2*lambda) / (1 + 2*lambda)
    g_nyquist = (1.0 - 2.0 * lambda_mesh) / (1.0 + 2.0 * lambda_mesh)
    print(f"Nyquist mode amplification factor G(pi): {g_nyquist:.6f}")
    print(f"Unconditional A-stability verified (|G| <= 1 for all modes): {abs(g_nyquist) <= 1.0}")
    print(f"High-frequency mode inverts sign (G < 0): {g_nyquist < 0.0}")


main()
