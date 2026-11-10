"""Rung 3 independent project verification on seeded grid (SIMULATED).

Standard library only. Runs the reference solver on the seed 0 generated grid (N = 2,000)
and verifies accuracy bounds and prints failure-region report counts.
"""

from __future__ import annotations

import math
import random


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
    tol = 1e-13 * spot

    for _ in range(100):
        f = bs_price(spot, strike, tau, rate, sigma, kind) - price
        if abs(f) <= tol or (b - a) <= 1e-13 * max(1.0, sigma):
            break

        if f < 0.0:
            a = sigma
        else:
            b = sigma

        v = vega(spot, strike, tau, rate, sigma)
        sigma = sigma - f / v if v > 1e-14 and a < (sigma - f / v) < b else 0.5 * (a + b)

    return sigma


def bounds(spot: float, strike: float, tau: float, rate: float, kind: str) -> tuple[float, float]:
    disc = math.exp(-rate * tau)
    if kind == "call":
        lower = max(spot - strike * disc, 0.0)
        upper = spot
    else:
        lower = max(strike * disc - spot, 0.0)
        upper = strike * disc
    return lower, upper


def main() -> None:
    # Seed 0 grid generator
    rng = random.Random(1_000_003 * 0 + 42)
    n_target = 2000

    spots: list[float] = []
    strikes: list[float] = []
    taus: list[float] = []
    rates: list[float] = []
    kinds: list[str] = []
    prices: list[float] = []
    vols: list[float] = []
    vegas_list: list[float] = []
    while len(spots) < n_target:
        s = rng.uniform(40.0, 300.0)
        scenario = rng.choice(["near_expiry", "deep_itm", "deep_otm", "standard", "standard"])
        if scenario == "near_expiry":
            tau = rng.choice([1.0 / 365.0, 2.0 / 365.0, 7.0 / 365.0, 1.0 / 52.0])
            log_m = rng.uniform(-0.5, 0.5)
            vol = rng.uniform(0.05, 1.5)
        elif scenario == "deep_itm":
            tau = rng.uniform(0.1, 2.0)
            log_m = rng.uniform(1.0, 2.2)
            vol = rng.uniform(0.1, 2.5)
        elif scenario == "deep_otm":
            tau = rng.uniform(0.05, 1.5)
            log_m = rng.uniform(-2.2, -1.0)
            vol = rng.uniform(0.1, 2.0)
        else:
            tau = rng.uniform(0.1, 2.0)
            log_m = rng.uniform(-0.8, 0.8)
            vol = rng.uniform(0.05, 3.5)

        kind = rng.choice(["call", "put"])
        k = s * math.exp(-log_m)
        r = rng.uniform(0.01, 0.08)
        lo, hi = bounds(s, k, tau, r, kind)
        p = bs_price(s, k, tau, r, vol, kind)

        if p <= lo + 1e-8 * s or p >= hi - 1e-8 * s:
            continue

        v = vega(s, k, tau, r, vol)
        spots.append(s)
        strikes.append(k)
        taus.append(tau)
        rates.append(r)
        kinds.append(kind)
        prices.append(p)
        vols.append(vol)
        vegas_list.append(v)

    n_solved = 0
    n_ill = 0
    max_res = 0.0
    max_fwd_well_conditioned = 0.0

    for i in range(n_target):
        v_hat = solve_implied_vol(prices[i], spots[i], strikes[i], taus[i], rates[i], kinds[i])
        recalc = bs_price(spots[i], strikes[i], taus[i], rates[i], v_hat, kinds[i])
        res = abs(recalc - prices[i]) / spots[i]
        if res > max_res:
            max_res = res

        v_calc = vega(spots[i], strikes[i], taus[i], rates[i], v_hat)
        if v_calc >= 0.01:
            n_solved += 1
            fwd = abs(v_hat - vols[i])
            if fwd > max_fwd_well_conditioned:
                max_fwd_well_conditioned = fwd
        else:
            n_ill += 1

    print("=== Rung 3 Verification on Seed 0 Grid (N = 2,000) ===")
    print(f"Total processed instances: {n_target}")
    print(f"Solved (well-conditioned, vega >= 0.01): {n_solved}")
    print(f"Ill-conditioned (vega < 0.01):           {n_ill}")
    print(f"Max relative price residual:             {max_res:.2e} (bound: 1.00e-12)")
    print(f"Max forward error on solved instances:   {max_fwd_well_conditioned:.2e} (bound: 1.00e-07)")
    print(f"All residual bounds satisfied:           {max_res <= 1.0e-12}")


main()
