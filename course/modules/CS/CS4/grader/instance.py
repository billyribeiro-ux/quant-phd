"""CS4 Autograder Instance Generator.

Generates deterministic instances for the Reproducibility Audit capstone project.
For each seed, computes the exact pseudo-random test sequence and reference summary statistics
using rational arithmetic (Fraction). Returns primitive types (int, float, str) only.
"""

from __future__ import annotations

import json
from fractions import Fraction


def make_instance(seed: int) -> dict[str, int | float | str]:
    """Generate deterministic project test instance for a given seed."""
    if seed < 0:
        raise ValueError("seed must be non-negative")

    n = 200
    values: list[int] = []
    for i in range(1, n + 1):
        # Exact linear congruential generator from specification (mod 1000003 prime)
        val = (1103515245 * seed + 12345 * i * i + 7 * i) % 1000003
        values.append(val)

    s = sum(values)
    s2 = sum(v * v for v in values)
    mean_frac = Fraction(s, n)
    var_frac = Fraction(n * s2 - s * s, n * (n - 1))

    expected_payload = {
        "count": n,
        "max": max(values),
        "mean": str(mean_frac),
        "min": min(values),
        "variance": str(var_frac),
    }

    expected_text = json.dumps(expected_payload, sort_keys=True, indent=2) + "\n"
    seq_str = ",".join(str(v) for v in values)

    return {
        "seed": seed,
        "n": n,
        "sequence": seq_str,
        "expected": expected_text,
        "mean": str(mean_frac),
        "variance": str(var_frac),
        "min": min(values),
        "max": max(values),
    }
