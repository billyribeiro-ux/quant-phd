"""E1 lab L09: a Pigouvian tax on a negative externality, and the vertical sum for a public good, in exact arithmetic.

Standard library only (fractions). No randomness and no network. Money is in cents and quantities are in units, so
every price is in cents per unit. Part A is a market with linear inverse demand P(q) = 1000 - 10 q, a constant
private marginal cost of 200 cents per unit, and a constant marginal external damage of 120 cents per unit. Part A
finds the private quantity, the efficient quantity, the tax that makes them equal, and the efficiency loss without
the tax, by two exact methods. It then checks every integer tax from 0 to 200 cents, and the integer quantity from 0
to 100 that maximises total surplus. Part B is a public good with
two consumers and a constant marginal cost of 400 cents per unit. Its willingness to pay is summed vertically, at
each quantity, and the total surplus is checked on the integer quantities 0 to 10. Both parts are exact
computations on the stated inputs, not simulations and not market data.
"""

from __future__ import annotations

from fractions import Fraction

CHOKE_CENTS = 1000  # the inverse demand P(q) = CHOKE_CENTS - SLOPE * q is in cents per unit
SLOPE = 10  # cents per unit, per unit of quantity
PRIVATE_COST = 200  # cents per unit: the private marginal cost, constant
DAMAGE = 120  # cents per unit: the marginal external damage, constant
PUBLIC_COST = 400  # cents per unit: the marginal cost of the public good, constant


def demand_price(q: Fraction) -> Fraction:
    """Inverse demand in cents per unit at quantity q (units), for q up to the choke quantity."""
    return CHOKE_CENTS - SLOPE * q


def private_quantity(tax: int) -> Fraction:
    """The quantity at which demand price equals private marginal cost plus the tax, in units."""
    return Fraction(CHOKE_CENTS - PRIVATE_COST - tax, SLOPE)


def welfare_loss_wedge(q: Fraction) -> Fraction:
    """The gap in cents per unit between the marginal social cost and the demand price at quantity q."""
    return (PRIVATE_COST + DAMAGE) - demand_price(q)


def social_surplus(q: Fraction) -> Fraction:
    """Total surplus in cents: the area under inverse demand from 0 to q, less the social cost (cost plus damage).

    Inverse demand is linear, so the trapezoid rule over [0, q] is exact.
    """
    area = (demand_price(Fraction(0)) + demand_price(q)) / 2 * q
    return area - (PRIVATE_COST + DAMAGE) * q


def part_a() -> None:
    private = private_quantity(0)
    efficient = private_quantity(DAMAGE)
    print(f"part A: private equilibrium quantity without a tax = {private} units")
    print(f"part A: efficient quantity, where demand price equals marginal social cost = {efficient} units")
    matching = [t for t in range(0, 201) if private_quantity(t) == efficient]
    print(f"part A: integer taxes from 0 to 200 cents that give the efficient quantity = {matching}")
    tax = matching[0]
    revenue = tax * efficient
    print(f"part A: revenue at the Pigouvian tax = {revenue} cents = {float(revenue / 100):.2f} CU")
    by_wedge = (welfare_loss_wedge(efficient) + welfare_loss_wedge(private)) / 2 * (private - efficient)
    by_surplus = social_surplus(efficient) - social_surplus(private)
    print(
        f"part A: efficiency loss of the untaxed market, by the wedge over [{efficient}, {private}] = {by_wedge} cents"
    )
    print(f"part A: efficiency loss of the untaxed market, by the surplus difference = {by_surplus} cents")
    grid = [Fraction(q) for q in range(0, 101)]
    best = max(grid, key=social_surplus)
    print(f"part A: integer quantity from 0 to 100 that maximises total surplus = {best} units")


def willingness_1(g: Fraction) -> Fraction:
    """Consumer 1's willingness to pay in cents per unit at quantity g of the public good."""
    return 1000 - 100 * g


def willingness_2(g: Fraction) -> Fraction:
    """Consumer 2's willingness to pay in cents per unit at quantity g; zero once the line reaches zero."""
    return max(Fraction(0), 600 - 200 * g)


def aggregate_willingness(g: Fraction) -> Fraction:
    """The vertical sum: both consumers' willingness to pay at the same quantity g, added in cents per unit."""
    return willingness_1(g) + willingness_2(g)


def public_surplus(g: Fraction) -> Fraction:
    """Total surplus in cents: the area under the vertical sum from 0 to g, less the public cost of g units.

    The vertical sum is linear on [0, 3] and on [3, 10] (consumer 2's line reaches zero at g = 3), so the trapezoid
    rule is exact when the interval is split at 3.
    """
    kink = Fraction(3)
    pieces = [(Fraction(0), min(g, kink))]
    if g > kink:
        pieces.append((kink, g))
    area = Fraction(0)
    for a, b in pieces:
        area += (aggregate_willingness(a) + aggregate_willingness(b)) / 2 * (b - a)
    return area - PUBLIC_COST * g


def part_b() -> None:
    print(f"part B: vertical sum at quantity 3 = {aggregate_willingness(Fraction(3))} cents per unit")
    print(f"part B: consumer 2 at quantity 6 = {willingness_2(Fraction(6))}; consumer 1 = {willingness_1(Fraction(6))}")
    efficient = [Fraction(g) for g in range(0, 11) if aggregate_willingness(Fraction(g)) == PUBLIC_COST]
    shown = [int(g) for g in efficient]
    print(f"part B: integer quantity where the vertical sum equals the cost of 400 cents per unit = {shown}")
    grid = [Fraction(g) for g in range(0, 11)]
    best = max(grid, key=public_surplus)
    print(f"part B: integer quantity from 0 to 10 that maximises total surplus = {best} units")
    print(f"part B: total surplus at 6 units = {public_surplus(Fraction(6))} cents")
    horizontal = Fraction(1000 - PUBLIC_COST, 100) + max(Fraction(0), Fraction(600 - PUBLIC_COST, 200))
    print(f"part B: quantity from adding the two demands at the same price of 400 cents = {horizontal} units")
    print(f"part B: total surplus at 7 units = {public_surplus(Fraction(7))} cents")


def main() -> None:
    part_a()
    part_b()


main()
