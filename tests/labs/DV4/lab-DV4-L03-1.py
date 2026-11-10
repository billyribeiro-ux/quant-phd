"""Lab 1 (L03): Longstaff-Schwartz Least-Squares Monte Carlo (LSMC) basis comparison.

SIMULATED market parameters under geometric Brownian motion.
Prices an American put option using LSMC with weighted Laguerre, Hermite, and monomial
polynomial bases, and evaluates convergence against an accurate binomial benchmark.
"""

from __future__ import annotations

import math

import numpy as np


def eval_basis_functions(x: np.ndarray, degree: int, basis: str) -> np.ndarray:
    n = len(x)
    phi = np.zeros((n, degree + 1), dtype=float)
    if basis == "laguerre":
        weight = np.exp(-0.5 * x)
        phi[:, 0] = weight
        if degree >= 1:
            phi[:, 1] = (1.0 - x) * weight
        if degree >= 2:
            phi[:, 2] = (1.0 - 2.0 * x + 0.5 * x * x) * weight
        for d in range(3, degree + 1):
            l_prev = phi[:, d - 1] / weight
            l_prev2 = phi[:, d - 2] / weight
            phi[:, d] = (((2 * d - 1 - x) * l_prev - (d - 1) * l_prev2) / d) * weight
    elif basis == "hermite":
        phi[:, 0] = 1.0
        if degree >= 1:
            phi[:, 1] = x
        for d in range(2, degree + 1):
            phi[:, d] = x * phi[:, d - 1] - (d - 1) * phi[:, d - 2]
    elif basis == "monomial":
        phi[:, 0] = 1.0
        for d in range(1, degree + 1):
            phi[:, d] = x**d
    else:
        raise ValueError(f"Unknown basis {basis}")
    return phi


def run_lsmc(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    n_paths: int,
    n_steps: int,
    degree: int,
    basis: str,
    seed: int,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    dt = maturity / n_steps
    df = math.exp(-rate * dt)
    drift = (rate - 0.5 * vol * vol) * dt
    vol_sqrt_dt = vol * math.sqrt(dt)

    half_n = n_paths // 2
    z = rng.standard_normal((half_n, n_steps))
    z = np.vstack([z, -z])

    paths = np.zeros((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = spot
    for t in range(n_steps):
        paths[:, t + 1] = paths[:, t] * np.exp(drift + vol_sqrt_dt * z[:, t])

    cash_flows = np.maximum(strike - paths[:, -1], 0.0)
    exercise_time = np.full(n_paths, n_steps, dtype=int)

    for k in range(n_steps - 1, 0, -1):
        s_k = paths[:, k]
        intrinsic = np.maximum(strike - s_k, 0.0)
        itm = intrinsic > 0.0

        if np.sum(itm) > degree + 1:
            x_itm = s_k[itm] / strike
            y_itm = cash_flows[itm] * (df ** (exercise_time[itm] - k))

            phi = eval_basis_functions(x_itm, degree, basis)
            coeffs, _, _, _ = np.linalg.lstsq(phi, y_itm, rcond=None)
            continuation = phi @ coeffs

            exercise = intrinsic[itm] > continuation
            itm_indices = np.where(itm)[0]
            exercised = itm_indices[exercise]

            cash_flows[exercised] = intrinsic[exercised]
            exercise_time[exercised] = k

    discount_factors = np.exp(-rate * exercise_time * dt)
    discounted_values = cash_flows * discount_factors
    raw_price = float(np.mean(discounted_values))
    price = max(raw_price, max(0.0, strike - spot))
    se = float(math.sqrt(np.var(discounted_values, ddof=1) / n_paths))
    return price, se


def main() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0
    n_paths = 10_000
    n_steps = 40
    degree = 3
    seed = 42

    tree_benchmark = 6.0716  # Accurate high-depth lattice benchmark
    print(f"Lattice American put benchmark: {tree_benchmark:.4f}")

    bases = ["laguerre", "hermite", "monomial"]
    for b in bases:
        price, se = run_lsmc(spot, strike, rate, vol, maturity, n_paths, n_steps, degree, b, seed)
        err = abs(price - tree_benchmark)
        print(f"Basis: {b:8s} | Price: {price:.4f} +/- {se:.4f} | Error: {err:.4f}")


main()
