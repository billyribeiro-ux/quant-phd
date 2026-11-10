"""CS1 lab L01: Function definitions, lexical scope, and closure bindings.

Standard library only. Demonstrates the LEGB (Local, Enclosing, Global, Built-in) rule,
variable shadowing, and closure capture.
SIMULATED toy discount factors and multipliers.
"""

from __future__ import annotations

from collections.abc import Callable

# Global scope
DISCOUNT_RATE: float = 0.05


def inspect_scope_shadowing(val: float) -> tuple[float, float]:
    """Demonstrate local variable shadowing of global scope."""
    # Local variable shadows global DISCOUNT_RATE
    DISCOUNT_RATE: float = val  # noqa: N806
    local_val = DISCOUNT_RATE
    return local_val, globals()["DISCOUNT_RATE"]


def make_accumulator(initial_cash: float) -> Callable[[float], float]:
    """Return a closure holding enclosing state."""
    balance: float = initial_cash

    def transact(cash_flow: float) -> float:
        nonlocal balance
        balance += cash_flow
        return balance

    return transact


def compound_discount(cash: float, rate: float, periods: int) -> float:
    """Compute simple discrete discounting: cash / (1 + rate)^periods."""
    if periods < 0:
        raise ValueError("periods must be non-negative")
    factor = 1.0
    for _ in range(periods):
        factor *= 1.0 + rate
    return cash / factor


def main() -> None:
    # 1. Global vs local shadowing
    local_rate, global_rate = inspect_scope_shadowing(0.12)
    print(f"global before: {DISCOUNT_RATE:.4f}")
    print(f"local inside: {local_rate:.4f}")
    print(f"global read via globals(): {global_rate:.4f}")
    print(f"shadowing does not mutate global: {DISCOUNT_RATE == 0.05}")

    # 2. Closure enclosing scope
    acc = make_accumulator(1000.0)
    b1 = acc(250.0)
    b2 = acc(-150.0)
    b3 = acc(50.0)
    print(f"closure step 1: balance = {b1:.1f}")
    print(f"closure step 2: balance = {b2:.1f}")
    print(f"closure step 3: balance = {b3:.1f}")

    # 3. Parameter binding and compound discount calculation
    pv = compound_discount(1102.5, 0.05, 2)
    print(f"discounted cash flow: {pv:.2f}")
    print(f"exact match to expected 1000.00: {abs(pv - 1000.0) < 1e-9}")


main()
