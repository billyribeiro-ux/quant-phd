"""Lab M8-L08-2: Dynamic bracket expansion for implied-volatility inversion.

Standard library only. Compares a naive fixed bracket [1e-6, 10] to dynamic bracket expansion
on an extreme high-volatility call quote.
"""

from __future__ import annotations

import math


def bs_call_price(s: float, k: float, tau: float, r: float, sigma: float) -> float:
    sqrt_t = math.sqrt(tau)
    v_sqrt_t = sigma * sqrt_t
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * tau) / v_sqrt_t
    d2 = d1 - v_sqrt_t
    disc = math.exp(-r * tau)
    c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return s * c1 - k * disc * c2


def vega(s: float, k: float, tau: float, r: float, sigma: float) -> float:
    sqrt_t = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * tau) / (sigma * sqrt_t)
    return s * sqrt_t * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)


def main() -> None:
    s = 100.0
    k = 100.0
    tau = 1.0
    r = 0.05
    target_price = 99.99995

    print("=== Fixed vs Dynamic Bracket Inversion for High-Volatility Call ===")
    print(f"Option quote: S={s}, K={k}, tau={tau}, r={r}, target price={target_price}")
    print(f"Strict no-arbitrage upper bound (S): {s}")
    print(f"Quote is strictly valid (price < S): {target_price < s}")

    # 1. Fixed bracket [1e-6, 10]
    lo_fixed, hi_fixed = 1e-6, 10.0
    c_lo_fixed = bs_call_price(s, k, tau, r, lo_fixed)
    c_hi_fixed = bs_call_price(s, k, tau, r, hi_fixed)

    print("\nFixed bracket [1e-6, 10]:")
    print(f"  C(1e-6) = {c_lo_fixed:.8f} (f_lo = {c_lo_fixed - target_price:.6f})")
    print(f"  C(10.0) = {c_hi_fixed:.8f} (f_hi = {c_hi_fixed - target_price:.6f})")
    fixed_brackets_root = (c_lo_fixed - target_price) * (c_hi_fixed - target_price) <= 0.0
    print(f"  Fixed bracket contains root: {fixed_brackets_root} (fails!)")

    # 2. Dynamic bracket expansion
    a = 1.0
    b = 2.0
    fa = bs_call_price(s, k, tau, r, a) - target_price
    fb = bs_call_price(s, k, tau, r, b) - target_price
    expansions = 0

    while fb < 0.0:
        expansions += 1
        a = b
        fa = fb
        b *= 2.0
        fb = bs_call_price(s, k, tau, r, b) - target_price

    print("\nDynamic bracket expansion:")
    print(f"  Expansions performed: {expansions}")
    print(f"  Expanded bracket: [{a:.1f}, {b:.1f}]")
    print(f"  C({a:.1f}) - price = {fa:.6e}")
    print(f"  C({b:.1f}) - price = {fb:.6e}")
    print(f"  Dynamic bracket contains root: {fa * fb <= 0.0}")

    # 3. Safeguarded Newton solve
    sigma = 0.5 * (a + b)
    steps = 0
    for _ in range(50):
        steps += 1
        f = bs_call_price(s, k, tau, r, sigma) - target_price
        if abs(f) <= 1e-12 * s:
            break
        if f < 0.0:
            a = sigma
        else:
            b = sigma
        v = vega(s, k, tau, r, sigma)
        sigma = sigma - f / v if v > 1e-14 and a < sigma - f / v < b else 0.5 * (a + b)

    recomputed = bs_call_price(s, k, tau, r, sigma)
    res = abs(recomputed - target_price)
    print(f"\nSolved implied volatility: {sigma:.8f}")
    print(f"Inversion iterations: {steps}")
    print(f"Recomputed price: {recomputed:.10f}")
    print(f"Residual |C(sigma) - price|: {res:.2e}")
    print(f"Residual <= 1e-12 * S: {res <= 1e-12 * s}")


main()
