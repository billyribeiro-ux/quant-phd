"""CS6 Project Rung 1: Worked example tracing counter-based RNG stream indexing.

Standard library + numpy. SIMULATED data. Demonstrates that SeedSequence with
spawn_key=(path_idx,) produces deterministic normal draws independent of chunk boundaries.
"""

from __future__ import annotations

import numpy as np
from numpy.random import Generator, Philox, SeedSequence


def demonstrate_counter_streams() -> None:
    base_seed = 42
    n_assets = 3
    n_paths = 6

    print("=== CS6 Project Rung 1: Counter-Based Stream Indexing ===")
    print(f"Base seed: {base_seed}, Assets: {n_assets}, Total paths: {n_paths}")

    # Generate sequentially
    seq_draws = np.empty((n_paths, n_assets), dtype=np.float64)
    for i in range(n_paths):
        ss = SeedSequence(base_seed, spawn_key=(i,))
        rng = Generator(Philox(ss))
        seq_draws[i] = rng.standard_normal(n_assets)

    # Generate in 2 chunks of 3 paths
    chunk1_draws = np.empty((3, n_assets), dtype=np.float64)
    for k in range(3):
        idx = 0 + k
        ss = SeedSequence(base_seed, spawn_key=(idx,))
        rng = Generator(Philox(ss))
        chunk1_draws[k] = rng.standard_normal(n_assets)

    chunk2_draws = np.empty((3, n_assets), dtype=np.float64)
    for k in range(3):
        idx = 3 + k
        ss = SeedSequence(base_seed, spawn_key=(idx,))
        rng = Generator(Philox(ss))
        chunk2_draws[k] = rng.standard_normal(n_assets)

    parallel_draws = np.vstack([chunk1_draws, chunk2_draws])

    max_diff = float(np.max(np.abs(seq_draws - parallel_draws)))
    print(f"Serial paths 0..2:\n{np.round(seq_draws[:3], 4)}")
    print(f"Chunk 1 paths 0..2:\n{np.round(chunk1_draws, 4)}")
    print(f"Serial paths 3..5:\n{np.round(seq_draws[3:], 4)}")
    print(f"Chunk 2 paths 3..5:\n{np.round(chunk2_draws, 4)}")
    print(f"Max absolute discrepancy: {max_diff:.8f}")
    print(f"Bit-for-bit reconciliation: {np.array_equal(seq_draws, parallel_draws)}")


demonstrate_counter_streams()
