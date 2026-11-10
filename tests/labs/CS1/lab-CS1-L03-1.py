"""CS1 lab L03: Object-oriented programming and structural protocols.

Standard library only. Tests class encapsulation, instance methods, and structural
conformance to a Protocol without nominal inheritance.
SIMULATED valuation models.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Pricer(Protocol):
    """Structural protocol defining pricing behavior."""

    def price(self, spot: float) -> float:
        """Compute fair value given underlying spot price."""
        ...


class LinearPricer:
    """Nominal class implementing forward payoff."""

    def __init__(self, multiplier: float, basis: float) -> None:
        self.multiplier = multiplier
        self.basis = basis

    def price(self, spot: float) -> float:
        return self.multiplier * spot + self.basis


class DiscountedCashFlow:
    """A completely independent class that never mentions Pricer or inherits from it."""

    def __init__(self, discount_factor: float) -> None:
        self.discount_factor = discount_factor

    def price(self, spot: float) -> float:
        return spot * self.discount_factor


def execute_valuation(pricer: Pricer, spot: float) -> float:
    """Polymorphic valuation function accepting any structural pricer."""
    return pricer.price(spot)


def main() -> None:
    linear = LinearPricer(1.5, -10.0)
    dcf = DiscountedCashFlow(0.95)

    # 1. Structural runtime protocol check
    print(f"LinearPricer conforms to Pricer: {isinstance(linear, Pricer)}")
    print(f"DiscountedCashFlow conforms to Pricer: {isinstance(dcf, Pricer)}")
    print(f"DiscountedCashFlow subclasses Pricer: {issubclass(DiscountedCashFlow, Pricer)}")

    # 2. Polymorphic dispatch through execute_valuation
    spot_quote = 100.0
    val_linear = execute_valuation(linear, spot_quote)
    val_dcf = execute_valuation(dcf, spot_quote)

    print(f"spot price: {spot_quote:.1f}")
    print(f"linear pricer valuation: {val_linear:.2f}")
    print(f"dcf pricer valuation: {val_dcf:.2f}")

    # 3. Encapsulation check
    print(f"linear pricer multiplier attribute: {linear.multiplier:.2f}")
    print(f"linear valuation matches direct calculation: {abs(val_linear - 140.0) < 1e-9}")


main()
