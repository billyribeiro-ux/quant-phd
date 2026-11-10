"""Lab 1 · Margrabe exchange option formula, homogeneity, and exchange parity.

An exchange option gives the holder the right to exchange asset 2 for asset 1, payoff max(S_1(T) - S_2(T), 0).
By Margrabe (1978), using asset 2 as numeraire produces a closed form independent of the risk-free rate r:
    V_0 = S_1(0) * exp(-q_1 * T) * Phi(d_1) - S_2(0) * exp(-q_2 * T) * Phi(d_2)
where sigma_M = sqrt(sigma_1^2 - 2 * rho * sigma_1 * sigma_2 + sigma_2^2) is the relative volatility.
This lab verifies the Margrabe closed form against 2D Monte Carlo (20,000 paths, SIMULATED),
and checks two exact mathematical invariants:
1. Homogeneity of degree 1: V(c * S_1, c * S_2) = c * V(S_1, S_2) for any c > 0.
2. Put-call exchange parity: Call(S_1, S_2) - Call(S_2, S_1) = S_1 * exp(-q_1 * T) - S_2 * exp(-q_2 * T).
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def margrabe_price(
    s1: float,
    s2: float,
    sig1: float,
    sig2: float,
    rho: float,
    q1: float,
    q2: float,
    t: float,
) -> float:
    sig_m = math.sqrt(max(sig1**2 - 2.0 * rho * sig1 * sig2 + sig2**2, 0.0))
    if sig_m <= 1e-12 or t <= 1e-12:
        f1_val = s1 * math.exp(-q1 * t)
        f2_val = s2 * math.exp(-q2 * t)
        return max(f1_val - f2_val, 0.0)

    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    sq_t = math.sqrt(t)
    d1 = (math.log(f1 / f2) + 0.5 * (sig_m**2) * t) / (sig_m * sq_t)
    d2 = d1 - sig_m * sq_t
    return f1 * norm_cdf(d1) - f2 * norm_cdf(d2)


def main() -> None:
    seed = 42
    s1 = 100.0
    s2 = 90.0
    sig1 = 0.25
    sig2 = 0.20
    rho = 0.40
    q1 = 0.02
    q2 = 0.01
    r = 0.04
    t = 1.0
    n_paths = 20000

    exact_price = margrabe_price(s1, s2, sig1, sig2, rho, q1, q2, t)

    # 2D Monte Carlo under risk-neutral measure Q
    rng = random.Random(seed)
    sq_t = math.sqrt(t)
    drift1 = (r - q1 - 0.5 * (sig1**2)) * t
    vol1 = sig1 * sq_t
    drift2 = (r - q2 - 0.5 * (sig2**2)) * t
    vol2 = sig2 * sq_t
    df = math.exp(-r * t)

    payoffs: list[float] = []
    for _ in range(n_paths):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        w1 = z1
        w2 = rho * z1 + math.sqrt(max(1.0 - rho**2, 0.0)) * z2

        s1_t = s1 * math.exp(drift1 + vol1 * w1)
        s2_t = s2 * math.exp(drift2 + vol2 * w2)
        payoffs.append(df * max(s1_t - s2_t, 0.0))

    mc_price = sum(payoffs) / n_paths
    var_mc = sum((x - mc_price) ** 2 for x in payoffs) / (n_paths - 1)
    se_mc = math.sqrt(var_mc / n_paths)

    # Invariant 1: Homogeneity of degree 1
    scale = 2.5
    scaled_price = margrabe_price(scale * s1, scale * s2, sig1, sig2, rho, q1, q2, t)
    homogeneity_error = abs(scaled_price - scale * exact_price)

    # Invariant 2: Put-call exchange parity
    # Call(S1, S2) - Call(S2, S1) = F1 - F2
    reverse_price = margrabe_price(s2, s1, sig2, sig1, rho, q2, q1, t)
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    parity_error = abs((exact_price - reverse_price) - (f1 - f2))

    print(f"analytical Margrabe price: {exact_price:.4f}")
    print(f"2D Monte Carlo price: {mc_price:.4f} (se {se_mc:.4f})")
    print(f"homogeneity error at scale {scale}: {homogeneity_error:.2e}")
    print(f"put-call exchange parity error: {parity_error:.2e}")
    print("MC inside 2*se band:", abs(mc_price - exact_price) <= 2.0 * se_mc)
    print("homogeneity holds to 1e-12:", homogeneity_error < 1e-12)
    print("exchange parity holds to 1e-12:", parity_error < 1e-12)


main()
