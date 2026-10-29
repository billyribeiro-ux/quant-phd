"""CS2 L11 lab 1: a deterministic quantile sketch, checked against exact ranks on a seeded stream.

Claim checked: after N = 5000 values, for each probe quantile q and each epsilon in {1/20, 1/10}, the value v
returned by the sketch satisfies #{x < v} <= qN + epsilon*N and #{x <= v} >= qN - epsilon*N, using exact
counts on the stream. The sketch keeps levels h = 0, 1, 2, ...; level h holds items of weight 2**h and has
capacity k_h = 2 * ceil((h+1)(h+2) / (2 epsilon)). A full level is sorted, its even-numbered items (the 2nd,
4th, ...; buffer[1::2] in 0-based indexing) are kept and promoted to level h+1, and the others are dropped.
All arithmetic on epsilon and q is exact (Fraction). SIMULATED stream: uniform on [0, 1) from
random.Random(SEED). Standard library only.
"""

from __future__ import annotations

import bisect
import math
import random
from fractions import Fraction

N = 5000
SEED = 2026
EPSILONS = (Fraction(1, 20), Fraction(1, 10))
PROBES = (
    Fraction(0),
    Fraction(1, 100),
    Fraction(1, 10),
    Fraction(1, 4),
    Fraction(1, 2),
    Fraction(3, 4),
    Fraction(9, 10),
    Fraction(99, 100),
    Fraction(1),
)


class QuantileSketch:
    """Deterministic compactor sketch; levels[h] holds the stored values of weight 2**h."""

    def __init__(self, epsilon: Fraction) -> None:
        self.epsilon = epsilon
        self.levels: list[list[float]] = []
        self.n = 0
        self.compactions = 0

    def capacity(self, h: int) -> int:
        """Capacity k_h of level h: an even integer, so that 1 / k_h <= epsilon / ((h+1)(h+2))."""
        return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / self.epsilon)

    def add(self, x: float) -> None:
        self.n += 1
        self._push(0, x)

    def _push(self, h: int, x: float) -> None:
        while len(self.levels) <= h:
            self.levels.append([])
        buffer = self.levels[h]
        buffer.append(x)
        if len(buffer) == self.capacity(h):
            buffer.sort()
            kept = buffer[1::2]
            self.levels[h] = []
            self.compactions += 1
            for y in kept:
                self._push(h + 1, y)

    def stored(self) -> int:
        return sum(len(buffer) for buffer in self.levels)

    def total_weight(self) -> int:
        return sum(len(buffer) * 2**h for h, buffer in enumerate(self.levels))

    def quantile(self, q: Fraction) -> float:
        """The smallest stored value whose cumulative weight reaches q * n."""
        pairs = sorted((value, 2**h) for h, buffer in enumerate(self.levels) for value in buffer)
        target = q * self.n
        cumulative = 0
        for value, weight in pairs:
            cumulative += weight
            if cumulative >= target:
                return value
        raise AssertionError("the stored weight does not reach q * n")


def main() -> None:
    rng = random.Random(SEED)
    xs = [rng.random() for _ in range(N)]
    ordered = sorted(xs)
    for epsilon in EPSILONS:
        sketch = QuantileSketch(epsilon)
        for x in xs:
            sketch.add(x)
        if sketch.total_weight() != N:
            raise AssertionError("stored weight differs from n")
        worst_excess = Fraction(0)
        worst_deficit = Fraction(0)
        for q in PROBES:
            v = sketch.quantile(q)
            below = bisect.bisect_left(ordered, v)  # exact #{x < v}
            at_or_below = bisect.bisect_right(ordered, v)  # exact #{x <= v}
            if below > q * N + epsilon * N or at_or_below < q * N - epsilon * N:
                raise AssertionError(f"the guarantee fails at q = {q}")
            worst_excess = max(worst_excess, Fraction(below) - q * N)
            worst_deficit = max(worst_deficit, q * N - Fraction(at_or_below))
        print(
            f"epsilon {epsilon}: capacities k0..k2 = {sketch.capacity(0)}, {sketch.capacity(1)}, {sketch.capacity(2)}; "
            f"stored items {sketch.stored()} of N = {N}; compactions {sketch.compactions}; "
            f"all {len(PROBES)} probes pass; "
            f"largest excess of #{{x < v}} over qN = {float(worst_excess / N):.4f} N; "
            f"largest deficit of #{{x <= v}} below qN = {float(worst_deficit / N):.4f} N"
        )


main()
