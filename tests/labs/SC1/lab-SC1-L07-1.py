"""SC1 lab L07: exact walk counts for the running maximum, grid maxima of seeded Brownian paths, and the closed form.

Standard library only. Part A and Part D use no randomness. Parts B and C are SIMULATED: they draw PATHS Brownian
paths on [0, 1] from random.Random(SEED), so every run prints the same lines.

Part A enumerates all 2**N step sequences for N = 1 to 12 and checks, for every level a from 1 to N, the discrete tail
identity of Lesson 6: the number of sequences with running maximum at least a equals the number with endpoint at least a
plus the number with endpoint above a. It then evaluates the same counts with math.comb for N = 4, 16, 64, 256 and 1024,
at the level m = sqrt(N), so that m / sqrt(N) = 1 on the scale of the Brownian path. The discrete tail identity holds
for all pairs in the enumerated range. The probabilities are exact integer counts divided by 2**N, computed as floats
and printed to six decimals.

Part B uses FINE = 256 equal steps on [0, 1]. The grids with N = 4, 16, 64 and 256 steps are subsets of the fine grid,
so the lab counts pathwise violations of the nested inequality between consecutive grids. It then prints, for each
grid, the proportion of paths whose grid maximum reaches level 1, with the standard error computed with divisor
PATHS - 1, next to the closed form 2 (1 - Phi(1)) of the running-maximum tail.

Part C prints the mean of the grid maximum on each grid, with its standard error, next to sqrt(2 / pi), the closed-form
mean of the running maximum on [0, 1].

Part D evaluates 1 - Phi(1) two ways: by erfc, and by composite Simpson integration of the standard normal density on
[1, 13] with SIMPSON_INTERVALS intervals. The Simpson value is a numerical rule; the erfc value is a library function.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable
from itertools import accumulate, pairwise, product

SEED = 20260507
PATHS = 400
FINE = 256
GRID_STEPS = (4, 16, 64, 256)
LEVEL = 1.0
MAX_ENUM = 12
EXACT_N = (4, 16, 64, 256, 1024)
SIMPSON_INTERVALS = 2000


def end_at_least(n: int, m: int) -> int:
    """The number of length-n step sequences whose endpoint S_n is at least m, as an exact integer.

    The endpoint is S_n = 2u - n, where u is the number of +1 steps, so the count is the sum of C(n, u) over the u
    for which 2u - n is at least m.
    """
    return sum(math.comb(n, (n + s) // 2) for s in range(-n, n + 1, 2) if s >= m)


def max_at_least(n: int, m: int) -> int:
    """The number of length-n step sequences whose running maximum over S_0 to S_n is at least m.

    By the discrete tail identity of Lesson 6, this equals the count with endpoint at least m plus the count with
    endpoint above m.
    """
    return end_at_least(n, m) + end_at_least(n, m + 1)


def enumerated_pairs(n: int) -> list[tuple[int, int]]:
    """For each of the 2**n step sequences of length n, the pair (running maximum, endpoint) of the walk S_0 = 0."""
    pairs: list[tuple[int, int]] = []
    for steps in product((1, -1), repeat=n):
        position = 0
        highest = 0
        for step in steps:
            position += step
            highest = max(highest, position)
        pairs.append((highest, position))
    return pairs


def part_a() -> None:
    """Check the discrete tail identity of Lesson 6 by enumeration for N <= 12, then print exact tails for larger N."""
    checked = 0
    identity_holds = 0
    formula_agrees = 0
    for n in range(1, MAX_ENUM + 1):
        pairs = enumerated_pairs(n)
        for m in range(1, n + 1):
            reached = sum(1 for top, _ in pairs if top >= m)
            at_least = sum(1 for _, end in pairs if end >= m)
            above = sum(1 for _, end in pairs if end > m)
            checked += 1
            identity_holds += reached == at_least + above
            formula_agrees += reached == max_at_least(n, m)
    print(
        "Part A: discrete tail identity of Lesson 6 (maximum >= a) = (endpoint >= a) + (endpoint > a): "
        f"{identity_holds} of {checked}"
    )
    print(f"Part A: counting formula agrees with the enumeration: {formula_agrees} of {checked}")
    print(f"Part A: pairs (N, a), N = 1 to {MAX_ENUM} and a = 1 to N; each count is exact")
    print("Part A: exact tails P(M_N >= m) at m = sqrt(N), so that m / sqrt(N) = 1")
    for n in EXACT_N:
        m = math.isqrt(n)
        probability = max_at_least(n, m) / 2**n
        print(f"  N = {n:4d}, m = {m:2d}: P(M_N >= m) = {probability:.6f}")


def std_normal_cdf(x: float) -> float:
    """The standard normal distribution function Phi(x) = erfc(-x / sqrt(2)) / 2, a probability."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def fine_path(rng: random.Random) -> list[float]:
    """The values of a Brownian path on [0, 1] at the times j / FINE for j = 0 to FINE, in length units.

    The path is the partial sum of FINE independent Gaussian increments with mean 0 and variance 1 / FINE.
    """
    scale = math.sqrt(1.0 / FINE)
    increments = [rng.gauss(0.0, scale) for _ in range(FINE)]
    return [0.0, *accumulate(increments)]


