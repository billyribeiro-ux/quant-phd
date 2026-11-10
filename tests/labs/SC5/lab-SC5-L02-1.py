"""Lab 2 · Merton jump-diffusion analytical series versus Monte Carlo pricing.

Under Merton's (1976) jump-diffusion model, the European call price is an infinite Poisson-weighted
sum of Black-Scholes formula values. Under the risk-neutral measure Q, the asset price is:
S_t = S_0 * exp((r - 0.5*sigma^2 - lambda*kappa)*t + sigma*B_t + sum_{k=1}^{N_t} Y_k)
where kappa = E[exp(Y) - 1] = exp(mu_j + 0.5*sigma_j^2) - 1.
This lab computes the analytical series price truncated at 40 terms, simulates 10,000 independent
paths (SIMULATED) using seed 123, evaluates the discounted payoff mean, and checks agreement within
3 standard errors.
"""

from __future__ import annotations

import math
import random


def _std_norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    seed = 123
    rng = random.Random(seed)

    spot = 100.0
    strike = 100.0
    tau = 0.5
    r = 0.04
    sigma = 0.15
    lam = 0.60
    mu_j = -0.10
    sigma_j = 0.15

    kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0

    # Merton analytical series calculation
    price_series = 0.0
    lam_tau = lam * tau
    drift_base = (r - 0.5 * sigma**2 - lam * kappa) * tau
    var_base = sigma**2 * tau
    p_n = math.exp(-lam_tau)
    log_sk = math.log(spot / strike)

    for n in range(40):
        if n > 0:
            p_n *= lam_tau / n
        m_n = drift_base + n * mu_j
        v_n = math.sqrt(var_base + n * sigma_j**2)
        d1 = (log_sk + m_n + v_n**2) / v_n
        d2 = d1 - v_n
        payoff = spot * math.exp(m_n + 0.5 * v_n**2) * _std_norm_cdf(d1) - strike * _std_norm_cdf(d2)
        price_series += p_n * payoff
        if p_n < 1e-12 and n > 5:
            break
    price_analytical = price_series * math.exp(-r * tau)

    # Monte Carlo simulation (SIMULATED)
    n_paths = 10000
    sq_tau = math.sqrt(tau)
    discount = math.exp(-r * tau)
    payoffs: list[float] = []

    for _ in range(n_paths):
        # Draw Poisson jump count
        l_exp = math.exp(-lam_tau)
        p = 1.0
        k = 0
        while True:
            p *= rng.random()
            if p <= l_exp:
                break
            k += 1
        n_jumps = k

        # Diffusion + jumps
        z = rng.gauss(0.0, 1.0)
        jump_sum = sum(rng.gauss(mu_j, sigma_j) for _ in range(n_jumps))
        log_return = (r - 0.5 * sigma**2 - lam * kappa) * tau + sigma * sq_tau * z + jump_sum
        s_tau = spot * math.exp(log_return)
        payoffs.append(discount * max(0.0, s_tau - strike))

    mc_price = sum(payoffs) / n_paths
    mc_var = sum((x - mc_price) ** 2 for x in payoffs) / (n_paths - 1)
    se_mc = math.sqrt(mc_var / n_paths)

    print(f"Merton analytical series call price: {price_analytical:.6f}")
    print(f"Monte Carlo price ({n_paths} paths, SIMULATED): {mc_price:.6f} (se {se_mc:.6f})")
    print(f"absolute difference: {abs(mc_price - price_analytical):.6f}")
    print("Monte Carlo within 3*se band:", abs(mc_price - price_analytical) <= 3.0 * se_mc)


main()
