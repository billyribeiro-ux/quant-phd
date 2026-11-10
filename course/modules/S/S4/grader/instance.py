"""Instance generator for S4 autograder: Atlas A4 time-series toolkit.

Deterministic per seed, generating valid simulation datasets for GARCH, HAR,
Kalman filtering, and ARMA estimation.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic instance for seed in 0..49."""
    rng = random.Random(seed * 10007 + 42)

    # 1. GARCH(1,1) returns path
    n_ret = 500 + (seed % 3) * 100  # 500, 600, or 700
    alpha = 0.06 + 0.0015 * (seed % 10)
    beta = 0.82 + 0.0010 * ((seed * 3) % 10)
    omega = 0.02 + 0.001 * ((seed * 7) % 10)
    uncond_var = omega / (1.0 - alpha - beta)

    # Burn-in 200 periods
    h = uncond_var
    for _ in range(200):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        h = omega + alpha * (eps**2) + beta * h

    returns: list[float] = []
    garch_h: list[float] = []
    for _ in range(n_ret):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        returns.append(eps)
        garch_h.append(h)
        h = omega + alpha * (eps**2) + beta * h

    # 2. HAR Realized Volatility series (length 400)
    n_rv = 400
    beta_0 = 0.03 + 0.001 * ((seed * 2) % 10)
    beta_d = 0.35 + 0.005 * ((seed * 5) % 10)
    beta_w = 0.28 + 0.004 * ((seed * 4) % 10)
    beta_m = 0.18 + 0.003 * ((seed * 6) % 10)
    uncond_rv = beta_0 / (1.0 - beta_d - beta_w - beta_m)

    rv_hist = [uncond_rv] * 25
    for _ in range(n_rv):
        d = rv_hist[-1]
        w = sum(rv_hist[-5:]) / 5.0
        m = sum(rv_hist[-22:]) / 22.0
        shock = rng.gauss(0.0, 0.015)
        next_val = max(0.005, beta_0 + beta_d * d + beta_w * w + beta_m * m + shock)
        rv_hist.append(next_val)
    rv = rv_hist[25:]

    # 3. Kalman local-level series (length 300)
    n_k = 300
    sigma_w2 = 0.01 + 0.001 * (seed % 8)
    sigma_v2 = 0.04 + 0.002 * ((seed * 3) % 8)
    x_level = 10.0
    kalman_y: list[float] = []
    for _ in range(n_k):
        x_level += rng.gauss(0.0, math.sqrt(sigma_w2))
        kalman_y.append(x_level + rng.gauss(0.0, math.sqrt(sigma_v2)))

    # 4. ARMA(1,1) series (length 400)
    n_arma = 400
    phi = 0.45 + 0.01 * (seed % 10)
    theta = 0.30 + 0.01 * ((seed * 3) % 10)
    sigma2_a = 1.0 + 0.02 * (seed % 5)

    arma_x = [0.0]
    e_prev = 0.0
    # Burn-in 100 periods
    for _ in range(100):
        e = rng.gauss(0.0, math.sqrt(sigma2_a))
        arma_x[0] = phi * arma_x[0] + e + theta * e_prev
        e_prev = e

    arma_series: list[float] = []
    curr_x = arma_x[0]
    for _ in range(n_arma):
        e = rng.gauss(0.0, math.sqrt(sigma2_a))
        curr_x = phi * curr_x + e + theta * e_prev
        arma_series.append(curr_x)
        e_prev = e

    return {
        "seed": seed,
        "returns": returns,
        "true_garch": [omega, alpha, beta, uncond_var],
        "rv": rv,
        "true_har": [beta_0, beta_d, beta_w, beta_m],
        "kalman_y": kalman_y,
        "sigma_w2": sigma_w2,
        "sigma_v2": sigma_v2,
        "arma_x": arma_series,
        "true_arma": [phi, theta, sigma2_a],
    }
