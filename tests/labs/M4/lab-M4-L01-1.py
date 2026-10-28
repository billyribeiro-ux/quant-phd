"""M4 lab L01: a finite discrete law, its CDF and its quantile function, computed exactly.

Standard library only (fractions). No randomness and no network: every probability and every
value of F and Q is an exact rational or an integer, so the output is the same on every run.
The law is a stated table, not data. The quantile function is Q(p) = inf{x : F(x) >= p} for
0 < p <= 1. On a finite law F changes only at support points, so Q(p) is the least support
point x with F(x) >= p. The program computes Q two ways (a scan of the support in increasing
order, and the minimum over the support points with F(x) >= p) and checks them against each
other on 100 grid points, p = j/100 for j = 1 to 100. It also checks F(Q(p)) >= p on the same
grid and checks Q(F(x)) = x at each support point. It prints Q at F(x) and just above F(x) to
show the jump. Each check covers only the finite list it runs on.
"""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from fractions import Fraction

Law = Sequence[tuple[int, Fraction]]

# value -> probability, values strictly increasing, probabilities exact and summing to 1
LAW: tuple[tuple[int, Fraction], ...] = (
    (-2, Fraction(1, 10)),
    (-1, Fraction(2, 10)),
    (0, Fraction(3, 10)),
    (1, Fraction(2, 10)),
    (2, Fraction(1, 10)),
    (3, Fraction(1, 10)),
)


def check_law(law: Law) -> None:
    """Raise ValueError unless the values strictly increase and the probabilities are in [0, 1] and sum to 1."""
    values = [v for v, _ in law]
    if any(a >= b for a, b in itertools.pairwise(values)):
        raise ValueError("values must be strictly increasing")
    if any(p < 0 or p > 1 for _, p in law):
        raise ValueError("each probability must lie in [0, 1]")
    if sum((p for _, p in law), Fraction(0)) != 1:
        raise ValueError("probabilities must sum to exactly 1")


def cdf(law: Law, x: int) -> Fraction:
    """F(x) = P(X <= x): the sum of the probabilities of the values at most x."""
    return sum((p for v, p in law if v <= x), Fraction(0))


def quantile(law: Law, p: Fraction) -> int:
    """Q(p) by a scan: the first value, in increasing order, whose cumulative probability reaches p."""
    if not 0 < p <= 1:
        raise ValueError(f"quantile needs 0 < p <= 1, got {p}")
    total = Fraction(0)
    for value, prob in law:
        total += prob
        if total >= p:
            return value
    raise ValueError("the law does not reach p; check_law should have rejected it")


def quantile_by_definition(law: Law, p: Fraction) -> int:
    """Q(p) as the minimum of {x : F(x) >= p} over the support points.

    F is constant between support points and equal to F at the support point just below, so
    the infimum over all real x with F(x) >= p is attained at a support point.
    """
    if not 0 < p <= 1:
        raise ValueError(f"quantile needs 0 < p <= 1, got {p}")
    return min(v for v, _ in law if cdf(law, v) >= p)


def main() -> None:
    check_law(LAW)
    values = [v for v, _ in LAW]
    print(f"law: {len(LAW)} values, probabilities sum to {sum((p for _, p in LAW), Fraction(0))}")

    cdfs = [cdf(LAW, v) for v in values]
    print("CDF F(x) at " + ", ".join(str(v) for v in values) + ": " + ", ".join(str(f) for f in cdfs))

    probes = [
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(11, 100),
        Fraction(1, 2),
        Fraction(3, 5),
        Fraction(61, 100),
        Fraction(9, 10),
        Fraction(91, 100),
        Fraction(99, 100),
        Fraction(1),
    ]
    for p in probes:
        print(f"Q({p}) = {quantile(LAW, p)}")

    grid = [Fraction(j, 100) for j in range(1, 101)]
    same = sum(quantile(LAW, p) == quantile_by_definition(LAW, p) for p in grid)
    reaches = sum(cdf(LAW, quantile(LAW, p)) >= p for p in grid)
    print(f"grid p = j/100, j = 1 to 100: scan equals definition at {same} of 100 points")
    print(f"F(Q(p)) >= p at {reaches} of 100 grid points")

    back = all(quantile(LAW, cdf(LAW, v)) == v for v in values)
    print(f"Q(F(x)) = x at all {len(values)} support points: {back}")

    eps = Fraction(1, 10**9)
    for v, f in zip(values[:-1], cdfs[:-1], strict=True):
        print(f"at x = {v}: Q(F(x)) = {quantile(LAW, f)}, Q(F(x) + eps) = {quantile(LAW, f + eps)}, eps = 1/10**9")


main()
