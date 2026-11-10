"""CS4 Lesson 6 Inline Lab 1: Deterministic computation and pseudo-random stream isolation.

Demonstrates deterministic pseudo-random number generation and state isolation.
Shows that two independent instances of random.Random seeded with identical keys produce
identical streams of draws bit-for-bit.
Demonstrates how reliance on shared global state (module-level random) introduces silent
non-determinism when intervening functions draw from the global generator.

Data: SIMULATED random streams generated with deterministic pseudo-random seeds.
"""

from __future__ import annotations

import random


def draw_stream_isolated(seed: int, count: int) -> list[int]:
    """Draw a deterministic sequence using an isolated, encapsulated generator instance."""
    rng = random.Random(seed)
    return [rng.randint(1, 1000) for _ in range(count)]


def draw_stream_global(count: int) -> list[int]:
    """Draw a sequence using global module-level random state (unencapsulated)."""
    return [random.randint(1, 1000) for _ in range(count)]


def intervening_third_party_call() -> None:
    """Simulate an external library or routine drawing from the shared global RNG."""
    _ = [random.random() for _ in range(7)]


def main() -> None:
    print("SIMULATED pseudo-random stream isolation evaluation:")

    seed = 42
    n_draws = 5

    # 1. Isolated generator determinism
    stream1 = draw_stream_isolated(seed, n_draws)
    stream2 = draw_stream_isolated(seed, n_draws)

    print(f"Isolated Generator Stream 1 (seed={seed}): {stream1}")
    print(f"Isolated Generator Stream 2 (seed={seed}): {stream2}")
    streams_equal = stream1 == stream2
    print(f"Isolated streams bit-for-bit identical: {streams_equal}")

    # 2. Global state contamination
    print("\nGlobal state contamination demonstration:")
    random.seed(seed)
    global_stream1 = draw_stream_global(n_draws)
    print(f"Global Stream Run 1 (seed={seed}): {global_stream1}")

    # Reset global seed to same value, but simulate intermediate call
    random.seed(seed)
    intervening_third_party_call()
    global_stream2 = draw_stream_global(n_draws)
    print(f"Global Stream Run 2 (after intervening call): {global_stream2}")

    global_equal = global_stream1 == global_stream2
    print(f"Global streams identical despite same seed: {global_equal}")

    print("\nConclusion: Encapsulating PRNG state in dedicated instances guarantees determinism.")


main()
