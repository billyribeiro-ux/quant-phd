"""Lab 1 · Numeraire invariance: money-market versus stock numeraire.

By Geman, El Karoui & Rochet (1995), arbitrage-free derivative pricing is invariant to the choice
of numeraire. For a European call with S_0 = 100, K = 100, r = 0.05, sigma = 0.20, T = 1.0:
1. Under money-market numeraire M_t = exp(r*t), the pricing formula is:
   V_0 = exp(-r*T) * E^Q[(S_T - K)^+], where log(S_T / S_0) ~ N((r - sigma^2/2)*T, sigma^2*T).
2. Under stock numeraire N_t = S_t, the measure is Q^S with density dQ^S / dQ = S_T / (S_0 * exp(r*T)).
   Under Q^S, log(S_T / S_0) ~ N((r + sigma^2/2)*T, sigma^2*T), and the pricing formula is:
   V_0 = S_0 * E^{Q^S}[(1 - K / S_T)^+].
This lab simulates 20,000 paths (SIMULATED) under both numeraires and verifies that both Monte Carlo
estimates match the Black-Scholes analytical price within 3 standard errors.
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
    k = 100.0
    r = 0.05
    sigma = 0.20
    t = 1.0
    n_paths = 20000

    exact_price = bs_call_price(s0, k, r, sigma, t)
    sq_t = math.sqrt(t)

    # 1. Money-market numeraire: Q measure
    rng_q = random.Random(seed)
    drift_q = (r - 0.5 * (sigma**2)) * t
    vol = sigma * sq_t
    df = math.exp(-r * t)

    payoffs_q: list[float] = []
    for _ in range(n_paths):
        z = rng_q.gauss(0.0, 1.0)
        st = s0 * math.exp(drift_q + vol * z)
        payoffs_q.append(df * max(st - k, 0.0))

    mean_q = sum(payoffs_q) / n_paths
    var_q = sum((x - mean_q) ** 2 for x in payoffs_q) / (n_paths - 1)
    se_q = math.sqrt(var_q / n_paths)

    # 2. Stock numeraire: Q^S measure
    rng_s = random.Random(seed)
    drift_s = (r + 0.5 * (sigma**2)) * t

    payoffs_s: list[float] = []
    for _ in range(n_paths):
        z = rng_s.gauss(0.0, 1.0)
        st = s0 * math.exp(drift_s + vol * z)
        # Relative payoff: (S_T - K)^+ / S_T = (1 - K / S_T)^+
        rel_payoff = max(1.0 - k / st, 0.0)
        payoffs_s.append(s0 * rel_payoff)

    mean_s = sum(payoffs_s) / n_paths
    var_s = sum((x - mean_s) ** 2 for x in payoffs_s) / (n_paths - 1)
    se_s = math.sqrt(var_s / n_paths)

    print(f"exact Black-Scholes price: {exact_price:.4f}")
    print(f"money-market numeraire (Q): {mean_q:.4f} (se {se_q:.4f})")
    print(f"stock numeraire (Q^S): {mean_s:.4f} (se {se_s:.4f})")
    print("Q estimate inside 3*se:", abs(mean_q - exact_price) <= 3.0 * se_q)
    print("Q^S estimate inside 3*se:", abs(mean_s - exact_price) <= 3.0 * se_s)
    print("numeraire invariance |mean_q - mean_s| <= 3*(se_q + se_s):", abs(mean_q - mean_s) <= 3.0 * (se_q + se_s))


main()
