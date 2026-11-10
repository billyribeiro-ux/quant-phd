"""Lab SC4-L04-1 · Far-field Boundary Condition Truncation Error in Log-Asset Coordinates.

Analyzes the truncation error introduced by restricting the infinite spatial domain to a bounded
interval [-L, L] with asymptotic Dirichlet boundary conditions in log-moneyness x = log(S/K).
Demonstrates exponential error decay as a function of domain half-width L (SIMULATED).
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


def solve_log_pde(k_factor: float, k_strike: float, r: float, sigma: float, horizon: float) -> float:
    """Solve Black-Scholes PDE in log-moneyness x = log(S/K) on domain [-L, L] where L = k_factor * sigma * sqrt(H)."""
    l_width = k_factor * sigma * math.sqrt(horizon)
    x_min, x_max = -l_width, l_width
    n_space = int(100 * k_factor)
    dx = (x_max - x_min) / n_space
    n_time = 150
    dt = horizon / n_time

    x = np.linspace(x_min, x_max, n_space + 1)
    s = k_strike * np.exp(x)

    # Initial condition: call payoff
    u = np.maximum(s - k_strike, 0.0)

    # Operator coefficients for u_tau = 0.5*sigma^2 * u_xx + (r - 0.5*sigma^2)*u_x - r*u
    drift = r - 0.5 * sigma * sigma
    diff = 0.5 * sigma * sigma

    alpha = diff / (dx**2) - 0.5 * drift / dx
    beta = -2.0 * diff / (dx**2) - r
    gamma = diff / (dx**2) + 0.5 * drift / dx

    tau = 0.0
    theta = 0.5
    for _ in range(n_time):
        tau_next = tau + dt
        disc = math.exp(-r * tau_next)
        u_low = 0.0
        u_high = k_strike * math.exp(x_max) - k_strike * disc

        d = (
            (1.0 + (1.0 - theta) * dt * beta) * u[1:-1]
            + (1.0 - theta) * dt * alpha * u[:-2]
            + (1.0 - theta) * dt * gamma * u[2:]
        )
        a_diag = np.full(n_space - 1, -theta * dt * alpha)
        b_diag = np.full(n_space - 1, 1.0 - theta * dt * beta)
        c_diag = np.full(n_space - 1, -theta * dt * gamma)

        d[0] -= a_diag[0] * u_low
        d[-1] -= c_diag[-1] * u_high

        u_int = thomas_solve(a_diag, b_diag, c_diag, d)
        u = np.concatenate([[u_low], u_int, [u_high]])
        tau = tau_next

    # Value at at-the-money (x = 0, S = K)
    idx_zero = np.argmin(np.abs(x))
    return float(u[idx_zero])


def main() -> None:
    k_strike = 100.0
    rate = 0.05
    sigma = 0.20
    horizon = 1.0

    # Exact analytical at-the-money call price
    d1 = (rate + 0.5 * sigma * sigma) * horizon / (sigma * math.sqrt(horizon))
    d2 = d1 - sigma * math.sqrt(horizon)
    exact_atm = k_strike * norm_cdf(d1) - k_strike * math.exp(-rate * horizon) * norm_cdf(d2)

    k_multipliers = [2.0, 3.0, 4.0, 5.0, 6.0]
    errors: list[float] = []

    print(f"Exact Black-Scholes ATM call price: {exact_atm:.6f}")
    print("Domain truncation error as a function of half-width L = k * sigma * sqrt(H):")
    for km in k_multipliers:
        price_num = solve_log_pde(km, k_strike, rate, sigma, horizon)
        err = abs(price_num - exact_atm)
        errors.append(err)
        print(f"  k = {km:.1f} (L = {km * sigma * math.sqrt(horizon):.2f}): price = {price_num:.6f}, error = {err:.2e}")

    # Check monotonic decay of truncation error
    decaying = all(errors[i] >= errors[i + 1] or errors[i + 1] < 1e-4 for i in range(len(errors) - 1))
    print(f"Error decreases monotonically or reaches discretization floor: {decaying}")
    print(f"Error at k=6.0 is below 1e-3: {errors[-1] < 1e-3}")


main()
