"""Lab 1 (L04): Carr-Madan FFT characteristic function inversion and damping parameter sweep.

SIMULATED market parameters under geometric Brownian motion.
Prices European call options across strikes using Carr-Madan FFT, sweeps damping parameter
alpha, and investigates strike-frequency grid spacing reciprocity.
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


def carr_madan_fft_prices(
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
    alpha: float = 1.5,
    n_points: int = 1024,
    eta: float = 0.25,
) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate European call option prices across strike grid using Carr-Madan FFT."""
    lambda_k = 2.0 * math.pi / (n_points * eta)
    b = 0.5 * n_points * lambda_k
    k_grid = -b + np.arange(n_points) * lambda_k  # Log-strikes k = ln(K)
    strikes = np.exp(k_grid)

    v = np.arange(n_points) * eta
    simpson_weights = 3.0 + (-1.0) ** (np.arange(n_points) + 1)
    simpson_weights[0] = 1.0
    simpson_weights[-1] = 1.0
    simpson_weights = simpson_weights / 3.0

    # Characteristic function of log(S_T) under Q
    u = v - (alpha + 1.0) * 1j
    # phi(u) = exp(i * u * (ln(S0) + (r - 0.5*sigma^2)*T) - 0.5 * sigma^2 * u^2 * T)
    drift = math.log(spot) + (rate - 0.5 * vol * vol) * maturity
    phi_u = np.exp(1j * u * drift - 0.5 * (vol * vol) * (u * u) * maturity)

    denom = alpha * alpha + alpha - v * v + 1j * (2.0 * alpha + 1.0) * v
    psi_v = math.exp(-rate * maturity) * phi_u / denom

    x = np.exp(1j * b * v) * psi_v * eta * simpson_weights
    fft_vals = np.fft.fft(x)

    c_damped = np.real(fft_vals) / math.pi
    call_prices = np.exp(-alpha * k_grid) * c_damped

    return strikes, call_prices


def main() -> None:
    spot = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    alphas = [0.75, 1.50, 2.50, 3.50]
    test_strikes = [90.0, 100.0, 110.0]

    print(f"Target strikes: {test_strikes}")
    print("Analytical BSM benchmarks:")
    for k in test_strikes:
        print(f"  K = {k:5.1f} | Price = {bsm_call_analytic(spot, k, rate, vol, maturity):.6f}")

    print("\nCarr-Madan FFT prices across damping alpha:")
    for a in alphas:
        strikes, prices = carr_madan_fft_prices(spot, rate, vol, maturity, alpha=a, n_points=1024, eta=0.20)
        # Interpolate to test strikes
        atm_price = float(np.interp(100.0, strikes, prices))
        atm_ref = bsm_call_analytic(spot, 100.0, rate, vol, maturity)
        err = abs(atm_price - atm_ref)
        print(f"  alpha = {a:4.2f} | ATM Price = {atm_price:.6f} | Error = {err:.2e}")


main()
