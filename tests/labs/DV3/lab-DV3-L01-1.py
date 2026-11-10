"""Lab 1 · Heston Characteristic Function & Fourier Option Pricing.

This lab implements the semi-analytical Heston (1993) Fourier inversion formula
with the Albrecher et al. (2007) stable branch formulation ('Little Heston Trap' fix),
computes European call prices across strikes and maturities on seed 0 (SIMULATED),
inverts Black-Scholes implied volatilities, and demonstrates that the short-time
ATMI skew converges to the finite diffusive limit rho * xi / (2 * sqrt(v0)).
"""

from __future__ import annotations

import cmath
import math


def heston_cf(
    u: complex,
    t: float,
    s0: float,
    r: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
) -> complex:
    """Characteristic function of log(S_T) under risk-neutral measure with stable branch."""
    beta = kappa - 1j * rho * xi * u
    d = cmath.sqrt(beta * beta + xi * xi * (u * u + 1j * u))
    g = (beta - d) / (beta + d)
    exp_neg_dt = cmath.exp(-d * t)

    # Little Heston Trap fix: use ln((1 - g*exp(-d*t)) / (1 - g))
    c_val = (kappa * theta / (xi * xi)) * ((beta - d) * t - 2.0 * cmath.log((1.0 - g * exp_neg_dt) / (1.0 - g)))
    d_val = ((beta - d) / (xi * xi)) * (1.0 - exp_neg_dt) / (1.0 - g * exp_neg_dt)

    return cmath.exp(c_val + d_val * v0 + 1j * u * (math.log(s0) + r * t))


def heston_call_price(
    s0: float,
    k: float,
    t: float,
    r: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
) -> float:
    """Compute European call price using Carr-Madan Fourier inversion."""
    alpha_cm = 1.5
    log_k = math.log(k)

    def psi(v: float) -> complex:
        u = v - (alpha_cm + 1.0) * 1j
        cf = heston_cf(u, t, s0, r, v0, kappa, theta, xi, rho)
        denom = (alpha_cm * alpha_cm + alpha_cm - v * v) + 1j * (2.0 * alpha_cm + 1.0) * v
        return math.exp(-r * t) * cf / denom

    # Midpoint integration rule
    n_steps = 1000
    v_max = 100.0
    dv = v_max / n_steps
    integral = 0.0
    for i in range(n_steps):
        v = (i + 0.5) * dv
        integrand = (cmath.exp(-1j * v * log_k) * psi(v)).real
        integral += integrand * dv

    call = math.exp(-alpha_cm * log_k) / math.pi * integral
    intrinsic = max(0.0, s0 - k * math.exp(-r * t))
    return max(intrinsic, call)


def bs_call_price(s0: float, k: float, t: float, r: float, sigma: float) -> float:
    """Black-Scholes call price."""
    if t <= 0.0 or sigma <= 0.0:
        return max(0.0, s0 - k * math.exp(-r * t))
    d1 = (math.log(s0 / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    def n_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    return s0 * n_cdf(d1) - k * math.exp(-r * t) * n_cdf(d2)


def bs_implied_vol(s0: float, k: float, t: float, r: float, price: float) -> float:
    """Invert Black-Scholes implied volatility via bisection."""
    intrinsic = max(0.0, s0 - k * math.exp(-r * t))
    if price <= intrinsic:
        return 1e-4
    low, high = 1e-4, 5.0
    for _ in range(60):
        mid = 0.5 * (low + high)
        p_mid = bs_call_price(s0, k, t, r, mid)
        if p_mid < price:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def main() -> None:
    print("=== Heston (1993) Fourier Option Pricing & Volatility Skew ===")
    s0 = 100.0
    r = 0.03
    v0 = 0.04
    kappa = 2.0
    theta = 0.04
    xi = 0.30
    rho = -0.70

    feller_ratio = (2.0 * kappa * theta) / (xi * xi)
    print(f"Model Parameters: S0={s0}, r={r}, v0={v0}, kappa={kappa}, theta={theta}, xi={xi}, rho={rho}")
    print(f"Feller Condition 2*kappa*theta >= xi^2: 2*{kappa}*{theta} = {2 * kappa * theta:.4f} vs xi^2 = {xi**2:.4f}")
    print(f"Feller Ratio: {feller_ratio:.4f} ({'Satisfied' if feller_ratio >= 1.0 else 'Violated'})")

    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]

    print("\nHeston European Call Prices (SIMULATED):")
    print(" Strike |   T=0.05 |   T=0.25 |   T=1.00 ")
    print("-----------------------------------------")
    for k in strikes:
        p_005 = heston_call_price(s0, k, 0.05, r, v0, kappa, theta, xi, rho)
        p_025 = heston_call_price(s0, k, 0.25, r, v0, kappa, theta, xi, rho)
        p_100 = heston_call_price(s0, k, 1.00, r, v0, kappa, theta, xi, rho)
        print(f" {k:6.1f} | {p_005:8.4f} | {p_025:8.4f} | {p_100:8.4f} ")

    print("\nBlack-Scholes Implied Volatilities:")
    print(" Strike |   T=0.05 |   T=0.25 |   T=1.00 ")
    print("-----------------------------------------")
    for k in strikes:
        iv_005 = bs_implied_vol(s0, k, 0.05, r, heston_call_price(s0, k, 0.05, r, v0, kappa, theta, xi, rho))
        iv_025 = bs_implied_vol(s0, k, 0.25, r, heston_call_price(s0, k, 0.25, r, v0, kappa, theta, xi, rho))
        iv_100 = bs_implied_vol(s0, k, 1.00, r, heston_call_price(s0, k, 1.00, r, v0, kappa, theta, xi, rho))
        print(f" {k:6.1f} | {iv_005:8.4f} | {iv_025:8.4f} | {iv_100:8.4f} ")

    print("\nATMI Skew Analysis (d(sigma_BS)/d(log(K/F)) at ATM):")
    theoretical_limit = (rho * xi) / (2.0 * math.sqrt(v0))
    print(f"Theoretical Short-Time Limit (rho * xi / (2 * sqrt(v0))): {theoretical_limit:.4f}")

    dk = 0.01
    for t_val in [0.02, 0.05, 0.10, 0.25, 1.00]:
        fwd = s0 * math.exp(r * t_val)
        k_down = fwd * math.exp(-dk)
        k_up = fwd * math.exp(dk)
        p_down = heston_call_price(s0, k_down, t_val, r, v0, kappa, theta, xi, rho)
        p_up = heston_call_price(s0, k_up, t_val, r, v0, kappa, theta, xi, rho)
        iv_down = bs_implied_vol(s0, k_down, t_val, r, p_down)
        iv_up = bs_implied_vol(s0, k_up, t_val, r, p_up)
        skew = (iv_up - iv_down) / (2.0 * dk)
        print(f"  T = {t_val:4.2f} yr | ATMI Skew = {skew:7.4f}")


main()
