"""FC2 lab L03: daily margining of a SIMULATED futures path, and the par rate of a swap from discount factors.

Part A is SIMULATED: the futures price path is generated from a seeded random number generator and describes no
contract or market. Prices are integer cents: each daily change is an integer number of cents, so the margin flows
and the account balance are exact integers. The margin account is assumed to earn no interest (assumption A8-prime of
the lesson).

Part B is exact: discount factors and the par rate are fractions.Fraction values, and the swap's notional is in
integer cents. Its input annual zero rates are typed in, and the discount factors are computed from them.
Money rounding is half up, to the nearest cent.

Standard library only; no network. The random generator is seeded, so every run prints the same path.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

SEED = 20261028
DAYS = 10
START_CENTS = 5000
MOVE_LOW_CENTS = -40
MOVE_HIGH_CENTS = 40
NOTIONAL_CENTS = 100_000_000
ZERO_RATES = [Fraction(3, 100), Fraction(7, 200), Fraction(4, 100), Fraction(9, 200), Fraction(5, 100)]


def simulate_path(seed: int, days: int, start_cents: int) -> list[int]:
    """Futures price in integer cents at the close of each day, starting at start_cents on day 0."""
    rng = random.Random(seed)
    path = [start_cents]
    for _ in range(days):
        path.append(path[-1] + rng.randint(MOVE_LOW_CENTS, MOVE_HIGH_CENTS))
    return path


def variation_margin(path: list[int]) -> list[int]:
    """Daily variation-margin flow to the long holder, in cents: the change in the futures price each day."""
    return [path[i] - path[i - 1] for i in range(1, len(path))]


def half_up(x: Fraction) -> int:
    """Round a fraction to the nearest integer; a value exactly halfway is rounded toward plus infinity."""
    return math.floor(x + Fraction(1, 2))


def discount_factors(zero_rates: list[Fraction]) -> list[Fraction]:
    """DF_0 = 1 and DF_i = (1 + z_i)^(-i) for annual payment i, where z_i is the zero rate to date i."""
    dfs = [Fraction(1)]
    for i, z in enumerate(zero_rates, start=1):
        dfs.append(Fraction(1) / (1 + z) ** i)
    return dfs


def par_rate(dfs: list[Fraction]) -> Fraction:
    """Fixed rate per unit period that makes the fixed leg equal the floating leg: (1 - DF_N) / sum of DF_i."""
    n = len(dfs) - 1
    return (1 - dfs[n]) / sum(dfs[1:], Fraction(0))


def main() -> None:
    path = simulate_path(SEED, DAYS, START_CENTS)
    margins = variation_margin(path)
    print("A. SIMULATED futures path, integer cents, day 0 to day 10")
    print("futures price by day:", " ".join(str(p) for p in path))
    print("daily variation margin to the long holder, in cents:", " ".join(str(m) for m in margins))
    balance = 0
    balances = []
    for m in margins:
        balance += m
        balances.append(balance)
    print("margin account balance after day 10, in cents:", balances[-1])
    print("settlement minus initial price, in cents:", path[-1] - path[0])
    print("sum of daily margin equals settlement minus initial price:", sum(margins) == path[-1] - path[0])
    print(
        "balance equals the futures price minus the initial price on every day:",
        all(balances[i] == path[i + 1] - path[0] for i in range(DAYS)),
    )
    print("days with a loss to the long holder:", sum(1 for m in margins if m < 0))

    print()
    print("B. Interest-rate swap, exact: notional 1,000,000 dollars, annual payments, typed-in zero rates")
    dfs = discount_factors(ZERO_RATES)
    print("discount factors DF_1 to DF_5, to six places:", " ".join(f"{float(d):.6f}" for d in dfs[1:]))
    annuity = sum(dfs[1:], Fraction(0))
    fixed_leg = par_rate(dfs) * annuity
    floating_leg = sum((dfs[i - 1] - dfs[i] for i in range(1, len(dfs))), Fraction(0))
    print("floating leg telescopes to 1 minus DF_5:", floating_leg == 1 - dfs[-1])
    rate = par_rate(dfs)
    print(f"par rate, to six places: {float(rate):.6f}")
    print("fixed leg at the par rate equals the floating leg exactly:", fixed_leg == floating_leg)
    payment = half_up(rate * NOTIONAL_CENTS)
    print("fixed payment per year at the par rate, in cents:", payment)
    struck = rate + Fraction(1, 100)
    value_to_payer = half_up((floating_leg - struck * annuity) * NOTIONAL_CENTS)
    print("value to the fixed payer of a swap struck 1 percentage point higher, in cents:", value_to_payer)
    print(
        "that value is minus one percent times the annuity times the notional, in cents:",
        half_up(-Fraction(1, 100) * annuity * NOTIONAL_CENTS),
    )


main()
