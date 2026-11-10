"""Lab SC4-L02-1 · Fokker-Planck Density Evolution and Conservation of Probability Mass.

Evolves the probability density of an Ornstein-Uhlenbeck process dX_t = kappa * (theta - X_t) * dt + sigma * dB_t
forward in time using the Fokker-Planck (Kolmogorov forward) PDE.
Verifies conservation of total probability mass and compares final moments against analytical values (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    kappa = 1.5
    theta = 0.10
    sigma = 0.30
    x0 = 0.50
    t_final = 1.0

    # Spatial grid
    x_min, x_max = -1.5, 2.0
    n_space = 350
    dx = (x_max - x_min) / n_space
    x = np.linspace(x_min, x_max, n_space + 1)

    # Initial condition: narrow Gaussian centered at x0 with std s0
    s0 = 0.05
    p = np.exp(-0.5 * ((x - x0) / s0) ** 2) / (s0 * math.sqrt(2.0 * math.pi))
    # Normalize initial mass
    initial_mass = float(np.sum(p) * dx)
    p /= initial_mass

    # Time stepping: conservative explicit flux discretization
    # CFL constraint requires dt <= dx^2 / sigma^2
    n_time = 4000
    dt = t_final / n_time

    for _ in range(n_time):
        # Flux at cell interfaces j + 1/2: F = kappa*(theta - x)*p - 0.5*sigma^2 * dp/dx
        # Using central differences for advection and diffusion
        x_mid = 0.5 * (x[:-1] + x[1:])
        p_mid = 0.5 * (p[:-1] + p[1:])
        dp_dx = (p[1:] - p[:-1]) / dx
        flux = kappa * (theta - x_mid) * p_mid - 0.5 * (sigma**2) * dp_dx

        # Update interior cells: p_j^{n+1} = p_j^n - dt/dx * (F_{j+1/2} - F_{j-1/2})
        p[1:-1] -= (dt / dx) * (flux[1:] - flux[:-1])
        # Zero-flux boundary conditions at far edges
        p[0] = 0.0
        p[-1] = 0.0

    final_mass = float(np.sum(p) * dx)
    num_mean = float(np.sum(x * p) * dx)
    num_var = float(np.sum(((x - num_mean) ** 2) * p) * dx)

    # Analytical OU moments at t_final
    # Initial variance was s0^2
    exact_mean = theta + (x0 - theta) * math.exp(-kappa * t_final)
    exact_var = (s0**2) * math.exp(-2.0 * kappa * t_final) + (sigma**2) / (2.0 * kappa) * (
        1.0 - math.exp(-2.0 * kappa * t_final)
    )

    mass_err = abs(final_mass - 1.0)
    mean_err = abs(num_mean - exact_mean)
    var_err = abs(num_var - exact_var)

    print(f"Total probability mass: {final_mass:.8f} (error: {mass_err:.2e})")
    print(f"Numerical mean: {num_mean:.6f} (Exact: {exact_mean:.6f}, err: {mean_err:.2e})")
    print(f"Numerical var:  {num_var:.6f} (Exact: {exact_var:.6f}, err: {var_err:.2e})")
    print(f"Mass conserved within 1e-4: {mass_err < 1e-4}")
    print(f"Moments agree within 0.01: {mean_err < 0.01 and var_err < 0.01}")


main()
