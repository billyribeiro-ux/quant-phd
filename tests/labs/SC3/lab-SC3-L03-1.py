"""Lab 1 · Discrete delta hedging and martingale representation convergence.

By the Martingale Representation Theorem, any square-integrable contingent claim X in the
Brownian filtration admits an exact representation as a stochastic integral of an adapted hedging
strategy Delta_t = partial V / partial S. In continuous time, the tracking error is identically zero.
In discrete time with N rebalancing intervals of size dt = H / N, the hedging error variance
Var(Pi_H - (S_H - K)^+) scales as O(1 / N).
This lab simulates discrete delta-hedging across N in {10, 40, 160} on 2,000 paths (SIMULATED),
verifying that tracking error variance diminishes inversely with the rebalancing step count.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price_and_delta(s: float, k: float, r: float, sigma: float, tau: float) -> tuple[float, float]:
    if tau <= 1e-12:
        val = max(s - k, 0.0)
        delta = 1.0 if s > k else 0.0
        return val, delta
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * (sigma**2)) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    price = s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)
    delta = norm_cdf(d1)
    return price, delta


def main() -> None:
    seed = 42
    s0 = 100.0
    k = 100.0
    r = 0.05
    sigma = 0.20
    horizon = 1.0
    n_paths = 2000

    n_steps_list = [10, 40, 160]
    variances: list[float] = []

    for n_steps in n_steps_list:
        rng = random.Random(seed)
        dt = horizon / n_steps
        sq_dt = math.sqrt(dt)
        drift = (r - 0.5 * (sigma**2)) * dt
        vol = sigma * sq_dt
        df = math.exp(r * dt)

        errors: list[float] = []

        for _ in range(n_paths):
            s = s0
            # Initial portfolio: replicate call
            price0, delta0 = bs_call_price_and_delta(s, k, r, sigma, horizon)
            cash = price0 - delta0 * s
            delta = delta0

            for step in range(n_steps):
                z = rng.gauss(0.0, 1.0)
                s = s * math.exp(drift + vol * z)
                tau = max(horizon - (step + 1) * dt, 0.0)
                portfolio_val = delta * s + cash * df
                if step < n_steps - 1:
                    _, new_delta = bs_call_price_and_delta(s, k, r, sigma, tau)
                    cash = portfolio_val - new_delta * s
                    delta = new_delta
                else:
                    payoff = max(s - k, 0.0)
                    errors.append(portfolio_val - payoff)

        mean_err = sum(errors) / n_paths
        var_err = sum((e - mean_err) ** 2 for e in errors) / (n_paths - 1)
        variances.append(var_err)

    ratio_1 = variances[0] / variances[1]
    ratio_2 = variances[1] / variances[2]

    print(f"S0: {s0:.1f}, K: {k:.1f}, r: {r:.2f}, sigma: {sigma:.2f}, H: {horizon:.1f}")
    for n_steps, var in zip(n_steps_list, variances, strict=True):
        print(f"N = {n_steps:3d} rebalancing steps: tracking variance = {var:.6f}")
    print(f"variance ratio N=10 to N=40: {ratio_1:.2f} (theoretical ~4.0)")
    print(f"variance ratio N=40 to N=160: {ratio_2:.2f} (theoretical ~4.0)")
    print("variance monotonically decreasing with N:", variances[0] > variances[1] > variances[2])


main()
