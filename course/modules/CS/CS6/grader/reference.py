"""CS6 Project Reference: Parallel Full-Portfolio Monte Carlo VaR Engine.

High-performance, bit-for-bit reproducible portfolio risk engine using
counter-based parallel random number generation (Philox via SeedSequence).
"""

from __future__ import annotations

import math
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import numpy as np
from numpy.random import Generator, Philox, SeedSequence


def _norm_cdf(x: np.ndarray | float) -> np.ndarray | float:
    """Elementwise standard normal cumulative distribution function via math.erf."""
    if isinstance(x, np.ndarray):
        flat = [0.5 * (1.0 + math.erf(float(v) / math.sqrt(2.0))) for v in x.flat]
        return np.asarray(flat, dtype=np.float64).reshape(x.shape)
    return 0.5 * (1.0 + math.erf(float(x) / math.sqrt(2.0)))


def cholesky_factor(corr_matrix: list[list[float]]) -> np.ndarray:
    """Compute lower-triangular Cholesky factor L such that L @ L.T = corr_matrix."""
    mat = np.asarray(corr_matrix, dtype=np.float64)
    if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
        raise ValueError("Correlation matrix must be square 2D array.")
    return np.linalg.cholesky(mat)


def black_scholes_price(
    spot: float | np.ndarray,
    strike: float,
    expiry: float,
    rate: float,
    vol: float,
    is_call: bool,
) -> float | np.ndarray:
    """Compute European option price using analytical Black-Scholes formula."""
    if expiry <= 0.0:
        if is_call:
            return np.maximum(spot - strike, 0.0) if isinstance(spot, np.ndarray) else max(spot - strike, 0.0)
        return np.maximum(strike - spot, 0.0) if isinstance(spot, np.ndarray) else max(strike - spot, 0.0)
    if vol <= 0.0:
        raise ValueError("Volatility must be strictly positive.")

    sqrt_t = math.sqrt(expiry)
    d1 = (np.log(spot / strike) + (rate + 0.5 * vol * vol) * expiry) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    df = math.exp(-rate * expiry)

    if is_call:
        return spot * _norm_cdf(d1) - strike * df * _norm_cdf(d2)
    return strike * df * _norm_cdf(-d2) - spot * _norm_cdf(-d1)


def simulate_paths_chunk(
    instance: dict[str, Any],
    start_idx: int,
    count: int,
) -> np.ndarray:
    """Simulate terminal asset prices for path indices [start_idx, start_idx + count).

    Uses independent counter-based RNG streams via SeedSequence with spawn_key=(global_path_idx,)
    and Philox bitgenerator to guarantee bit-for-bit reproducibility across thread counts.
    """
    if count <= 0:
        return np.empty((0, int(instance["n_assets"])), dtype=np.float64)

    n_assets = int(instance["n_assets"])
    base_seed = int(instance["base_seed"])
    s0 = np.asarray(instance["s0"], dtype=np.float64)
    vols = np.asarray(instance["volatilities"], dtype=np.float64)
    drift = float(instance["drift"])
    horizon = float(instance["horizon"])

    l_mat = cholesky_factor(instance["corr_matrix"])
    drift_vec = (drift - 0.5 * vols * vols) * horizon
    vol_sqrt_h = vols * math.sqrt(horizon)

    spots = np.empty((count, n_assets), dtype=np.float64)

    for k in range(count):
        global_idx = start_idx + k
        ss = SeedSequence(base_seed, spawn_key=(global_idx,))
        rng = Generator(Philox(ss))
        z_uncorr = rng.standard_normal(n_assets)
        z_corr = z_uncorr @ l_mat.T
        spots[k, :] = s0 * np.exp(drift_vec + vol_sqrt_h * z_corr)

    return spots


def value_portfolio(
    spot_matrix: np.ndarray,
    instance: dict[str, Any],
    at_horizon: bool = True,
) -> np.ndarray:
    """Compute mark-to-market portfolio value across simulated asset paths."""
    weights = np.asarray(instance["weights"], dtype=np.float64)
    drift = float(instance["drift"])
    horizon = float(instance["horizon"]) if at_horizon else 0.0

    # Equity value: (N, n_assets) @ (n_assets,) -> (N,)
    equity_val = spot_matrix @ weights

    # Options values
    n_options = len(instance["option_underlyings"])
    options_val = np.zeros(spot_matrix.shape[0], dtype=np.float64)

    for i in range(n_options):
        u_idx = int(instance["option_underlyings"][i])
        strike = float(instance["option_strikes"][i])
        expiry = float(instance["option_expiries"][i]) - horizon
        is_call = bool(instance["option_is_calls"][i])
        qty = float(instance["option_quantities"][i])
        vol = float(instance["volatilities"][u_idx])

        opt_price = black_scholes_price(
            spot=spot_matrix[:, u_idx],
            strike=strike,
            expiry=expiry,
            rate=drift,
            vol=vol,
            is_call=is_call,
        )
        options_val += qty * np.asarray(opt_price, dtype=np.float64)

    return equity_val + options_val


