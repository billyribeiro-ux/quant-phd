"""Lab 1 · Discrete rebalancing and the asymptotic distribution of hedging error.

Verifies the theoretical O(N^{-1/2}) scaling of discrete delta-hedging error as established
by Boyle & Emanuel (1980). Simulates hedging error distributions across rebalancing frequencies
N in {16, 64, 256, 1024} for a European call option.
Evaluates the log-log empirical scaling slope:
    d log(Std(eps_N)) / d log(N) ~= -0.50,
confirming that the root-mean-square hedging error scales inversely with the square root of
rebalancing frequency.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical European call option price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_call_delta(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical European call delta."""
    if tau <= 1e-12:
        return 1.0 if s > k else 0.0
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    return norm_cdf(d1)


def simulate_hedging_errors(
    s0: float,
    k: float,
    r: float,
    sigma: float,
    maturity: float,
    n_steps: int,
    n_paths: int,
    seed: int,
) -> list[float]:
    """Simulate terminal discrete hedging errors eps_N = Payoff - V_T^(N)."""
    dt = maturity / n_steps
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)
    df_step = math.exp(r * dt)

    rng = random.Random(seed)
    c0 = bs_call_price(s0, k, r, sigma, maturity)

    errors: list[float] = []

    for _ in range(n_paths):
        s = s0
        delta = bs_call_delta(s, k, r, sigma, maturity)
        cash = c0 - delta * s

        for step in range(1, n_steps):
            z = rng.gauss(0.0, 1.0)
            s_next = s * math.exp(drift + vol * z)
            cash = cash * df_step

            tau_rem = max(maturity - step * dt, 1e-12)
            delta_new = bs_call_delta(s_next, k, r, sigma, tau_rem)

            cash -= (delta_new - delta) * s_next
            delta = delta_new
            s = s_next

        z = rng.gauss(0.0, 1.0)
        s_t = s * math.exp(drift + vol * z)
        cash = cash * df_step

        payoff = max(s_t - k, 0.0)
        v_terminal = delta * s_t + cash
        # Hedging error defined as shortfall: Payoff - Replicating Portfolio
        hedging_error = payoff - v_terminal
        errors.append(hedging_error)

    return errors


def main() -> None:
    # Contract and market parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    r = 0.04
    sigma = 0.20
    maturity = 0.5
    step_counts = [16, 64, 256, 1024]
    n_paths = 2500
    seed = 101

    log_n: list[float] = []
    log_std: list[float] = []

    print("Discrete Rebalancing Hedging Error Asymptotic Scaling (SIMULATED):")
    for n in step_counts:
        errs = simulate_hedging_errors(s0, k, r, sigma, maturity, n, n_paths, seed + n)
        mean_err = sum(errs) / n_paths
        std_err = math.sqrt(sum((x - mean_err) ** 2 for x in errs) / (n_paths - 1))
        # Normalized error std: Std(sqrt(N) * eps_N)
        norm_std = std_err * math.sqrt(n)

        log_n.append(math.log(n))
        log_std.append(math.log(std_err))

        print(
            f"N = {n:4d} | dt = {maturity / n:8.5f} | Std(eps_N) = {std_err:8.5f} | "
            f"Std(sqrt(N)*eps_N) = {norm_std:7.4f} | Mean(eps_N) = {mean_err:8.5f}"
        )

    # Compute empirical regression slope of log(Std) vs log(N)
    mean_ln = sum(log_n) / len(log_n)
    mean_ls = sum(log_std) / len(log_std)
    numerator = sum((x - mean_ln) * (y - mean_ls) for x, y in zip(log_n, log_std, strict=True))
    denominator = sum((x - mean_ln) ** 2 for x in log_n)
    scaling_slope = numerator / denominator

    print(f"Empirical log-log scaling slope: {scaling_slope:.4f} (Theoretical: -0.5000)")
    slope_pass = abs(scaling_slope - (-0.5000)) <= 0.08
    print("Empirical slope within [-0.58, -0.42]:", slope_pass)


main()
