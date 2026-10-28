"""M6 lab L02: the measure and probability axioms on a finite sample space, checked exactly with Fraction.

Standard library only. Every probability is an exact Fraction, and every check runs over all subsets of the
six-point sample space, so each count and each True or False is exact for the set it names. Nothing is random.
A finite check establishes the finite case only; the general case is proved on the page, not checked here.
"""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from itertools import combinations
from typing import NamedTuple

Subset = frozenset[int]
SetFunction = Callable[[Subset], Fraction]

OMEGA: Subset = frozenset(range(1, 7))


def all_subsets(omega: Subset) -> list[Subset]:
    """Every subset of omega, the power set. A set with n members has 2 to the power n subsets."""
    items = sorted(omega)
    return [frozenset(c) for r in range(len(items) + 1) for c in combinations(items, r)]


def weighted(weights: dict[int, Fraction]) -> SetFunction:
    """The set function A -> sum of the weights of the members of A. Weights must be given for every point."""

    def measure(a: Subset) -> Fraction:
        return sum((weights[x] for x in a), Fraction(0))

    return measure


def squared_cardinality(a: Subset) -> Fraction:
    """The set function A -> (number of members of A divided by 6) squared, on the six-point space."""
    return Fraction(len(a), 6) ** 2


class AxiomReport(NamedTuple):
    """The result of the exhaustive axiom check of one set function on OMEGA."""

    nonnegative: bool
    total_mass_one: bool
    additive: bool
    monotone: bool
    failing_pairs: int
    disjoint_pairs: int


def check_axioms(omega: Subset, prob: SetFunction) -> AxiomReport:
    """Test the probability axioms of the finite case for prob, over every subset of omega.

    Nonnegative: prob(A) >= 0 for every subset A. Total mass one: prob(omega) equals 1. Additive: for every
    ordered pair of disjoint subsets, prob(A or B) equals prob(A) + prob(B); failing_pairs counts the pairs
    where it does not. Monotone: prob(A) <= prob(B) whenever A is contained in B. disjoint_pairs counts the
    ordered disjoint pairs tested.
    """
    subsets = all_subsets(omega)
    nonnegative = all(prob(a) >= 0 for a in subsets)
    total_mass_one = prob(omega) == 1
    monotone = True
    failing_pairs = 0
    disjoint_pairs = 0
    for a in subsets:
        for b in subsets:
            if not (a & b):
                disjoint_pairs += 1
                if prob(a | b) != prob(a) + prob(b):
                    failing_pairs += 1
            if a <= b and prob(a) > prob(b):
                monotone = False
    return AxiomReport(nonnegative, total_mass_one, failing_pairs == 0, monotone, failing_pairs, disjoint_pairs)


def main() -> None:
    fair = weighted({x: Fraction(1, 6) for x in range(1, 7)})
    biased = weighted(
        {
            1: Fraction(1, 2),
            2: Fraction(1, 4),
            3: Fraction(1, 8),
            4: Fraction(1, 16),
            5: Fraction(1, 32),
            6: Fraction(1, 32),
        }
    )
    light = weighted({x: Fraction(3, 20) for x in range(1, 7)})
    concentrated = weighted(
        {1: Fraction(1), 2: Fraction(0), 3: Fraction(0), 4: Fraction(0), 5: Fraction(0), 6: Fraction(0)}
    )
    cases: list[tuple[str, SetFunction]] = [
        ("fair die", fair),
        ("biased die", biased),
        ("six weights of 3/20", light),
        ("squared cardinality over 6", squared_cardinality),
        ("all mass on the face 1", concentrated),
    ]
    print(f"subsets of the six-point sample space: {len(all_subsets(OMEGA))}")
    for label, prob in cases:
        report = check_axioms(OMEGA, prob)
        print(
            f"{label}: nonnegative {report.nonnegative}; total mass one {report.total_mass_one}; "
            f"additive {report.additive}; monotone {report.monotone}"
        )
        print(f"  disjoint pairs where additivity fails: {report.failing_pairs} of {report.disjoint_pairs}")

    even = frozenset({2, 4, 6})
    print(f"fair die: P(even) = {fair(even)}")
    first, second = frozenset({1, 2}), frozenset({2, 3})
    print(
        f"overlapping events {{1, 2}} and {{2, 3}}: P of first + P of second = {fair(first) + fair(second)}; "
        f"P of their union = {fair(first | second)}"
    )
    print(f"all mass on the face 1: P({{2}}) = {concentrated(frozenset({2}))} for the nonempty set {{2}}")


main()
