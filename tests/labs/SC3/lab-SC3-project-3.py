"""Lab 3 · Rung 3 reference verification: contract-pinned simulation values on seed 0.

Evaluates the numeraire toolkit reference solution on seed 0 (SIMULATED) under the contract-pinned draw order.
Seed 0 parameters produce:
1. Margrabe exchange option:
   Analytical closed-form price: 15.538676
   Monte Carlo estimate (5,000 paths): 15.637391 with standard error 0.305782
2. Quanto European call option:
   Analytical closed-form price: 15.812105
   Monte Carlo estimate (5,000 paths): 15.850822 with standard error 0.318629
This script verifies that the numerical implementation reproduces these contract-pinned values
within 1e-5.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # Seed 0 parameters (SIMULATED)
    s1 = 113.777
    s2 = 110.318
    sig1 = 0.234
    sig2 = 0.202
    rho = 0.014
    q1 = 0.026
    q2 = 0.041
    t = 0.955
    r = 0.039

    s_f = 107.501
    k_quanto = 100.141
    r_d = 0.038
    r_f = 0.033
    sig_s = 0.273
    sig_x = 0.125
    rho_sx = 0.410
    n_paths = 5000
    seed = 0

    # 1. Margrabe closed-form and Monte Carlo
    sig_m = math.sqrt(sig1**2 - 2.0 * rho * sig1 * sig2 + sig2**2)
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    sq_t = math.sqrt(t)
    d1_m = (math.log(f1 / f2) + 0.5 * (sig_m**2) * t) / (sig_m * sq_t)
    d2_m = d1_m - sig_m * sq_t
    margrabe_closed = f1 * norm_cdf(d1_m) - f2 * norm_cdf(d2_m)

    rng_m = random.Random(seed)
    drift1 = (r - q1 - 0.5 * (sig1**2)) * t
    vol1 = sig1 * sq_t
    drift2 = (r - q2 - 0.5 * (sig2**2)) * t
    vol2 = sig2 * sq_t
    df_m = math.exp(-r * t)

    payoffs_m: list[float] = []
    for _ in range(n_paths):
        z1 = rng_m.gauss(0.0, 1.0)
        z2 = rng_m.gauss(0.0, 1.0)
        w1 = z1
        w2 = rho * z1 + math.sqrt(1.0 - rho**2) * z2
        s1_t = s1 * math.exp(drift1 + vol1 * w1)
        s2_t = s2 * math.exp(drift2 + vol2 * w2)
        payoffs_m.append(df_m * max(s1_t - s2_t, 0.0))

    margrabe_sim = sum(payoffs_m) / n_paths
    var_m = sum((x - margrabe_sim) ** 2 for x in payoffs_m) / (n_paths - 1)
    se_m = math.sqrt(var_m / n_paths)

    # 2. Quanto closed-form and Monte Carlo
    drift_adj = r_f - rho_sx * sig_s * sig_x
    f_q = s_f * math.exp(drift_adj * t)
    d1_q = (math.log(f_q / k_quanto) + 0.5 * (sig_s**2) * t) / (sig_s * sq_t)
    d2_q = d1_q - sig_s * sq_t
    quanto_closed = math.exp(-r_d * t) * (f_q * norm_cdf(d1_q) - k_quanto * norm_cdf(d2_q))

    rng_q = random.Random(seed)
    drift_qd = (r_f - rho_sx * sig_s * sig_x - 0.5 * (sig_s**2)) * t
    vol_qd = sig_s * sq_t
    df_q = math.exp(-r_d * t)

    payoffs_q: list[float] = []
    for _ in range(n_paths):
        z = rng_q.gauss(0.0, 1.0)
        sf_t = s_f * math.exp(drift_qd + vol_qd * z)
        payoffs_q.append(df_q * max(sf_t - k_quanto, 0.0))

    quanto_sim = sum(payoffs_q) / n_paths
    var_q = sum((x - quanto_sim) ** 2 for x in payoffs_q) / (n_paths - 1)
    se_q = math.sqrt(var_q / n_paths)

    print(f"seed 0 Margrabe analytical price: {margrabe_closed:.6f}")
    print(f"seed 0 Margrabe MC price: {margrabe_sim:.6f} (se {se_m:.6f})")
    print(f"seed 0 quanto analytical price: {quanto_closed:.6f}")
    print(f"seed 0 quanto MC price: {quanto_sim:.6f} (se {se_q:.6f})")
    print("Margrabe MC matches pinned value 15.637391:", abs(margrabe_sim - 15.637391) < 1e-5)
    print("quanto MC matches pinned value 15.850822:", abs(quanto_sim - 15.850822) < 1e-5)


main()
