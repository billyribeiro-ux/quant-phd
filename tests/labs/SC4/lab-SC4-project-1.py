"""Lab project-1 · Rung 1 worked example: Crank-Nicolson heat-equation and option solver on seed 0.

Solves the Black-Scholes PDE backward in time for a European call option using the Crank-Nicolson
scheme with the Thomas tridiagonal algorithm. Evaluates on the deterministic seed 0 SIMULATED instance.
"""

from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def thomas_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
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
    # Seed 0 parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    maturity = 1.0
    rate = 0.05
    vol = 0.20
    m_space = 200
    n_time = 100

    s_min = 0.0
    s_max = 4.0 * max(s0, k)
    s = np.linspace(s_min, s_max, m_space + 1, dtype=np.float64)
    ds = (s_max - s_min) / m_space
    dt = maturity / n_time

    # Payoff at tau = 0
    v = np.maximum(s - k, 0.0)

    # Interior operator coefficients
    s_int = s[1:-1]
    alpha = 0.5 * vol * vol * (s_int**2) / (ds**2) - 0.5 * rate * s_int / ds
    beta = -vol * vol * (s_int**2) / (ds**2) - rate
    gamma = 0.5 * vol * vol * (s_int**2) / (ds**2) + 0.5 * rate * s_int / ds

    tau = 0.0
    theta = 0.5
    for _ in range(n_time):
        tau_next = tau + dt
        disc = math.exp(-rate * tau_next)
        v_low = 0.0
        v_high = s_max - k * disc

        d = (
            (1.0 + (1.0 - theta) * dt * beta) * v[1:-1]
            + (1.0 - theta) * dt * alpha * v[:-2]
            + (1.0 - theta) * dt * gamma * v[2:]
        )
        a_diag = -theta * dt * alpha
        b_diag = 1.0 - theta * dt * beta
        c_diag = -theta * dt * gamma

        d[0] -= a_diag[0] * v_low
        d[-1] -= c_diag[-1] * v_high

        v_int = thomas_solve(a_diag, b_diag, c_diag, d)
        v = np.concatenate([[v_low], v_int, [v_high]])
        tau = tau_next

    pde_price = float(np.interp(s0, s, v))
    d1 = (math.log(s0 / k) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    exact_price = s0 * norm_cdf(d1) - k * math.exp(-rate * maturity) * norm_cdf(d2)
    err = abs(pde_price - exact_price)

    print(f"PDE price: {pde_price:.6f}")
    print(f"Exact Black-Scholes price: {exact_price:.6f}")
    print(f"Absolute error: {err:.4e}")
    print(f"Agreement within 0.02: {err < 0.02}")


main()
