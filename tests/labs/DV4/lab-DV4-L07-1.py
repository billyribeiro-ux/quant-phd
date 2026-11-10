"""Lab 1 (L07): Cross-method pricing consistency matrix and error envelope validation.

SIMULATED market parameters under geometric Brownian motion.
Prices European vanilla options across strikes and maturities using analytical BSM,
binomial tree, trinomial tree, Crank-Nicolson PDE, and Monte Carlo simulation,
verifying that all numerical solvers fall within their theoretical error envelopes.
"""

from __future__ import annotations

import math

import numpy as np


def bsm_call(s: float, k: float, r: float, v: float, t: float) -> float:
    sq = math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * v * v) * t) / (v * sq)
    d2 = d1 - v * sq
    n1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    n2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return float(s * n1 - k * math.exp(-r * t) * n2)


def binomial_call(s: float, k: float, r: float, v: float, t: float, n: int = 150) -> float:
    dt = t / n
    u = math.exp(v * math.sqrt(dt))
    d = 1.0 / u
    df = math.exp(-r * dt)
    p = (math.exp(r * dt) - d) / (u - d)
    st = s * (u ** np.arange(n + 1)) * (d ** np.arange(n, -1, -1))
    vals = np.maximum(st - k, 0.0)
    for step in range(n - 1, -1, -1):
        vals = df * (p * vals[1 : step + 2] + (1.0 - p) * vals[0 : step + 1])
    return float(vals[0])


def trinomial_call(s: float, k: float, r: float, v: float, t: float, n: int = 100) -> float:
    dt = t / n
    dx = v * math.sqrt(3.0 * dt)
    df = math.exp(-r * dt)
    nu = (r - 0.5 * v * v) * dt
    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)
    indices = np.arange(-n, n + 1)
    st = s * np.exp(indices * dx)
    vals = np.maximum(st - k, 0.0)
    for step in range(n - 1, -1, -1):
        vals = df * (pu * vals[2 : 2 * step + 3] + pm * vals[1 : 2 * step + 2] + pd * vals[0 : 2 * step + 1])
    return float(vals[0])


def pde_call(s: float, k: float, r: float, v: float, t: float, n_t: int = 60, n_x: int = 70) -> float:
    std = v * math.sqrt(t)
    x_max = 4.0 * std + r * t
    x_min = -4.0 * std
    dx = (x_max - x_min) / (n_x - 1)
    dt = t / n_t
    x = np.linspace(x_min, x_max, n_x)
    sg = k * np.exp(x)
    vals = np.maximum(sg - k, 0.0)
    mu = r - 0.5 * v * v
    alpha = 0.5 * (v * v) / (dx * dx)
    beta = 0.5 * mu / dx
    a_c = alpha - beta
    b_c = -2.0 * alpha - r
    c_c = alpha + beta
    theta = 0.5
    m = n_x - 2
    diag_a = -dt * theta * a_c * np.ones(m)
    diag_b = (1.0 - dt * theta * b_c) * np.ones(m)
    diag_c = -dt * theta * c_c * np.ones(m)
    for step in range(1, n_t + 1):
        tau = step * dt
        rhs = vals[1:-1] + dt * (1.0 - theta) * (a_c * vals[:-2] + b_c * vals[1:-1] + c_c * vals[2:])
        bc_up = sg[-1] - k * math.exp(-r * tau)
        rhs[-1] += dt * theta * c_c * bc_up
        # Thomas solver
        c_p = np.zeros(m)
        d_p = np.zeros(m)
        c_p[0] = diag_c[0] / diag_b[0]
        d_p[0] = rhs[0] / diag_b[0]
        for i in range(1, m):
            denom = diag_b[i] - diag_a[i] * c_p[i - 1]
            c_p[i] = diag_c[i] / denom if i < m - 1 else 0.0
            d_p[i] = (rhs[i] - diag_a[i] * d_p[i - 1]) / denom
        v_next = np.zeros(m)
        v_next[-1] = d_p[-1]
        for i in range(m - 2, -1, -1):
            v_next[i] = d_p[i] - c_p[i] * v_next[i + 1]
        vals[0] = 0.0
        vals[-1] = bc_up
        vals[1:-1] = v_next
    return float(np.interp(s, sg, vals))


def mc_call(s: float, k: float, r: float, v: float, t: float, n_paths: int = 15_000, seed: int = 42) -> float:
    rng = np.random.default_rng(seed)
    half = n_paths // 2
    z = rng.standard_normal(half)
    drift = (r - 0.5 * v * v) * t
    vol_t = v * math.sqrt(t)
    s_pos = s * np.exp(drift + vol_t * z)
    s_neg = s * np.exp(drift - vol_t * z)
    df = math.exp(-r * t)
    p_pos = np.maximum(s_pos - k, 0.0)
    p_neg = np.maximum(s_neg - k, 0.0)
    return float(df * 0.5 * np.mean(p_pos + p_neg))


def main() -> None:
    spot = 100.0
    rate = 0.05
    vol = 0.20
    test_grid = [(90.0, 0.5), (100.0, 1.0), (110.0, 1.5)]

    print("Cross-method pricing consistency matrix (Call Options):")
    print("Strike  Maturity |   BSM     Binomial  Trinomial   PDE        MC     | Max Error")
    print("-" * 75)

    all_consistent = True
    for strike, maturity in test_grid:
        p_bsm = bsm_call(spot, strike, rate, vol, maturity)
        p_bin = binomial_call(spot, strike, rate, vol, maturity)
        p_tri = trinomial_call(spot, strike, rate, vol, maturity)
        p_pde = pde_call(spot, strike, rate, vol, maturity)
        p_mc = mc_call(spot, strike, rate, vol, maturity)

        errors = [abs(p - p_bsm) for p in (p_bin, p_tri, p_pde, p_mc)]
        max_err = max(errors)
        tolerance = 0.05 * max(p_bsm, 1.0) + 0.05
        consistent = max_err <= tolerance
        all_consistent = all_consistent and consistent

        line = (
            f"{strike:5.1f}   {maturity:4.1f} yr | "
            f"{p_bsm:8.4f}  {p_bin:8.4f}  {p_tri:8.4f}  {p_pde:8.4f}  {p_mc:8.4f} |  {max_err:6.4f}"
        )
        print(line)

    print("-" * 75)
    print(f"All methods consistent within tolerance envelope: {all_consistent}")


main()
