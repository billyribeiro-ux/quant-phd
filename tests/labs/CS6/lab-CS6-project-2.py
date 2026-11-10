"""CS6 Project Rung 2: Completion problem for parallel chunk partition and VaR estimation.

Standard library + numpy. SIMULATED data. Fills in worker path chunk partitioning
and empirical VaR quantile computation.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.random import Generator, Philox, SeedSequence


def simulate_chunk(base_seed: int, start: int, count: int, s0: float, sigma: float, dt: float) -> np.ndarray:
    spots = np.empty(count, dtype=np.float64)
    drift = -0.5 * sigma * sigma * dt
    vol_sqrt = sigma * math.sqrt(dt)
    for i in range(count):
        idx = start + i
        ss = SeedSequence(base_seed, spawn_key=(idx,))
        rng = Generator(Philox(ss))
        z = float(rng.standard_normal())
        spots[i] = s0 * math.exp(drift + vol_sqrt * z)
    return spots


def complete_parallel_risk(n_paths: int = 1000, n_workers: int = 2) -> tuple[float, float, float]:
    base_seed = 101
    s0 = 100.0
    sigma = 0.20
    dt = 1.0 / 252.0
    alpha = 0.95

    chunk_size = n_paths // n_workers
    chunks: list[np.ndarray] = []

    for w in range(n_workers):
        # Completed line 1: chunk start and end bounds
        start = w * chunk_size
        end = (w + 1) * chunk_size if w < n_workers - 1 else n_paths
        count = end - start
        chunks.append(simulate_chunk(base_seed, start, count, s0, sigma, dt))

    terminal_spots = np.concatenate(chunks)
    losses = s0 - terminal_spots

    # Completed line 2: empirical VaR quantile index calculation
    sorted_losses = np.sort(losses)
    idx = math.ceil(alpha * len(sorted_losses)) - 1
    var_95 = float(sorted_losses[idx])
    es_95 = float(np.mean(sorted_losses[idx:]))
    max_loss = float(sorted_losses[-1])

    return var_95, es_95, max_loss


v95, es95, m_loss = complete_parallel_risk(1000, 2)
print("=== CS6 Project Rung 2: Completion Problem Output ===")
print("Paths: 1000, Workers: 2, Alpha: 0.95")
print(f"Estimated 95% VaR: {v95:.4f}")
print(f"Estimated 95% ES:  {es95:.4f}")
print(f"Maximum loss:      {m_loss:.4f}")