def grid_maximum(path: list[float], n: int) -> float:
    """The maximum of the path over the n + 1 grid times of the equal partition of [0, 1] into n steps."""
    stride = FINE // n
    return max(path[::stride])


def mean_and_standard_error(values: list[float]) -> tuple[float, float]:
    """The sample mean, and the standard error sd / sqrt(n) with sd computed by divisor n - 1."""
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(variance / n)


def simulate_maxima(rng: random.Random) -> dict[int, list[float]]:
    """For each of the PATHS seeded paths, the grid maximum on each grid in GRID_STEPS, using the same path."""
    maxima: dict[int, list[float]] = {n: [] for n in GRID_STEPS}
    for _ in range(PATHS):
        path = fine_path(rng)
        for n in GRID_STEPS:
            maxima[n].append(grid_maximum(path, n))
    return maxima


def nesting_violations(maxima: dict[int, list[float]]) -> int:
    """The number of (path, pair of consecutive grids) with a coarse maximum above the finer maximum. Exact count."""
    violations = 0
    for coarse, fine in pairwise(GRID_STEPS):
        for coarse_max, fine_max in zip(maxima[coarse], maxima[fine], strict=True):
            violations += coarse_max > fine_max
    return violations


def part_b(maxima: dict[int, list[float]]) -> None:
    """Print the nesting check and the grid tail estimates against the closed form at level 1 on [0, 1]."""
    closed = 2.0 * (1.0 - std_normal_cdf(LEVEL))
    print(f"Part B: {PATHS} seeded Brownian paths on [0, 1] (SIMULATED), fine grid of {FINE} steps")
    violations = nesting_violations(maxima)
    print(f"Part B: pathwise violations of nesting (coarse maximum above fine maximum): {violations}")
    for n in GRID_STEPS:
        indicators = [1.0 if m >= LEVEL else 0.0 for m in maxima[n]]
        estimate, se = mean_and_standard_error(indicators)
        print(
            f"Part B: N = {n:3d} steps: P(grid max >= 1) = {estimate:.4f}, se {se:.4f}; "
            f"closed form P(M_1 >= 1) = {closed:.4f}; difference {estimate - closed:+.4f}"
        )


def part_c(maxima: dict[int, list[float]]) -> None:
    """Print the mean of the grid maximum on each grid, with its standard error, against sqrt(2 / pi)."""
    target = math.sqrt(2.0 / math.pi)
    print(f"Part C: closed-form mean of the running maximum on [0, 1], sqrt(2 / pi) = {target:.6f}")
    for n in GRID_STEPS:
        mean, se = mean_and_standard_error(maxima[n])
        print(
            f"Part C: N = {n:3d} steps: mean grid maximum {mean:.4f}, se {se:.4f}; "
            f"difference from sqrt(2 / pi) {mean - target:+.4f}"
        )


def simpson(g: Callable[[float], float], a: float, b: float, intervals: int) -> float:
    """Composite Simpson rule for the integral of g on [a, b] with an even number of intervals."""
    h = (b - a) / intervals
    total = g(a) + g(b)
    for i in range(1, intervals):
        total += (4.0 if i % 2 else 2.0) * g(a + i * h)
    return total * h / 3.0


def standard_normal_density(x: float) -> float:
    """The standard normal density exp(-x^2 / 2) / sqrt(2 pi), a density per unit of x."""
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def part_d() -> None:
    """Evaluate 1 - Phi(1) by erfc and by Simpson integration of the density, and compare them."""
    by_erfc = 0.5 * math.erfc(1.0 / math.sqrt(2.0))
    by_simpson = simpson(standard_normal_density, 1.0, 13.0, SIMPSON_INTERVALS)
    print(f"Part D: 1 - Phi(1) by erfc = {by_erfc:.10f}")
    print(f"Part D: 1 - Phi(1) by Simpson on [1, 13] with {SIMPSON_INTERVALS} intervals = {by_simpson:.10f}")
    print(f"Part D: the two values agree to 1e-9: {abs(by_erfc - by_simpson) < 1e-9}")


def main() -> None:
    part_a()
    maxima = simulate_maxima(random.Random(SEED))
    part_b(maxima)
    part_c(maxima)
    part_d()


main()
