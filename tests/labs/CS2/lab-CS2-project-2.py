"""CS2 project lab 2 (rung 2, completion): one step of Welford's update, on a SIMULATED stream.

SIMULATED: eight integers near a common offset of 1,000,000, written out here. They are not market data.
Standard library only, no randomness, no network. Each blank in the page is one expression of the update: the
new mean is the old mean plus the deviation divided by the new count, and the new M2 is the old M2 plus the
deviation times the deviation from the new mean.

Fill in each blank so that the output matches the expected output below. The other lines are given.
"""

from __future__ import annotations

STREAM: list[int] = [1000002, 1000005, 1000001, 1000004, 1000009, 1000003, 1000006, 1000000]


def update(count: int, mean: float, m2: float, x: float) -> tuple[int, float, float]:
    """One Welford step. Arguments: the count, mean and M2 before x, and x. Returns the same three after x."""
    count = count + 1
    delta = x - mean
    mean = mean + delta / count
    m2 = m2 + delta * (x - mean)
    return count, mean, m2


def main() -> None:
    count, mean, m2 = 0, 0.0, 0.0
    for x in STREAM:
        count, mean, m2 = update(count, mean, m2, float(x))
    print(f"count {count}")
    print(f"mean {mean:.6f}")
    print(f"sample variance {m2 / (count - 1):.6f}")


main()
