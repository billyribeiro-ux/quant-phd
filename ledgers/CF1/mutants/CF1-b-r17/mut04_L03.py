"""CF1 L03 lab 1: one SIMULATED project discounted consistently in real and in nominal terms.

SIMULATED: the project is a fixed input written here. It is not any firm's project.
Units: money in cents. Real cash flows are stated at base-year prices, so each real flow is in base-year cents.
Rates are decimals per year. Inflation is constant at pi per year, so the price level at year t is (1 + pi)**t,
and the nominal rate n follows the exact Fisher form (1 + n) = (1 + r)(1 + pi), where r is the real rate.
Discounted and inflated amounts are floats, not rounded to whole cents. The lab draws no random numbers.
"""

from __future__ import annotations

from collections.abc import Sequence

# t = 0 is the outlay; t = 1 to 5 are operating inflows, all in base-year cents.
REAL_FLOWS: tuple[int, ...] = (-100_000_000, 30_000_000, 30_000_000, 30_000_000, 30_000_000, 30_000_000)
REAL_RATE = 0.06
INFLATION = 0.03
INFLATION_GRID = (0.0, 0.01, 0.03, 0.05)
REAL_RATE_GRID = (0.02, 0.06, 0.10)


def nominal_rate(real: float, inflation: float) -> float:
    """Nominal rate per year from the exact Fisher form (1 + n) = (1 + r)(1 + pi); all inputs are decimals per year."""
    return (1.0 + real) * (1.0 + inflation) - 1.0


def npv(flows: Sequence[float], rate: float) -> float:
    """Net present value in cents: the sum of flows[t] / (1 + rate)**t over every year t, rate per year."""
    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))


def nominal_flows(real: Sequence[float], inflation: float) -> list[float]:
    """Nominal cash flows in cents: real[t] * (1 + inflation)**t, the price-level conversion at constant inflation."""
    return [cf * (1.0 + inflation) ** (t - 1 if t else 0) for t, cf in enumerate(real)]


def usd(cents: float) -> str:
    """Cents shown as dollars with two decimals and no thousands separator."""
    return f"{cents / 100:.2f}"


def mixed_identity(real: Sequence[float], real_rate: float, inflation: float) -> float:
    """The mixed-discounting gap, cents: sum over t >= 1 of real[t] * ((1 + pi)**t - 1) / (1 + r)**t."""
    return sum(cf * ((1.0 + inflation) ** t - 1.0) / (1.0 + real_rate) ** t for t, cf in enumerate(real) if t >= 1)


def main() -> None:
    n = nominal_rate(REAL_RATE, INFLATION)
    nominal = nominal_flows(REAL_FLOWS, INFLATION)
    print(f"real rate {REAL_RATE:.6f}, inflation {INFLATION:.6f}, nominal rate {n:.6f}")
    print("t  real_cents  nominal_cents")
    for t, (real_cf, nominal_cf) in enumerate(zip(REAL_FLOWS, nominal, strict=True)):
        print(f"{t}  {real_cf}  {nominal_cf:.2f}")

    real_npv = npv(REAL_FLOWS, REAL_RATE)
    consistent = npv(nominal, n)
    mixed_over = npv(nominal, REAL_RATE)
    mixed_under = npv(REAL_FLOWS, n)
    print(f"NPV real flows at real rate: {usd(real_npv)} USD")
    print(f"NPV nominal flows at nominal rate: {usd(consistent)} USD")
    print(f"NPV nominal flows at real rate (mixed): {usd(mixed_over)} USD")
    print(f"NPV real flows at nominal rate (mixed): {usd(mixed_under)} USD")
    print(f"largest absolute gap, consistent minus real, cents: {abs(consistent - real_npv):.6f}")
    gap = mixed_over - real_npv
    print(f"mixed minus real, cents: {gap:.2f}")
    print(
        "identity gap, mixed minus real less the sum over t >= 1, cents: "
        f"{abs(gap - mixed_identity(REAL_FLOWS, REAL_RATE, INFLATION)):.6f}"
    )

    additive = REAL_RATE + INFLATION
    print(
        f"exact nominal rate minus (real + inflation): {n - additive:.6f}; "
        f"real x inflation: {REAL_RATE * INFLATION:.6f}"
    )
    print(f"NPV real flows at additive rate r + pi = {additive:.6f}: {usd(npv(REAL_FLOWS, additive))} USD")

    print("grid of 12 cases (inflation 0 to 0.05, real rate 0.02 to 0.10): consistency and mixed gaps")
    worst_consistency = 0.0
    for inflation in INFLATION_GRID:
        for real_rate in REAL_RATE_GRID:
            nom = nominal_flows(REAL_FLOWS, inflation)
            rate_n = nominal_rate(real_rate, inflation)
            gap_case = npv(nom, rate_n) - npv(REAL_FLOWS, real_rate)
            worst_consistency = max(worst_consistency, abs(gap_case))
    print(f"largest absolute consistency gap over the grid, cents: {worst_consistency:.6f}")

    print("inflation  mixed minus real, USD (nominal flows at the real rate 0.06)")
    for inflation in INFLATION_GRID:
        mixed = npv(nominal_flows(REAL_FLOWS, inflation), REAL_RATE) - real_npv
        print(f"{inflation:.2f}  {mixed / 100:.2f}")


main()
