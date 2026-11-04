"""SC1 lab L06: exact enumeration of the discrete reflection identity for the symmetric simple random walk.

Standard library only. Nothing is random: the lab enumerates all 2**N step sequences for each N from 1 to 12,
so every count is an exact integer and every probability is an exact fraction. The walk starts at S_0 = 0, and
S_k is the sum of the steps e_1 to e_k, where each step e_i is +1 or -1. For an integer level a >= 1, M_N is
the largest of S_0 to S_N. Proposition 1.3 of the page proves, for every N, every integer a >= 1 and every
integer b < a, that the number of paths with M_N >= a and S_N = b equals the number of paths with S_N = 2a - b.
The lab checks that identity for every N from 1 to 12, every integer a with 1 <= a <= N, and every integer b < a
with b >= -N, and checks the tail identity of Corollary 1.4 for the same (N, a). Part D shows the term that the
discrete identity keeps and the continuous identity drops. Part E evaluates the continuous tail 2 P(B_1 > 1) in
closed form.
"""

from __future__ import annotations

import math
from collections import Counter
from fractions import Fraction
from itertools import product

MAX_N = 12


def path_summary(steps: tuple[int, ...]) -> tuple[int, int]:
    """Return (maximum of S_0 .. S_N, S_N) for the walk with the given +1 and -1 steps."""
    position = 0
    highest = 0
    for step in steps:
        position += step
        highest = max(highest, position)
    return highest, position


def summaries(n: int) -> list[tuple[int, int]]:
    """The (maximum, endpoint) pair of each of the 2**n paths of length n."""
    return [path_summary(steps) for steps in product((1, -1), repeat=n)]


def main() -> None:
    print("Part A: reflection identity #{M_N >= a, S_N = b} = #{S_N = 2a - b} for b < a")
    triples = 0
    equal = 0
    for n in range(1, MAX_N + 1):
        pairs = summaries(n)
        ends = Counter(end for _, end in pairs)
        for a in range(1, n + 1):
            hits_a = Counter(end for top, end in pairs if top >= a)
            for b in range(-n, a):
                triples += 1
                equal += hits_a[b] == ends[2 * a - b]
    print(f"triples (N, a, b) checked: {triples}; equal: {equal}")
    print(f"Part A holds for every triple: {triples == equal}")

    print("Part B: tail identity #{M_N >= a} = #{S_N >= a} + #{S_N > a}")
    checks = 0
    tail_equal = 0
    for n in range(1, MAX_N + 1):
        pairs = summaries(n)
        for a in range(1, n + 1):
            checks += 1
            maxima = sum(1 for top, _ in pairs if top >= a)
            at_least = sum(1 for _, end in pairs if end >= a)
            above = sum(1 for _, end in pairs if end > a)
            tail_equal += maxima == at_least + above
    print(f"pairs (N, a) checked: {checks}; equal: {tail_equal}")

    print("Part C: the example N = 12, a = 3")
    pairs = summaries(12)
    maxima_12 = sum(1 for top, _ in pairs if top >= 3)
    ends_12 = Counter(end for _, end in pairs)
    print(f"paths with M_12 >= 3: {maxima_12} of {2**12}")
    print(f"paths with M_12 >= 3 and S_12 = 2: {sum(1 for top, end in pairs if top >= 3 and end == 2)}")
    print(f"paths with S_12 = 4 (the reflected endpoint 2 * 3 - 2): {ends_12[4]}")

    print("Part D: the discrete correction, N = 10 and a = 2")
    pairs = summaries(10)
    total = 2**10
    tail = Fraction(sum(1 for top, _ in pairs if top >= 2), total)
    above_exact = Fraction(sum(1 for _, end in pairs if end > 2), total)
    at_level = Fraction(sum(1 for _, end in pairs if end == 2), total)
    print(f"P(M_10 >= 2) = {tail} = {float(tail):.6f}")
    print(f"2 P(S_10 > 2) = {2 * above_exact} = {float(2 * above_exact):.6f}")
    print(f"P(S_10 = 2) = {at_level} = {float(at_level):.6f}")
    print(f"P(M_10 >= 2) - 2 P(S_10 > 2) equals P(S_10 = 2): {tail - 2 * above_exact == at_level}")

    print("Part E: continuous tail at t = 1, a = 1")
    two_tail = math.erfc(1.0 / math.sqrt(2.0))
    print(f"2 P(B_1 > 1) = erfc(1 / sqrt(2)) = {two_tail:.10f}")
    print(f"P(B_1 > 1) = {two_tail / 2:.10f}")


main()
