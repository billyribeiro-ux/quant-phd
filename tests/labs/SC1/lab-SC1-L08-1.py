"""SC1 lab L08: first-passage counts of the simple random walk, truncated means, and the Brownian first-passage law.

Standard library only. Parts A, B and D use no randomness. Part C is SIMULATED: it draws SIM_PATHS seeded simple random
walk paths from random.Random(SEED), so every run prints the same lines.

The walk is S_0 = 0 and S_k is the sum of the steps e_1 through e_k, each e_i equal to +1 or -1.
For an integer level a >= 1, the first passage index nu_a is the smallest k with S_k >= a, and it is None
when no k <= n has this property.

Part A enumerates all 2**n step sequences for n = 1 to 12 and every level a from 1 to n. For each sequence it
compares the event {nu_a <= n} with the event {running maximum over S_0 .. S_n is at least a}. Because the walk
moves by one step at a time, the two events agree on every sequence, and the lab checks this for every sequence in
the enumeration. It
also checks the count of such sequences against the walk identity of Lesson 6, and prints the first-passage counts
for n = 12 and a = 3, and two probabilities for that case.

Part B computes the truncated mean E[min(nu_1, N)] exactly, from the identity E[min(nu, N)] = sum over k < N of
P(nu > k), with P(nu_1 > k) = 1 - P(max over S_0 .. S_k is at least 1). The values are exact fractions printed
to six decimals.

Part C is SIMULATED. It draws SIM_PATHS seeded walks of length SIM_STEPS, records min(nu_1, SIM_STEPS) on each, and
compares the sample mean of min(nu_1, N) with the exact value from Part B for N = 16, 64 and 256.

Part D evaluates the first-passage distribution function of Brownian motion, erfc(a / sqrt(2 H)), and its density,
a / (sqrt(2 pi) H^(3/2)) exp(-a^2 / (2 H)), at a = 1 and at the horizons H = 1 and H = 2. The density is compared
with a central difference of the distribution function. Part D evaluates formulas; it does not check the assumption that
the lesson states for them.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import product

SEED = 20260508
MAX_ENUM = 12
EXACT_STEPS = (16, 64, 256)
SIM_PATHS = 1000
SIM_STEPS = 256
DIFFERENCE_STEP = 1e-5


def end_at_least(n: int, m: int) -> int:
    """The number of length-n step sequences whose endpoint S_n is at least m, as an exact integer."""
    return sum(math.comb(n, (n + s) // 2) for s in range(-n, n + 1, 2) if s >= m)


def max_at_least(n: int, m: int) -> int:
    """The number of length-n step sequences whose running maximum over S_0 to S_n is at least m (walk identity)."""
    return end_at_least(n, m) + end_at_least(n, m + 1)


def enumerated_paths(n: int, a: int) -> list[tuple[int | None, int]]:
    """For each step sequence of length n: (first k with S_k >= a, or None, and the running maximum over S_0 to S_n)."""
    results: list[tuple[int | None, int]] = []
    for steps in product((1, -1), repeat=n):
        position = 0
        highest = 0
        hit: int | None = None
        for k, step in enumerate(steps, start=1):
            position += step
            highest = max(highest, position)
            if hit is None and position >= a:
                hit = k
        results.append((hit, highest))
    return results


def part_a() -> None:
    """Compare the first-passage event with the maximum event on every sequence, for n <= 12 and a <= n."""
    sequences = 0
    pathwise_agree = 0
    counts_agree = 0
    pairs = 0
    for n in range(1, MAX_ENUM + 1):
        for a in range(1, n + 1):
            paths = enumerated_paths(n, a)
            pairs += 1
            sequences += len(paths)
            hits_by_n = sum(1 for hit, _ in paths if hit is not None and hit <= n)
            pathwise_agree += sum(1 for hit, top in paths if (hit is not None) == (top >= a))
            counts_agree += hits_by_n == max_at_least(n, a)
    print(f"Part A: pairs (n, a) checked: {pairs}; counts agree with the walk identity for {counts_agree} of {pairs}")
    print(f"Part A: sequences checked: {sequences}; {{nu_a <= n}} equals {{maximum >= a}} on {pathwise_agree} of them")
    print(f"Part A: pathwise agreement holds for every sequence: {pathwise_agree == sequences}")

    n, a = MAX_ENUM, 3
    paths = enumerated_paths(n, a)
    by_step = [sum(1 for hit, _ in paths if hit == k) for k in range(a, n + 1)]
    print(f"Part A: counts of first passage to {a} at step k, for k = {a} to {n}: {by_step}")
    hits = sum(by_step)
    walk_count = max_at_least(n, a)
    print(f"Part A: sum of the counts equals the walk identity count {walk_count}: {hits == walk_count}")
    print(f"Part A: P(nu_{a} <= {n}) = {hits} / {2**n} = {hits / 2**n:.6f}")
    print(f"Part A: P(S_{n} >= {a}) = {end_at_least(n, a)} / {2**n} = {end_at_least(n, a) / 2**n:.6f}")


def part_b() -> None:
    """Print the exact truncated means E[min(nu_1, N)] for the step counts in EXACT_STEPS."""
    largest = max(EXACT_STEPS)
    tail_above = [Fraction(max_at_least(k, 1), 2**k) for k in range(largest)]
    survive = [1 - tail for tail in tail_above]
    running = Fraction(0)
    truncated: dict[int, Fraction] = {}
    for k in range(largest):
        running += survive[k]
        if k + 1 in EXACT_STEPS:
            truncated[k + 1] = running
    print("Part B: exact truncated means E[min(nu_1, N)] = sum over k < N of P(nu_1 > k) for the simple random walk")
    for n in EXACT_STEPS:
        print(f"Part B: N = {n:4d}: E[min(nu_1, N)] = {float(truncated[n]):.6f}")


def simulated_first_passage(rng: random.Random) -> list[int]:
    """For each of SIM_PATHS seeded walks of length SIM_STEPS, the value min(nu_1, SIM_STEPS), in steps."""
    capped: list[int] = []
    for _ in range(SIM_PATHS):
        position = 0
        first = SIM_STEPS
        for k in range(1, SIM_STEPS + 1):
            position += 1 if rng.random() < 0.5 else -1
            if position >= 1:
                first = k
                break
        capped.append(first)
    return capped


def mean_and_standard_error(values: list[float]) -> tuple[float, float]:
    """The sample mean, and the standard error sd / sqrt(n) with sd computed by divisor n - 1."""
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, math.sqrt(variance / n)


def part_c() -> None:
    """Compare the seeded sample mean of min(nu_1, N) with the exact truncated mean from Part B."""
    capped = simulated_first_passage(random.Random(SEED))
    print(f"Part C: {SIM_PATHS} seeded simple random walk paths (SIMULATED), each followed for {SIM_STEPS} steps")
    largest = max(EXACT_STEPS)
    tails = [Fraction(max_at_least(k, 1), 2**k) for k in range(largest)]
    running = Fraction(0)
    exact: dict[int, Fraction] = {}
    for k in range(largest):
        running += 1 - tails[k]
        if k + 1 in EXACT_STEPS:
            exact[k + 1] = running
    for n in EXACT_STEPS:
        values = [float(min(c, n)) for c in capped]
        mean, se = mean_and_standard_error(values)
        target = float(exact[n])
        print(
            f"Part C: N = {n:4d}: sample mean {mean:.4f}, se {se:.4f}; exact {target:.4f}; "
            f"z = {(mean - target) / se:+.2f}"
        )


def first_passage_cdf(a: float, horizon: float) -> float:
    """P(tau_a <= H) = erfc(a / sqrt(2 H)) = 2 (1 - Phi(a / sqrt(H))), for a > 0 and H > 0, with H the horizon."""
    return math.erfc(a / math.sqrt(2.0 * horizon))


def first_passage_density(a: float, horizon: float) -> float:
    """The density a / (sqrt(2 pi) H^(3/2)) exp(-a^2 / (2 H)) per unit of time H, for a > 0 and H > 0."""
    return a / (math.sqrt(2.0 * math.pi) * horizon * math.sqrt(horizon)) * math.exp(-(a * a) / (2.0 * horizon))


def part_d() -> None:
    """Evaluate the first-passage distribution and compare its density with a central difference."""
    level = 1.0
    for horizon in (1.0, 2.0):
        cdf = first_passage_cdf(level, horizon)
        upper = first_passage_cdf(level, horizon + DIFFERENCE_STEP)
        lower = first_passage_cdf(level, horizon - DIFFERENCE_STEP)
        numeric = (upper - lower) / (2.0 * DIFFERENCE_STEP)
        closed = first_passage_density(level, horizon)
        print(f"Part D: a = 1, H = {horizon:g}: P(tau_a <= H) = {cdf:.6f}")
        print(
            f"Part D: a = 1, H = {horizon:g}: density {closed:.6f}; central difference {numeric:.6f}; "
            f"agree to 1e-8: {abs(closed - numeric) < 1e-8}"
        )


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
