"""Lab M8-L07-1: Variance reduction efficiency: antithetic and control variates.

Standard library only. Compares variance and standard error of crude Monte Carlo,
antithetic variates, and underlying asset control variates for a European call (SIMULATED).
"""

from __future__ import annotations

import math
import random


def bs_call_price(s: float, k: float, tau: float, r: float, sigma: float) -> float:
    """Exact Black-Scholes call price via math.erf."""
    v_sqrt_t = sigma * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * tau) / v_sqrt_t
    d2 = d1 - v_sqrt_t
    disc = math.exp(-r * tau)
    phi_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    phi_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return s * phi_d1 - k * disc * phi_d2


def main() -> None:
    s0 = 100.0
    k = 100.0
    tau = 1.0
    r = 0.05
    sigma = 0.20
    n = 50_000
    disc = math.exp(-r * tau)
    drift = (r - 0.5 * sigma * sigma) * tau
    vol_sqrt = sigma * math.sqrt(tau)

    exact_price = bs_call_price(s0, k, tau, r, sigma)
    print("=== Variance Reduction for European Call Option (SIMULATED) ===")
    print(f"Parameters: S0={s0}, K={k}, tau={tau}, r={r}, sigma={sigma}")
    print(f"Exact Black-Scholes price: {exact_price:.10f}")

    rng = random.Random(42)

    # 1. Crude Monte Carlo
    z_crude = [rng.gauss(0.0, 1.0) for _ in range(n)]
    payoffs_crude = [disc * max(s0 * math.exp(drift + vol_sqrt * z) - k, 0.0) for z in z_crude]
    mc_est = sum(payoffs_crude) / n
    mc_var = sum((x - mc_est) ** 2 for x in payoffs_crude) / (n - 1)
    mc_se = math.sqrt(mc_var / n)

    # 2. Antithetic Variates (n/2 pairs = n evaluations)
    rng_anti = random.Random(42)
    n_pairs = n // 2
    anti_estimates: list[float] = []
    for _ in range(n_pairs):
        z = rng_anti.gauss(0.0, 1.0)
        s_pos = s0 * math.exp(drift + vol_sqrt * z)
        s_neg = s0 * math.exp(drift - vol_sqrt * z)
        c_pos = disc * max(s_pos - k, 0.0)
        c_neg = disc * max(s_neg - k, 0.0)
        anti_estimates.append(0.5 * (c_pos + c_neg))

    anti_est = sum(anti_estimates) / n_pairs
    anti_var = sum((x - anti_est) ** 2 for x in anti_estimates) / (n_pairs - 1)
    anti_se = math.sqrt(anti_var / n_pairs)

    # 3. Control Variates: using terminal stock price S_tau as control
    # Known expectation: E[S_tau] = S0 * exp(r * tau)
    # Discounted terminal price: E[e^{-r*tau} S_tau] = S0
    y_vals = [disc * s0 * math.exp(drift + vol_sqrt * z) for z in z_crude]
    e_y = s0  # exact expectation of discounted stock price

    y_mean = sum(y_vals) / n
    cov_xy = sum((payoffs_crude[i] - mc_est) * (y_vals[i] - y_mean) for i in range(n)) / (n - 1)
    var_y = sum((y - y_mean) ** 2 for y in y_vals) / (n - 1)
    b_star = cov_xy / var_y

    cv_payoffs = [payoffs_crude[i] - b_star * (y_vals[i] - e_y) for i in range(n)]
    cv_est = sum(cv_payoffs) / n
    cv_var = sum((x - cv_est) ** 2 for x in cv_payoffs) / (n - 1)
    cv_se = math.sqrt(cv_var / n)

    corr_xy = cov_xy / math.sqrt(mc_var * var_y)
    theoretical_reduction = 1.0 - corr_xy**2

    print("\nEstimator Performance (N = 50,000 evaluations):")
    print(f"Crude MC:     Estimate = {mc_est:.6f}, Std Err = {mc_se:.4e}, Variance = {mc_var:.4f}")
    print(
        f"Antithetic:   Estimate = {anti_est:.6f}, Std Err = {anti_se:.4e}, "
        f"Variance ratio to MC = {anti_var / mc_var:.4f}"
    )
    print(f"Control Var:  Estimate = {cv_est:.6f}, Std Err = {cv_se:.4e}, Variance = {cv_var:.4f}")
    print(f"Correlation corr(Payoff, S_tau): {corr_xy:.4f}")
    print(f"Empirical variance ratio Var(CV) / Var(MC): {cv_var / mc_var:.4f}")
    print(f"Theoretical variance ratio (1 - rho^2):     {theoretical_reduction:.4f}")


main()