def compute_var_es(
    losses: np.ndarray,
    alpha: float,
) -> tuple[float, float]:
    """Compute Value-at-Risk and Expected Shortfall from 1D array of portfolio losses."""
    if not (0.0 < alpha < 1.0):
        raise ValueError("Confidence level alpha must be strictly between 0 and 1.")
    if losses.size == 0:
        raise ValueError("Loss array cannot be empty.")

    sorted_losses = np.sort(losses)
    idx = math.ceil(alpha * len(sorted_losses)) - 1
    idx = min(max(idx, 0), len(sorted_losses) - 1)
    var_val = float(sorted_losses[idx])

    tail = sorted_losses[idx:]
    es_val = float(np.mean(tail)) if tail.size > 0 else var_val
    return var_val, es_val


def run_serial_simulation(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute full Monte Carlo VaR simulation in serial mode."""
    n_paths = int(instance["n_paths"])
    if n_paths <= 0:
        raise ValueError("Number of simulation paths must be strictly positive.")
    alpha = float(instance["alpha"])

    t0 = time.perf_counter()

    # Initial portfolio value at t=0
    s0 = np.asarray(instance["s0"], dtype=np.float64).reshape(1, -1)
    v0 = float(value_portfolio(s0, instance, at_horizon=False)[0])

    # Simulate terminal spot prices
    spots = simulate_paths_chunk(instance, 0, n_paths)
    v_tau = value_portfolio(spots, instance, at_horizon=True)
    losses = v0 - v_tau
    var_val, es_val = compute_var_es(losses, alpha)

    runtime_s = time.perf_counter() - t0

    return {
        "losses": losses,
        "var": var_val,
        "es": es_val,
        "portfolio_v0": v0,
        "runtime_s": runtime_s,
        "spots": spots,
    }


def run_parallel_simulation(
    instance: dict[str, Any],
    n_workers: int = 4,
) -> dict[str, Any]:
    """Execute full Monte Carlo VaR simulation partitioned across n_workers."""
    n_paths = int(instance["n_paths"])
    if n_paths <= 0:
        raise ValueError("Number of simulation paths must be strictly positive.")
    if n_workers < 1:
        raise ValueError("Number of workers must be at least 1.")
    alpha = float(instance["alpha"])

    t0 = time.perf_counter()

    # Initial portfolio value at t=0
    s0 = np.asarray(instance["s0"], dtype=np.float64).reshape(1, -1)
    v0 = float(value_portfolio(s0, instance, at_horizon=False)[0])

    # Partition paths into balanced contiguous chunks
    chunk_size = n_paths // n_workers
    ranges: list[tuple[int, int]] = []
    for w in range(n_workers):
        start = w * chunk_size
        end = (w + 1) * chunk_size if w < n_workers - 1 else n_paths
        ranges.append((start, end - start))

    # Execute chunks in parallel (with fallback for single-threaded WASM / Pyodide runtimes)
    try:
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = [pool.submit(simulate_paths_chunk, instance, start, count) for start, count in ranges]
            chunk_results = [f.result() for f in futures]
    except RuntimeError:
        chunk_results = [simulate_paths_chunk(instance, start, count) for start, count in ranges]

    spots = np.vstack(chunk_results) if chunk_results else np.empty((0, int(instance["n_assets"])))
    v_tau = value_portfolio(spots, instance, at_horizon=True)
    losses = v0 - v_tau
    var_val, es_val = compute_var_es(losses, alpha)

    runtime_s = time.perf_counter() - t0

    return {
        "losses": losses,
        "var": var_val,
        "es": es_val,
        "portfolio_v0": v0,
        "runtime_s": runtime_s,
        "spots": spots,
        "n_workers": n_workers,
    }


def reconcile_runs(
    serial_result: dict[str, Any],
    parallel_result: dict[str, Any],
    tol: float = 1e-7,
) -> dict[str, Any]:
    """Reconcile serial and parallel simulation outputs."""
    s_losses = np.asarray(serial_result["losses"], dtype=np.float64)
    p_losses = np.asarray(parallel_result["losses"], dtype=np.float64)

    if s_losses.shape != p_losses.shape:
        return {
            "reconciled": False,
            "max_loss_diff": float("inf"),
            "var_diff": float("inf"),
            "es_diff": float("inf"),
        }

    max_loss_diff = float(np.max(np.abs(s_losses - p_losses)))
    var_diff = abs(float(serial_result["var"]) - float(parallel_result["var"]))
    es_diff = abs(float(serial_result["es"]) - float(parallel_result["es"]))

    reconciled = (max_loss_diff <= tol) and (var_diff <= tol) and (es_diff <= tol)

    return {
        "reconciled": reconciled,
        "max_loss_diff": max_loss_diff,
        "var_diff": var_diff,
        "es_diff": es_diff,
    }


def benchmark_scaling(
    instance: dict[str, Any],
    worker_counts: list[int],
) -> dict[int, dict[str, float]]:
    """Measure execution runtime, speedup, and parallel efficiency across worker counts."""
    # Run single-worker baseline
    t1_res = run_parallel_simulation(instance, n_workers=1)
    t1 = max(t1_res["runtime_s"], 1e-6)

    results: dict[int, dict[str, float]] = {}
    for w in worker_counts:
        if w == 1:
            results[1] = {"runtime_s": t1, "speedup": 1.0, "efficiency": 1.0}
        else:
            w_res = run_parallel_simulation(instance, n_workers=w)
            tw = max(w_res["runtime_s"], 1e-6)
            speedup = t1 / tw
            efficiency = speedup / float(w)
            results[w] = {"runtime_s": tw, "speedup": speedup, "efficiency": efficiency}

    return results
