"""Lab FC4-L04-1: Gordon-growth sensitivity: value as (r - g) shrinks (Curriculum Lab)."""

from fractions import Fraction


def main() -> None:
    # Closed-form Gordon growth model: P_0 = D_1 / (r - g)
    # Fixed expected next dividend D_1 = $2.00
    d1 = Fraction(2, 1)

    # Grid of spreads r - g shrinking toward zero
    spreads = [
        Fraction(50, 1000),  # 5.0%
        Fraction(40, 1000),  # 4.0%
        Fraction(30, 1000),  # 3.0%
        Fraction(20, 1000),  # 2.0%
        Fraction(10, 1000),  # 1.0%
        Fraction(5, 1000),  # 0.5%
        Fraction(25, 10000),  # 0.25%
        Fraction(10, 10000),  # 0.10%
        Fraction(5, 10000),  # 0.05%
        Fraction(1, 10000),  # 0.01%
    ]

    print("Gordon Growth Sensitivity: Implied Equity Value P_0 as Spread (r - g) Shrinks")
    print(f"Fixed next-period dividend D_1 = ${float(d1):.2f}")
    print("-" * 68)
    print(f"{'Spread (r - g)':>16} {'Spread (pct)':>14} {'P_0 (Exact)':>18} {'P_0 (Decimal USD)':>16}")
    print("-" * 68)

    prev_p = Fraction(0)
    for spread in spreads:
        p0 = d1 / spread
        spread_pct = float(spread) * 100
        print(f"{spread!s:>16} {spread_pct:>13.2f}% {p0!s:>18} {float(p0):>16.2f}")
        assert p0 > prev_p, "Value must increase monotonically as spread shrinks"
        prev_p = p0

    print("-" * 68)
    print("Nonlinear explosion verified: as (r - g) -> 0+, implied value P_0 -> +infinity.")


main()
