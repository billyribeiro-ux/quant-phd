"""E2 L05 lab 1: a two-type menu of quantity-transfer contracts, with incentive and participation constraints.

Inputs are illustrative, not data. A seller offers a menu of two contracts (q_L, m_L) and (q_H, m_H) to a buyer who
is a low type with value 3,000 cents per unit with probability 3/4, or a high type with value 6,000 cents per unit
with probability 1/4. The buyer's utility is theta * q - m, and the seller's cost of q units is q^2 / 2 cents
(Assumption 2 on the page). Quantities are in units and money is in integer cents.

Part A prints the four constraints at the menu that the page derives, with an explicit participation check for the
low type only; the high type's utility and the two incentive slacks are printed as values. Part B enumerates the
low type's quantity on the integer grid 0..6000 with the high type's quantity fixed at its first-best value, and
finds the profit maximizer. Part C enumerates the high type's quantity on the grid 0..12000 in steps of 1000 with the
low type's quantity fixed at the menu value. Part D prints the first-best profit and the gap to the menu profit.

Profit is computed as exact Fractions and rounded once, half up, to whole cents for printing.
No random draws are used, so every run prints the same lines.
"""

from __future__ import annotations

import math
from fractions import Fraction

THETA_LOW = 3_000  # cents per unit, low type
THETA_HIGH = 6_000  # cents per unit, high type
P_LOW = Fraction(3, 4)
P_HIGH = Fraction(1, 4)


def cost(q: Fraction) -> Fraction:
    """Seller's cost in cents of q units: q^2 / 2 cents."""
    return q * q / 2


def transfers(q_low: Fraction, q_high: Fraction) -> tuple[Fraction, Fraction]:
    """Transfers that bind the low type's participation and the high type's incentive constraint."""
    t_low = THETA_LOW * q_low
    t_high = THETA_HIGH * q_high - (THETA_HIGH - THETA_LOW) * q_low
    return t_low, t_high


def profit(q_low: Fraction, q_high: Fraction) -> Fraction:
    """Expected seller profit in cents for the binding menu (q_low, q_high)."""
    t_low, t_high = transfers(q_low, q_high)
    return P_LOW * (t_low - cost(q_low)) + P_HIGH * (t_high - cost(q_high))


def cents(x: Fraction) -> int:
    """Round a non-negative exact amount half up to whole cents."""
    return math.floor(x + Fraction(1, 2))


def main() -> None:
    q_low = Fraction(2000)
    q_high = Fraction(6000)
    t_low, t_high = transfers(q_low, q_high)
    u_low = THETA_LOW * q_low - t_low
    u_high = THETA_HIGH * q_high - t_high

    print("Part A: the menu and its four constraints (cents)")
    print(f"low contract: q_L = {q_low}, m_L = {t_low}")
    print(f"high contract: q_H = {q_high}, m_H = {t_high}")
    print(f"low type utility, participation: {u_low} >= 0 holds: {u_low >= 0}")
    print(f"high type utility: {u_high}")
    print(f"high type deviation to the low contract: {THETA_HIGH * q_low - t_low}")
    print(f"high type incentive slack: {u_high - (THETA_HIGH * q_low - t_low)}")
    print(f"low type deviation to the high contract: {THETA_LOW * q_high - t_high}")
    print(f"low type incentive slack: {u_low - (THETA_LOW * q_high - t_high)}")
    print(f"information rent of the high type, (theta_H - theta_L) q_L: {(THETA_HIGH - THETA_LOW) * q_low}")

    print("Part B: low-type quantity on the grid 0..6000, high-type quantity fixed at 6000")
    best_q = max(range(0, 6001), key=lambda q: (profit(Fraction(q), Fraction(6000)), -q))
    print(f"profit maximizing low-type quantity on the grid: {best_q}")
    print(f"profit at that quantity, rounded to cents: {cents(profit(Fraction(best_q), Fraction(6000)))}")

    print("Part C: high-type quantity on the grid 0..12000 in steps of 1000, low-type quantity fixed at 2000")
    grid_high = range(0, 12001, 1000)
    best_high = max(grid_high, key=lambda q: (profit(Fraction(2000), Fraction(q)), -q))
    print(f"profit maximizing high-type quantity on the grid: {best_high}")

    print("Part D: first best against the menu (cents)")
    first_low, first_high = Fraction(THETA_LOW), Fraction(THETA_HIGH)
    first_best = P_LOW * (THETA_LOW * first_low - cost(first_low)) + P_HIGH * (
        THETA_HIGH * first_high - cost(first_high)
    )
    menu_profit = profit(q_low, q_high)
    print(f"first-best quantities: q_L = {first_low}, q_H = {first_high}")
    print(f"first-best expected profit: {cents(first_best)}")
    print(f"menu expected profit: {cents(menu_profit)}")
    print(f"gap, first best minus menu: {cents(first_best - menu_profit)}")


main()
