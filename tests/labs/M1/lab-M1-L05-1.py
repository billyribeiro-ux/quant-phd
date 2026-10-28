"""M1 L05 lab 1: discount factors for one 5% rate under three conventions.

Inputs are illustrative, not data: a rate r = 0.05, a cash flow of 1,000,000 cents (10,000.00 CU) due after the
year fractions t listed below, and no random draws. A year fraction is an input number of years; this lab does not
define a day-count convention.

Conventions, for a rate r and a time t in years:
  annual effective:    DF = 1 / (1 + r)^t
  semiannual nominal:  DF = 1 / (1 + r/2)^(2t)
  continuous:          DF = e^(-r t)
The continuous factor is also computed at the equivalent continuous rate delta = ln(1 + r). There, e^(-delta t)
must equal the annual effective factor.

Every factor is a Decimal at 60 significant digits. CU is the currency unit; 1 CU is 100 cents.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, getcontext

getcontext().prec = 60

RATE = Decimal("0.05")
FACE_CENTS = 1_000_000
YEARS = (Decimal("0.5"), Decimal("1"), Decimal("2"), Decimal("5"), Decimal("10"))


def df_annual(rate: Decimal, t: Decimal) -> Decimal:
    """Annual effective discount factor 1/(1 + rate)^t, for a time t in years."""
    return 1 / (1 + rate) ** t


def df_semiannual(rate: Decimal, t: Decimal) -> Decimal:
    """Discount factor with two compounding periods a year at nominal rate: 1/(1 + rate/2)^(2t)."""
    return 1 / (1 + rate / 2) ** (2 * t)


def df_continuous(rate: Decimal, t: Decimal) -> Decimal:
    """Continuous discount factor e^(-rate t)."""
    return (-rate * t).exp()


def to_cents(amount: Decimal) -> int:
    """The amount in whole cents, with a tie going to the even cent."""
    return int(amount.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def main() -> None:
    """Print the equivalent continuous rate, the factor table, two checks, and the present values at t = 5."""
    delta = (1 + RATE).ln()
    print(f"equivalent_continuous_rate {delta:.10f}")
    gaps: list[Decimal] = []
    decreasing = True
    inside = True
    previous = Decimal(1)
    for t in YEARS:
        annual = df_annual(RATE, t)
        semi = df_semiannual(RATE, t)
        cont = df_continuous(RATE, t)
        equiv = df_continuous(delta, t)
        gaps.append(abs(equiv - annual))
        decreasing = decreasing and annual < previous
        inside = inside and Decimal(0) < annual < Decimal(1)
        previous = annual
        print(
            f"t {t} annual {annual:.10f} semiannual {semi:.10f} "
            f"continuous_at_5pct {cont:.10f} equivalent_continuous {equiv:.10f}"
        )
    print(f"max_gap_equivalent_vs_annual {max(gaps):.10f}")
    print(f"annual_decreasing_in_t {decreasing}")
    print(f"annual_between_zero_and_one {inside}")

    t5 = Decimal("5")
    print("present values at t = 5 of 1,000,000 cents, in whole cents")
    print(f"annual cents {to_cents(FACE_CENTS * df_annual(RATE, t5))}")
    print(f"semiannual cents {to_cents(FACE_CENTS * df_semiannual(RATE, t5))}")
    print(f"continuous cents {to_cents(FACE_CENTS * df_continuous(RATE, t5))}")


main()
