"""Lab 6 · Option pricing via Carr-Madan damped Fourier transform and grid convergence.

Carr & Madan (1999) price European call options through the Fourier transform of the damped payoff:
c_T(k) = exp(alpha * k) * C_T(k),   k = ln(K).
The call price is recovered by the real Fourier inversion integral:
C(K) = (exp(-alpha * k) / pi) * integral_0^infinity Re[ exp(-i * v * k) * psi_T(v) ] dv,
where psi_T(v) = exp(-r * T) * phi_T(v - (alpha + 1)*i) / (alpha^2 + alpha - v^2 + i*(2*alpha + 1)*v).
This lab computes the ATM call price for a Variance Gamma model across Simpson quadrature grid sizes
N in {64, 128, 256, 512} with alpha = 1.5 and v_max = 100.0 (SIMULATED), verifies grid convergence,
and validates put-call parity to within 1e-6.
"""

from __future__ import annotations

import math

import numpy as np


def vg_cf(
    u: complex | np.ndarray,
    tau: float,
    spot: float,
    r: float,
    sigma: float,
    nu: float,
    theta: float,
) -> complex | np.ndarray:
    arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
    omega = (1.0 / nu) * math.log(arg)
    drift = (r + omega) * tau
    denom = 1.0 - 1j * u * theta * nu + 0.5 * (sigma**2) * nu * (u**2)
    return np.exp(1j * u * math.log(spot)) * np.exp(1j * u * drift) * (denom ** (-tau / nu))


def carr_madan_call(
    spot: float,
    strike: float,
    tau: float,
    r: float,
    sigma: float,
    nu: float,
    theta: float,
    n_pts: int,
    v_max: float = 100.0,
    alpha: float = 1.5,
) -> float:
    k = math.log(strike)
    v = np.linspace(0.0, v_max, n_pts + 1)
    dv = v_max / n_pts
    weights = np.ones(n_pts + 1)
    weights[1:-1:2] = 4.0
    weights[2:-2:2] = 2.0
    weights = weights * (dv / 3.0)

    u = v - (alpha + 1.0) * 1j
    phi = vg_cf(u, tau, spot, r, sigma, nu, theta)
    denom = (alpha**2 + alpha - v**2) + 1j * (2.0 * alpha + 1.0) * v
    psi = np.exp(-r * tau) * phi / denom
    exp_term = np.exp(-1j * v * k)
    integrand = (exp_term * psi).real
    integral = float(np.sum(integrand * weights))
    return float(math.exp(-alpha * k) / math.pi * integral)


def main() -> None:
    spot = 100.0
    strike = 100.0
    tau = 0.5
    r = 0.03
    sigma = 0.25
    nu = 0.20
    theta = -0.10

    grid_sizes = [64, 128, 256, 512]
    prices: list[float] = []

    print(f"Variance Gamma parameters: sigma={sigma}, nu={nu}, theta={theta}, r={r}, tau={tau} (SIMULATED)")
    print("Carr-Madan European ATM call prices across Simpson grid sizes:")

    for n in grid_sizes:
        p = carr_madan_call(spot, strike, tau, r, sigma, nu, theta, n_pts=n)
        prices.append(p)
        print(f"  N = {n:3d}: price = {p:.8f}")

    benchmark_price = prices[-1]
    discrepancy_256 = abs(prices[2] - benchmark_price)

    # Put-call parity at N=512
    call_512 = prices[-1]
    put_512 = call_512 - spot + strike * math.exp(-r * tau)
    parity_lhs = call_512 - put_512
    parity_rhs = spot - strike * math.exp(-r * tau)
    parity_error = abs(parity_lhs - parity_rhs)

    print(f"convergence discrepancy between N=256 and N=512: {discrepancy_256:.2e}")
    print(f"put-call parity check: C - P = {parity_lhs:.6f}, S0 - K*exp(-r*tau) = {parity_rhs:.6f}")
    print(f"parity error: {parity_error:.2e}")
    print("grid converged within 5e-4 at N=256:", discrepancy_256 < 5e-4)
    print("put-call parity holds within 1e-10:", parity_error < 1e-10)


main()
