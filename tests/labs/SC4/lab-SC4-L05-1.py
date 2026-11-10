"""Lab SC4-L05-1 · CFL Stability Threshold and Explosive Instability in Explicit FTCS Scheme.

Demonstrates the sharp stability transition for the explicit Forward Time, Central Space (FTCS)
finite difference scheme on the diffusion equation u_t = u_xx. High-frequency spatial modes
(excited by machine roundoff or non-smooth data) explode exponentially when the mesh ratio
lambda = dt / dx^2 exceeds 0.50 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def run_explicit_ftcs(lambda_mesh: float, n_space: int, n_steps: int) -> tuple[float, float, bool]:
    """Run explicit FTCS scheme on u_t = u_xx with initial fundamental and high-frequency modes.

    Initial condition: u(x, 0) = sin(pi * x) + 1e-4 * sin((N - 1) * pi * x).
    Returns (max_numerical_value, max_error_to_fundamental, is_bounded).
    """
    dx = 1.0 / n_space
    dt = lambda_mesh * (dx**2)
    x = np.linspace(0.0, 1.0, n_space + 1)

    # Initial condition: fundamental mode plus tiny high-frequency Nyquist perturbation
    u = np.sin(math.pi * x) + 1e-4 * np.sin((n_space - 1) * math.pi * x)

    # Advance n_steps
    for _ in range(n_steps):
        u_next = np.zeros_like(u)
        u_next[1:-1] = u[1:-1] + lambda_mesh * (u[2:] - 2.0 * u[1:-1] + u[:-2])
        u = u_next
        if np.any(np.isnan(u)) or np.max(np.abs(u)) > 1e12:
            break

    t_final = n_steps * dt
    exact = math.exp(-(math.pi**2) * t_final) * np.sin(math.pi * x)
    max_val = float(np.max(np.abs(u)))
    max_err = float(np.max(np.abs(u - exact)))
    is_bounded = max_val < 10.0

    return max_val, max_err, is_bounded


def main() -> None:
    n_space = 40
    n_steps = 150

    lambda_stable = 0.48
    lambda_unstable = 0.55

    max_val_s, max_err_s, is_b_s = run_explicit_ftcs(lambda_stable, n_space, n_steps)
    max_val_u, _, is_b_u = run_explicit_ftcs(lambda_unstable, n_space, n_steps)

    print(f"Explicit FTCS on u_t = u_xx with {n_space} grid intervals over {n_steps} steps:")
    print(f"  Stable case (lambda = {lambda_stable:.2f} <= 0.50):")
    print(f"    Maximum solution amplitude: {max_val_s:.6f}")
    print(f"    Maximum error vs exact:     {max_err_s:.6e}")
    print(f"    Stable and bounded:         {is_b_s}")
    print(f"  Unstable case (lambda = {lambda_unstable:.2f} > 0.50):")
    print(f"    Maximum solution amplitude: {max_val_u:.4e}")
    print(f"    Explosive blow-up observed: {not is_b_u}")


main()
