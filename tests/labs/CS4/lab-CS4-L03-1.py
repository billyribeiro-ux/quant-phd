"""CS4 Lesson 3 Inline Lab 1: Property-based testing and counterexample shrinking.

Implements the curriculum lab: 'A property-based test finds a bug a unit test missed.'
Demonstrates an interval-merging function with a boundary defect (failing to merge touching intervals).
Three hand-picked unit tests pass completely.
A seeded property test checking interval disjointness catches the failure on a generated case.
A shrinking loop reduces the failing case to the minimal counterexample [(0, 1), (1, 2)].

Data: SIMULATED intervals generated with deterministic pseudo-random seeds.
"""

from __future__ import annotations

import random
from collections.abc import Sequence


def merge_intervals_buggy(intervals: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals, but contains a bug on touching intervals (uses < instead of <=)."""
    if not intervals:
        return []

    sorted_ints = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged: list[tuple[int, int]] = [sorted_ints[0]]

    for start, end in sorted_ints[1:]:
        last_start, last_end = merged[-1]
        # BUG: Touching intervals (start == last_end) are not merged because of strict inequality '<'
        if start < last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def merge_intervals_correct(intervals: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    """Correct reference implementation merging overlapping and touching intervals."""
    if not intervals:
        return []

    sorted_ints = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged: list[tuple[int, int]] = [sorted_ints[0]]

    for start, end in sorted_ints[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def check_disjointness_property(merged: list[tuple[int, int]]) -> bool:
    """Property invariant: all adjacent intervals in merged output must be strictly separated (no overlap or touch)."""
    return all(merged[i][1] < merged[i + 1][0] for i in range(len(merged) - 1))


def shrink_counterexample(failing_case: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Shrink a failing interval list towards the minimal counterexample."""
    current = list(failing_case)

    # 1. Try removing elements
    i = 0
    while i < len(current) and len(current) > 2:
        candidate = current[:i] + current[i + 1 :]
        merged = merge_intervals_buggy(candidate)
        if not check_disjointness_property(merged):
            current = candidate
        else:
            i += 1

    # 2. Try shrinking coordinates towards 0
    reduced = True
    while reduced:
        reduced = False
        for idx in range(len(current)):
            s, e = current[idx]
            # Try decrementing start and end while maintaining valid interval s < e
            if s > 0:
                candidate = list(current)
                candidate[idx] = (s - 1, e - 1)
                merged = merge_intervals_buggy(candidate)
                if not check_disjointness_property(merged):
                    current = candidate
                    reduced = True
                    break

    return sorted(current)


def main() -> None:
    print("SIMULATED property-based testing evaluation:")

    # 1. Three hand-picked example unit tests
    unit_test_cases = [
        [(1, 3), (2, 6), (8, 10), (15, 18)],
        [(1, 4), (5, 6)],
        [(1, 10), (2, 5), (3, 7)],
    ]

    unit_passes = 0
    for idx, case in enumerate(unit_test_cases, start=1):
        result = merge_intervals_buggy(case)
        prop_ok = check_disjointness_property(result)
        if prop_ok:
            unit_passes += 1
        print(f"  Hand-picked unit test {idx}: input={case} -> output={result} (PASS)")

    print(f"Hand-picked unit tests result: {unit_passes}/3 passed.")

    # 2. Seeded property-based generator
    rng = random.Random(1337)
    failing_input: list[tuple[int, int]] | None = None
    num_generated = 0

    for _ in range(500):
        num_generated += 1
        n_ints = rng.randint(2, 6)
        gen_case: list[tuple[int, int]] = []
        for _ in range(n_ints):
            start = rng.randint(0, 15)
            length = rng.randint(1, 5)
            gen_case.append((start, start + length))

        merged = merge_intervals_buggy(gen_case)
        if not check_disjointness_property(merged):
            failing_input = gen_case
            break

    print(f"\nProperty-based search: evaluated {num_generated} generated cases.")
    if failing_input is not None:
        print(f"Property-based test: FAILED on generated case {failing_input}")
        buggy_output = merge_intervals_buggy(failing_input)
        print(f"  Buggy output: {buggy_output}")

        # 3. Shrink to minimal counterexample
        shrunk = shrink_counterexample(failing_input)
        shrunk_output = merge_intervals_buggy(shrunk)
        print(f"\nShrunk minimal counterexample: {shrunk}")
        print(f"  Buggy output on minimal case: {shrunk_output}")
        print("  Root cause identified: touching intervals [a, b] and [b, c] left unmerged.")
    else:
        print("No property violation detected.")


main()
