"""CS4 Capstone Project Lab 2: Rung 2 completed solution - Sequence generation and exact variance.

Completed solution for Rung 2 completion problem.
Implements the exact linear congruential sequence generator and exact sample variance.
Computes and verifies metrics on seed 10.

Data: SIMULATED study run for seed 10.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction


def generate_sequence(seed: int, n: int = 200) -> list[int]:
    """Generate deterministic sequence using the exact modular arithmetic formula."""
    if seed < 0:
        raise ValueError("seed must be non-negative")
    seq: list[int] = []
    for i in range(1, n + 1):
        val = (1103515245 * seed + 12345 * i * i + 7 * i) % 1000003
        seq.append(val)
    return seq


def summarize(values: Sequence[int]) -> dict[str, object]:
    """Compute exact summary statistics using Fraction for mean and sample variance."""
    n = len(values)
    if n < 2:
        raise ValueError("len(values) must be at least 2")
    s = sum(values)
    s2 = sum(v * v for v in values)
    mean_frac = Fraction(s, n)
    var_frac = Fraction(n * s2 - s * s, n * (n - 1))
    return {
        "count": n,
        "max": max(values),
        "mean": str(mean_frac),
        "min": min(values),
        "variance": str(var_frac),
    }


def main() -> None:
    print("SIMULATED reproducibility audit - Rung 2 completion verification:")
    seed = 10
    values = generate_sequence(seed)
    stats = summarize(values)

    print(f"Seed {seed} sequence length: {len(values)}")
    print(f"First 3 values: {values[:3]}")
    print(f"Computed mean: {stats['mean']}")
    print(f"Computed variance: {stats['variance']}")
    print(f"Output count verification: {stats['count'] == 200}")


main()
