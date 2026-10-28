"""CS2 L10 lab 1: a monotonic deque for rolling minimum and maximum, checked against brute force.

Claim checked: for a seeded integer series of N = 200 values and the five window sizes 1, 2, 5, 13 and 30,
the deque's rolling minimum and rolling maximum equal the brute-force minimum and maximum at every position.
At position i the window holds the last min(w, i + 1) values, so the first w - 1 positions use partial windows.
The total number of deque operations (appends plus removals) for each deque is counted and compared with 2N.
The largest number of removals made by a single push is also printed. SIMULATED integer series, seeded.
Standard library only. No network access.
"""

from __future__ import annotations

import random
from collections import deque

N = 200
SEED = 1010
WINDOWS = (1, 2, 5, 13, 30)


class MonotonicDeque:
    """Keeps (index, value) pairs.

    In min mode the values strictly increase from front to back; in max mode they strictly decrease.
    """

    def __init__(self, window: int, is_min: bool) -> None:
        self.window = window
        self.is_min = is_min
        self.items: deque[tuple[int, int]] = deque()
        self.operations = 0
        self.largest_single_push_removals = 0
        self.largest_size = 0

    def push(self, index: int, x: int) -> None:
        removals = 0
        while self.items:
            back = self.items[-1][1]
            dominated = back >= x if self.is_min else back <= x
            if not dominated:
                break
            self.items.pop()
            removals += 1
        self.items.append((index, x))
        while self.items[0][0] <= index - self.window:
            self.items.popleft()
            removals += 1
        self.operations += 1 + removals
        self.largest_single_push_removals = max(self.largest_single_push_removals, removals)
        self.largest_size = max(self.largest_size, len(self.items))

    def best(self) -> int:
        return self.items[0][1]


def brute(series: list[int], i: int, window: int, want_min: bool) -> int:
    """Minimum or maximum of the last min(window, i + 1) values, by scanning the window."""
    segment = series[max(0, i - window + 1) : i + 1]
    return min(segment) if want_min else max(segment)


def main() -> None:
    rng = random.Random(SEED)
    series = [rng.randint(0, 999) for _ in range(N)]
    for window in WINDOWS:
        low = MonotonicDeque(window, is_min=True)
        high = MonotonicDeque(window, is_min=False)
        for i, x in enumerate(series):
            low.push(i, x)
            high.push(i, x)
            if low.best() != brute(series, i, window, want_min=True):
                raise AssertionError(f"rolling minimum differs at window {window}, position {i}")
            if high.best() != brute(series, i, window, want_min=False):
                raise AssertionError(f"rolling maximum differs at window {window}, position {i}")
            if low.largest_size > window or high.largest_size > window:
                raise AssertionError(f"a deque holds more than {window} indices")
        print(
            f"window {window:>2}: all {N} positions match brute force; "
            f"operations min {low.operations}, max {high.operations}, bound 2N = {2 * N}; "
            f"largest single-push removals {max(low.largest_single_push_removals, high.largest_single_push_removals)}; "
            f"largest deque size {max(low.largest_size, high.largest_size)}"
        )


main()
