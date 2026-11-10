"""Lab 1 · Risk-Neutral Densities & Breeden-Litzenberger Extraction.

Extracts the risk-neutral probability density q(S_T) from European call prices
using the Breeden-Litzenberger identity q(K) = exp(r*tau) * d^2 C / dK^2.
Compares numerical finite-difference extraction with analytical SVI density p(k)
and verifies unit integral and martingale expectation E^Q[S_T] = F.
All data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    if tau <= 1e-12:
        return max(s - k, 0.0)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def svi_derivs(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> tuple[float, float, float]:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    w = a + b * (rho * diff + disc)
    w_p = b * (rho + diff / disc)
    w_pp = b * (sigma**2) / (disc**3)
    return w, w_p, w_pp


def g_factor(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    w, w_p, w_pp = svi_derivs(k, a, b, rho, m, sigma)
    term1 = (1.0 - (k * w_p) / (2.0 * w)) ** 2
    term2 = (w_p**2 / 4.0) * (1.0 / w + 0.25)
    term3 = 0.5 * w_pp
    return term1 - term2 + term3


def svi_rnd_density(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    """Analytical risk-neutral density in log-moneyness p(k)."""
    w, _, _ = svi_derivs(k, a, b, rho, m, sigma)
    g = g_factor(k, a, b, rho, m, sigma)
    d2 = -k / math.sqrt(w) - 0.5 * math.sqrt(w)
    return (g / math.sqrt(2.0 * math.pi * w)) * math.exp(-0.5 * d2**2)


def main() -> None:
    spot = 100.0
    rate = 0.03
    tau = 0.50
    fwd = spot * math.exp(rate * tau)

    # Benchmark SVI slice parameters (SIMULATED)
    params = {"a": 0.030, "b": 0.120, "rho": -0.35, "m": 0.015, "sigma": 0.080}

    # Extract density across strike grid
    strikes = [round(fwd * math.exp(-0.40 + 0.05 * i), 2) for i in range(17)]  # k in [-0.4, 0.4]

    print("Strike (K) | Log-Moneyness (k) | Breeden-Litzenberger q(K) | Analytical SVI q(K)")
    print("-" * 80)

    bl_densities: list[float] = []
    svi_densities: list[float] = []

    for k_strike in strikes:
        k_log = math.log(k_strike / fwd)

        # Numerical Breeden-Litzenberger via central finite difference of call prices
        h = 0.50
        k_up = k_strike + h
        k_down = k_strike - h
        w_up, _, _ = svi_derivs(math.log(k_up / fwd), **params)
        w_down, _, _ = svi_derivs(math.log(k_down / fwd), **params)
        w_mid, _, _ = svi_derivs(k_log, **params)

        c_up = bs_call_price(spot, k_up, rate, math.sqrt(w_up / tau), tau)
        c_down = bs_call_price(spot, k_down, rate, math.sqrt(w_down / tau), tau)
        c_mid = bs_call_price(spot, k_strike, rate, math.sqrt(w_mid / tau), tau)

        # q(K) = exp(r * tau) * (C(K+h) - 2C(K) + C(K-h)) / h^2
        q_bl = math.exp(rate * tau) * (c_up - 2.0 * c_mid + c_down) / (h**2)

        # Analytical SVI density transformed to strike: q(K) = p(k) / K
        p_log = svi_rnd_density(k_log, **params)
        q_svi = p_log / k_strike

        bl_densities.append(q_bl)
        svi_densities.append(q_svi)

        print(f"{k_strike:10.2f} | {k_log:17.4f} | {q_bl:25.6f} | {q_svi:20.6f}")

    # Dense numerical integration over k in [-2.5, 2.5]
    n_steps = 5000
    step = 5.0 / n_steps
    int_mass = 0.0
    int_exp_k = 0.0
    int_k = 0.0

    for j in range(n_steps):
        k_val = -2.5 + (j + 0.5) * step
        p_val = svi_rnd_density(k_val, **params)
        int_mass += p_val * step
        int_exp_k += math.exp(k_val) * p_val * step
        int_k += k_val * p_val * step

    mean_s_t = fwd * int_exp_k

    print("-" * 80)
    print(f"Total Probability Mass Integral:        {int_mass:.6f} (Theoretical: 1.000000)")
    print(f"Martingale Asset Expectation E^Q[S_T]:  {mean_s_t:.4f} (Forward F = {fwd:.4f})")
    print(f"Risk-Neutral Mean Log-Return E^Q[k]:    {int_k:.6f} (Negative due to Jensen's inequality)")
    print(
        "Numerical vs Analytical BL max diff < 1e-4:",
        max(abs(a - b) for a, b in zip(bl_densities, svi_densities, strict=True)) < 1e-4,
    )
    print("Martingale Pricing Identity Verified:   ", abs(mean_s_t - fwd) < 1e-3)


main()
