"""CS3 Lesson 1 Inline Lab 1: Relational algebra closure and operations.

Demonstrates relations as sets of named tuples, selection, projection,
natural join, and verifies closure under relational operations.
Data: SIMULATED market orders and instruments.
"""

from __future__ import annotations

from typing import NamedTuple


class Instrument(NamedTuple):
    symbol: str
    asset_class: str
    currency: str


class Order(NamedTuple):
    order_id: int
    symbol: str
    quantity: int
    price: float


def select_orders_by_symbol(orders: set[Order], symbol: str) -> set[Order]:
    """Relational selection: sigma_{symbol = sym}(Orders)."""
    return {o for o in orders if o.symbol == symbol}


def project_order_symbols(orders: set[Order]) -> set[str]:
    """Relational projection: pi_{symbol}(Orders)."""
    return {o.symbol for o in orders}


class EnrichedOrder(NamedTuple):
    order_id: int
    symbol: str
    quantity: int
    price: float
    asset_class: str
    currency: str


def natural_join(orders: set[Order], instruments: set[Instrument]) -> set[EnrichedOrder]:
    """Relational natural join: Orders bowtie Instruments on symbol."""
    inst_map = {inst.symbol: inst for inst in instruments}
    joined: set[EnrichedOrder] = set()
    for o in orders:
        if o.symbol in inst_map:
            inst = inst_map[o.symbol]
            joined.add(
                EnrichedOrder(
                    order_id=o.order_id,
                    symbol=o.symbol,
                    quantity=o.quantity,
                    price=o.price,
                    asset_class=inst.asset_class,
                    currency=inst.currency,
                )
            )
    return joined


def main() -> None:
    # SIMULATED relations
    instruments: set[Instrument] = {
        Instrument("AAPL", "EQUITY", "USD"),
        Instrument("MSFT", "EQUITY", "USD"),
        Instrument("EURUSD", "FX", "USD"),
        Instrument("UST10Y", "BOND", "USD"),
    }

    orders: set[Order] = {
        Order(101, "AAPL", 100, 150.25),
        Order(102, "AAPL", 200, 150.50),
        Order(103, "MSFT", 50, 310.00),
        Order(104, "EURUSD", 100000, 1.0850),
        Order(105, "UNKNOWN", 10, 99.00),
    }

    print(f"Total initial orders: {len(orders)}")
    print(f"Total instruments: {len(instruments)}")

    # 1. Selection
    aapl_orders = select_orders_by_symbol(orders, "AAPL")
    print(f"Selection sigma_(symbol='AAPL') count: {len(aapl_orders)}")
    for o in sorted(aapl_orders, key=lambda x: x.order_id):
        print(f"  Order {o.order_id}: {o.symbol} qty={o.quantity} px={o.price:.2f}")

    # 2. Projection
    distinct_symbols = project_order_symbols(orders)
    print(f"Projection pi_(symbol) distinct count: {len(distinct_symbols)}")
    print(f"  Distinct symbols: {sorted(distinct_symbols)}")

    # 3. Natural Join
    enriched = natural_join(orders, instruments)
    print(f"Natural join count: {len(enriched)}")
    for eo in sorted(enriched, key=lambda x: x.order_id):
        print(f"  Enriched {eo.order_id}: {eo.symbol} class={eo.asset_class} ccy={eo.currency}")

    # 4. Relational closure check
    # The output of natural join is itself a set of tuples with no duplicate rows.
    is_relation = isinstance(enriched, set) and all(isinstance(x, tuple) for x in enriched)
    print(f"Relational closure verified: {is_relation}")


if __name__ == "__main__":
    main()
