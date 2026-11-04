"""Rung 2 completion problem: the reflection identity for the simple random walk, by exact enumeration.

A walk takes n steps of +1 or -1, each with probability 1/2 and each of the 2**n walks equally likely. For a >= 1, the
number of walks whose maximum reaches a equals the number of walks ending at a or above, plus the number ending at a + 1
or above. Reflecting each walk after its first visit to a gives this identity. The lab counts all three quantities over
every walk and prints exact integers. It draws no random numbers, so every run prints the same lines.
"""

from __future__ import annotations

import itertools


def count_by_enumeration(n: int, a: int) -> tuple[int, int]:
    """Over all 2**n walks of n steps: (the number whose maximum is at least a, the number ending at least a)."""
    max_hits = 0
    end_hits = 0
    for steps in itertools.product((1, -1), repeat=n):
        sums = list(itertools.accumulate(steps))
        if max(sums) >= a:
            max_hits += 1
        if sums[-1] >= a:
            end_hits += 1
    return max_hits, end_hits


def main() -> None:
    """Count the walks for n = 6 and a = 2, and compare the maximum count with the identity."""
    n = 6
    a = 2
    max_hits, end_hits = count_by_enumeration(n, a)
    end_above = count_by_enumeration(n, a + 1)[1]
    identity = end_hits + end_above
    print(f"n = {n}, a = {a}: walks with maximum >= a: {max_hits}")
    print(f"walks ending at >= a: {end_hits}, walks ending at >= a + 1: {end_above}")
    print("reflection identity holds:", max_hits == identity)


main()
