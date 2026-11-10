"""Lab AP5-L02-1: Campbell-Shiller Log-Linear Present-Value Identity.

SIMULATED: verifies the Campbell-Shiller log-linear return approximation and
the forward-solved present value identity on a simulated asset price path.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(123)
    n_periods = 120  # 120 periods (e.g. 10 years of monthly or 120 quarters)

    # Simulate dividend growth and dividend-price ratio
    # delta_t = d_t - p_t follows persistent AR(1) around mean -3.2 (approx 4.0% annual dividend yield)
    delta_mean = -3.20
    phi_delta = 0.92
    sigma_delta = 0.08
    delta = np.zeros(n_periods)
    delta[0] = delta_mean
    for t in range(1, n_periods):
        delta[t] = delta_mean + phi_delta * (delta[t - 1] - delta_mean) + sigma_delta * rng.standard_normal()

    # Dividend growth: Delta d_{t+1} has mean 0.01 and vol 0.03
    delta_d = 0.01 + 0.03 * rng.standard_normal(n_periods)

    # Reconstruct log dividends and log prices
    d = np.cumsum(delta_d)
    p = d - delta

    # Exact gross return and log return
    # R_{t+1} = (P_{t+1} + D_{t+1}) / P_t
    r_exact = np.zeros(n_periods - 1)
    for t in range(n_periods - 1):
        p_curr = np.exp(p[t])
        p_next = np.exp(p[t + 1])
        d_next = np.exp(d[t + 1])
        r_exact[t] = np.log((p_next + d_next) / p_curr)

    # Campbell-Shiller linearization constants
    d_minus_p_bar = float(np.mean(delta[:-1]))
    rho = 1.0 / (1.0 + np.exp(d_minus_p_bar))
    k = -np.log(rho) - (1.0 - rho) * np.log(1.0 / rho - 1.0)

    # Linearized return: r_{t+1}^approx = k - rho*delta_{t+1} + delta_t + Delta d_{t+1}
    r_approx = np.zeros(n_periods - 1)
    for t in range(n_periods - 1):
        r_approx[t] = k - rho * delta[t + 1] + delta[t] + delta_d[t + 1]

    # Calculate approximation error
    errors = r_exact - r_approx
    max_abs_err = float(np.max(np.abs(errors)))
    mean_abs_err = float(np.mean(np.abs(errors)))
    corr = float(np.corrcoef(r_exact, r_approx)[0, 1])

    # Check multi-period forward identity for horizon = 50
    # delta_t = -k/(1-rho) + sum_{j=1}^H rho^{j-1}(r_j - Delta d_j) + rho^H delta_H
    horizon = 50
    lhs = delta[0]
    discount_factors = rho ** np.arange(horizon)
    sum_r = float(np.sum(discount_factors * r_approx[:horizon]))
    sum_d = float(np.sum(discount_factors * delta_d[1 : horizon + 1]))
    terminal = (rho**horizon) * delta[horizon]
    const_term = -k * (1.0 - rho**horizon) / (1.0 - rho)
    rhs = const_term + sum_r - sum_d + terminal
    identity_gap = abs(lhs - rhs)

    print("Campbell-Shiller (1988) Log-Linearization Verification")
    print(f"Sample length T:             {n_periods} periods")
    print(f"Mean log dividend-price:     {d_minus_p_bar:.4f}")
    print(f"Linearization parameter rho: {rho:.4f}")
    print(f"Linearization constant k:    {k:.4f}")
    print(f"Max abs approximation error: {max_abs_err:.6f}")
    print(f"Mean abs approx error:       {mean_abs_err:.6f}")
    print(f"Correlation (exact, approx): {corr:.6f}")
    print(f"Forward identity (H={horizon}):     LHS={lhs:.5f}, RHS={rhs:.5f}")
    print(f"Identity gap:                {identity_gap:.8e}")


main()
