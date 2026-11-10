"""Lab 1 · Curriculum lab: Importance sampling via Girsanov for deep-OTM options.

For deep out-of-the-money options, standard Monte Carlo simulation suffers from severe variance
because the payoff event {S_T > K} is extremely rare.
By Girsanov's theorem, we can change the drift of the underlying Brownian motion so that paths
frequently terminate in the money, and weight each simulated payoff by the Radon-Nikodym likelihood ratio:
    L = exp(-theta * W_T - (1/2) * theta^2 * T).
Choosing the drift shift theta* = (log(K / S_0) - (r - sigma^2/2) * T) / (sigma * T) centers the terminal
distribution at the strike K.
This lab simulates 20,000 paths (SIMULATED) under standard Monte Carlo and Girsanov importance sampling
for a deep-OTM call (S_0 = 100, K = 220, r = 0.05, sigma = 0.20, T = 1.0), verifying that Girsanov importance
sampling yields an unbiased estimate with an empirical variance reduction exceeding 50x.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s0: float, k: float, r: float, sigma: float, t: float) -> float:
    sq_t = math.sqrt(t)
    d1 = (math.log(s0 / k) + (r + 0.5 * (sigma**2)) * t) / (sigma * sq_t)
    d2 = d1 - sigma * sq_t
    return s0 * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def main() -> None:
    seed = 42
    s0 = 100.0
    k = 220.0
    r = 0.05
    sigma = 0.20
    t = 1.0
    n_paths = 20000

    exact_price = bs_call_price(s0, k, r, sigma, t)
    sq_t = math.sqrt(t)

    # 1. Standard Monte Carlo
    rng_std = random.Random(seed)
    drift_std = (r - 0.5 * (sigma**2)) * t
    vol = sigma * sq_t
    df = math.exp(-r * t)

    vals_std: list[float] = []
    hits_std = 0
    for _ in range(n_paths):
        z = rng_std.gauss(0.0, 1.0)
        st = s0 * math.exp(drift_std + vol * z)
        payoff = max(st - k, 0.0)
        if payoff > 0.0:
            hits_std += 1
        vals_std.append(df * payoff)

    mean_std = sum(vals_std) / n_paths
    var_std = sum((x - mean_std) ** 2 for x in vals_std) / (n_paths - 1)
    se_std = math.sqrt(var_std / n_paths)

    # 2. Girsanov Importance Sampling
    # Optimal drift shift theta to center S_T at K
    theta_star = (math.log(k / s0) - (r - 0.5 * (sigma**2)) * t) / (sigma * t)

    rng_is = random.Random(seed)
    vals_is: list[float] = []
    hits_is = 0

    for _ in range(n_paths):
        z_tilde = rng_is.gauss(0.0, 1.0)
        z_orig = z_tilde + theta_star * sq_t
        st = s0 * math.exp(drift_std + vol * z_orig)
        payoff = max(st - k, 0.0)
        if payoff > 0.0:
            hits_is += 1
        # Likelihood ratio L = exp(-theta* * W_T - 0.5 * (theta*)^2 * T)
        # where W_T = z_tilde * sqrt(T) + theta* * T
        lr = math.exp(-theta_star * sq_t * z_tilde - 0.5 * (theta_star**2) * t)
        vals_is.append(df * payoff * lr)

    mean_is = sum(vals_is) / n_paths
    var_is = sum((x - mean_is) ** 2 for x in vals_is) / (n_paths - 1)
    se_is = math.sqrt(var_is / n_paths)
    var_reduction_ratio = var_std / var_is if var_is > 0.0 else float("inf")

    print(f"exact analytical deep-OTM call price: {exact_price:.6e}")
    print(f"standard MC estimate: {mean_std:.6e} (se {se_std:.6e}, hits {hits_std}/{n_paths})")
    print(f"Girsanov IS estimate: {mean_is:.6e} (se {se_is:.6e}, hits {hits_is}/{n_paths})")
    print(f"empirical variance reduction ratio: {var_reduction_ratio:.1f}x")
    print("Girsanov IS inside 2*se of exact:", abs(mean_is - exact_price) <= 2.0 * se_is)
    print("variance reduction exceeds 50x:", var_reduction_ratio > 50.0)


main()
