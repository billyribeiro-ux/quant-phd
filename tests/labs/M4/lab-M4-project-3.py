"""Rung 3 reference numbers: the closed-form values the report quotes, with no random draws.

Standard library only. The inputs are the illustrative two-asset portfolio of Lab 1, a SIMULATED example and not market
data. Every number here is a formula evaluated on unrounded values; the rounding is for display only. The sampled
numbers of your own module depend on its random stream, so the report quotes these closed forms, and its sampled
numbers with the seed it used.
"""

import math
import statistics
from fractions import Fraction

POSITIONS = [3_000_000, 2_000_000]  # cents, illustrative
COV = [[0.0004, 0.0001], [0.0001, 0.0009]]  # per-period covariance, SIMULATED


def main() -> None:
    target = sum(POSITIONS[i] * POSITIONS[j] * COV[i][j] for i in range(2) for j in range(2))
    sd = math.sqrt(target)
    z99 = statistics.NormalDist().inv_cdf(0.99)
    print("portfolio variance w'Sigma w (cents^2):", f"{target:.1f}")
    print("standard deviation of the loss (cents):", f"{sd:.3f}")
    print("standard normal 99% point z:", f"{z99:.6f}")
    print("parametric Gaussian 99% loss (cents, rounded once):", round(z99 * sd))
    for nu in (3, 4, 5, 8):
        print(f"nu = {nu}: matched factor {(nu - 2) / nu:.6f}, unmatched variance inflation {nu / (nu - 2):.6f}")
    for n in (100, 101, 19_987):
        exact = Fraction(99, 100) * n
        print(f"n = {n}: 0.99 n = {float(exact):.2f}, ceil index {math.ceil(exact)}, floor index {math.floor(exact)}")


main()
