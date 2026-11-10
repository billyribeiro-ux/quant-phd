"""DV4 Project Rung 2: Completion problem for Crank-Nicolson PDE American pricer.

SIMULATED market data under geometric Brownian motion.
Completes the Thomas algorithm forward sweep and the Brennan-Schwartz obstacle condition
enforcing the early-exercise free boundary on a log-spot spatial grid.
"""

from __future__ import annotations

import math

import numpy as np


def solve_american_pde(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_time: int = 100,
    n_spot: int = 100,
) -> float:
    std = vol * math.sqrt(maturity)
    x_max = 4.0 * std + rate * maturity
    x_min = -4.0 * std
    dx = (x_max - x_min) / (n_spot - 1)
    dt = maturity / n_time

    x = np.linspace(x_min, x_max, n_spot)
    s_grid = strike * np.exp(x)
    intrinsic = np.maximum(strike - s_grid, 0.0)
    v = intrinsic.copy()

    mu = rate - 0.5 * vol * vol
    alpha = 0.5 * (vol * vol) / (dx * dx)
    beta = 0.5 * mu / dx

    a_coef = alpha - beta
    b_coef = -2.0 * alpha - rate
    c_coef = alpha + beta

    theta = 0.5  # Crank-Nicolson
    m = n_spot - 2

    # Tridiagonal system matrix coefficients
    diag_a = -dt * theta * a_coef * np.ones(m)
    diag_b = (1.0 - dt * theta * b_coef) * np.ones(m)
    diag_c = -dt * theta * c_coef * np.ones(m)

    for step in range(1, n_time + 1):
        tau = step * dt
        rhs = v[1:-1] + dt * (1.0 - theta) * (a_coef * v[:-2] + b_coef * v[1:-1] + c_coef * v[2:])

        bc_lower = strike * math.exp(-rate * tau) - s_grid[0]
        bc_upper = 0.0

        rhs[0] += dt * theta * a_coef * bc_lower
        rhs[-1] += dt * theta * c_coef * bc_upper

        # Thomas algorithm forward sweep
        c_p = np.zeros(m)
        d_p = np.zeros(m)
        c_p[0] = diag_c[0] / diag_b[0]
        d_p[0] = rhs[0] / diag_b[0]

        for i in range(1, m):
            denom = diag_b[i] - diag_a[i] * c_p[i - 1]
            c_p[i] = diag_c[i] / denom if i < m - 1 else 0.0
            d_p[i] = (rhs[i] - diag_a[i] * d_p[i - 1]) / denom

        # Backward substitution with Brennan-Schwartz obstacle condition
        v_next = np.zeros(m)
        v_next[-1] = max(d_p[-1], intrinsic[-2])
        for i in range(m - 2, -1, -1):
            sol_val = d_p[i] - c_p[i] * v_next[i + 1]
            # Enforce American early exercise free boundary obstacle
            v_next[i] = max(sol_val, intrinsic[i + 1])

        v[0] = bc_lower
        v[-1] = bc_upper
        v[1:-1] = v_next

    return float(np.interp(spot, s_grid, v))


def main() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    price = solve_american_pde(spot, strike, rate, vol, maturity, n_time=120, n_spot=120)
    print(f"Crank-Nicolson American put price: {price:.4f}")


main()
