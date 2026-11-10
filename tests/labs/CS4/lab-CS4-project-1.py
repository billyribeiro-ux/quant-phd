"""CS4 Capstone Project Lab 1: Rung 1 worked example - Repairing wall-clock time leak.

Demonstrates the triage and repair of Defect D3 (wall-clock timestamp injected into output).
Shows that broken execution produces divergent outputs between consecutive runs with the same seed.
Shows that the repaired deterministic engine produces bit-for-bit identical outputs.

Data: SIMULATED study execution on fixed seed 42.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from fractions import Fraction


def generate_sequence(seed: int, n: int = 200) -> list[int]:
    """Generate deterministic sequence using the exact LCG formula from spec."""
    if seed < 0:
        raise ValueError("seed must be non-negative")
    seq: list[int] = []
    for i in range(1, n + 1):
        val = (1103515245 * seed + 12345 * i * i + 7 * i) % 1000003
        seq.append(val)
    return seq


def summarize(values: Sequence[int]) -> dict[str, object]:
    """Compute exact summary statistics using Fraction."""
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


def run_broken_with_timestamp(seed: int, fake_time: str) -> str:
    """Broken implementation injecting variable timestamp."""
    seq = generate_sequence(seed)
    stats = summarize(seq)
    payload = dict(stats)
    payload["timestamp"] = fake_time
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def run_repaired(seed: int) -> str:
    """Repaired implementation without timestamp."""
    seq = generate_sequence(seed)
    stats = summarize(seq)
    return json.dumps(stats, sort_keys=True, indent=2) + "\n"


def main() -> None:
    print("SIMULATED reproducibility audit - Defect D3 repair (worked example):")
    seed = 42

    # Broken engine with timestamp
    broken_run1 = run_broken_with_timestamp(seed, "2026-11-10T09:00:00.123456Z")
    broken_run2 = run_broken_with_timestamp(seed, "2026-11-10T09:00:00.654321Z")

    print("Broken engine (with timestamp) comparison:")
    print(f"Run 1 matches Run 2: {broken_run1 == broken_run2}")

    # Repaired engine without timestamp
    repaired_run1 = run_repaired(seed)
    repaired_run2 = run_repaired(seed)

    print("\nRepaired engine (deterministic) comparison:")
    print(f"Run 1 matches Run 2: {repaired_run1 == repaired_run2}")
    print("\nRepaired output preview (seed 42):")
    for line in repaired_run1.splitlines()[:7]:
        print(f"  {line}")


main()
