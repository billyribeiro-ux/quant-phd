"""Lab 1 (L05): The Fang-Oosterlee COS method and exponential convergence verification.

SIMULATED market parameters under geometric Brownian motion.
Prices European options using Fourier-cosine series expansions, sweeps expansion order N
from 8 to 128, and measures exponential convergence rates toward analytical machine precision.
"""

from __future__ import annotations

import math

import numpy as np


def bsm_call_analytic(spot: float, strike: float, rate: float, vol: float, maturity: float) -> float:
    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    cdf_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return float(spot * cdf_d1 - strike * math.exp(-rate * maturity) * cdf_d2)


def cos_method_call_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_terms: int = 64,
    l_param: float = 10.0,
) -> float:
    """Evaluate European call price using Fang-Oosterlee (2008) Fourier-cosine series."""
    # Cumulants for truncation interval [a, b]
    c1 = (rate - 0.5 * vol * vol) * maturity
    c2 = vol * vol * maturity
    c4 = 0.0

    a = c1 - l_param * math.sqrt(c2 + math.sqrt(c4))
    b = c1 + l_param * math.sqrt(c2 + math.sqrt(c4))

    k = np.arange(n_terms)
    omega = k * math.pi / (b - a)

    # Characteristic function of x = ln(S_T / K) - ln(S_0 / K)
    # phi(u) = exp(i * u * c1 - 0.5 * c2 * u^2)
    phi_val = np.exp(1j * omega * c1 - 0.5 * c2 * omega * omega)

    # Cosine expansion coefficients of density
    cf_term = np.real(phi_val * np.exp(-1j * omega * a))
    f_k = (2.0 / (b - a)) * cf_term

    # Analytical integration of call payoff: g(y) = K (exp(x + x0) - 1)
    x0 = math.log(spot / strike)
    # Truncated integral of cos(omega * (y - a)) against (exp(y + x0) - 1) over [0, b - x0]
    d = b - x0
    c_lim = max(0.0, -x0)

    # Chi and Psi functions
    # Chi_k = int_{c}^{d} exp(y) cos(omega * (y - a)) dy
    denom = 1.0 + omega * omega
    cos_d = np.cos(omega * (d - a))
    sin_d = np.sin(omega * (d - a))
    cos_c = np.cos(omega * (c_lim - a))
    sin_c = np.sin(omega * (c_lim - a))

    chi_k = (math.exp(d) * (cos_d + omega * sin_d) - math.exp(c_lim) * (cos_c + omega * sin_c)) / denom

    # Psi_k = int_{c}^{d} cos(omega * (y - a)) dy
    psi_k = np.zeros(n_terms)
    psi_k[0] = d - c_lim
    psi_k[1:] = (sin_d[1:] - sin_c[1:]) / omega[1:]

    # Payoff expansion coefficients V_k
    v_k = (2.0 / (b - a)) * strike * (math.exp(x0) * chi_k - psi_k)

    # Option price summation (term 0 carries factor 0.5)
    terms = f_k * v_k
    terms[0] *= 0.5
    price = math.exp(-rate * maturity) * 0.5 * (b - a) * float(np.sum(terms))

    return max(0.0, price)


def main() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    bsm_ref = bsm_call_analytic(spot, strike, rate, vol, maturity)
    print(f"Analytical BSM benchmark: {bsm_ref:.12f}")

    n_values = [8, 16, 32, 64, 128]
    print("\nCOS method convergence across expansion order N:")
    for n in n_values:
        p = cos_method_call_price(spot, strike, rate, vol, maturity, n_terms=n)
        err = abs(p - bsm_ref)
        print(f"  N = {n:3d} | Price = {p:.12f} | Absolute Error = {err:.2e}")


main()
