"""FC2 lab L02: the no-arbitrage forward price S e^(r tau), its replication, and a mispriced quote.

The spot price, rate, expiry, quote and states are typed in for this lab; they describe no market. The conventions
are those of the lesson: the asset pays no income, the rate r is continuously compounded and constant, and
borrowing, lending and short sales are allowed at that rate. Prices are integer cents. Formula values are computed
in floating point and printed to two decimals of a cent, so a printed cent value is a display rounding of an
unrounded value. The replication check is printed as a boolean against a tolerance of 1e-6 cents.
Standard library only; no network; no randomness.
"""

from __future__ import annotations

import math

SPOT_CENTS = 5000
RATE = 0.05
TAU = 0.5
QUOTE_CENTS = 5200
EXPIRY_STATES_CENTS = [3000, 4500, 6000, 7500]
TOLERANCE_CENTS = 1e-6


def forward_price_cents(spot_cents: int, rate: float, tau: float) -> float:
    """No-arbitrage forward price in cents: the spot price times e to the power rate times tau."""
    return spot_cents * math.exp(rate * tau)


def replicating_payoff_cents(spot_at_expiry: int, spot_cents: int, rate: float, tau: float) -> float:
    """Payoff at expiry of holding one unit bought at spot_cents and borrowing spot_cents at rate for tau years."""
    return spot_at_expiry - spot_cents * math.exp(rate * tau)


def long_forward_payoff_cents(spot_at_expiry: int, price_cents: float) -> float:
    """Payoff at expiry of a long forward contract agreed at price_cents."""
    return spot_at_expiry - price_cents


def forward_value_cents(spot_now: float, price_cents: float, rate: float, years_left: float) -> float:
    """Value today of a long forward agreed at price_cents: spot minus price_cents discounted over years_left."""
    return spot_now - price_cents * math.exp(-rate * years_left)


def main() -> None:
    fair = forward_price_cents(SPOT_CENTS, RATE, TAU)
    print(f"A. Spot {SPOT_CENTS} cents, rate {RATE:.2f} continuously compounded, expiry {TAU} years")
    print(f"no-arbitrage forward price, in cents: {fair:.2f}")

    print()
    print("B. Replication: a long forward at the fair price against holding the asset and borrowing the spot price")
    worst = 0.0
    for s in EXPIRY_STATES_CENTS:
        forward_leg = long_forward_payoff_cents(s, fair)
        replica = replicating_payoff_cents(s, SPOT_CENTS, RATE, TAU)
        worst = max(worst, abs(forward_leg - replica))
        print(f"spot at expiry {s}: forward payoff {forward_leg:.2f}, replicating portfolio {replica:.2f}")
    print("forward payoff equals replicating payoff in every state, to 1e-6 cents:", worst < TOLERANCE_CENTS)

    print()
    print("C. A forward quoted above its fair price: sell the forward, buy the asset with a loan")
    net_today = SPOT_CENTS - SPOT_CENTS
    print("net cash today, in cents (loan proceeds less the asset's cost):", net_today)
    gains = []
    for s in EXPIRY_STATES_CENTS:
        net = (QUOTE_CENTS - s) + (s - SPOT_CENTS * math.exp(RATE * TAU))
        gains.append(net)
        print(f"spot at expiry {s}: net payoff {net:.2f} cents")
    same = max(gains) - min(gains) < TOLERANCE_CENTS
    print("net payoff is the same in every state, to 1e-6 cents:", same)
    print(f"that payoff equals quote minus fair price, in cents: {QUOTE_CENTS - fair:.2f}")

    print()
    print("D. Fair quote: the same strategy earns nothing")
    at_fair = max(abs((fair - s) + (s - SPOT_CENTS * math.exp(RATE * TAU))) for s in EXPIRY_STATES_CENTS)
    print("net payoff at the fair quote is zero in every state, to 1e-6 cents:", at_fair < TOLERANCE_CENTS)

    print()
    print("E. Value of a fair forward after 0.25 years, for the long side")
    value_now = forward_value_cents(5300, fair, RATE, TAU - 0.25)
    print(f"spot 5300 cents, years left 0.25: value {value_now:.2f} cents")
    print(
        "value at inception of a forward struck at the fair price is zero:",
        abs(forward_value_cents(SPOT_CENTS, fair, RATE, TAU)) < TOLERANCE_CENTS,
    )


main()
