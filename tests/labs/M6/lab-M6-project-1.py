"""Rung 1 worked example: E[S_tau] for a bounded stopping time of the fair walk, by exact enumeration.

The fair walk S starts at S_0 = 0 and takes steps of +1 or -1, each with probability 1/2. The stopping time tau is the
first time the walk reaches +1, or the cap N = 3, whichever comes first, so tau is bounded by 3. Optional stopping for a
bounded stopping time says E[S_tau] = S_0 = 0. The lab lists the 8 equally likely paths of length 3, prints the value of
S at tau on each path, and prints E[S_(tau and k)] for k = 0, 1, 2, 3. Each printed expectation should be 0.
Everything is an exact fractions.Fraction on a finite space, so every run prints the same lines. No random draws.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

HORIZON = 3
LEVEL = 1


def stopping_time(steps: tuple[int, ...]) -> int:
    """tau for one path: the first k with S_k = LEVEL, and HORIZON if the walk does not reach LEVEL by then."""
    position = 0
    for k, step in enumerate(steps, start=1):
        position += step
        if position == LEVEL:
            return k
    return HORIZON


def main() -> None:
    """Enumerate the paths, print tau and S_tau on each, then the expectation of the stopped walk at each time."""
    paths = list(itertools.product((1, -1), repeat=HORIZON))
    weight = Fraction(1, len(paths))
    total = Fraction(0)
    print("path tau S_tau weight")
    for steps in paths:
        tau = stopping_time(steps)
        value = sum(steps[:tau])
        total += weight * value
        label = "".join("+" if step == 1 else "-" for step in steps)
        print(f"{label} {tau} {value:+d} {weight}")
    print("E[S_tau] =", total)
    for k in range(HORIZON + 1):
        expectation = sum(
            (weight * sum(steps[: min(k, stopping_time(steps))]) for steps in paths),
            Fraction(0),
        )
        print(f"E[S_(tau and {k})] =", expectation)


main()
