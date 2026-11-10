"""CS4 Lesson 7 Inline Lab 1: Bit-for-bit reproducibility and floating-point non-associativity.

Demonstrates that IEEE 754 binary floating-point addition is non-associative: summing the
identical set of numbers in different summation orders produces distinct bit representations.
Compares floating-point accumulation against exact rational arithmetic using fractions.Fraction,
proving that rational summation is strictly commutative and associative, yielding bit-for-bit
identical output independent of summation order.
"""

from __future__ import annotations

from fractions import Fraction


def sum_floats(values: list[float]) -> float:
    """Accumulate floating-point numbers in specified list order."""
    total = 0.0
    for v in values:
        total += v
    return total


def sum_fractions(values: list[Fraction]) -> Fraction:
    """Accumulate exact rational numbers in specified list order."""
    total = Fraction(0, 1)
    for v in values:
        total += v
    return total


def main() -> None:
    print("Bit-for-bit reproducibility and numerical representation evaluation:")

    # Four floating-point values where magnitude differences expose non-associativity
    # 1e16 + 1.0 loses the 1.0 in float64 precision, but 1.0 + -1.0 cancels exactly
    float_forward = [1e16, 1.0, -1e16, 1e-16]
    float_reverse = list(reversed(float_forward))

    sum_fwd = sum_floats(float_forward)
    sum_rev = sum_floats(float_reverse)

    print(f"Float forward values: {float_forward}")
    print(f"Float forward sum:    {sum_fwd} (hex: {sum_fwd.hex()})")
    print(f"Float reverse sum:    {sum_rev} (hex: {sum_rev.hex()})")
    floats_identical = sum_fwd.hex() == sum_rev.hex()
    print(f"Floating-point bit-for-bit equality: {floats_identical}")

    # Exact rational equivalents: 10^16, 1, -10^16, 10^-16
    frac_forward = [
        Fraction(10**16, 1),
        Fraction(1, 1),
        Fraction(-(10**16), 1),
        Fraction(1, 10**16),
    ]
    frac_reverse = list(reversed(frac_forward))

    sum_frac_fwd = sum_fractions(frac_forward)
    sum_frac_rev = sum_fractions(frac_reverse)

    print(f"\nExact Fraction forward sum: {sum_frac_fwd}")
    print(f"Exact Fraction reverse sum: {sum_frac_rev}")
    fracs_identical = sum_frac_fwd == sum_frac_rev
    print(f"Fraction bit-for-bit equality: {fracs_identical}")

    print("\nConclusion: Exact rational arithmetic guarantees order-invariant bit reproducibility.")


main()
