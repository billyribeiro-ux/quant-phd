"""LX1 L02 lab 1: the real value of a fixed nominal debt over a SIMULATED price-index path.

SIMULATED. The price index is generated from seeded draws of integer percentage changes, one per period, so
every run prints the same lines. No economy is described by these numbers. The nominal debt is an illustrative
amount of 10,000.00 currency units, which is 1,000,000 cents, and the base-date index is P_0 = 100 index points.

All money is in integer cents. The price index is an exact Fraction. The real value of the fixed nominal debt at date t,
in base-date cents, is V_t = D * P_0 / P_t, computed exactly and rounded once, half up, to a whole cent. The index is
shown to four decimal places, rounded half up, for display only.

Part A: the simulated price index P_t for t = 0 to 12, from the seeded draws.
Part B: the real value V_t in whole cents, and the exact identity V_t / V_(t-1) = P_(t-1) / P_t for every period.
Part C: the periods in which the price index falls, the periods in which the real value rises, and whether the two sets
are equal.
Part D: the change in real value over the whole horizon, exactly and in whole cents.
Part E: Proposition 1.2 at an illustrative parity: the currency price of one gram is 1 / kappa, and kappa times that
price is 1 exactly.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

SEED = 20261104
HORIZON = 12
DEBT_CENTS = 1_000_000
BASE_INDEX = Fraction(100)
CHANGE_LOW_PERCENT = -4
CHANGE_HIGH_PERCENT = 3
KAPPA_GRAMS_PER_UNIT = Fraction(2, 5)


def round_half_up(amount: Fraction) -> int:
    """Round a Fraction to a whole number, with a tie going toward plus infinity."""
    return math.floor(amount + Fraction(1, 2))


def fixed_decimal(amount: Fraction, places: int) -> str:
    """Show a non-negative Fraction with a fixed number of decimal places, rounded half up, for display only."""
    scaled = round_half_up(amount * 10**places)
    whole, frac = divmod(scaled, 10**places)
    return f"{whole}.{frac:0{places}d}"


def price_path(seed: int, horizon: int) -> tuple[list[Fraction], list[int]]:
    """Return (P_0 .. P_horizon, percentage changes c_1 .. c_horizon) for a seeded simulated index.

    The index P_t = P_(t-1) * (1 + c_t / 100) is exact. Each change c_t is an integer percent drawn uniformly from
    CHANGE_LOW_PERCENT to CHANGE_HIGH_PERCENT, inclusive.
    """
    rng = random.Random(seed)
    prices = [BASE_INDEX]
    changes: list[int] = []
    for _ in range(horizon):
        change = rng.randint(CHANGE_LOW_PERCENT, CHANGE_HIGH_PERCENT)
        changes.append(change)
        prices.append(prices[-1] * (1 + Fraction(change, 100)))
    return prices, changes


def real_value(debt_cents: int, base: Fraction, price: Fraction) -> Fraction:
    """Real value of a fixed nominal debt, in base-date cents: D * P_0 / P_t.

    Raises ValueError when the price index is not positive, because the real value is then undefined.
    """
    if price <= 0:
        raise ValueError("the price index must be positive")
    return Fraction(debt_cents) * base / price


def gram_price(kappa: Fraction) -> Fraction:
    """Currency units per gram at a parity of kappa grams per currency unit: 1 / kappa, exact.

    Raises ValueError when the parity is not positive, because the price is then undefined.
    """
    if kappa <= 0:
        raise ValueError("the parity must be positive")
    return 1 / kappa


def main() -> None:
    """Print Parts A to E in a fixed order."""
    prices, changes = price_path(SEED, HORIZON)

    print("Part A: SIMULATED price index, base P_0 = 100 index points, shown to four decimals, rounded half up")
    print(f"t =  0: index {fixed_decimal(prices[0], 4)}")
    for t in range(1, HORIZON + 1):
        print(f"t = {t:2d}: change {changes[t - 1]:+d} percent; index {fixed_decimal(prices[t], 4)}")

    values = [real_value(DEBT_CENTS, BASE_INDEX, p) for p in prices]
    cents = [round_half_up(v) for v in values]
    print(f"Part B: real value of the fixed nominal debt of {DEBT_CENTS} cents, in base-date cents")
    for t in range(HORIZON + 1):
        print(f"t = {t:2d}: real value {cents[t]} cents")
    identity = all(values[t] / values[t - 1] == prices[t - 1] / prices[t] for t in range(1, HORIZON + 1))
    print(f"identity V_t / V_(t-1) = P_(t-1) / P_t holds exactly for t = 1 to {HORIZON}: {identity}")

    falls = [t for t in range(1, HORIZON + 1) if prices[t] < prices[t - 1]]
    rises = [t for t in range(1, HORIZON + 1) if values[t] > values[t - 1]]
    print("Part C: falls in the price index and rises in the real value")
    print(f"periods with a falling price index: {len(falls)} of {HORIZON}")
    print(f"periods with a rising real value: {len(rises)} of {HORIZON}")
    print(f"real value rises exactly in the periods where the index falls: {falls == rises}")
    steps = [cents[t] - cents[t - 1] for t in range(1, HORIZON + 1)]
    top = max(range(HORIZON), key=lambda i: steps[i]) + 1
    print(f"largest one-period rise in real value: {steps[top - 1]} cents at t = {top}")

    print("Part D: change over the whole horizon")
    print(f"real value at t = {HORIZON}: {cents[HORIZON]} cents, against {cents[0]} cents at t = 0")
    telescoped = values[HORIZON] / values[0] == prices[0] / prices[HORIZON]
    print(f"V_{HORIZON} / V_0 = P_0 / P_{HORIZON} holds exactly: {telescoped}")
    print(f"ratio V_{HORIZON} / V_0 to six decimals: {fixed_decimal(values[HORIZON] / values[0], 6)}")

    kappa = KAPPA_GRAMS_PER_UNIT
    price_per_gram = gram_price(kappa)
    print(f"Part E: Proposition 1.2 at an illustrative parity of {kappa} gram per currency unit")
    print(f"currency price of one gram = 1 / kappa = {price_per_gram} currency units")
    print(f"kappa times the gram price equals 1 exactly: {kappa * price_per_gram == 1}")


main()
