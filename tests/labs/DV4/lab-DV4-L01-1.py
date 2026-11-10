"""Lab 1 (L01): Trinomial lattice convergence and stability conditions.

SIMULATED market parameters under geometric Brownian motion.
Prices a European call option across tree depths N in {25, 50, 100, 200},
verifies transition probability positivity, and calculates empirical convergence to BSM.
"""

from __future__ import annotations

import math

import numpy as np


def bsm_call_price(spot: float, strike: float, rate: float, vol: float, maturity: float) -> float:
    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    cdf_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return float(spot * cdf_d1 - strike * math.exp(-rate * maturity) * cdf_d2)


def trinomial_call(spot: float, strike: float, rate: float, vol: float, maturity: float, n_steps: int) -> float:
    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    u = math.exp(dx)
    1.0 / u
    df = math.exp(-rate * dt)
    nu = (rate - 0.5 * vol * vol) * dt

    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    # Assert stability: probabilities strictly within (0, 1)
    if not (0.0 < pu < 1.0 and 0.0 < pm < 1.0 and 0.0 < pd < 1.0):
        raise ValueError(f"Stability violated: pu={pu:.4f}, pm={pm:.4f}, pd={pd:.4f}")

    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)
    v = np.maximum(s_terminal - strike, 0.0)

    for k in range(n_steps - 1, -1, -1):
        v = df * (pu * v[2 : 2 * k + 3] + pm * v[1 : 2 * k + 2] + pd * v[0 : 2 * k + 1])

    return float(v[0])


def main() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0

    bsm_ref = bsm_call_price(spot, strike, rate, vol, maturity)
    print(f"Analytical BSM benchmark: {bsm_ref:.6f}")

    steps = [25, 50, 100, 200]
    prices: list[float] = []
    errors: list[float] = []

    for n in steps:
        p = trinomial_call(spot, strike, rate, vol, maturity, n)
        err = abs(p - bsm_ref)
        prices.append(p)
        errors.append(err)
        print(f"N = {n:3d} | Price = {p:.6f} | Error = {err:.6f}")

    # Empirical convergence order estimate
    log_steps = [math.log(n) for n in steps]
    log_errs = [math.log(e) for e in errors]
    slope = -(log_errs[-1] - log_errs[0]) / (log_steps[-1] - log_steps[0])
    print(f"Empirical convergence order: {slope:.2f}")


main()
