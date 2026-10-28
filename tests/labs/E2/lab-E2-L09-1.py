"""E2 L09 lab 1: uniform-price and discriminatory payments on fixed bid profiles, in exact cents.

Inputs are illustrative, not data. Four bidders compete for two identical units. Each bidder wants at most one
unit, and the bids and values are whole cents. The bids are held fixed in every comparison below: the lab asks
what each payment rule would collect from the same bids. It does not model how bidders would change their bids
under either rule, and no equilibrium is computed. No random draws are used.

Rules, as the lab implements them. The winners are the k highest bids, and a tie goes to the lower bidder index.
Under the uniform-price format each winner pays the (k+1)-th highest bid. Under the discriminatory format each
winner pays its own bid. Revenue is the total paid. The value of the winners is the sum of the values of the
winning bidders, and efficiency is that value divided by the sum of the k highest values.

Part A: one fixed profile, with the allocation, both payment rules, both revenues and the efficiency.
Part B: every bid profile with bids in {0, 1, 2, 3} for the four bidders, which is 256 profiles, with k = 2.
Part C: the same 256 profiles with k = 1, where the uniform-price rule is the second-price rule.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

BIDDERS = 4
VALUES = [9000, 5000, 6000, 7000]
BIDS = [8000, 9500, 6500, 7000]


def ranking(bids: list[int]) -> list[int]:
    """Bidder indices from the highest bid to the lowest, a tie going to the lower index."""
    return sorted(range(len(bids)), key=lambda i: (-bids[i], i))


def winners(bids: list[int], units: int) -> list[int]:
    """The indices of the units highest bids, in ranking order."""
    return ranking(bids)[:units]


def payments(fmt: str, bids: list[int], units: int) -> list[int]:
    """Cents paid by each bidder. A loser pays 0. Uniform: each winner pays the (units+1)-th highest bid.
    Discriminatory: each winner pays its own bid."""
    order = ranking(bids)
    paid = [0] * len(bids)
    clearing = bids[order[units]]
    for i in order[:units]:
        paid[i] = clearing if fmt == "uniform" else bids[i]
    return paid


def revenue(fmt: str, bids: list[int], units: int) -> int:
    """Total cents paid by the winners under the given format."""
    return sum(payments(fmt, bids, units))


def efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    """(value of the winners, value of the units highest values), both in cents."""
    won = sum(values[i] for i in winners(bids, units))
    best = sum(sorted(values, reverse=True)[:units])
    return won, best


def part_a() -> None:
    """Part A: allocation, both payment rules, revenues and efficiency for one fixed profile."""
    units = 2
    print("Part A: one fixed profile, two units, four bidders")
    print(f"values_cents {' '.join(str(v) for v in VALUES)}")
    print(f"bids_cents {' '.join(str(b) for b in BIDS)}")
    print(f"ranking {' '.join(str(i) for i in ranking(BIDS))}")
    print(f"winners {' '.join(str(i) for i in sorted(winners(BIDS, units)))}")
    print(f"uniform_payments_cents {' '.join(str(p) for p in payments('uniform', BIDS, units))}")
    print(f"discriminatory_payments_cents {' '.join(str(p) for p in payments('discriminatory', BIDS, units))}")
    print(f"uniform_revenue_cents {revenue('uniform', BIDS, units)}")
    print(f"discriminatory_revenue_cents {revenue('discriminatory', BIDS, units)}")
    won, best = efficiency(VALUES, BIDS, units)
    print(f"value_of_winners_cents {won}")
    print(f"value_of_top_values_cents {best}")
    print(f"efficiency {Fraction(won, best)}")


def part_b() -> None:
    """Part B: over all 256 profiles with bids in {0, 1, 2, 3}, compare the two revenues with k = 2."""
    units = 2
    grid = list(itertools.product(range(4), repeat=BIDDERS))
    higher = equal = lower = 0
    for profile in grid:
        bids = list(profile)
        uniform = revenue("uniform", bids, units)
        discriminatory = revenue("discriminatory", bids, units)
        if discriminatory > uniform:
            higher += 1
        elif discriminatory == uniform:
            equal += 1
        else:
            lower += 1
    print(f"Part B: profiles with bids in {{0,1,2,3}}, k = {units}")
    print(f"profiles {len(grid)}")
    print(f"discriminatory_above_uniform {higher}")
    print(f"discriminatory_equal_uniform {equal}")
    print(f"discriminatory_below_uniform {lower}")


def part_c() -> None:
    """Part C: over the same 256 profiles with k = 1, the uniform rule pays the second-highest bid."""
    units = 1
    grid = list(itertools.product(range(4), repeat=BIDDERS))
    second_price = 0
    own_bid = 0
    for profile in grid:
        bids = list(profile)
        order = ranking(bids)
        winner = order[0]
        if payments("uniform", bids, units)[winner] == bids[order[1]]:
            second_price += 1
        if payments("discriminatory", bids, units)[winner] == bids[winner]:
            own_bid += 1
    print(f"Part C: the same profiles with k = {units}")
    print(f"uniform_winner_pays_second_highest {second_price} of {len(grid)}")
    print(f"discriminatory_winner_pays_own_bid {own_bid} of {len(grid)}")


def main() -> None:
    """Run Parts A, B and C in order."""
    part_a()
    part_b()
    part_c()


main()
