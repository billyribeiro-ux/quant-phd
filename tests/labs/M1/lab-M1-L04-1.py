"""M1 L04 lab 1: compounding frequency, the effective annual rate, and the factor e^(r t).

Inputs are illustrative, not data: a nominal annual rate r = 0.05 and a principal of 10,000.00 CU, which is
1,000,000 cents. No random draws are used, so every run prints the same lines.

Part A: the effective annual rate (1 + r/m)^m - 1 for m periods per year.
Part B: the one-year factor (1 + r/m)^m for growing m, beside e^r, with the error e^r minus the factor.
Part C: the value of the principal after 10 years, in whole cents, for annual, monthly, daily and continuous
compounding.

Every factor is a Decimal computed at 60 significant digits. CU is the currency unit; 1 CU is 100 cents.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, getcontext

getcontext().prec = 60

RATE = Decimal("0.05")
PRINCIPAL_CENTS = 1_000_000
PERIODS = (1, 2, 4, 12, 52, 365, 1000, 10000, 100000, 1000000)


def periodic_factor(rate: Decimal, periods: int, years: int) -> Decimal:
    """Growth factor (1 + rate/periods)^(periods * years) for a nominal annual rate, equal periods, whole years."""
    return (Decimal(1) + rate / periods) ** (periods * years)


def continuous_factor(rate: Decimal, years: int) -> Decimal:
    """The continuously compounded factor e^(rate * years)."""
    return (rate * years).exp()


def to_cents(amount: Decimal) -> int:
    """The amount in whole cents, with a tie going to the even cent."""
    return int(amount.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def main() -> None:
    """Print Parts A, B and C. Each line is a fixed string or a number, so the output is reproducible."""
    print("Part A: effective annual rate for a nominal 5% rate")
    for m in (1, 2, 4, 12, 365):
        ear = periodic_factor(RATE, m, 1) - 1
        print(f"periods {m} effective_annual_rate {ear:.10f}")

    print("Part B: one-year factor (1 + r/m)^m beside e^r")
    e_r = continuous_factor(RATE, 1)
    print(f"continuous_factor_one_year {e_r:.10f}")
    previous = Decimal(0)
    increasing = True
    below = True
    for m in PERIODS:
        factor = periodic_factor(RATE, m, 1)
        increasing = increasing and factor > previous
        below = below and factor < e_r
        previous = factor
        print(f"periods {m} factor {factor:.10f} error {e_r - factor:.10f}")
    print(f"factor_increases_with_periods {increasing}")
    print(f"factor_below_continuous {below}")

    print("Part C: value of 1,000,000 cents after 10 years, in whole cents")
    values: dict[str, int] = {}
    for label, m in (("annual", 1), ("monthly", 12), ("daily", 365)):
        values[label] = to_cents(PRINCIPAL_CENTS * periodic_factor(RATE, m, 10))
        print(f"{label} cents {values[label]}")
    values["continuous"] = to_cents(PRINCIPAL_CENTS * continuous_factor(RATE, 10))
    print(f"continuous cents {values['continuous']}")
    print(f"monthly_minus_annual_cents {values['monthly'] - values['annual']}")
    print(f"continuous_minus_daily_cents {values['continuous'] - values['daily']}")


main()
