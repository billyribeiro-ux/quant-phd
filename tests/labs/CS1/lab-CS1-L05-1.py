"""CS1 lab L05: Type hints, annotations, and static typing semantics.

Standard library only. Demonstrates typing inspection via __annotations__ and typing.get_type_hints,
showing that Python does not enforce hints at runtime without external checkers.
SIMULATED fixed-income interest calculations.
"""

from __future__ import annotations

import typing
from collections.abc import Sequence


def compute_coupon_payment(face: float, coupon_rate: float, frequency: int = 2) -> float:
    """Compute per-period coupon payment: (face * coupon_rate) / frequency."""
    return (face * coupon_rate) / float(frequency)


def aggregate_cash_flows(flows: Sequence[float], discount_factor: float | None = None) -> float:
    """Aggregate a sequence of flows with optional discounting."""
    factor = 1.0 if discount_factor is None else discount_factor
    return sum(flows) * factor


def dynamic_type_bypass(x: float, y: float) -> float:
    """Function annotated as float -> float, demonstrating runtime non-enforcement."""
    return x + y


def main() -> None:
    # 1. Type annotations inspection
    hints = typing.get_type_hints(compute_coupon_payment)
    print(f"face annotation: {hints['face'].__name__}")
    print(f"coupon_rate annotation: {hints['coupon_rate'].__name__}")
    print(f"frequency annotation: {hints['frequency'].__name__}")
    print(f"return annotation: {hints['return'].__name__}")

    # 2. Correctly typed execution
    payment = compute_coupon_payment(1000.0, 0.06, 2)
    print(f"semi-annual coupon: {payment:.2f}")

    # 3. Optional union typing
    flows: list[float] = [30.0, 30.0, 1030.0]
    total_undiscounted = aggregate_cash_flows(flows)
    total_discounted = aggregate_cash_flows(flows, 0.95)
    print(f"undiscounted flows: {total_undiscounted:.1f}")
    print(f"discounted flows: {total_discounted:.2f}")

    # 4. Runtime non-enforcement proof
    # At runtime, passing strings into an annotated float function concatenates strings:
    str_result = dynamic_type_bypass("quant-", "phd")  # type: ignore[arg-type]
    print(f"runtime bypass result: {str_result}")
    print(f"hints exist in __annotations__: {'coupon_rate' in compute_coupon_payment.__annotations__}")


main()
