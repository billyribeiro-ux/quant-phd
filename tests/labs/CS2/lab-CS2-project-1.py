"""CS2 project lab 1 (rung 1, worked example): a rolling minimum and maximum with a monotonic deque.

SIMULATED: twelve integers drawn from random.Random(12) in [0, 99]. They are generated here and are not market data.
Standard library only, no randomness after the seed, no network. The window holds the last four values. For every
value the code prints the window and its minimum and maximum. At the end it prints whether every step agrees with a
brute-force scan of its window, then the count of deque pushes and pops over both deques and the bound 4n on that count.
"""

from __future__ import annotations

import random
from collections import deque

WINDOW = 4
_RNG = random.Random(12)
SERIES: list[int] = [_RNG.randint(0, 99) for _ in range(12)]


class RollingMinMax:
    """Minimum and maximum of the last WINDOW values. Each deque holds (index, value) pairs."""

    def __init__(self, window: int) -> None:
        self.window = window
        self.index = -1  # index of the latest value pushed
        # Why: the minimum deque keeps values in increasing order, so its front is the window's minimum.
        self.mins: deque[tuple[int, int]] = deque()
        # Why: the maximum deque keeps values in decreasing order, so its front is the window's maximum.
        self.maxs: deque[tuple[int, int]] = deque()
        self.ops = 0  # pushes and pops on both deques, counted to measure the work

    def push(self, x: int) -> None:
        self.index += 1
        # Why: an older value at least as large as x can never be the minimum again while x is in the window.
        while self.mins and self.mins[-1][1] >= x:
            self.mins.pop()
            self.ops += 1
        self.mins.append((self.index, x))
        self.ops += 1
        # Why: an older value at most as large as x can never be the maximum again while x is in the window.
        while self.maxs and self.maxs[-1][1] <= x:
            self.maxs.pop()
            self.ops += 1
        self.maxs.append((self.index, x))
        self.ops += 1
        # Why: an index at or before index - window has left the window, and it can only be at the front.
        while self.mins[0][0] <= self.index - self.window:
            self.mins.popleft()
            self.ops += 1
        while self.maxs[0][0] <= self.index - self.window:
            self.maxs.popleft()
            self.ops += 1

    def minimum(self) -> int:
        return self.mins[0][1]

    def maximum(self) -> int:
        return self.maxs[0][1]


def main() -> None:
    rolling = RollingMinMax(WINDOW)
    print("series:", SERIES)
    all_agree = True
    for t, x in enumerate(SERIES, start=1):
        rolling.push(x)
        window = SERIES[max(0, t - WINDOW) : t]
        agree = rolling.minimum() == min(window) and rolling.maximum() == max(window)
        all_agree = all_agree and agree
        print(f"step {t:2d} value {x:2d} window {window} min {rolling.minimum()} max {rolling.maximum()}")
    print("every step agrees with brute force:", all_agree)
    print(f"deque operations: {rolling.ops} for n = {len(SERIES)} values, bound 4n = {4 * len(SERIES)}")


main()
