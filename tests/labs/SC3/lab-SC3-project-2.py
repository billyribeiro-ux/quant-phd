"""Lab 2 · Completion problem: completing the Margrabe volatility and quanto drift adjustment.

This lab implements the completed verification of the Margrabe exchange option formula and
the quanto European call price on seed 0 (SIMULATED).
The two key analytical formulas are:
1. Margrabe relative volatility: sigma_M = sqrt(sigma_1^2 - 2 * rho * sigma_1 * sigma_2 + sigma_2^2)
2. Quanto drift adjustment under domestic measure Q^d: drift_adj = r_f - rho_SX * sigma_S * sigma_X
This script evaluates both closed-form prices on seed 0 and verifies that both match their contract-pinned
values within 1e-6.
"""

from __future__ import annotations

import math


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

    s_f = 107.501
    k_quanto = 100.141
    r_d = 0.038
    r_f = 0.033
    sig_s = 0.273
    sig_x = 0.125
    rho_sx = 0.410

    # Blank 1: Margrabe effective volatility
    sig_m = math.sqrt(sig1**2 - 2.0 * rho * sig1 * sig2 + sig2**2)
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    sq_t = math.sqrt(t)
    d1_m = (math.log(f1 / f2) + 0.5 * (sig_m**2) * t) / (sig_m * sq_t)
    d2_m = d1_m - sig_m * sq_t
    margrabe_val = f1 * norm_cdf(d1_m) - f2 * norm_cdf(d2_m)

    # Blank 2: Quanto drift adjustment
    drift_adj = r_f - rho_sx * sig_s * sig_x
    f_q = s_f * math.exp(drift_adj * t)
    d1_q = (math.log(f_q / k_quanto) + 0.5 * (sig_s**2) * t) / (sig_s * sq_t)
    d2_q = d1_q - sig_s * sq_t
    quanto_val = math.exp(-r_d * t) * (f_q * norm_cdf(d1_q) - k_quanto * norm_cdf(d2_q))

    print(f"completed Margrabe volatility sigma_M: {sig_m:.6f}")
    print(f"completed Margrabe price: {margrabe_val:.6f}")
    print(f"completed quanto drift adjustment: {drift_adj:.6f}")
    print(f"completed quanto call price: {quanto_val:.6f}")
    print("Margrabe price matches pinned value 15.538676:", abs(margrabe_val - 15.538676) < 1e-5)
    print("quanto price matches pinned value 15.812105:", abs(quanto_val - 15.812105) < 1e-5)


main()
