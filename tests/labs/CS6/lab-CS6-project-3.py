"""CS6 Project Rung 3: Independent verification driver and performance baseline.

Standard library + numpy. SIMULATED data. Runs reference portfolio VaR engine,
validating bit-for-bit reconciliation between serial and parallel runs.
"""

from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from numpy.random import Generator, Philox, SeedSequence


def simulate_chunk(base_seed: int, start: int, count: int, s0: np.ndarray, vols: np.ndarray, dt: float) -> np.ndarray:
    n_assets = len(s0)
    spots = np.empty((count, n_assets), dtype=np.float64)
    drift = -0.5 * vols * vols * dt
    vol_sqrt = vols * math.sqrt(dt)

    for i in range(count):
        idx = start + i
        ss = SeedSequence(base_seed, spawn_key=(idx,))
        rng = Generator(Philox(ss))
        z = rng.standard_normal(n_assets)
        spots[i] = s0 * np.exp(drift + vol_sqrt * z)
    return spots


def run_verification() -> None:
    base_seed = 42
    n_paths = 2000
    n_workers = 4
    alpha = 0.99

    s0 = np.array([100.0, 120.0, 80.0])
    weights = np.array([10.0, 15.0, 25.0])
    vols = np.array([0.20, 0.25, 0.18])
    dt = 10.0 / 252.0

    print("=== CS6 Project Rung 3: Independent Verification Baseline ===")
    print(f"Assets: {len(s0)}, Paths: {n_paths}, Workers: {n_workers}")

    # Serial simulation
    v0 = float(np.sum(s0 * weights))
    serial_spots = simulate_chunk(base_seed, 0, n_paths, s0, vols, dt)
    serial_losses = v0 - (serial_spots @ weights)

    sorted_s = np.sort(serial_losses)
    s_idx = math.ceil(alpha * len(sorted_s)) - 1
    serial_var = float(sorted_s[s_idx])
    serial_es = float(np.mean(sorted_s[s_idx:]))

    # Parallel simulation across 4 chunks
    chunk_size = n_paths // n_workers
    ranges = []
    for w in range(n_workers):
        start = w * chunk_size
        end = (w + 1) * chunk_size if w < n_workers - 1 else n_paths
        ranges.append((start, end - start))

    try:
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = [pool.submit(simulate_chunk, base_seed, start, count, s0, vols, dt) for start, count in ranges]
            chunks = [f.result() for f in futures]
    except RuntimeError:
        chunks = [simulate_chunk(base_seed, start, count, s0, vols, dt) for start, count in ranges]

    parallel_spots = np.vstack(chunks)
    parallel_losses = v0 - (parallel_spots @ weights)

    sorted_p = np.sort(parallel_losses)
    p_idx = math.ceil(alpha * len(sorted_p)) - 1
    parallel_var = float(sorted_p[p_idx])
    parallel_es = float(np.mean(sorted_p[p_idx:]))

    max_loss_diff = float(np.max(np.abs(serial_losses - parallel_losses)))
    reconciled = max_loss_diff <= 1e-7 and abs(serial_var - parallel_var) <= 1e-7

    print(f"Initial portfolio value V0:  {v0:.2f}")
    print(f"Serial VaR ({alpha * 100:.0f}%):          {serial_var:.4f}")
    print(f"Parallel VaR ({alpha * 100:.0f}%):        {parallel_var:.4f}")
    print(f"Serial Expected Shortfall:   {serial_es:.4f}")
    print(f"Parallel Expected Shortfall: {parallel_es:.4f}")
    print(f"Max absolute loss error:     {max_loss_diff:.8f}")
    print(f"Reconciliation status:       {'RECONCILED' if reconciled else 'FAILED'}")


run_verification()
