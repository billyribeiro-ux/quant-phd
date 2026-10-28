"""FC2 L04 lab 1: call and put payoffs at expiry, and an exercise comparison on one SIMULATED price path.

SIMULATED: the price path is a fixed list written in this file. It is not market data.
Units: prices, the strike and the premiums are integer cents; dates are years, with t = 0 first.
Part 1 prints the expiry payoff and the profit (payoff minus premium, with no interest on the premium) of one call
and one put on a grid of expiry prices. Part 2 compares, on the single path, the intrinsic value of exercising at
each date with the value at that date of holding the same option to expiry. The holding value discounts the expiry
payoff at the continuously compounded rate RATE (assumption A4). Part 2 is a comparison with hindsight on one path:
it is not a decision rule, and it leaves out the choice to sell the option before expiry, which Lesson 5 treats.
The lab draws no random numbers.
"""

from __future__ import annotations

import math

STRIKE_CENTS = 10_000  # 100 USD
CALL_PREMIUM_CENTS = 800
PUT_PREMIUM_CENTS = 700
RATE = 0.10  # continuously compounded, per year (assumption A4)
PATH_CENTS: tuple[int, ...] = (10_000, 12_000, 9_000, 8_000, 11_000)  # spot at t = 0, 1, 2, 3, 4 years
GRID_CENTS: tuple[int, ...] = tuple(range(0, 20_001, 2_500))  # expiry prices 0 to 200 USD in steps of 25 USD


def call_payoff(spot_cents: int, strike_cents: int = STRIKE_CENTS) -> int:
    """Payoff of a call at expiry in cents: max(spot - strike, 0)."""
    return max(spot_cents - strike_cents, 0)


def put_payoff(spot_cents: int, strike_cents: int = STRIKE_CENTS) -> int:
    """Payoff of a put at expiry in cents: max(strike - spot, 0)."""
    return max(strike_cents - spot_cents, 0)


def usd(cents: float) -> str:
    """Cents shown as dollars with two decimals, formatted by Python's fixed-point rule; no thousands separator."""
    return f"{cents / 100:.2f}"


def part_one() -> None:
    """Payoff and profit of the call and the put on the expiry grid, plus the two break-even prices."""
    print(
        f"strike {STRIKE_CENTS} cents; call premium {CALL_PREMIUM_CENTS} cents; put premium {PUT_PREMIUM_CENTS} cents"
    )
    print("expiry spot (USD)  call payoff  call profit  put payoff  put profit")
    for spot in GRID_CENTS:
        c = call_payoff(spot)
        p = put_payoff(spot)
        print(
            f"{spot / 100:>17.2f}  {usd(c):>12}  {usd(c - CALL_PREMIUM_CENTS):>11}  "
            f"{usd(p):>10}  {usd(p - PUT_PREMIUM_CENTS):>10}"
        )
    print(f"call break-even spot, strike plus premium (USD): {usd(STRIKE_CENTS + CALL_PREMIUM_CENTS)}")
    print(f"put break-even spot, strike minus premium (USD): {usd(STRIKE_CENTS - PUT_PREMIUM_CENTS)}")


def part_two() -> None:
    """Intrinsic value of exercising at each date, and the value of holding to expiry, on the one path."""
    expiry = len(PATH_CENTS) - 1
    spot_expiry = PATH_CENTS[expiry]
    print(f"path (USD) at t = 0..{expiry}: " + ", ".join(usd(s) for s in PATH_CENTS))
    print("date  spot  call exercise  call hold (PV)  put exercise  put hold (PV)")
    call_pv_exercise: list[float] = []
    put_pv_exercise: list[float] = []
    for t, spot in enumerate(PATH_CENTS):
        discount = math.exp(-RATE * (expiry - t))
        call_hold = call_payoff(spot_expiry) * discount
        put_hold = put_payoff(spot_expiry) * discount
        call_now = call_payoff(spot)
        put_now = put_payoff(spot)
        print(
            f"{t:>4}  {usd(spot):>5}  {usd(call_now):>13}  {usd(call_hold):>14}  "
            f"{usd(put_now):>12}  {usd(put_hold):>12}"
        )
        call_pv_exercise.append(call_now * math.exp(-RATE * t))
        put_pv_exercise.append(put_now * math.exp(-RATE * t))
    best_call = max(range(len(PATH_CENTS)), key=lambda t: call_pv_exercise[t])
    best_put = max(range(len(PATH_CENTS)), key=lambda t: put_pv_exercise[t])
    call_best_pv = usd(call_pv_exercise[best_call])
    put_best_pv = usd(put_pv_exercise[best_put])
    print(f"hindsight best exercise date for the call on this path: t = {best_call}, PV at 0 {call_best_pv}")
    print(f"hindsight best exercise date for the put on this path: t = {best_put}, PV at 0 {put_best_pv}")
    held_call_pv0 = call_payoff(spot_expiry) * math.exp(-RATE * expiry)
    print(f"call held to expiry, PV at 0: {usd(held_call_pv0)}")


def main() -> None:
    part_one()
    part_two()


main()
