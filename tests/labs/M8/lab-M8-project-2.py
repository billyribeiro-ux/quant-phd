"""Rung 2 completed solution: robust inversion safeguard (SIMULATED).

Standard library only. Complete implementation of the bracket update and safeguarded
Newton step for the completion problem.
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


def solve_implied_vol(price: float, spot: float, strike: float, tau: float, rate: float, kind: str) -> float:
    a, b = 1e-4, 2.0
    fa = bs_price(spot, strike, tau, rate, a, kind) - price
    fb = bs_price(spot, strike, tau, rate, b, kind) - price

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

    sigma = 0.5 * (a + b)
    tol = 1e-12 * spot

    for _ in range(50):
        f = bs_price(spot, strike, tau, rate, sigma, kind) - price
        if abs(f) <= tol:
            break

        if f < 0.0:
            a = sigma
        else:
            b = sigma

        v = vega(spot, strike, tau, rate, sigma)
        sigma = sigma - f / v if v > 1e-14 and a < sigma - f / v < b else 0.5 * (a + b)

    return sigma


def main() -> None:
    spot, strike, tau, rate, kind = 100.0, 95.0, 0.25, 0.04, "call"
    true_vol = 0.22
    price = bs_price(spot, strike, tau, rate, true_vol, kind)

    v_hat = solve_implied_vol(price, spot, strike, tau, rate, kind)
    recalc = bs_price(spot, strike, tau, rate, v_hat, kind)
    residual = abs(recalc - price)

    print("=== Rung 2 Completion Problem Solution ===")
    print(f"Option price: {price:.10f}")
    print(f"Solved vol:   {v_hat:.10f}")
    print(f"True vol:     {true_vol:.10f}")
    print(f"Price error:  {residual:.2e}")
    print(f"Solved successfully: {residual <= 1e-12 * spot}")


main()
