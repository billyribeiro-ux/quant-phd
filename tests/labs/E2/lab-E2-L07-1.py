"""E2 L07 lab 1: a two-type direct mechanism, every misreport enumerated, and the revelation construction.

Inputs are illustrative, not data. A buyer has one of two values in integer cents: 6000 (type L) or 10000
(type H), with prior probability 3/10 on L and 7/10 on H. A mechanism gives each reported type a probability of
trade q (a number from 0 to 1) and a payment t (in cents). A buyer of value v who reports r gets the utility
v * q(r) - t(r), in cents. No random draws are used.

Part A: three direct mechanisms and one infeasible menu. Every report of every type is enumerated. Each line
prints a utility, and the last lines print whether the mechanism is incentive compatible and individually
rational, and its expected revenue in whole cents (half up).
Part B: a grid search over the allocation pairs (q_L, q_H) with 0 <= q_L <= q_H <= 1 in steps of 1/4. Each pair
gets the payments that leave type L with zero utility and leave type H indifferent to reporting L. The search
keeps the pair with the largest expected revenue among grid points that pass the enumerated checks.
Part C: a menu of three messages, a strategy that maps each type to a message, and the direct mechanism that
the strategy induces. A type with a tie between two messages picks the one listed first (low-price is listed
before decline). The induced direct mechanism is checked by the same enumeration as Part A.

Money is integer cents. Probabilities and expected values are exact Fractions; only the printed cents are rounded.
"""

from __future__ import annotations

import math
from fractions import Fraction

VALUES = {"L": 6000, "H": 10000}
PRIOR = {"L": Fraction(3, 10), "H": Fraction(7, 10)}
TYPES = ("L", "H")


def utility(value: int, trade: Fraction, payment: int) -> Fraction:
    """Utility in cents of a buyer with the given value who gets probability trade and pays payment cents."""
    return value * trade - payment


def half_up_cents(amount: Fraction) -> int:
    """The amount in whole cents, a tie going up (amount is nonnegative here)."""
    return math.floor(amount + Fraction(1, 2))


def check(mechanism: dict[str, tuple[Fraction, int]]) -> tuple[bool, bool, Fraction]:
    """Enumerate every type and every report. Return (incentive compatible, individually rational, revenue).

    mechanism maps each reported type to (probability of trade, payment in cents). Revenue is the prior-weighted
    payment in cents, as an exact Fraction.
    """
    ic = True
    ir = True
    for theta in TYPES:
        truthful = utility(VALUES[theta], *mechanism[theta])
        if truthful < 0:
            ir = False
        for report in TYPES:
            if utility(VALUES[theta], *mechanism[report]) > truthful:
                ic = False
    revenue = sum((PRIOR[theta] * mechanism[theta][1] for theta in TYPES), Fraction(0))
    return ic, ir, revenue


def show(name: str, mechanism: dict[str, tuple[Fraction, int]]) -> None:
    """Print one direct mechanism with every type-report utility and its checks."""
    print(f"mechanism {name}")
    for theta in TYPES:
        for report in TYPES:
            u = utility(VALUES[theta], *mechanism[report])
            print(f"  type {theta} reports {report} utility {u}")
    ic, ir, revenue = check(mechanism)
    print(f"  incentive_compatible {ic} individually_rational {ir} revenue_cents {half_up_cents(revenue)}")


def part_a() -> None:
    """Part A: three feasible-looking menus and one menu that fails individual rationality."""
    print("Part A: every report of every type, for four direct mechanisms")
    show("exclude_type_L", {"L": (Fraction(0), 0), "H": (Fraction(1), 10000)})
    show("pool_at_low_value", {"L": (Fraction(1), 6000), "H": (Fraction(1), 6000)})
    show("pool_at_high_value", {"L": (Fraction(1), 10000), "H": (Fraction(1), 10000)})
    show("high_price_for_H_only_trade", {"L": (Fraction(1), 6000), "H": (Fraction(0), 0)})


def part_b() -> None:
    """Part B: the grid over (q_L, q_H) with q_L <= q_H, payments set by the two binding constraints."""
    print("Part B: grid search over allocation pairs, payments leave L with zero utility")
    steps = [Fraction(k, 4) for k in range(5)]
    best: tuple[Fraction, Fraction, Fraction] | None = None
    passing = 0
    for q_low in steps:
        for q_high in steps:
            if q_low > q_high:
                continue
            t_low = int(VALUES["L"] * q_low)
            t_high = int(VALUES["H"] * q_high - (VALUES["H"] - VALUES["L"]) * q_low)
            mechanism = {"L": (q_low, t_low), "H": (q_high, t_high)}
            ic, ir, revenue = check(mechanism)
            if ic and ir:
                passing += 1
                if best is None or revenue > best[2]:
                    best = (q_low, q_high, revenue)
    print(f"grid_points_passing {passing}")
    assert best is not None
    print(f"best_q_low {best[0]} best_q_high {best[1]} best_revenue_cents {half_up_cents(best[2])}")
    print(f"exact_best_revenue {best[2]}")


def part_c() -> None:
    """Part C: a menu with three messages, a best-response strategy, and the induced direct mechanism."""
    print("Part C: the revelation construction on a menu of three messages")
    menu = {
        "low-price": (Fraction(1), 6000),
        "high-price": (Fraction(1), 10000),
        "decline": (Fraction(0), 0),
    }
    order = list(menu)
    strategy: dict[str, str] = {}
    for theta in TYPES:
        best_message = order[0]
        best_utility = utility(VALUES[theta], *menu[best_message])
        for message in order[1:]:
            u = utility(VALUES[theta], *menu[message])
            if u > best_utility:
                best_message, best_utility = message, u
        strategy[theta] = best_message
        print(f"type {theta} chooses {best_message} utility {best_utility}")
    induced = {theta: menu[strategy[theta]] for theta in TYPES}
    ic, ir, revenue = check(induced)
    print(f"induced_direct_mechanism L {induced['L'][0]} {induced['L'][1]} H {induced['H'][0]} {induced['H'][1]}")
    print(f"induced_incentive_compatible {ic} induced_individually_rational {ir}")
    print(f"induced_revenue_cents {half_up_cents(revenue)}")
    alternative = dict(induced)
    alternative["L"] = menu["decline"]
    alt_ic, alt_ir, alt_revenue = check(alternative)
    print(f"tie_break_declines_for_L incentive_compatible {alt_ic} individually_rational {alt_ir}")
    print(f"tie_break_declines_for_L_revenue_cents {half_up_cents(alt_revenue)}")


def main() -> None:
    """Run Parts A, B and C in order."""
    part_a()
    part_b()
    part_c()


main()
