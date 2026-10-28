"""Student docstring: the relevant-cost rule is coded with the comparison reversed (make when the net buy cost is lower).

AC4 lab L03 (lab 1): make-or-buy, sunk cost and keep-or-drop on a SIMULATED case.

SIMULATED: the firm, its products and every figure below are invented inputs of a hypothetical plant. Nothing here
is a company's data, and no network or file is read. Money is integer cents (100 cents = 1 currency unit, CU);
volumes are units or machine hours. Standard library only.

Rule the lab tests: a cost is relevant to a decision when it is a future cash flow that differs between the
alternatives. A sunk cost is the same under both alternatives, and so is any allocated common cost that stays
after one alternative is chosen. The lab prints the decision under the relevant-cost method and under the full-cost
method, changes the sunk and allocated inputs, and prints whether the relevant-cost difference and the decision move.
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class MakeOrBuy:
    """Annual make-or-buy inputs for component K, all money in cents."""

    units: int
    material_per_unit: int
    labour_per_unit: int
    variable_overhead_per_unit: int
    dedicated_fixed: int  # supervisor and dedicated tooling; avoided if the part is bought
    allocated_overhead_per_unit: int  # plant overhead spread over units; stays after the decision
    buy_price_per_unit: int
    scrap_value: int  # cash received for the existing equipment if the part is bought
    equipment_book_value: int  # sunk: depreciated cost already incurred


def fmt(cents: int) -> str:
    """Render integer cents as CU with two decimals, without rounding."""
    sign = "-" if cents < 0 else ""
    magnitude = abs(cents)
    return f"{sign}{magnitude // 100:,}.{magnitude % 100:02d}"


def avoidable_make_cost(c: MakeOrBuy) -> int:
    """Future cash cost of making in-house that stops if the part is bought, in cents per year."""
    per_unit = c.material_per_unit + c.labour_per_unit + c.variable_overhead_per_unit
    return c.units * per_unit + c.dedicated_fixed


def net_buy_cost(c: MakeOrBuy) -> int:
    """Future cash cost of buying: purchase price less the scrap cash received, in cents per year."""
    return c.units * c.buy_price_per_unit - c.scrap_value


def relevant_difference(c: MakeOrBuy) -> int:
    """Make cost minus buy cost. A positive value means buying is cheaper by that many cents per year."""
    return avoidable_make_cost(c) - net_buy_cost(c)


def full_cost_per_unit(c: MakeOrBuy) -> int:
    """Full unit cost of making: variable cost, allocated overhead and the dedicated fixed cost spread per unit.
    The division is exact here, which the lab checks."""
    if c.dedicated_fixed % c.units != 0:
        raise ValueError("dedicated fixed cost does not divide evenly by units; choose inputs that do")
    return (
        c.material_per_unit
        + c.labour_per_unit
        + c.variable_overhead_per_unit
        + c.allocated_overhead_per_unit
        + c.dedicated_fixed // c.units
    )


def full_cost_decision(c: MakeOrBuy) -> str:
    """Compare full unit cost of making with the buy price per unit."""
    return "buy" if c.buy_price_per_unit < full_cost_per_unit(c) else "make"


def relevant_decision(c: MakeOrBuy) -> str:
    """Choose the alternative with the lower relevant (differential) cash cost."""
    return "make" if net_buy_cost(c) < avoidable_make_cost(c) else "buy"


@dataclass(frozen=True)
class ProductLine:
    """Annual figures for product line B, all money in cents."""

    revenue: int
    variable_cost: int
    avoidable_fixed: int  # product-specific staff and advertising; stops if the line is dropped
    common_fixed: int  # plant-level cost allocated to B; stays if B is dropped


def operating_income(p: ProductLine) -> int:
    """Reported operating income of the line, including its share of common fixed cost."""
    return p.revenue - p.variable_cost - p.avoidable_fixed - p.common_fixed


def profit_if_kept(p: ProductLine) -> int:
    """Total profit of the firm from the line, with the common fixed cost counted once."""
    return operating_income(p)


def profit_if_dropped(p: ProductLine) -> int:
    """Total profit with the line dropped: revenue and avoidable costs go, the common fixed cost stays."""
    return -p.common_fixed


def main() -> None:
    base = MakeOrBuy(
        units=20_000,
        material_per_unit=400,
        labour_per_unit=300,
        variable_overhead_per_unit=150,
        dedicated_fixed=1_200_000,
        allocated_overhead_per_unit=200,
        buy_price_per_unit=1_050,
        scrap_value=300_000,
        equipment_book_value=2_000_000,
    )

    print("Part K, make or buy: 20,000 units a year (SIMULATED)")
    avoidable_per_unit = avoidable_make_cost(base) // base.units
    print(f"  avoidable make cost per unit (variable + dedicated fixed / units): {fmt(avoidable_per_unit)}")
    full_per_unit = fmt(full_cost_per_unit(base))
    print(f"  full make cost per unit (adds allocated overhead 2.00): {full_per_unit}")
    print(f"  buy price per unit: {fmt(base.buy_price_per_unit)}")
    print(f"  annual avoidable make cost: {fmt(avoidable_make_cost(base))}")
    print(f"  annual net buy cost (price less scrap {fmt(base.scrap_value)}): {fmt(net_buy_cost(base))}")
    print(f"  relevant difference (make minus buy): {fmt(relevant_difference(base))}")
    print(f"  relevant-cost decision: {relevant_decision(base)}")
    print(f"  full-cost decision: {full_cost_decision(base)}")

    sunk_changed = replace(base, equipment_book_value=5_000_000)
    print("Sunk cost check: book value of the equipment changed")
    print(f"  book value {fmt(base.equipment_book_value)} gives difference {fmt(relevant_difference(base))}")
    changed_diff = fmt(relevant_difference(sunk_changed))
    print(f"  book value {fmt(sunk_changed.equipment_book_value)} gives difference {changed_diff}")
    print(f"  decision unchanged: {relevant_decision(sunk_changed) == relevant_decision(base)}")

    overhead_changed = replace(base, allocated_overhead_per_unit=400)
    print("Allocated overhead check: allocated overhead per unit raised from 200 to 400")
    print(f"  full cost per unit: {fmt(full_cost_per_unit(overhead_changed))}")
    print(f"  relevant difference: {fmt(relevant_difference(overhead_changed))}")
    print(f"  relevant decision unchanged: {relevant_decision(overhead_changed) == relevant_decision(base)}")

    price_cut = replace(base, buy_price_per_unit=950)
    print("Price check: supplier offers 9.50 per unit")
    print(f"  relevant difference: {fmt(relevant_difference(price_cut))}")
    print(f"  relevant decision: {relevant_decision(price_cut)}")
    breakeven_price = (avoidable_make_cost(base) + base.scrap_value) // base.units
    print(f"  buy price at which buying equals making, scrap netted: {fmt(breakeven_price)}")

    line = ProductLine(
        revenue=1_500_000,
        variable_cost=900_000,
        avoidable_fixed=400_000,
        common_fixed=300_000,
    )
    print("Product line B, keep or drop: annual figures (SIMULATED)")
    print(f"  contribution margin: {fmt(line.revenue - line.variable_cost)}")
    print(f"  reported operating income after common fixed cost: {fmt(operating_income(line))}")
    print(f"  firm profit if kept: {fmt(profit_if_kept(line))}")
    print(f"  firm profit if dropped: {fmt(profit_if_dropped(line))}")
    print(f"  change in firm profit from dropping: {fmt(profit_if_dropped(line) - profit_if_kept(line))}")
    print(f"  keep-or-drop decision: {'keep' if profit_if_kept(line) > profit_if_dropped(line) else 'drop'}")

    spare_hours = 40_000 - 36_000
    order_units = 3_000
    order_price = 1_200
    order_variable = 700
    order_hours_per_unit = 2
    order_hours = order_units * order_hours_per_unit
    order_contribution = order_units * (order_price - order_variable)
    excess_hours = max(0, order_hours - spare_hours)
    displaced_contribution_per_unit = 1_000
    displaced_hours_per_unit = 2
    displaced_contribution_per_hour = displaced_contribution_per_unit // displaced_hours_per_unit
    lost_contribution = excess_hours * displaced_contribution_per_hour
    net_order = order_contribution - lost_contribution
    print("Special order under a machine-hour constraint (SIMULATED)")
    print(f"  machine hours needed: {order_hours}, spare hours: {spare_hours}, excess hours: {excess_hours}")
    print(f"  order contribution: {fmt(order_contribution)}")
    per_hour = fmt(displaced_contribution_per_hour)
    print(f"  contribution forgone on product D ({per_hour} per hour, excess hours): {fmt(lost_contribution)}")
    print(f"  net effect of accepting: {fmt(net_order)}")
    print(f"  decision: {'accept' if net_order > 0 else 'reject'}")
    naive_order_per_hour = (order_price - order_variable) // order_hours_per_unit
    print(f"  naive per-hour comparison: order earns {fmt(naive_order_per_hour)}, D earns {per_hour} per hour")
    print(f"  naive decision: {'accept' if naive_order_per_hour > displaced_contribution_per_hour else 'reject'}")


main()
