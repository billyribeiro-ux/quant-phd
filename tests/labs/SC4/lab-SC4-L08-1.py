"""Lab SC4-L08-1 · Damping Spurious Oscillations via Rannacher Smoothing on Non-Smooth Payoffs.

Demonstrates the failure of raw Crank-Nicolson for discontinuous payoffs (digital call options)
where high-frequency Fourier modes produce severe sign-alternating oscillations in Gamma.
Shows that Rannacher smoothing (4 half-steps of fully implicit Euler) eliminates oscillations (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


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


def solve_digital_option(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    vol: float,
    n_space: int,
    n_time: int,
    rannacher: bool,
) -> tuple[np.ndarray, np.ndarray, int]:
    s_min = 0.0
    s_max = 3.0 * strike
    s = np.linspace(s_min, s_max, n_space + 1, dtype=np.float64)
    ds = (s_max - s_min) / n_space
    dt = maturity / n_time

    # Digital call payoff: 1 if S > K else 0
    v = np.where(s > strike, 1.0, 0.0)
    v[np.isclose(s, strike, atol=1e-12)] = 0.5

    s_int = s[1:-1]
    alpha = 0.5 * (vol**2) * (s_int**2) / (ds**2) - 0.5 * rate * s_int / ds
    beta = -(vol**2) * (s_int**2) / (ds**2) - rate
    gamma = 0.5 * (vol**2) * (s_int**2) / (ds**2) + 0.5 * rate * s_int / ds

    def step(v_curr: np.ndarray, tau_next: float, theta: float, step_dt: float) -> np.ndarray:
        disc = math.exp(-rate * tau_next)
        v_low = 0.0
        v_high = disc
        d = (
            (1.0 + (1.0 - theta) * step_dt * beta) * v_curr[1:-1]
            + (1.0 - theta) * step_dt * alpha * v_curr[:-2]
            + (1.0 - theta) * step_dt * gamma * v_curr[2:]
        )
        a_diag = -theta * step_dt * alpha
        b_diag = 1.0 - theta * step_dt * beta
        c_diag = -theta * step_dt * gamma

        d[0] -= a_diag[0] * v_low
        d[-1] -= c_diag[-1] * v_high

        v_int = thomas_solve(a_diag, b_diag, c_diag, d)
        v_new = np.empty_like(v_curr)
        v_new[0] = v_low
        v_new[-1] = v_high
        v_new[1:-1] = v_int
        return v_new

    tau = 0.0
    if rannacher and n_time >= 4:
        # 4 half-steps of fully implicit Euler (theta = 1.0)
        for _ in range(4):
            v = step(v, tau + dt / 2.0, 1.0, dt / 2.0)
            tau += dt / 2.0
        for _ in range(n_time - 2):
            v = step(v, tau + dt, 0.5, dt)
            tau += dt
    else:
        for _ in range(n_time):
            v = step(v, tau + dt, 0.5, dt)
            tau += dt

    # Compute discrete Gamma
    gamma_vals = (v[2:] - 2.0 * v[1:-1] + v[:-2]) / (ds * ds)
    idx_strike = np.argmin(np.abs(s_int - strike))
    local_gamma = gamma_vals[max(0, idx_strike - 8) : min(len(gamma_vals), idx_strike + 9)]

    # Count sign changes in the local Gamma profile
    sign_changes = int(np.sum(local_gamma[:-1] * local_gamma[1:] < 0))

    return s, gamma_vals, sign_changes


def main() -> None:
    spot = 100.0
    strike = 100.0
    maturity = 0.5
    rate = 0.05
    vol = 0.30
    n_space = 400
    n_time = 12

    _, _, osc_raw = solve_digital_option(spot, strike, maturity, rate, vol, n_space, n_time, rannacher=False)
    _, _, osc_ran = solve_digital_option(spot, strike, maturity, rate, vol, n_space, n_time, rannacher=True)

    print(f"Digital call option Gamma oscillations around strike (N_space={n_space}, N_time={n_time}):")
    print(f"  Raw Crank-Nicolson Gamma sign changes:       {osc_raw}")
    print(f"  Rannacher-smoothed Crank-Nicolson sign changes: {osc_ran}")
    print(f"  Oscillations present in raw Crank-Nicolson:  {osc_raw > 0}")
    print(f"  Oscillations suppressed by Rannacher:       {osc_ran <= 2}")


main()
