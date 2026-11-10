"""CS6 Lab L05-1: Parallel Monte Carlo with Independent RNG Streams: Reproducibility Check.

Standard library + numpy. Validates that counter-based PRNG streams (Philox via SeedSequence)
guarantee bit-for-bit identical Monte Carlo pricing across arbitrary worker counts and chunk distributions.
"""

from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from numpy.random import Generator, Philox, SeedSequence


def simulate_stream_slice(
    base_seed: int, start_idx: int, count: int, s0: float, vol: float, r: float, tau: float
) -> np.ndarray:
    """Generate terminal asset prices using counter-based path indexing."""
    spots = np.empty(count, dtype=np.float64)
    drift = (r - 0.5 * vol * vol) * tau
    vol_sqrt = vol * math.sqrt(tau)

    for i in range(count):
        global_path = start_idx + i
        ss = SeedSequence(base_seed, spawn_key=(global_path,))
        rng = Generator(Philox(ss))
        z = float(rng.standard_normal())
        spots[i] = s0 * math.exp(drift + vol_sqrt * z)
    return spots


def run_reproducibility_check() -> None:
    base_seed = 2026
    total_paths = 8000
    s0 = 100.0
    strike = 100.0
    vol = 0.20
    rate = 0.05
    tau = 1.0
    df = math.exp(-rate * tau)

    print("=== CS6 Lab 5: Parallel Monte Carlo Stream Reproducibility Check ===")
    print(f"Total paths: {total_paths:,}, Base seed: {base_seed}, Strike: {strike}, Expiry: {tau}y\n")

    # 1. Serial Single-Worker Run
    serial_spots = simulate_stream_slice(base_seed, 0, total_paths, s0, vol, rate, tau)
    serial_payoffs = df * np.maximum(serial_spots - strike, 0.0)
    serial_price = float(np.mean(serial_payoffs))
    serial_se = float(np.std(serial_payoffs, ddof=1) / math.sqrt(total_paths))

    print("1. Serial Simulation (1 worker, paths 0..7999):")
    print(f"   Estimated Call Price:        {serial_price:.6f}")
    print(f"   Standard Error:              {serial_se:.6f}")
    print(f"   First 3 terminal prices:     {np.round(serial_spots[:3], 4)}")
    print(f"   Last 3 terminal prices:      {np.round(serial_spots[-3:], 4)}\n")

    # 2. Parallel Run: 4 Workers (2,000 paths each)
    n_workers = 4
    chunk_size = total_paths // n_workers
    ranges = [(w * chunk_size, chunk_size) for w in range(n_workers)]

    try:
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = [
                pool.submit(simulate_stream_slice, base_seed, start, count, s0, vol, rate, tau)
                for start, count in ranges
            ]
            parallel_chunks = [f.result() for f in futures]
    except RuntimeError:
        parallel_chunks = [
            simulate_stream_slice(base_seed, start, count, s0, vol, rate, tau) for start, count in ranges
        ]

    parallel_spots = np.concatenate(parallel_chunks)
    parallel_payoffs = df * np.maximum(parallel_spots - strike, 0.0)
    parallel_price = float(np.mean(parallel_payoffs))
    parallel_se = float(np.std(parallel_payoffs, ddof=1) / math.sqrt(total_paths))

    print("2. Parallel Simulation (4 workers, 2,000 paths/worker):")
    print(f"   Estimated Call Price:        {parallel_price:.6f}")
    print(f"   Standard Error:              {parallel_se:.6f}")
    print(f"   First 3 terminal prices:     {np.round(parallel_spots[:3], 4)}")
    print(f"   Last 3 terminal prices:      {np.round(parallel_spots[-3:], 4)}\n")

    # 3. Bit-for-Bit Identity and Stream Overlap Audit
    max_abs_diff = float(np.max(np.abs(serial_spots - parallel_spots)))
    price_diff = abs(serial_price - parallel_price)
    bit_identical = np.array_equal(serial_spots, parallel_spots)

    print("3. Audit & Verification Verdict:")
    print(f"   Max absolute spot error:     {max_abs_diff:.8f}")
    print(f"   Price estimate discrepancy:  {price_diff:.8f}")
    print(f"   Bit-for-bit identical paths: {bit_identical}")
    print(f"   Reconciliation verdict:      {'PASSED' if bit_identical else 'FAILED'}")


run_reproducibility_check()
