"""AC4 lab L04 (lab 1): volume-based and activity-based unit costs for two SIMULATED products.

SIMULATED: the two products, the overhead pools and every driver count are invented inputs of a hypothetical plant.
Nothing here is a company's data, and no network or file is read. Money is integer cents (100 cents = 1 currency
unit, CU). Every allocation divides exactly; a rate that does not divide evenly raises ValueError, so no
rounding can hide a reconciliation error. Standard library only.

Two methods are compared on the same overhead pool of 100,000.00 CU. Volume-based costing spreads the pool by one
volume driver (direct labour hours). Activity-based costing (two stages) first assigns each activity pool to products by
its own driver, then divides by product volume. The lab prints whether each method allocates the whole pool, and prints
the cross-subsidy between the two products.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Annual volume and direct figures for one product. Money in cents."""

    name: str
    units: int
    direct_cost_per_unit: int
    price_per_unit: int
    labour_hours: int  # direct labour hours in total for the year (volume driver)


@dataclass(frozen=True)
class ActivityPool:
    """One activity cost pool with its cost driver counts per product, in cents."""

    name: str
    cost: int
    driver_counts: tuple[int, ...]  # one count per product, same order as the products


def fmt(cents: int) -> str:
    """Render integer cents as CU with two decimals, without rounding."""
    sign = "-" if cents < 0 else ""
    magnitude = abs(cents)
    return f"{sign}{magnitude // 100:,}.{magnitude % 100:02d}"


def exact_rate(cost: int, driver_total: int, label: str) -> int:
    """Cost per driver unit in cents. Raises ValueError unless the division is exact."""
    if driver_total <= 0:
        raise ValueError(f"{label}: the driver total must be positive")
    if cost % driver_total != 0:
        raise ValueError(f"{label}: {cost} does not divide evenly by {driver_total} driver units")
    return cost // driver_total


def volume_based(products: tuple[Product, ...], pool: int) -> dict[str, int]:
    """Overhead per product in cents: the pool spread by direct labour hours."""
    total_hours = sum(p.labour_hours for p in products)
    rate = exact_rate(pool, total_hours, "labour-hour rate")
    return {p.name: rate * p.labour_hours for p in products}


def activity_based(products: tuple[Product, ...], pools: tuple[ActivityPool, ...]) -> dict[str, int]:
    """Overhead per product in cents: stage one assigns each pool by its driver counts, stage two sums per product."""
    totals = {p.name: 0 for p in products}
    for pool in pools:
        if len(pool.driver_counts) != len(products):
            raise ValueError(f"{pool.name}: one driver count per product is required")
        rate = exact_rate(pool.cost, sum(pool.driver_counts), pool.name)
        for product, count in zip(products, pool.driver_counts, strict=True):
            totals[product.name] += rate * count
    return totals


def unit_cost(product: Product, overhead: int) -> int:
    """Full unit cost in cents: direct cost plus overhead per unit, with exact division."""
    if overhead % product.units != 0:
        raise ValueError(f"{product.name}: overhead does not divide evenly by units")
    return product.direct_cost_per_unit + overhead // product.units


def unit_margin(product: Product, overhead: int) -> int:
    """Price less full unit cost, in cents per unit."""
    return product.price_per_unit - unit_cost(product, overhead)


def main() -> None:
    pool_total = 10_000_000
    x = Product("X", units=10_000, direct_cost_per_unit=1_200, price_per_unit=2_000, labour_hours=8_000)
    y = Product("Y", units=2_000, direct_cost_per_unit=1_500, price_per_unit=3_000, labour_hours=2_000)
    products = (x, y)
    pools = (
        ActivityPool("setups", 4_000_000, (20, 60)),
        ActivityPool("inspections", 2_000_000, (100, 300)),
        ActivityPool("machine hours", 4_000_000, (6_000, 2_000)),
    )

    print("Overhead pool, total: " + fmt(pool_total) + " (SIMULATED)")
    print("Product inputs (SIMULATED)")
    for p in products:
        print(
            f"  {p.name}: units {p.units:,}, direct cost {fmt(p.direct_cost_per_unit)}, "
            f"price {fmt(p.price_per_unit)}, labour hours {p.labour_hours:,}"
        )

    vol = volume_based(products, pool_total)
    print("Volume-based costing (direct labour hours)")
    print(f"  labour-hour rate: {fmt(pool_total // sum(p.labour_hours for p in products))} per hour")
    for p in products:
        print(f"  {p.name}: overhead {fmt(vol[p.name])}, per unit {fmt(vol[p.name] // p.units)}")
    print(f"  allocated total: {fmt(sum(vol.values()))}, equals pool: {sum(vol.values()) == pool_total}")

    act = activity_based(products, pools)
    print("Activity-based costing (two stages)")
    for pool in pools:
        rate = exact_rate(pool.cost, sum(pool.driver_counts), pool.name)
        print(f"  {pool.name}: pool {fmt(pool.cost)}, rate {fmt(rate)} per driver unit")
        for p, count in zip(products, pool.driver_counts, strict=True):
            print(f"    {p.name}: {count:,} drivers, {fmt(rate * count)}")
    for p in products:
        print(f"  {p.name}: overhead {fmt(act[p.name])}, per unit {fmt(act[p.name] // p.units)}")
    print(f"  allocated total: {fmt(sum(act.values()))}, equals pool: {sum(act.values()) == pool_total}")

    print("Cross-subsidy and unit margins")
    for p in products:
        shift = act[p.name] - vol[p.name]
        print(f"  {p.name}: activity-based minus volume-based overhead {fmt(shift)}")
        print(f"    unit margin, volume-based: {fmt(unit_margin(p, vol[p.name]))}")
        print(f"    unit margin, activity-based: {fmt(unit_margin(p, act[p.name]))}")
    profit_vol = {p.name: unit_margin(p, vol[p.name]) * p.units for p in products}
    profit_act = {p.name: unit_margin(p, act[p.name]) * p.units for p in products}
    print(f"  annual margin, volume-based: X {fmt(profit_vol['X'])}, Y {fmt(profit_vol['Y'])}")
    print(f"  annual margin, activity-based: X {fmt(profit_act['X'])}, Y {fmt(profit_act['Y'])}")
    total_margin = sum(profit_vol.values())
    print(f"  total margin, both methods: {fmt(total_margin)} and {fmt(sum(profit_act.values()))}")
    print(f"  totals agree: {total_margin == sum(profit_act.values())}")
    y_break_vol = y.direct_cost_per_unit + vol["Y"] // y.units
    y_break_act = y.direct_cost_per_unit + act["Y"] // y.units
    print(
        f"  price at which Y breaks even per unit: volume-based {fmt(y_break_vol)}, activity-based {fmt(y_break_act)}"
    )

    sens_pools = (
        ActivityPool("setups", 4_000_000, (20, 20)),
        pools[1],
        pools[2],
    )
    sens = activity_based(products, sens_pools)
    print("Sensitivity: Y setups cut from 60 to 20 (same pools)")
    for p in products:
        print(f"  {p.name}: overhead {fmt(sens[p.name])}, per unit {fmt(sens[p.name] // p.units)}")
    print(f"  allocated total: {fmt(sum(sens.values()))}, equals pool: {sum(sens.values()) == pool_total}")


main()
