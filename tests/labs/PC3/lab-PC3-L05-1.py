"""PC3 lab L05: sliding-window maximum by a monotonic deque and by a naive scan, on one seeded sequence.

SEEDED. The sequence is 200 integers in 0 to 999 drawn from random.Random(5). It is a generated test input, not data.
No data file is read and there is no network access. Standard library only.

Every count below is an operation count: comparisons of stored values, and pushes and pops on the deque. No count is a
wall-clock time, and none is a claim about how long an interview allows.

Part 1 runs both methods at window size 8 and prints the operation counts. The naive scan makes k - 1 comparisons per
window, so its count is (n - k + 1)(k - 1), which the lab prints beside the measured count. It then runs both methods
on the seed-6 sequence of the same length at the same window and prints that sequence's counts.

Part 2 compares the two outputs for every window size from 1 to 20, and checks the edge cases: window size 1, a window
equal to the length, a window longer than the sequence, and an empty sequence. A match is a check on this sequence only.
"""

from __future__ import annotations

import random
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass

SEED = 5
LENGTH = 200
WINDOW = 8
LOW = 0
HIGH = 999


@dataclass
class Ops:
    """Operation counts for one run: comparisons of stored values, and deque pushes and pops."""

    comparisons: int = 0
    pushes: int = 0
    pops: int = 0


def make_sequence(seed: int, length: int) -> list[int]:
    """Integers in LOW..HIGH drawn from random.Random(seed), in order."""
    rng = random.Random(seed)
    return [rng.randint(LOW, HIGH) for _ in range(length)]


def naive_maxima(xs: Sequence[int], k: int) -> tuple[list[int], int]:
    """The maximum of each window of k consecutive values, found by scanning the window. Returns the maxima and the
    number of comparisons, which is k - 1 for each of the n - k + 1 windows."""
    maxima: list[int] = []
    comparisons = 0
    for start in range(len(xs) - k + 1):
        best = xs[start]
        for x in xs[start + 1 : start + k]:
            comparisons += 1
            if x > best:
                best = x
        maxima.append(best)
    return maxima, comparisons


def deque_maxima(xs: Sequence[int], k: int) -> tuple[list[int], Ops]:
    """The maximum of each window of k values, using a deque of indices whose values decrease from front to back.

    The front index is the index of the current window's maximum. Each index is pushed once and popped at most once.
    """
    window: deque[int] = deque()
    maxima: list[int] = []
    ops = Ops()
    for i, x in enumerate(xs):
        while window:
            ops.comparisons += 1
            if xs[window[-1]] > x:
                break
            window.pop()
            ops.pops += 1
        window.append(i)
        ops.pushes += 1
        if window[0] <= i - k:
            window.popleft()
            ops.pops += 1
        if i >= k - 1:
            maxima.append(xs[window[0]])
    return maxima, ops


def part_one() -> None:
    print(f"Part 1 · seeded sequence, seed {SEED}, length {LENGTH}, window {WINDOW}, values {LOW} to {HIGH}")
    xs = make_sequence(SEED, LENGTH)
    print(f"first five values: {xs[:5]}")
    naive, naive_count = naive_maxima(xs, WINDOW)
    fast, ops = deque_maxima(xs, WINDOW)
    windows = LENGTH - WINDOW + 1
    print(f"windows = {windows}")
    print(f"first five maxima by deque: {fast[:5]}")
    print(f"outputs equal: {naive == fast}")
    print(f"naive comparisons = {naive_count}, formula (n - k + 1)(k - 1) = {windows * (WINDOW - 1)}")
    print(f"deque comparisons = {ops.comparisons}, pushes = {ops.pushes}, pops = {ops.pops}")
    print(f"deque comparisons at most 2n = {2 * LENGTH}: {ops.comparisons <= 2 * LENGTH}")
    print(f"each index pushed once: {ops.pushes == LENGTH}")
    seed_six = make_sequence(6, LENGTH)
    naive_six, naive_six_count = naive_maxima(seed_six, WINDOW)
    fast_six, ops_six = deque_maxima(seed_six, WINDOW)
    print(f"seed 6 at window {WINDOW}: outputs equal: {naive_six == fast_six}")
    print(
        f"seed 6: naive comparisons = {naive_six_count}, deque comparisons = {ops_six.comparisons}, "
        f"pushes = {ops_six.pushes}, pops = {ops_six.pops}"
    )


def part_two() -> None:
    print("Part 2 · every window size from 1 to 20, and edge cases, on the same sequence")
    xs = make_sequence(SEED, LENGTH)
    agree = all(naive_maxima(xs, k)[0] == deque_maxima(xs, k)[0] for k in range(1, 21))
    print(f"outputs equal for window sizes 1 to 20: {agree}")
    print(f"window 1 returns the sequence itself: {deque_maxima(xs, 1)[0] == xs}")
    whole, _ = deque_maxima(xs, LENGTH)
    print(f"window equal to the length gives one maximum, equal to max(xs) = {max(xs)}: {whole == [max(xs)]}")
    print(f"window longer than the sequence gives no maxima: {deque_maxima(xs, LENGTH + 1)[0] == []}")
    print(f"empty sequence, window 3, gives no maxima: {deque_maxima([], 3)[0] == []}")
    print(f"naive scan on the empty sequence gives no maxima: {naive_maxima([], 3)[0] == []}")


def part_three() -> None:
    print("Part 3 · operation counts by window size, same sequence")
    xs = make_sequence(SEED, LENGTH)
    print("  k  windows  naive  (n-k+1)(k-1)  deque_comparisons  pops  pushes")
    for k in (1, 2, 8, 32, 200):
        _, naive_count = naive_maxima(xs, k)
        _, ops = deque_maxima(xs, k)
        windows = LENGTH - k + 1
        print(
            f"{k:>3}  {windows:>7}  {naive_count:>5}  {windows * (k - 1):>12}  "
            f"{ops.comparisons:>17}  {ops.pops:>4}  {ops.pushes:>6}"
        )


def main() -> None:
    part_one()
    part_two()
    part_three()


main()
