"""CS2 project lab 3 (rung 3, reference numbers): an eleven-value SIMULATED stream, checked against exact arithmetic.

SIMULATED: the eleven values are written out here, one decimal each, with a common offset of 10,000 (dimensionless).
They are not market data. Standard library only, no randomness, no network. The code computes the exact mean and
sample variance with Fraction, the same values by Welford's update in floats, the minimum and maximum of the last
four values, and the exact rank target and answer for the median with epsilon 0.1. Exact values are printed to six
decimals, rounded from the unrounded Fraction.
"""

from __future__ import annotations

import math
from fractions import Fraction

STREAM: list[str] = [
    "10003.2",
    "10001.7",
    "10007.5",
    "10000.4",
    "10004.9",
    "10002.1",
    "10009.6",
    "10001.0",
    "10006.3",
    "10003.8",
    "10005.5",
]
WINDOW = 4
EPSILON = Fraction("0.1")


def welford(values: list[float]) -> tuple[float, float]:
    """Return the mean and the sample variance by Welford's update."""
    count, mean, m2 = 0, 0.0, 0.0
    for x in values:
        count += 1
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    return mean, m2 / (count - 1)


def main() -> None:
    exact = [Fraction(s) for s in STREAM]
    n = len(exact)
    mean_exact = sum(exact) / n
    var_exact = sum((x - mean_exact) ** 2 for x in exact) / (n - 1)
    print(f"count {n}")
    print(f"exact mean {float(mean_exact):.6f}")
    print(f"exact sample variance {float(var_exact):.6f}")
    mean_w, var_w = welford([float(s) for s in STREAM])
    print(f"welford mean {mean_w:.6f}")
    print(f"welford sample variance {var_w:.6f}")
    print("welford mean within 1e-9 of exact:", abs(mean_w - float(mean_exact)) <= 1e-9)
    last = [float(s) for s in STREAM[-WINDOW:]]
    print(f"last {WINDOW} values minimum {min(last):.1f} maximum {max(last):.1f}")
    q = Fraction(1, 2)
    target = max(1, math.ceil(q * n - EPSILON * n))
    ordered = sorted(exact)
    print(f"median target rank k = {target} of {n} with epsilon 0.1")
    print(f"the {target}th smallest value is {float(ordered[target - 1]):.1f}")


main()
