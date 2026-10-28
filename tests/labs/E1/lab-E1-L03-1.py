"""E1 lab L03: the linear competitive equilibrium in exact arithmetic, and the firm-level check behind the supply.

Standard library only (fractions). No randomness and no network. Demand is D(p) = a - b p with a = 100 and
b = 2. There are n = 10 identical price-taking firms, each with the cost of Lesson 2 at c = 2 and k = 1, so each
firm supplies (p - c) / (2 k) for p >= c and nothing below c. The market supply is S(p) = 5 (p - 2) for p >= 2 and
0 below 2. Prices are exact Fractions in the price unit of the example. The lab uses the equilibrium formula
p* = (a + s c) / (b + s) with s = n / (2 k), and it checks four things. First, D(p*) = S(p*), so the market clears.
Second, on the grid p = i / 7 for i = 0 to 140 (prices 0 to 20), the excess demand Z(p) = D(p) - S(p) is positive
below p*, zero at p* and negative above it. Third, it prints demand, market supply and excess demand at p = 20, the
end of the grid, and at p* the ratio of market supply to one firm's supply, which is n = 10. Fourth, at p* a firm's
grid maximiser, on output steps of 1 / 14 from 0 to 10, is 48 / 7 for fixed cost F = 0 and for F = 100. A grid is
finite: it tests these inputs only, and the proofs for every linear case are on the page.
"""

from __future__ import annotations

from fractions import Fraction

A = Fraction(100)  # demand intercept: D(p) = A - B p
B = Fraction(2)  # demand slope
N_FIRMS = 10
UNIT_COST = Fraction(2)  # c
CAPACITY_SLOPE = Fraction(1)  # k, in the firm's cost C(q) = F + c q + k q^2
S_SLOPE = Fraction(N_FIRMS) / (2 * CAPACITY_SLOPE)  # s = n / (2 k): market supply is s (p - c) for p >= c


def demand(p: Fraction) -> Fraction:
    """Quantity demanded D(p) = a - b p at price p."""
    return A - B * p


def firm_supply(p: Fraction) -> Fraction:
    """One firm's supply (p - c) / (2 k) at price p, zero below the unit cost c."""
    return max(Fraction(0), (p - UNIT_COST) / (2 * CAPACITY_SLOPE))


def supply(p: Fraction) -> Fraction:
    """Market supply S(p) = n times one firm's supply at price p."""
    return N_FIRMS * firm_supply(p)


def excess_demand(p: Fraction) -> Fraction:
    """Excess demand Z(p) = D(p) - S(p)."""
    return demand(p) - supply(p)


def equilibrium_price() -> Fraction:
    """p* = (a + s c) / (b + s), the price at which the linear market supply meets demand."""
    return (A + S_SLOPE * UNIT_COST) / (B + S_SLOPE)


def profit(q: Fraction, p: Fraction, fixed: Fraction) -> Fraction:
    """One firm's profit p q - F - c q - k q^2 at output q, price p and fixed cost F."""
    return p * q - fixed - UNIT_COST * q - CAPACITY_SLOPE * q * q


def firm_grid_maximiser(p: Fraction, fixed: Fraction) -> Fraction:
    """The output on the grid j / 14 for j = 0 to 140 with the largest profit at price p."""
    best_q, best_pi = Fraction(0), None
    for j in range(141):
        q = Fraction(j, 14)
        pi = profit(q, p, fixed)
        if best_pi is None or pi > best_pi:
            best_q, best_pi = q, pi
    return best_q


def main() -> None:
    p_star = equilibrium_price()
    q_star = demand(p_star)
    print(f"demand D(p) = {A} - {B} p; market supply S(p) = {S_SLOPE} (p - {UNIT_COST}) for p >= {UNIT_COST}")
    print(f"equilibrium price p* = {p_star}; equilibrium quantity Q* = {q_star}")
    print(f"D(p*) = {demand(p_star)}, S(p*) = {supply(p_star)}, market clears: {demand(p_star) == supply(p_star)}")
    print(f"a > b c ({A} > {B * UNIT_COST}): {A > B * UNIT_COST}, so p* > c: {p_star > UNIT_COST}")
    grid = [Fraction(i, 7) for i in range(141)]
    below = sum(excess_demand(p) > 0 for p in grid if p < p_star)
    at = sum(excess_demand(p) == 0 for p in grid)
    above = sum(excess_demand(p) < 0 for p in grid if p > p_star)
    print(
        f"grid p = i / 7, i = 0 to 140: excess demand positive below p* at {below} points, "
        f"zero at {at} point, negative above p* at {above} points"
    )
    price_end = Fraction(20)
    print(
        f"at p = {price_end}: D = {demand(price_end)}, S = {supply(price_end)}, "
        f"excess demand {excess_demand(price_end)}"
    )
    one_firm = firm_supply(p_star)
    print(f"one firm's supply at p*: {one_firm}; market supply S(p*) / one firm's supply: {supply(p_star) / one_firm}")
    q_free = firm_grid_maximiser(p_star, Fraction(0))
    q_fixed = firm_grid_maximiser(p_star, Fraction(100))
    print(
        f"firm grid maximiser at p*: F=0 gives q={q_free}, F=100 gives q={q_fixed}; "
        f"both equal 48/7: {q_free == Fraction(48, 7) and q_fixed == Fraction(48, 7)}"
    )


main()
