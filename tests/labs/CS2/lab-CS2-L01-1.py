"""CS2 lab L01: operation counts of a single loop and a nested loop, at n = 2**k.

Standard library only. No randomness and no network. Every count printed is an exact integer in a counting
model: one comparison for each element after the first in a maximum scan, and one inner step for each ordered
pair of positions in a nested loop. The ratio lines print four-decimal quotients of two such counts. No
wall-clock time is measured, so the output does not depend on the machine.
"""

from __future__ import annotations


def max_scan_comparisons(values: list[int]) -> tuple[int, int]:
    """Return (maximum, comparisons) of a scan that compares each element after the first with the running maximum.

    A list of n >= 1 values makes exactly n - 1 comparisons. An empty list is refused.
    """
    if not values:
        raise ValueError("max_scan_comparisons needs at least one value")
    best = values[0]
    comparisons = 0
    for x in values[1:]:
        comparisons += 1
        if x > best:
            best = x
    return best, comparisons


def ordered_pair_steps(n: int) -> int:
    """Count the inner steps of a nested loop over all ordered pairs (i, j) with 0 <= i < n and 0 <= j < n."""
    if n < 0:
        raise ValueError(f"ordered_pair_steps needs n >= 0, got {n}")
    steps = 0
    for _ in range(n):
        for _ in range(n):
            steps += 1
    return steps


def first_failure(c: int) -> int:
    """Return the smallest integer n >= 1 with n * n > c * n, found by scanning n upward from 1."""
    if c < 1:
        raise ValueError(f"first_failure needs c >= 1, got {c}")
    n = 1
    while not n * n > c * n:
        n += 1
    return n


def main() -> None:
    print("n = 2**k, maximum-scan comparisons (n - 1), ordered-pair steps (n * n)")
    scan = []
    pairs = []
    for k in range(11):
        n = 2**k
        best, comparisons = max_scan_comparisons(list(range(n)))
        steps = ordered_pair_steps(n)
        scan.append(comparisons)
        pairs.append(steps)
        print(f"k={k:2d} n={n:5d} comparisons={comparisons:5d} pair_steps={steps:8d} maximum={best}")
    for k in range(2, 11):
        print(
            f"doubling from 2**{k - 1} to 2**{k}: pair-step ratio {pairs[k] / pairs[k - 1]:.4f}, "
            f"comparison ratio {scan[k] / scan[k - 1]:.4f}"
        )
    holds = sum(max_scan_comparisons(list(range(n)))[1] <= n for n in range(1, 1001))
    print(f"comparisons at most 1 * n for n = 1 to 1000: {holds} of 1000")
    print(f"first n with n * n greater than 1000 * n: n = {first_failure(1000)}")


main()
