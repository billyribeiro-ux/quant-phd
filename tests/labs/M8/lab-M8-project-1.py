"""Rung 1 worked example: step-by-step robust implied-volatility inversion (SIMULATED).

Standard library only. Inverts one European call option quote from the seeded test suite,
showing the no-arbitrage boundary check, dynamic bracket expansion, and safeguarded Newton steps.
"""

from __future__ import annotations

import math


def bs_price(spot: float, strike: float, tau: float, rate: float, vol: float, kind: str) -> float:
    sqrt_t = math.sqrt(tau)
    v_sqrt_t = vol * sqrt_t
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / v_sqrt_t
    d2 = d1 - v_sqrt_t
    disc = math.exp(-rate * tau)
    c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    if kind == "call":
        return spot * c1 - strike * disc * c2
    else:
        return strike * disc * (1.0 - c2) - spot * (1.0 - c1)


def vega(spot: float, strike: float, tau: float, rate: float, vol: float) -> float:
    sqrt_t = math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / (vol * sqrt_t)
    return spot * sqrt_t * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)


def main() -> None:
    # Representative instance from make_instance(0)
    spot = 120.0
    strike = 115.0
    tau = 0.5
    rate = 0.03
    kind = "call"
    true_vol = 0.28
    price = bs_price(spot, strike, tau, rate, true_vol, kind)

    print("=== Rung 1: Step-by-Step Robust Implied Volatility Inversion ===")
    print(f"Option quote: S={spot}, K={strike}, tau={tau}, r={rate}, kind={kind}")
    print(f"Target market price: {price:.10f}")

    # Step 1: Strict no-arbitrage bounds check
    disc = math.exp(-rate * tau)
    lo = max(spot - strike * disc, 0.0)
    hi = spot
    print(f"\nStep 1: Bounds check. Lower={lo:.6f}, Upper={hi:.6f}")
    assert lo < price < hi, "Price violates strict no-arbitrage bounds"
    print("  Result: Valid interior quote strictly between theoretical bounds.")

    # Step 2: Dynamic bracket expansion
    a, b = 1e-4, 1.0
    fa = bs_price(spot, strike, tau, rate, a, kind) - price
    fb = bs_price(spot, strike, tau, rate, b, kind) - price
    print(f"\nStep 2: Initial bracket [{a:.4f}, {b:.4f}], f(a)={fa:.6f}, f(b)={fb:.6f}")

    while fa > 0.0 and a > 1e-15:
        b = a
        fb = fa
        a /= 4.0
        fa = bs_price(spot, strike, tau, rate, a, kind) - price

    while fb < 0.0 and b < 1e6:
        a = b
        fa = fb
        b *= 2.0
        fb = bs_price(spot, strike, tau, rate, b, kind) - price

    print(f"  Guaranteed root bracket: [{a:.6f}, {b:.6f}] with f(a)*f(b) <= 0")

    # Step 3: Safeguarded Newton-Raphson iteration
    print("\nStep 3: Safeguarded Newton iteration")
    sigma = 0.5 * (a + b)
    tol = 1e-12 * spot

    for step in range(1, 15):
        f = bs_price(spot, strike, tau, rate, sigma, kind) - price
        v = vega(spot, strike, tau, rate, sigma)
        print(f"  Iter {step:2d}: sigma={sigma:.10f}, f(sigma)={f:.2e}, vega={v:.4f}")

        if abs(f) <= tol:
            print(f"  Converged: residual |f| <= {tol:.2e}")
            break

        if f < 0.0:
            a = sigma
        else:
            b = sigma

        # Proposed Newton step
        sigma = sigma - f / v if v > 1e-14 and a < sigma - f / v < b else 0.5 * (a + b)

    v_final = vega(spot, strike, tau, rate, sigma)
    reg = "solved" if v_final >= 0.01 else "ill_conditioned"
    print("\nFinal Result:")
    print(f"  Solved volatility sigma_hat: {sigma:.12f}")
    print(f"  Generating true volatility:  {true_vol:.12f}")
    print(f"  Forward error |sigma - true|: {abs(sigma - true_vol):.2e}")
    print(f"  Final vega: {v_final:.4f} -> Region: {reg}")


main()
