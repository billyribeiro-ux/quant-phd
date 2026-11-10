"""Deterministic SIMULATED instance generator for M8 implied-volatility autograder."""

from __future__ import annotations

import math
import random
from typing import Any


def _bs_price(spot: float, strike: float, tau: float, rate: float, vol: float, kind: str) -> float:
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


def _vega(spot: float, strike: float, tau: float, rate: float, vol: float) -> float:
    sqrt_t = math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * tau) / (vol * sqrt_t)
    return spot * sqrt_t * math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)


def _bounds(spot: float, strike: float, tau: float, rate: float, kind: str) -> tuple[float, float]:
    disc = math.exp(-rate * tau)
    if kind == "call":
        lower = max(spot - strike * disc, 0.0)
        upper = spot
    else:
        lower = max(strike * disc - spot, 0.0)
        upper = strike * disc
    return lower, upper


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic SIMULATED grid of option inversion problems.

    All generated inputs strictly lie inside the theoretical no-arbitrage bounds.
    The grid covers deep in-the-money, deep out-of-the-money, and near-expiry regimes.

    Args:
        seed: Learner workspace integer seed.

    Returns:
        Dictionary of input parameters and oracle targets.
    """
    rng = random.Random(1_000_003 * int(seed) + 42)
    n_target = 2000

    spots: list[float] = []
    strikes: list[float] = []
    taus: list[float] = []
    rates: list[float] = []
    kinds: list[str] = []
    prices: list[float] = []
    vols: list[float] = []
    vegas: list[float] = []
    regions: list[str] = []

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
        lo, hi = _bounds(s, k, tau, r, kind)
        p = _bs_price(s, k, tau, r, vol, kind)

        # Ensure strict interior status with safety buffer
        if p <= lo + 1e-8 * s or p >= hi - 1e-8 * s:
            continue

        v = _vega(s, k, tau, r, vol)
        reg = "solved" if v >= 0.01 else "ill_conditioned"

        spots.append(s)
        strikes.append(k)
        taus.append(tau)
        rates.append(r)
        kinds.append(kind)
        prices.append(p)
        vols.append(vol)
        vegas.append(v)
        regions.append(reg)

    n_solved = regions.count("solved")
    n_ill = regions.count("ill_conditioned")

    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "n_total": len(spots),
        "n_solved": n_solved,
        "n_ill_conditioned": n_ill,
        "spots": spots,
        "strikes": strikes,
        "taus": taus,
        "rates": rates,
        "kinds": kinds,
        "prices": prices,
        "vols": vols,
        "vegas": vegas,
        "regions": regions,
    }
