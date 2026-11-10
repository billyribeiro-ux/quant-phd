"""CS4 Capstone Project Lab 3: Rung 3 independent project reference verification.

Executes the reference study implementation for seed 7.
Prints the exact deterministic JSON output that the student's repository must reproduce bit-for-bit.

Data: SIMULATED study reference execution for seed 7.
"""

from __future__ import annotations

import json
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


def run(seed: int) -> str:
    """Generate sequence, compute summary statistics, and return formatted JSON."""
    seq = generate_sequence(seed)
    stats = summarize(seq)
    return json.dumps(stats, sort_keys=True, indent=2) + "\n"


def main() -> None:
    seed = 7
    output = run(seed)
    print(f"SIMULATED study reference output for seed {seed}:")
    print(output.strip())


main()
